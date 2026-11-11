#!/usr/bin/env python3
"""Offline regression tests using original synthetic material."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from extract_captions import extract as captions
from extract_pdf import extract as pdf
from make_example import create_pdf, example
from validate_content import validate


class PipelineTests(unittest.TestCase):
    def test_pdf_pages_and_provenance(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'original.pdf'
            create_pdf(path)
            result = pdf(path, 'sample', 'local:original.pdf')
            self.assertEqual(result['page_count'], 2)
            self.assertEqual([p['pdf_page'] for p in result['pages']], [1, 2])
            self.assertIn('Queue order', result['pages'][0]['text'])
            self.assertEqual(len(result['input_sha256']), 64)
            self.assertTrue(all(p['needs_visual_review'] for p in result['pages']))

    def test_vtt_and_srt(self):
        vtt = '\ufeffWEBVTT\n\nNOTE import only\n\nidentifier\n00:01.000 --> 00:02.200 align:start\n<v Teacher>A &amp; B</v>\n'
        self.assertEqual(captions(vtt)[0]['text'], 'A & B')
        srt = '1\r\n00:00:01,500 --> 00:00:02,700\r\nOriginal sample\r\n'
        self.assertEqual(captions(srt)[0]['start_seconds'], 1.5)

    def test_invalid_caption(self):
        for raw in ['WEBVTT', '00:03.000 --> 00:02.000\nwrong', '00:01.000 --> 00:02.000\n', 'not a caption', '00:99.000 --> 01:00.000\nInvalid seconds']:
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                captions(raw)

    def test_valid_original_content(self):
        self.assertEqual(validate(example()), ([], []))

    def test_invalid_provenance_and_locators(self):
        for mutation in [lambda d: d['slides'].append(copy.deepcopy(d['slides'][0])),
                         lambda d: d['slides'][0]['citations'][0].update(pdf_page=3),
                         lambda d: d['slides'][0].update(lecture_id='missing'),
                         lambda d: d['slides'][0].update(evidence_kind='paraphrase', citations=[]),
                         lambda d: d['sources'][0].pop('rights'),
                         lambda d: d['lectures'][0]['coverage'].update(slides_processed=3),
                         lambda d: d['slides'][0].update(alignment_status='exact')]:
            data = example()
            mutation(data)
            self.assertTrue(validate(data)[0])

    def test_video_alignment_evidence(self):
        data = example()
        data['sources'].append(dict(source_id='vid', title='Demo', source_type='video', url='local:demo.webm',
                                    provenance='user-provided', rights='Original', access_status='available',
                                    extraction_status='not attempted', duration_seconds=10))
        slide = data['slides'][0]
        slide.update(alignment_status='approximate', video={'source_id': 'vid', 'start_seconds': 1, 'end_seconds': 5,
                                                         'evidence': 'Observed manually in synthetic recording'})
        self.assertEqual(validate(data)[0], [])
        slide['video']['end_seconds'] = 20
        self.assertTrue(validate(data)[0])
        slide['video'].pop('evidence')
        self.assertTrue(any('evidence' in e for e in validate(data)[0]))

    def test_end_to_end_build(self):
        from build_example import build
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / 'nested' / 'reader'
            build(output)
            reader = json.loads((output / 'demo-data.json').read_text())
            content = json.loads((output / 'evidence/content.json').read_text())
            self.assertEqual(validate(content)[0], [])
            self.assertEqual(len(reader['slides']), 2)
            for slide in reader['slides']:
                self.assertTrue((output / slide['media']['url']).is_file())
                self.assertIsInstance(slide['explanation'], list)
            self.assertIn('not run', json.loads((output / 'delivery.json').read_text())['visual_qa'])
            with self.assertRaises(ValueError):
                build(output)

    def test_malformed_top_level(self):
        self.assertTrue(validate([])[0])
        self.assertTrue(validate({'sources': [None], 'lectures': [], 'slides': []})[0])


if __name__ == '__main__':
    unittest.main()
