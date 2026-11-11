# UI and content-presentation contract

Use this contract to define and review the interface before and after implementation. Select the pieces appropriate to the sources and output; this is not a mandatory universal layout.

## UI brief

Record:
- Audience, learning goal, expected session length, and output mode.
- Information architecture: routes or sections, entry point, index, related-content links, and source/coverage location.
- Page anatomy and reading order, including what the reader sees first and how deeper detail is reached.
- Content-to-component mapping, responsive behavior, typography/spacing, and treatment of diagrams, math, code, and tables.
- Interaction states, URL/deep-link behavior, keyboard/focus behavior, and media failure fallbacks.
- Acceptance criteria and any user-requested review gate.

## Presentation by content type

| Content | Presentation decision |
| --- | --- |
| Executive summary | Brief opening summary with the problem, mechanism, and takeaway. Keep technical detail below it. |
| Concepts and explanations | Clear headings, prerequisite links when useful, worked examples, and distinct supplemental explanation labels. |
| Slide notes | Visible slide/page identity, concise key idea, detailed explanation, source locator, and optional exercise. |
| Diagrams | Labeled relationships, caption, text equivalent, readable sizing, and verified notation. |
| Equations, code, tables | Legible formatting; preserve semantics and units; allow controlled overflow when reflow would distort meaning. |
| Evidence and citations | Put source links/locators beside the claim or content unit they support. A source appendix alone is insufficient for detailed notes. |
| Review questions | Separate prompt from optional answer/explanation; use keyboard-accessible disclosure if interactive. |
| Coverage and gaps | Show missing sources, partial processing, uncertain alignment, and sampled QA visibly near affected content and in the coverage summary. |

## Choose a navigation model

A larger wiki can use course overview → lecture index → lecture pages, with concept links and previous/next lecture navigation. A small curated webpage can use an opening summary, thematic sections, an optional section index, and source/coverage details.

Use search when the amount of content warrants it, not as a substitute for clear hierarchy. Avoid empty page types or placeholder sections. Define meaningful headings and stable URLs/anchors.

## Adaptive page templates


### Course overview

Show the course title and edition, audience/prerequisites, concise outcomes, suggested learning sequence, lecture or topic cards, and prominent coverage limitations. Include source links without allowing them to overwhelm the starting study path. Do not imply estimated study times are measured; label estimates if used.

### Slide-led lecture study page

Start with the problem, objectives, summary, and prerequisites. Follow with an ordered slide outline, source region, and explanation region.

- On wide screens, use an outline with adjacent slide/source and note panels when the content benefits from comparison. Preserve legibility rather than cramming three narrow columns onto every desktop.
- Give slide/source and note records the same stable slide ID. Selecting an outline entry, previous/next control, or deep link must update the selected slide and corresponding explanation together. Keep notes and active navigation consistent across reloads.
- Show the current page/slide number, source locator, key idea, explanation, optional worked example/diagram, and relevant check-your-understanding item.
- Display source slide images or embeds only when reproduction/embedding is supported and authorized. Otherwise show a titled source link and original explanatory content; do not design a permanently broken viewer.
- On mobile, collapse the outline into an accessible menu and stack source then notes, with clear selected-slide controls. Preserve state and anchors. Avoid sticky overlays that obscure text or trap scrolling.
- Treat slide-note synchronization separately from video synchronization. Add a seek link only for verified timestamps. If alignment is approximate, say so; if unaligned, retain independent source access. Never invent transitions or timestamps to satisfy the design.

### Reading-led or mixed-material lecture

Use an explanatory article with local contents, contextual source citations, definitions, worked examples, and diagrams. Add optional source excerpts or slide references where useful, without imposing a slide carousel on prose. For mixed lectures, choose the dominant learning flow and embed secondary media near relevant explanations.

### Concept/reference page

Show a concise definition, prerequisites, notation, explanation, example, misconception, related concepts/lectures, and provenance. Omit unsupported fields. Keep references distinguishable from newly written supplemental teaching.

### Source and coverage view

Show each source's title, edition, original URL, retrieval/extraction state, rights/attribution, and known gaps. Report numerator/denominator coverage and explain what “covered” means. Keep inaccessible media and missing transcripts visible without making the whole experience unusable.

## Format the material deliberately

- Use a readable text measure, consistent type scale, comfortable line spacing, and clear section rhythm. Make titles, summaries, body prose, captions, citations, and metadata visually distinct.
- Use purposeful components: summary panel, definition block, worked example with steps, misconception callout, labeled figure, accessible math, source citation, and optional expandable solution. Avoid indiscriminate card grids and decorative charts.
- Keep long prose in a continuous reading flow. Use bullets for actual lists and tables for genuine comparisons; provide narrow-screen alternatives or bounded horizontal scrolling for large tables and code.
- Place citations near the supported statement and link to the exact page/slide/time where available. Show source type and uncertainty with text, not color alone.
- Keep essential explanations visible. Use disclosure controls for supplementary detail or answers, not to hide the entire lesson. Support print-friendly reading when it is useful and feasible.

## Coordinated slide/notes reader, when applicable

- Use one selected-slide identifier to drive the slide representation, notes, position indicator, and deep link.
- Provide previous/next controls with correct boundary states and an accessible slide index. Preserve a useful reading position on selection changes.
- Show the original slide only where reproduction or embedding is permitted. Otherwise use a source link and clearly labeled original explanatory content, not a fabricated slide image.
- On desktop, consider a two-pane layout if both slide and notes remain readable. On mobile, stack content or use accessible tabs that preserve the selected slide and expose all notes.
- Synchronize video only from verified mappings. Distinguish precise and approximate mappings, state how user selection affects playback, and avoid feedback loops between playback updates and slide selection.
- Preserve manual selection for unaligned slides and reading access when the video or slide media fails.
- Do not promise video-following behavior if only timestamp links are implemented.

## Accessibility and visual QA

Inspect real renders at representative desktop and narrow mobile sizes, plus a long or complex lesson. Test:
- Heading hierarchy, link names, keyboard reachability, focus visibility, and focus behavior after navigation.
- Text contrast, line length, spacing, readable diagram labels, and text alternatives.
- Long titles, equations, code, tables, empty states, unavailable media, and citation placement.
- Slide/notes agreement, index navigation, boundaries, direct-link reload, Back/Forward, and repeated quick selections.
- Search, answer disclosures, and media controls only when implemented.
- Loading and error states without losing readable content.

Record actual pages, viewports, states, results, and untested cases. Recheck defects after correction. Screenshots support visual review but do not replace functional interaction checks.

## Delivery gate

A finished result includes an implemented wiki or curated webpage, not only source extraction and prose. Include the source manifest, structured lesson content, UI brief, runnable artifact or verified preview, and honest QA/coverage report. Publishing remains separate from preview delivery and must respect the user's authorization and requested review.


## Optional scroll-following variant

When explicitly selected, apply [scroll-reader-contract.md](scroll-reader-contract.md): scrolling source-slide cards drives matching notes and the canonical selected-slide state. The reference template is replaceable presentation code, not a mandatory visual language. Adapt it using user preferences or another UI skill, then test the same behavioral acceptance criteria.
