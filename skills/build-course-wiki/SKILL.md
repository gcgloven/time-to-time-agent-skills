---
name: build-course-wiki
description: Build a source-grounded course wiki or curated learning webpage through a complete pipeline of data extraction, synthesis, UI definition, implementation, and verified delivery. Use for lecture companions, slide-level study guides, and curated learning sites where evidence, content presentation, and slide/video alignment matter.
---

# Build Course Wiki

Deliver the full pipeline: **source inventory → data extraction → synthesis → UI and content-presentation definition → implementation → visual and evidence QA → wiki or curated webpage**. A transcript dump, notes document, or generic page shell is not the completed deliverable unless the user explicitly limits the scope. Read [references/content-contract.md](references/content-contract.md) for source/content records and [references/ui-presentation-contract.md](references/ui-presentation-contract.md) when defining and validating the interface.

## 1. Scope the learning experience

- Establish the learner's goal, background, preferred depth, course/version, selected lectures, and output destination from the request. Ask only for missing decisions that materially change the work; otherwise state reasonable assumptions.
- Preserve explicit constraints on publishing, sharing, source selection, and review. Separate building, reviewing, deploying, and changing the audience. Obtain permission before publication or audience expansion unless the user has already explicitly authorized that destination and audience. Do not treat a local preview or successful build as a published site.
- Choose a multi-page wiki for substantial lecture collections or cross-linked concepts; choose a curated webpage for a focused topic or smaller source set. Respect an explicit output choice and explain any proposed change.
- Use the relevant PDF, presentation, software-engineering, and Sites skills and their available tools for implementation as needed. Keep this workflow independent of a particular course, framework, and hosting provider. Identify unavailable capabilities before promising extraction or publication.
- Record the selected scope, inputs, output format, audience, review gates, and acceptance checks in a short delivery plan.

## Bundled implementation resources

- For a requested scroll-synchronized slide/notes experience, read [references/scroll-reader-contract.md](references/scroll-reader-contract.md). Use [assets/reader-template/index.html](assets/reader-template/index.html) as an optional functional starting point, not a fixed design. Customize HTML, CSS, JavaScript, or framework to the user’s tastes and relevant UI skills while preserving the behavioral contract. Do not select this reader automatically for every wiki. Read [references/reader-template.md](references/reader-template.md) for its data schema, run commands, and regression tests.
- For real PDF/caption extraction and structural checks, read [references/extraction-and-validation.md](references/extraction-and-validation.md) and use the bundled scripts; record their dependencies and limitations.
- For a complete original sample and nested-path publishing guidance, read [references/worked-example.md](references/worked-example.md). Keep example data separate from real course evidence.

## 2. Inventory, extract, and normalize sources

1. Build a source manifest with stable IDs, titles, lecture IDs, original URLs, version/date, source type, access status, provenance, rights information, and extraction status. Use the schema in [references/content-contract.md](references/content-contract.md).
2. Prefer official course pages and instructor-hosted materials. Confirm that slide decks, videos, and readings belong to the same lecture and edition. Record discrepancies rather than silently combining versions.
3. Extract slide text with page boundaries intact. Inspect rendered pages for figures, equations, speaker notes, and OCR errors. Distinguish PDF page index from printed slide number.
4. Obtain actual captions or transcripts through an authorized source, or transcribe accessible audio only when authorized and supported. Retain timestamps and label human captions, automatic captions, and machine transcription distinctly.
5. If no transcript is available, mark it unavailable and produce explicitly slide-grounded notes. Never invent spoken content, quotations, timestamps, or transcript coverage from slides or general knowledge. Do not label a summary as a transcript.
6. Track coverage using explicit denominators: lectures inspected/selected, slides covered/total, and transcripts obtained/expected. Separate discovery from successful retrieval, extraction, grounding, and validation. Describe partial work honestly.

## 3. Synthesize content for learning

- Produce structured lesson/concept records with source locators before rendering. Distinguish extraction from synthesis: preserve original page numbers and timestamps, then derive summaries, explanations, and review material with traceable evidence.
- Organize a course overview, lecture index, lecture pages, concept/glossary pages, and source/coverage page. Add prerequisites and a suggested study sequence when useful.
- Give each lecture an executive summary, learning objectives, key concepts, worked explanations, diagrams, slide-by-slide notes, review questions, and source links. Scale depth to available evidence; do not generate filler to populate every section.
- Make each explanation self-contained enough for study while linking back to its sources. Label instructor material, paraphrase, independent explanation, inference, and supplemental examples clearly. Attribute external explanations separately.
- Connect concepts across lectures only where supported. State assumptions, notation, limitations, and distinctions that prevent common misunderstandings.
- Keep executive summaries genuinely brief, with the main problem, mechanism, takeaway, and implications. Reserve technical detail for the body.

## 4. Align slides, videos, and notes

- Give each slide a stable anchor, visible page/slide number, concise title, source link, key idea, explanation, and optional diagram or exercise.
- Associate transcript segments with slides only where timestamps or observed content support the mapping. Record exact, approximate, or unaligned status. Never imply word-level or slide-transition synchronization from a rough topic match.
- Link timestamped video segments when verified. For gaps, expose the limitation in the UI instead of fabricating a start/end time. Provide usable slide navigation without requiring video access.
- Keep rendering separate from structured source and lesson data so citations, coverage, and corrections remain consistent.

## 5. Define the UI and content presentation before implementation

- Write a concrete UI brief: sitemap or page outline, navigation model, page types, content hierarchy, typography and spacing, diagram/math treatment, source display, responsive behavior, and interactive states. Use [references/ui-presentation-contract.md](references/ui-presentation-contract.md).
- Map each content type to its presentation: executive summary, concept explanation, slide note, diagram, source citation, review question, and coverage/gap notice. Define what is visible initially versus progressively disclosed. Do not hide essential caveats behind optional controls.
- Choose layouts from the material rather than imposing one template. A course wiki may need an index, lecture pages, and linked concepts; a focused curated page may need an overview, themed sections, and a source appendix.
- When slide-by-slide learning is in scope and slides are available, define a coordinated slide/notes reader: a stable current-slide state, previous/next and index navigation, deep links, and matching notes. Add video synchronization only for evidence-backed mappings; label approximate alignment and preserve manual navigation for unaligned segments.
- Define mobile behavior explicitly: e.g. stack the slide and notes or use accessible tabs while preserving selection and reading context. Specify keyboard behavior, focus, loading/empty/error states, and fallbacks for missing media.
- Review the UI brief against the user's goals and requested approval gates. Resolve material decisions before building; otherwise proceed with documented assumptions.

## 6. Implement readable, rights-aware pages

- Default to a lightweight static site with responsive layout, clear navigation, deep links, and optional client-side search. Avoid unnecessary accounts, tracking, or backend services.
- Create original explanatory diagrams with labeled relationships, a caption, and a text equivalent. Mark conceptual illustrations as such; do not present invented measurements as data. Check arrows, units, equations, and semantics against the source.
- Use semantic headings, descriptive links, keyboard navigation, visible focus, sufficient contrast, accessible math, alt text, and no color-only encoding. Ensure diagrams and tables remain readable on small screens.
- Link to copyrighted sources by default. Public availability is not redistribution permission. Record licenses and attribution; reproduce slides, figures, or long excerpts only within applicable permissions and policy. Do not bundle entire source decks or transcripts merely because they are downloadable.

## 7. Validate evidence, UI, and delivery

- Run available build, lint, and content checks. Check internal links, stable anchors, duplicate IDs, missing references, manifest totals, and nonempty lesson sections. Separate verified from untested external links.
- Audit all core claims and a representative sample of slide notes, equations, diagrams, and timestamp mappings against original sources. Increase coverage when errors appear. Do not claim exhaustive review after sampling.
- Inspect actual desktop and mobile renders against the UI brief. Check typography, hierarchy, long equations/tables, diagram labels, citations, gap notices, keyboard focus, overflow, and navigation. Record the viewports and pages inspected; fix defects and recheck them.
- Test selected-slide/notes agreement, direct-link reload, Back/Forward, previous/next boundaries, and rapid or repeated navigation when a coordinated reader is included. Test timestamp jumps only where supported and verify missing media does not break reading. Test search and disclosure controls when implemented.
- Report actual checks and unresolved issues rather than assuming that compilation proves usability.
- Present a reviewable preview or artifact, scope/coverage, source limitations, rights caveats, and validation results. Honor any review-before-publish request; obtain any required approval before deployment or audience changes.
- Deliver the runnable wiki or curated webpage, its verified preview/artifact/link, source manifest, structured content, UI brief, and concise QA/coverage report. Include run/build instructions when source code is delivered. State exactly what is completed, missing, sampled, untested, and published versus only prepared; retain records for corrections.
- If implementation, rendering, or hosting is unavailable, deliver the completed intermediate artifacts and identify the blocked stage. Do not call a plan, Markdown-only synthesis, or unverified URL a finished website.
