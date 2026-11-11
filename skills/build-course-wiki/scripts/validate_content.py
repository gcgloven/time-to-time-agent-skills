#!/usr/bin/env python3
"""Validate portable course content before adapting it to a site's renderer.

Checks structure and locators, not semantic truth, rights permission, or remote reachability.
"""
import argparse
import json
import math
from pathlib import Path
from urllib.parse import urlsplit


def number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def validate(data):
    errors = []
    warnings = []
    if not isinstance(data, dict):
        return ['Root must be an object'], warnings
    def error(message):
        errors.append(message)
    def table(name, key):
        records = data.get(name)
        if not isinstance(records, list):
            error(f'{name}: required array')
            return {}
        result = {}
        for i, record in enumerate(records):
            if not isinstance(record, dict):
                error(f'{name}[{i}]: expected object')
                continue
            ident = record.get(key)
            if not isinstance(ident, str) or not ident.strip():
                error(f'{name}[{i}]: missing {key}')
            elif ident in result:
                error(f'{name}: duplicate {key} {ident}')
            else:
                result[ident] = record
        return result
    sources = table('sources', 'source_id')
    lectures = table('lectures', 'lecture_id')
    slides = table('slides', 'slide_id')
    for ident, src in sources.items():
        for key in ['title', 'source_type', 'url', 'provenance', 'rights', 'access_status', 'extraction_status']:
            if not src.get(key):
                error(f'source {ident}: missing {key}')
        url = src.get('url', '')
        if isinstance(url, str):
            parsed = urlsplit(url)
            if parsed.scheme not in ('http', 'https', 'local') or (parsed.scheme in ('http', 'https') and not parsed.netloc):
                error(f'source {ident}: use http(s) URL or local: identifier')
            if parsed.username or parsed.password:
                error(f'source {ident}: credential-bearing URL prohibited')
        else:
            error(f'source {ident}: url must be text')
        if src.get('rights') == 'unknown':
            warnings.append(f'source {ident}: unknown rights; link rather than redistribute')
        if 'page_count' in src and (type(src['page_count']) is not int or src['page_count'] < 1):
            error(f'source {ident}: page_count must be positive integer')
        if src.get('source_type') == 'transcript':
            for key in ['transcript_origin', 'language', 'timestamped', 'quality_notes']:
                if key not in src:
                    error(f'source {ident}: missing transcript {key}')
    def references(record, label):
        ids = record.get('source_ids', [])
        if not isinstance(ids, list):
            error(f'{label}: source_ids must be an array')
            return
        for ident in ids:
            if not isinstance(ident, str) or ident not in sources:
                error(f'{label}: unknown source {ident}')
    def citations(record, label):
        values = record.get('citations', [])
        if not isinstance(values, list):
            error(f'{label}: citations must be an array')
            return
        for cite in values:
            if not isinstance(cite, dict):
                error(f'{label}: citation must be an object')
                continue
            src = sources.get(cite.get('source_id')) if isinstance(cite.get('source_id'), str) else None
            if src is None:
                error(f'{label}: citation has unknown source')
                continue
            if not any(key in cite for key in ['pdf_page', 'start_seconds', 'locator']):
                error(f'{label}: citation requires pdf_page, start_seconds, or locator')
            if 'pdf_page' in cite:
                page = cite['pdf_page']
                if type(page) is not int or page < 1:
                    error(f'{label}: pdf_page must be one-based positive integer')
                elif type(src.get('page_count')) is int and page > src['page_count']:
                    error(f'{label}: citation page exceeds source page_count')
            if 'start_seconds' in cite and (not number(cite['start_seconds']) or cite['start_seconds'] < 0):
                error(f'{label}: invalid citation start_seconds')
    for ident, lecture in lectures.items():
        references(lecture, f'lecture {ident}')
        coverage = lecture.get('coverage', {})
        if not isinstance(coverage, dict):
            error(f'lecture {ident}: coverage must be object')
        else:
            for numerator, denominator in [('slides_processed', 'slides_total'), ('sources_processed', 'sources_total')]:
                if numerator in coverage or denominator in coverage:
                    a, b = coverage.get(numerator), coverage.get(denominator)
                    if type(a) is not int or type(b) is not int or not 0 <= a <= b:
                        error(f'lecture {ident}: invalid coverage {numerator}/{denominator}')
    for ident, slide in slides.items():
        label = f'slide {ident}'
        if not isinstance(slide.get('lecture_id'), str) or slide.get('lecture_id') not in lectures:
            error(f'{label}: unknown lecture_id')
        references(slide, label)
        citations(slide, label)
        for key in ['title', 'explanation', 'evidence_kind', 'alignment_status']:
            if not isinstance(slide.get(key), str) or not slide[key].strip():
                error(f'{label}: missing {key}')
        if slide.get('evidence_kind') not in ['source quotation', 'paraphrase', 'independent explanation', 'inference', 'supplemental example']:
            error(f'{label}: invalid evidence_kind')
        if slide.get('evidence_kind') in ['source quotation', 'paraphrase', 'inference'] and not slide.get('citations'):
            error(f'{label}: source-derived content requires citations')
        if slide.get('alignment_status') not in ['exact', 'approximate', 'unaligned', 'video unavailable']:
            error(f'{label}: invalid alignment_status')
        mapping = slide.get('video')
        if mapping is not None:
            if not isinstance(mapping, dict):
                error(f'{label}: video must be object')
                continue
            if slide.get('alignment_status') not in ['exact', 'approximate']:
                error(f'{label}: video times require exact or approximate alignment')
            start, end = mapping.get('start_seconds'), mapping.get('end_seconds')
            if not number(start) or not number(end) or not 0 <= start < end:
                error(f'{label}: invalid video interval')
            if not mapping.get('evidence'):
                error(f'{label}: video mapping requires evidence')
            source = sources.get(mapping.get('source_id')) if isinstance(mapping.get('source_id'), str) else None
            if not source or source.get('source_type') != 'video':
                error(f'{label}: video requires a video source_id')
            elif number(end) and number(source.get('duration_seconds')) and end > source['duration_seconds']:
                error(f'{label}: interval exceeds video duration')
        elif slide.get('alignment_status') in ['exact', 'approximate']:
            error(f'{label}: claimed alignment needs a video mapping')
    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('content', type=Path)
    args = parser.parse_args()
    try:
        errors, warnings = validate(json.loads(args.content.read_text()))
    except (OSError, ValueError) as exc:
        parser.exit(1, f'Unable to load content: {exc}\n')
    print(json.dumps({'valid': not errors, 'errors': errors, 'warnings': warnings}, indent=2))
    raise SystemExit(bool(errors))


if __name__ == '__main__':
    main()
