#!/usr/bin/env python3
"""Normalize an authorized local WebVTT/SRT transcript; never infer slide timing."""
import argparse
import hashlib
import html
import json
import re
from pathlib import Path

TIME = r'(?:\d{2,}:)?\d{2}:\d{2}[.,]\d{3}'
TIMING = re.compile(rf'^({TIME})\s+-->\s+({TIME})(?:\s+.*)?$')


def seconds(value):
    parts = value.replace(',', '.').split(':')
    if float(parts[-1]) >= 60 or int(parts[-2]) >= 60:
        raise ValueError('Caption minute/second components must be below 60')
    return sum(float(part) * 60 ** i for i, part in enumerate(reversed(parts)))


def extract(text):
    cues = []
    for block in re.split(r'\n\s*\n', text.lstrip('\ufeff').replace('\r\n', '\n').strip()):
        lines = block.splitlines()
        if not lines or lines[0].startswith(('WEBVTT', 'NOTE', 'STYLE', 'REGION')):
            continue
        index = 0 if '-->' in lines[0] else 1
        if index >= len(lines):
            raise ValueError(f'Unrecognized caption block: {lines[0][:80]}')
        match = TIMING.match(lines[index].strip())
        if not match:
            raise ValueError(f'Invalid cue timing: {lines[index][:80]}')
        start, end = map(seconds, match.groups())
        if end <= start:
            raise ValueError('Cue end must be greater than start')
        body = html.unescape(re.sub(r'<[^>]*>', '', '\n'.join(lines[index + 1:]))).strip()
        if not body:
            raise ValueError('Caption cue has no text')
        cues.append({'cue_id': f'cue-{len(cues) + 1}', 'start_seconds': start, 'end_seconds': end, 'text': body})
    if not cues:
        raise ValueError('No timed captions found')
    if any(a['start_seconds'] > b['start_seconds'] for a, b in zip(cues, cues[1:])):
        raise ValueError('Caption start times must be chronological (overlap is permitted)')
    return cues


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('captions', type=Path)
    parser.add_argument('--source-id', required=True)
    parser.add_argument('--source-url', required=True)
    parser.add_argument('--origin', choices=['human captions', 'automatic captions', 'machine transcription'], required=True)
    parser.add_argument('--language', required=True)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    try:
        raw = args.captions.read_bytes()
        cues = extract(raw.decode('utf-8-sig'))
        result = {'source_id': args.source_id, 'url': args.source_url, 'transcript_origin': args.origin,
                  'language': args.language, 'timestamped': True, 'alignment_status': 'unaligned',
                  'input_sha256': hashlib.sha256(raw).hexdigest(), 'cues': cues,
                  'quality_notes': 'Imported timings, not independently verified. No slide alignment inferred.'}
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    except (OSError, ValueError, UnicodeError) as exc:
        parser.exit(1, f'Caption extraction failed: {exc}\n')


if __name__ == '__main__':
    main()
