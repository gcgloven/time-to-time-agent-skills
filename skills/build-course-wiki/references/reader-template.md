# Reference reader implementation

Use only when the requested learning experience calls for scroll-synchronized source slides and notes. Read [scroll-reader-contract.md](scroll-reader-contract.md) for the behavioral requirements. HTML, CSS, typography, colors, layouts, and implementation technology are replaceable according to the user's preferences or another UI skill. This reference is not a mandatory visual theme.

## Run and customize

Copy `assets/reader-template/` into the destination site's chosen nested directory. Serve over HTTP, for example `python3 -m http.server 8000 --directory assets/reader-template`, then open `http://localhost:8000/index.html`. There are no runtime package dependencies and no network/CDN assets. `file://` cannot reliably fetch JSON and is not supported.

Change CSS custom properties or replace the stylesheet. Keep the independently scrollable `#slides` and `#notes` containers, selected state, visible focus, live status and controls, or adapt the JavaScript to an equivalent semantic structure. Desktop has side-by-side panes; mobile stacks two independently scrollable panes and retains the selection. Arrow Left/Right, Home and End work while either pane itself has focus; normal scrolling keys remain browser-native. Links and form controls keep their own keyboard behavior. Navigation does not steal focus. The skip link focuses notes without resetting selection.

The supplied implementation uses immediate scroll alignment, including when reduced motion is requested. It does not require animation. Passive scrolling updates state without flooding the live region; deliberate navigation announces the new slide. Both directions of synchronization are implemented: source scrolling aligns notes, and notes scrolling aligns sources. Scrolling replaces the current hash; explicit navigation creates history entries. Reload and Back/Forward restore the selected slide. The reference's cards have a minimum height of the pane, allowing the final card to align without snapping back. Keep an equivalent trailing-space guarantee if changing that layout.

## Render view model

`index.html` points to `./demo-data.json` via the module script's `data-source` attribute. That attribute resolves relative to the HTML page. Media and source URLs within the JSON resolve relative to the JSON file, not the domain root. Copy media with the JSON or rewrite URLs against the actual deployed directory. Test the real nested path and trailing-slash URL.

This small render view model is **not** the full grounded-content validation format. Validate source/lesson records first and adapt them explicitly, as in `scripts/build_example.py` and [worked-example.md](worked-example.md).

```json
{
  "title": "Lecture title",
  "description": "Coverage and source caveat",
  "sources": [{"id": "source-1", "title": "Original source", "url": "./source.pdf"}],
  "lectures": [{"id": "lecture-1", "title": "Lecture title"}],
  "slides": [{
    "id": "slide-1", "lecture_id": "lecture-1", "source_id": "source-1",
    "pdf_page": 1, "title": "Slide title", "keyIdea": "Text equivalent",
    "explanation": ["First paragraph.", "Second paragraph."],
    "caveat": "No transcript available.",
    "media": {"url": "./media/page-1.svg", "alt": "Diagram text equivalent"}
  }]
}
```

`id`, `title`, and the paragraph-array `explanation` are required for every slide; IDs must be unique. `media` is optional. Missing or failed images show a readable fallback without breaking navigation. Source URLs are optional and permit only HTTP(S), including relative URLs resolved to HTTP(S); unsafe schemes are not rendered as links. All content is rendered with text nodes, never inserted as HTML. Treat untrusted SVG/media and publication rights separately during source ingestion.

The sample has three original synthetic slides, two original diagrams, no transcript, and no private or copyrighted course material. `demo-source.html` records provenance. The final slide intentionally has no image to demonstrate the fallback.

## Browser regressions

Test-only dependencies: Node.js 18+ and `playwright@1.62.1`, plus its Chromium binary or an installed Chromium selected with `CHROMIUM_PATH`. Install test packages in a separate test workspace rather than including `node_modules` in a skill or publication. From a test workspace:

```sh
npm install --no-save playwright@1.62.1
npx playwright install chromium
NODE_PATH="$PWD/node_modules" node /absolute/path/to/reader-template/tests/reader.spec.cjs
# Or use a system browser:
CHROMIUM_PATH=/usr/bin/chromium NODE_PATH="$PWD/node_modules" \
  node /absolute/path/to/reader-template/tests/reader.spec.cjs
```

The suite starts its own local HTTP server, mounts the template at `/nested/course/`, and checks source-to-notes and notes-to-source scrolling, selected-state agreement, selector and boundaries, keyboard navigation, direct-link reload, Back/Forward, repeated navigation, mobile resizing and overflow, invalid hash recovery, missing-image fallback, empty data, and failed data retrieval. It checks uncaught JavaScript errors. Set `READER_SCREENSHOTS=/absolute/output/path` to save desktop (1280×900) and mobile (390×844) screenshots for visual inspection. Screenshot generation alone is not visual QA; inspect the images.

Report the actual results on each run. A browser startup failure is not a passed test. Check screen-reader announcements and touch usability manually when available. The suite is not a full accessibility audit or browser-compatibility certification.

## Deliberate limits

This reference handles one loaded lecture dataset, image/source-card media, and an in-memory DOM. It does not implement or test lecture switching, asynchronous PDF rendering/cancellation, PDF.js worker configuration, canvas virtualization, video synchronization, search, OCR, or extraction. The separate reader contract documents production PDF adapters and bounded rendering. For large decks, implement and test virtualization without breaking selection or reading positions. Do not claim those adapters are complete because this small image-based demo passes.
