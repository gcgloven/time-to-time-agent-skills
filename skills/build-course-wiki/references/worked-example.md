# Worked example and delivery

## Original micro-lesson

Use the included queue lesson to exercise the pipeline without private or copyrighted course material. The PDF and caption generator creates original synthetic fixtures. They are not a recording, an instructor transcript, or evidence of any real course. The example's teaching text is explicitly supplemental explanation.

**Scope:** One small lecture, two source pages, a curated responsive reader, local preview only. Assume a learner familiar with lists. Objective: distinguish first-in-first-out order from capacity. No video alignment is claimed.

**Inventory:** Generate the PDF, synthetic captions, and structured source/lesson records with `scripts/make_example.py`. Preserve source IDs and one-based PDF page numbers. See [extraction-and-validation.md](extraction-and-validation.md) for executable commands, expected outputs, dependencies, and the full example build command.

**Extract:** Run the PDF extractor and caption normalizer. Retain page boundaries, input hash, timestamp intervals, and extraction provenance. Inspect the rendered PDF before interpreting ambiguous symbols. Empty text does not mean a blank slide: it can indicate a scan requiring OCR. Caption extraction is not speech transcription and never fills a missing transcript automatically.

**Synthesize:** Keep the short source title distinct from the original instructional explanation. Page 1 explains removing A before B; page 2 explains that two occupied slots fill capacity two. State that these details are supplemental examples rather than quotations from the generated title-only PDF. Keep the video mapping unavailable.

**Define UI:** Use an optional source-following reader because this example explicitly demonstrates that interaction. Show the active page, neighboring pages, corresponding notes, evidence kind, and source links. Use previous/next and an index, preserve deep links, and expose gaps in plain language. The provided visual design is one editable starting point; a requested UI skill may replace it while retaining the behavior contract.

**Implement:** Run `python scripts/build_example.py /tmp/course-example-reader` from the skill directory, then `python -m http.server 8000 --directory /tmp/course-example-reader` and open `http://localhost:8000/`. Choose a new, empty destination for repeated builds. The generated example copies the functional template and writes its normalized reader data. Keep extraction output and source manifest as separate artifacts. Do not silently substitute sample explanations for missing real course notes.

**Verify:** Run Python tests and the bundled browser tests. Inspect desktop and mobile screenshots in addition to assertions. Record the checks actually run. The default demo also contains deliberate failure/empty cases for regression testing; those cases are not evidence of missing real sources.

**Deliver:** Provide the generated preview directory, normalized source/lesson data, extraction records, UI brief above (adapted as needed), and a QA report. State “local preview” until a real hosting deployment is verified. A file in a repository is not automatically a live webpage.

## Host and asset handling

For any Sites workflow, read the active Sites skill before deployment. Do not assume the host accepts every local file type or serves a directory exactly as a local HTTP server does.

- Keep all runtime files together: HTML, CSS, JS, data JSON, images and any authorized PDF. Transfer binary assets using the host's supported upload mechanism, not text serialization. Retain returned asset IDs/URLs and verify MIME types.
- For a plain static folder, resolve reader data/media URLs relative to the data file or module as documented by the template. Avoid root-relative `/assets/...` when the site lives at `/study/lecture/`. Test a nested path with a trailing slash and a direct `index.html` URL.
- For platform-managed asset URLs, replace the corresponding fields using the verified URLs; do not invent a URL from an asset name. If a data file is moved to a CDN, its relative image paths change meaning unless intentionally rebased.
- For bundlers, import/package assets or use the framework's configured base path. Do not rely on development-server fallback routes to hide production 404s. Include a real page for direct-link reloads or configure authorized rewrites.
- Keep external source URLs separate from hosted media URLs. Never upload a deck just to fix a broken preview without verifying redistribution rights and the requested audience.
- For PDF.js adapters, verify worker, font, CMap and WASM URLs and CSP/CORS in the actual deployed environment. An iframe page fragment is not a substitute for controllable page rendering.
- After deployment, open the final URL at desktop and mobile widths, reload a selected-slide deep link, exercise Back/Forward and scroll synchronization, and check failed network requests. Verify source/download links and media content types. Report locally tested versus deployment-tested separately.

## Minimal QA record

Record date, source/version, output URL or artifact, browser/version, viewports, script/test names, assertion count, inspected screenshots, and limitations. Include actual observed outcomes for scrolling, history, missing sources, responsive layout, and rights checks. Mark unavailable tests “not run” with a reason. Structural validation cannot certify factual correctness, full accessibility, source licensing, external link availability, or actual video synchronization.
