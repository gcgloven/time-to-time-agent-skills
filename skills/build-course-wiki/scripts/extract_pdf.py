#!/usr/bin/env python3
"""Extract local authorized PDFs with one-based page locators and provenance."""
import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def extract(path, source_id, source_url, render_dir=None):
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError('Install extraction dependency: python -m pip install pypdf==6.21.4') from exc
    reader = PdfReader(path)
    if reader.is_encrypted:
        raise ValueError('Encrypted PDF: provide an authorized decrypted copy; no password bypass is attempted.')
    pages = []
    if render_dir:
        Path(render_dir).mkdir(parents=True, exist_ok=True)
        subprocess.run(['pdftoppm', '-png', '-scale-to', '1600', str(path), str(Path(render_dir) / 'page')], check=True)
    for index, page in enumerate(reader.pages, 1):
        text = page.extract_text() or ''
        pages.append({'pdf_page': index, 'text': text, 'needs_visual_review': True,
                      'text_status': 'extracted' if text.strip() else 'empty_or_scanned'})
    return {'source_id': source_id, 'url': source_url,
            'extracted_at': datetime.now(timezone.utc).isoformat(),
            'input_sha256': hashlib.sha256(Path(path).read_bytes()).hexdigest(),
            'extractor': f'pypdf {__import__("pypdf").__version__}', 'page_indexing': 'one-based',
            'page_count': len(pages), 'extraction_status': 'extracted' if all(p['text'].strip() for p in pages) else 'partial',
            'limitations': ['Text extraction is not visual verification or OCR. Inspect every relevant rendered figure and equation.',
                             'Printed slide numbers may differ from PDF page numbers.'], 'pages': pages}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf', type=Path)
    parser.add_argument('--source-id', required=True)
    parser.add_argument('--source-url', required=True, help='Original URL or local: identifier, never a secret-bearing URL')
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--render-dir', type=Path, help='Optional local PNG preview directory; requires pdftoppm')
    args = parser.parse_args()
    try:
        result = extract(args.pdf, args.source_id, args.source_url, args.render_dir)
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f'Extraction failed: {exc}\n')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    main()
