# Optional scroll-synchronized reader

Read this specification only when a user requests a scroll-synchronized slide/notes experience, or explicitly accepts it in the UI brief. Do not impose it on every course wiki. Treat the behavior below as the reusable contract; the bundled HTML/CSS/JS is an editable implementation example, not a prescribed visual style. Adapt colors, typography, density, layout, components, framework, and animation to the user's tastes and relevant UI skills. Re-run acceptance tests after a redesign.

## State and transitions

Keep one canonical `(lecture_id, slide_id)` selection. Derive the current source page, matching notes, current index item, page indicator, navigation boundaries, and deep link from that state. Use stable IDs, not display titles. PDF pages are one-based physical pages; printed slide labels are separate.

- **Scroll:** As the learner scrolls continuous source-slide cards, select the card crossing a documented reading line inside the scroll container. Update matching notes and active index without snapping the slide pane back. If notes are also continuous, define which pane owns the interaction; do not create a feedback loop.
- **Explicit navigation:** Previous/next, page input, index selection, and lecture selection update all dependent UI together, then reveal the chosen card. Clamp page input to known boundaries. Avoid interpreting arrow keys inside inputs, selects, textareas, editable regions, or modified shortcuts.
- **History:** Use pushState for deliberate selections and replaceState for passive scroll tracking. Handle both popstate and external hash changes. Restore selection and scroll on direct load, reload, Back, and Forward without adding another history entry. Parse and validate malformed, unknown, or percent-encoded IDs safely; fall back visibly or predictably.
- **Rapid changes:** Cancel obsolete observers, fetches, renderer tasks, and queued work. Guard async writes with a generation token even when cancellation is imperfect. A late render from the previous lecture must never overwrite the current lecture.
- **Layout changes:** Recompute the scroll owner and reading line after resize, font/image load, disclosure changes, or mobile layout changes. Retain the selected ID while moving between layouts.
- **Persistence:** Optional local storage must be nonessential and exception-safe. URL selection wins over saved state. Do not send reading activity to analytics by default.

## Accessible behavior

Use semantic controls, labels, current-state attributes, visible keyboard focus, and a modest live-region announcement of deliberate changes. Avoid announcing every scroll frame. Focus must not jump during passive scrolling. Keep focus usable after explicit navigation, and do not remove the focused control while re-rendering notes. Disable unavailable previous/next controls.

Keep every essential note reachable on mobile. Stacking, tabs, accordions, or a compact source preview are design choices; preserve the selection, source locator, and manual navigation. Avoid tall sticky media that leaves no reading space. Honor prefers-reduced-motion, support zoom and narrow widths, and provide text alternatives for diagrams and source images. Test keyboard operation separately from pointer operation.

## Source rendering strategies

Choose based on access, rights, scale, platform, and offline needs; document the choice in the UI brief.

1. **Source-link cards:** Always viable when linking is permitted. Show page identity and original explanations. Do not represent a fabricated slide as the original.
2. **Authorized pre-rendered images:** Simple, consistent browser behavior. Preserve page order/aspect ratios, reserve dimensions, use lazy loading and useful alt text, and retain the original source link. Rendering is not redistribution permission.
3. **PDF.js:** Use a pinned, compatible library and worker from a trusted source, preferably self-hosted with needed fonts/CMaps/WASM. Resolve worker and asset URLs against the deployed base URL. Limit concurrent renders and nearby-page prefetch, cap pixel resolution/device scale, cancel obsolete tasks, reclaim canvases, and test CORS, CSP, worker and missing-PDF errors. Treat document text as untrusted. Do not copy a course's outdated version without reviewing current official guidance.
4. **Native PDF iframe/object:** Useful as a fallback, but page fragment behavior and mobile/accessibility differ. Do not claim scroll synchronization inside a cross-origin native viewer you cannot observe. Keep external navigation and text notes usable.

An image/source-card reference implementation does not prove PDF.js loading, text selection, OCR, math, video playback, or multi-thousand-page performance. Record each separately as tested, not run, or unsupported.

## Data and provenance

Keep source manifest, normalized extraction, synthesis, and UI state separate. The original demo is an illustrative micro-lesson, not a real course transcript. Each course-specific note needs a source/page locator, evidence kind, and alignment status. When no notes exist show “Notes pending”; when no transcript exists show “Transcript unavailable”; do not turn extracted text into fabricated curated notes. Preserve approximate and unaligned video statuses. Timestamp links are not continuous video synchronization.

## Acceptance matrix

Run the template's browser regression tests and inspect real desktop/mobile screenshots. Test the redesigned implementation, not only the stock template.

- Source scrolling changes selected ID, matched notes, URL, index, and progress without feedback loops.
- First/last boundaries; page input invalid/negative/too large; keyboard ignores editable controls.
- Direct link, reload, malformed link, Back/Forward, and rapid repeated selection.
- Lecture switch and a slow stale media response; missing image/PDF, missing notes, empty deck, and unaligned video.
- Mobile and desktop resize preserve state, text remains readable, and no viewport-wide overflow occurs.
- Keyboard focus, reduced motion, media alternatives, source citations, and disclosure controls work.
- Root and nested deployment paths resolve HTML, JS, CSS, data, images, workers, and source files.

Report browser/version, viewport, fixtures, actual assertions, and untested cases. Passing a build or static validator is not evidence of functional scrolling or visual usability.
