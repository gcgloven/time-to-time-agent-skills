#!/usr/bin/env python3
"""Create original, synthetic public-safe PDF/caption/content fixtures in an output directory."""
import argparse
import json
from pathlib import Path


def create_pdf(path):
    # Minimal uncompressed text PDF; no external PDF-generation dependency.
    objects = [b'<< /Type /Catalog /Pages 2 0 R >>',
               b'<< /Type /Pages /Kids [3 0 R 5 0 R] /Count 2 >>']
    for page_id, title in [(3, b'Example: Queue order'), (5, b'Example: Queue capacity')]:
        objects.append(f'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 640 360] /Resources << /Font << /F1 7 0 R >> >> /Contents {page_id + 1} 0 R >>'.encode())
        stream = b'BT /F1 24 Tf 40 280 Td (' + title + b') Tj ET'
        objects.append(b'<< /Length ' + str(len(stream)).encode() + b' >>\nstream\n' + stream + b'\nendstream')
    objects.append(b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>')
    content = b'%PDF-1.4\n'
    offsets = [0]
    for i, obj in enumerate(objects, 1):
        offsets.append(len(content))
        content += str(i).encode() + b' 0 obj\n' + obj + b'\nendobj\n'
    start = len(content)
    content += f'xref\n0 {len(objects)+1}\n0000000000 65535 f \n'.encode()
    content += b''.join(f'{offset:010d} 00000 n \n'.encode() for offset in offsets[1:])
    content += f'trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{start}\n%%EOF\n'.encode()
    path.write_bytes(content)


def example():
    return {'sources': [{'source_id': 'demo-slides', 'title': 'Original queue demonstration',
                        'source_type': 'slides', 'url': 'local:synthetic-slides.pdf', 'provenance': 'user-provided',
                        'rights': 'Original synthetic fixture; reuse permitted', 'access_status': 'available',
                        'extraction_status': 'extracted', 'page_count': 2}],
            'lectures': [{'lecture_id': 'demo', 'title': 'Queue demonstration', 'source_ids': ['demo-slides'],
                          'coverage': {'slides_processed': 2, 'slides_total': 2, 'transcript_availability': 'synthetic fixture only'}}],
            'slides': [{'slide_id': f'demo-{i}', 'lecture_id': 'demo', 'title': title,
                        'explanation': explanation, 'source_ids': ['demo-slides'], 'pdf_page': i,
                        'citations': [{'source_id': 'demo-slides', 'pdf_page': i}],
                        'evidence_kind': 'supplemental example', 'alignment_status': 'video unavailable'}
                       for i, title, explanation in [(1, 'Queue order', 'In this original example, place A before B and remove A first.'),
                                                    (2, 'Queue capacity', 'In this original example, a capacity of two leaves no free slot after adding A and B.')]]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    create_pdf(args.output / 'synthetic-slides.pdf')
    (args.output / 'synthetic-captions.vtt').write_text('WEBVTT\n\n00:00.000 --> 00:02.000\nAn original queue example.\n\n00:02.000 --> 00:04.000\nA arrives before B.\n')
    (args.output / 'content.json').write_text(json.dumps(example(), indent=2) + '\n')


if __name__ == '__main__':
    main()
