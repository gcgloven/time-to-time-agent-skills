# Extraction, rendering, and validation

## Dependencies and boundaries

Use Python 3.10+ and `python -m pip install -r scripts/requirements.txt` in an isolated environment. `pypdf==6.21.4` supplies PDF text extraction; caption extraction and structural validation use the standard library. Optional PNG rendering requires Poppler's `pdftoppm` on PATH. Use an installed system package or install Poppler through the platform's official package source only when authorized. Record actual tool versions with the QA report; do not claim a particular renderer was tested merely because it is listed here.

All scripts accept local inputs only. Obtain source files through authorized tools first; these scripts do not bypass authentication, download videos, transcribe audio, or solve access restrictions. Keep originals and extracted text private unless redistribution is permitted. Never put credentials in `--source-url`; use a canonical public URL or an opaque `local:` identifier.

## Runnable synthetic pipeline

Run from the skill directory. The fixture generator creates two original text slides, a short invented caption file, and portable content records. It includes no real course material. The example is a technical demonstration, not an academically verified lecture, and captions do not imply slide alignment.

```sh
python scripts/make_example.py /tmp/course-example
python scripts/extract_pdf.py /tmp/course-example/synthetic-slides.pdf \
  --source-id demo-slides --source-url local:synthetic-slides.pdf \
  --output /tmp/course-example/slides-extracted.json \
  --render-dir /tmp/course-example/rendered
python scripts/extract_captions.py /tmp/course-example/synthetic-captions.vtt \
  --source-id demo-captions --source-url local:synthetic-captions.vtt \
  --origin 'human captions' --language en \
  --output /tmp/course-example/captions-extracted.json
python scripts/validate_content.py /tmp/course-example/content.json
python scripts/test_pipeline.py
```

Omit `--render-dir` when Poppler is unavailable and report visual extraction review as not run. Inspect generated page PNGs before claiming text, diagrams, equations, or page correspondence are verified. `extracted_at` records the local extraction time. Preserve the actual acquisition timestamp separately as `retrieved_at` in the source manifest; do not substitute one for the other.

The fixture `content.json` shows the normalized content shape `{sources, lectures, slides}`. Convert real extraction output into this shape through evidence-backed synthesis, not automatic filler. Source manifest entries use `source_id`; lecture entries use `lecture_id`; slide entries use `slide_id`. `pdf_page` is always one-based and must not silently become a printed slide number. Claims need citations with `source_id` and `pdf_page`, `start_seconds`, or a descriptive `locator`. For paragraph-level or claim-level citations, keep additional structured claims in the project and extend its validator: the bundled validator checks slide-level citations only.

Map these records explicitly into the chosen site's render schema. Preserve stable IDs and locators during adaptation; do not drop provenance just because a template expects shorter field names. The extraction output is not the reader's data file and not a finished wiki. Finish synthesis, UI definition, rendering, browser tests, and delivery as required by SKILL.md.

## Build the runnable reader from the extraction pipeline

Run `python scripts/build_example.py /tmp/course-reader`, choosing an absent or empty output directory. This executes PDF/caption extraction, preserves hashes and locators, derives titles from actual extracted pages, adds explicit original supplemental explanations, validates the normalized records, and adapts them to `demo-data.json` for the bundled reader. It also produces evidence files and a delivery record. Caption text and timings are invented fixture material, not a real transcript or alignment evidence.

Serve with `python -m http.server 8000 --directory /tmp/course-reader`, then open `http://localhost:8000/`. The SVGs are original semantic title cards, not faithful PDF renders. Change the renderer for actual lecture needs and permitted media. The build refuses to overwrite a nonempty directory and does not publish, perform visual QA, or run browser regressions. Run those checks separately before calling the result verified.

## Extraction results and failure behavior

- PDF: retain a SHA-256 hash, extractor version, page count, one-based pages, text, and per-page `needs_visual_review`. Empty/scanned pages become `empty_or_scanned` and make extraction partial. Text extraction never establishes OCR, reading order, math accuracy, or figure understanding. Encrypted inputs fail rather than attempting passwords or removing restrictions.
- Captions: accept UTF-8 WebVTT and SRT, retain cue boundaries and numerical seconds, normalize cue markup to plain text, and reject missing, backwards, or malformed timings. Overlapping cues are permitted. Voice/style markup is not preserved in normalized text; retain the original caption file for speaker attribution and formatting. Captions remain explicitly `unaligned`; human/automatic/machine origin is supplied, not guessed.
- Unsupported caption variants, PDFs, corrupt input, or missing dependencies must fail visibly. Do not quietly output an empty “success.” Preserve the source and record extraction gaps; use another authorized extractor when justified.
- OCR is a separate optional step, not implemented here. For scans, use available OCR tooling, record tool/language/settings and uncertainty, and compare critical equations/figures against renders. Never advertise the text extractor as OCR.

## Slide renderer decision

Choose the renderer independently of the visual theme. Record the choice and known compromises in the UI brief.

1. **Original semantic HTML/SVG slides:** Best for generated explanatory slides, responsive text, accessibility, and simple deployment. Label them as independent explanations, not reproductions of source slides.
2. **Pre-rendered PNG/WebP images:** Predictable rendering and page boundaries; useful for authorized source-slide reproduction. Provide informative alternatives and separate searchable notes. Inspect resolution, equations, file weight, and aspect ratios. Use `pdftoppm` output locally; do not publish it without rights.
3. **PDF.js page renderer:** Useful for zoom or selectable text. Pin the official dependency/version, bundle matching worker assets, resolve worker paths under the actual base route, and test loading/error states. No PDF.js renderer is bundled here and it is not part of the synthetic browser test coverage unless separately implemented.
4. **Native PDF iframe/object:** Simple fallback only. Browser support, fragment handling, focus, and page-change events vary; an iframe cannot be assumed to report its displayed page reliably. Never claim robust notes synchronization from a native PDF embed alone. Retain an explicit page selector and accessible source link.

For oversized decks, lazy-load or cache adjacent pages; clear stale async render work so a slow older request cannot overwrite the new selection. Treat missing page images as a recoverable slide-render failure while retaining notes, citations, and navigation.

## Validator scope and project checks

`validate_content.py` exits nonzero for duplicate IDs, missing provenance/rights fields, unknown source or lecture references, absent source-derived citations, invalid/out-of-range page locators, inconsistent coverage counts, and unsupported timing claims. Aligned video requires a source of type `video`, an increasing interval, and explicit evidence; intervals must fit a known duration. Unknown rights produce a warning, not permission to reproduce.

It does not establish claim truth, citation entailment, source edition compatibility, actual reproduction rights, remote link reachability, UI accessibility, screenshot quality, or browser synchronization. Extend checks for the project's schema, audit claims against original sources, and record sampled versus exhaustive review.

Validate generated routes and assets separately: resolve relative URLs against each page's deployed directory (not repository root), exercise a nested route with a trailing slash, verify encoded filenames, inspect 404/network errors, and re-run after bundling. Prefer route-relative asset URLs or a single explicit base-URL helper; do not accidentally turn `/assets/...` into a site-root request when publishing below `/course/...`. Link-only sources may be remote; bundling a source file changes redistribution and asset-delivery requirements.
