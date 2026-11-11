#!/usr/bin/env python3
"""Run the original synthetic pipeline and build a standalone reader directory.

The output is a local preview, not a deployed website. No real course content is used.
"""
import argparse
import html
import json
import shutil
import subprocess
import sys
from pathlib import Path
from validate_content import validate


HERE = Path(__file__).resolve().parent


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')


def build(output):
    if output.exists() and any(output.iterdir()):
        raise ValueError('Output must be absent or empty; refusing to overwrite existing work')
    output.mkdir(parents=True, exist_ok=True)
    evidence = output / 'evidence'
    subprocess.run([sys.executable, str(HERE / 'make_example.py'), str(evidence)], check=True)
    subprocess.run([sys.executable, str(HERE / 'extract_pdf.py'), str(evidence / 'synthetic-slides.pdf'),
                    '--source-id', 'demo-slides', '--source-url', 'local:synthetic-slides.pdf',
                    '--output', str(evidence / 'slides-extracted.json')], check=True)
    subprocess.run([sys.executable, str(HERE / 'extract_captions.py'), str(evidence / 'synthetic-captions.vtt'),
                    '--source-id', 'demo-captions', '--source-url', 'local:synthetic-captions.vtt',
                    '--origin', 'human captions', '--language', 'en',
                    '--output', str(evidence / 'captions-extracted.json')], check=True)
    content = json.loads((evidence / 'content.json').read_text())
    extracted = json.loads((evidence / 'slides-extracted.json').read_text())
    transcript = json.loads((evidence / 'captions-extracted.json').read_text())
    content['sources'][0]['input_sha256'] = extracted['input_sha256']
    content['sources'][0]['page_count'] = extracted['page_count']
    content['sources'].append({'source_id': 'demo-captions', 'title': 'Invented captions, no recorded lecture',
                               'source_type': 'transcript', 'url': 'local:synthetic-captions.vtt',
                               'provenance': 'user-provided', 'rights': 'Original synthetic fixture; reuse permitted',
                               'access_status': 'available', 'extraction_status': 'extracted',
                               'transcript_origin': transcript['transcript_origin'], 'language': transcript['language'],
                               'timestamped': True, 'input_sha256': transcript['input_sha256'],
                               'quality_notes': 'Invented demonstration text/times, not a real lecture transcript; unaligned.'})
    # This explicit mapping is original authored synthesis, not a generic slide-to-summary algorithm.
    for slide, page in zip(content['slides'], extracted['pages']):
        if slide['pdf_page'] != page['pdf_page'] or not page['text'].strip():
            raise ValueError('Synthetic source page correspondence failed')
        slide['title'] = page['text'].strip().removeprefix('Example: ')
        slide['extraction_reference'] = {'file': 'slides-extracted.json', 'pdf_page': page['pdf_page']}
    content['lectures'][0]['coverage'].update(slides_processed=len(content['slides']), slides_total=extracted['page_count'])
    errors, warnings = validate(content)
    if errors:
        raise ValueError('Content validation failed: ' + '; '.join(errors))
    write_json(evidence / 'content.json', content)
    write_json(evidence / 'validation.json', {'valid': True, 'errors': [], 'warnings': warnings})
    template = HERE.parent / 'assets' / 'reader-template'
    for filename in ['index.html', 'reader.js', 'reader.css']:
        shutil.copy2(template / filename, output / filename)
    (output / 'slides').mkdir()
    slides = []
    for slide in content['slides']:
        # Semantic original SVG reconstruction, not a screenshot or faithful PDF rendering.
        image_url = f"slides/{slide['slide_id']}.svg"
        title = html.escape(slide['title'])
        (output / image_url).write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" role="img" aria-label="{title}">'
            '<rect width="640" height="360" fill="#f7f8fc"/>'
            f'<text x="32" y="100" font-family="sans-serif" font-size="32" fill="#182039">{title}</text>'
            '<text x="32" y="160" font-family="sans-serif" font-size="18" fill="#182039">Original synthetic example</text></svg>\n')
        slides.append({'id': slide['slide_id'], 'lecture_id': slide['lecture_id'], 'title': slide['title'],
                       'source_id': 'demo-slides', 'pdf_page': slide['pdf_page'],
                       'keyIdea': slide['explanation'], 'explanation': [slide['explanation'],
                           'This is an independently authored supplemental example, not speech extracted from a lecture.'],
                       'media': {'url': image_url, 'alt': 'Original illustrative title card: ' + slide['title']},
                       'caveat': 'Synthetic source and invented caption timings. No video exists; no slide/video synchronization is claimed.',
                       'evidence_kind': slide['evidence_kind'], 'alignment_status': slide['alignment_status'],
                       'citations': slide['citations']})
    reader = {'title': 'Synthetic queue study reader',
              'description': 'Original public-safe example: real PDF and caption extraction, authored synthesis, structural validation, then reader adaptation. No real lecture content.',
              'sources': [{**source, 'id': source['source_id'], 'type': source['source_type'],
                           'url': 'evidence/' + source['url'].removeprefix('local:')} for source in content['sources']],
              'lectures': [{**lecture, 'id': lecture['lecture_id']} for lecture in content['lectures']], 'slides': slides}
    write_json(output / 'demo-data.json', reader)
    write_json(output / 'delivery.json', {'status': 'local preview only', 'content': 'original synthetic fixtures',
                                        'extraction': '2 PDF pages and 2 invented caption cues',
                                        'structural_validation': 'passed', 'visual_qa': 'not run by this script',
                                        'browser_regressions': 'not run by this script',
                                        'renderer': 'original SVG title cards; not faithful PDF reproduction',
                                        'publication': 'not performed'})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    try:
        build(args.output)
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f'Example build failed: {exc}\n')
    print(f'Built local preview at {args.output}; serve over HTTP and run browser QA before delivery.')


if __name__ == '__main__':
    main()
