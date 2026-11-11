---
name: build-course-wiki
description: Turn course lectures, slide PDFs, readings, and authentic video transcripts into a source-grounded self-learning static wiki. Use for course companion sites, lecture study guides, executive summaries, concept diagrams, slide-level learning notes, and cross-lecture synthesis, especially when source completeness and slide/video alignment matter.
---

# Build Course Wiki

## Scope the learning experience

- Establish the learner's goal, background, preferred depth, course/version, selected lectures, and output destination from the request. Ask only for missing decisions that materially change the work; otherwise state reasonable assumptions.
- Preserve explicit constraints on publishing, sharing, source selection, and review. Separate building, reviewing, deploying, and changing the audience. Do not treat a local preview or successful build as a published site.
- Use relevant PDF, presentation, software-engineering, and Sites skills for their respective implementation steps. Keep this workflow independent of a particular course, framework, and hosting provider.

## Inventory and verify sources first

1. Build a source manifest with stable IDs, titles, lecture IDs, original URLs, version/date, source type, access status, provenance, rights information, and extraction status. Use the schema in [references/content-contract.md](references/content-contract.md).
2. Prefer official course pages and instructor-hosted materials. Confirm that slide decks, videos, and readings belong to the same lecture and edition. Record discrepancies rather than silently combining versions.
3. Extract slide text with page boundaries intact. Inspect rendered pages for figures, equations, speaker notes, and OCR errors. Distinguish PDF page index from printed slide number.
4. Obtain actual captions or transcripts through an authorized source, or transcribe accessible audio only when authorized and supported. Retain timestamps and label human captions, automatic captions, and machine transcription distinctly.
5. If no transcript is available, mark it unavailable and produce explicitly slide-grounded notes. Never invent spoken content, quotations, timestamps, or transcript coverage from slides or general knowledge. Do not label a summary as a transcript.
6. Track coverage using explicit denominators: lectures inspected/selected, slides covered/total, and transcripts obtained/expected. Separate discovery from successful retrieval, extraction, grounding, and validation. Describe partial work honestly.

## Plan the wiki around learning

- Organize a course overview, lecture index, lecture pages, concept/glossary pages, and source/coverage page. Add prerequisites and a suggested study sequence when useful.
- Give each lecture an executive summary, learning objectives, key concepts, worked explanations, diagrams, slide-by-slide notes, review questions, and source links. Scale depth to available evidence; do not generate filler to populate every section.
- Make each explanation self-contained enough for study while linking back to its sources. Label instructor material, paraphrase, independent explanation, inference, and supplemental examples clearly. Attribute external explanations separately.
- Connect concepts across lectures only where supported. State assumptions, notation, limitations, and distinctions that prevent common misunderstandings.
- Keep executive summaries genuinely brief, with the main problem, mechanism, takeaway, and implications. Reserve technical detail for the body.

## Align slides, videos, and notes

- Give each slide a stable anchor, visible page/slide number, concise title, source link, key idea, explanation, and optional diagram or exercise.
- Associate transcript segments with slides only where timestamps or observed content support the mapping. Record exact, approximate, or unaligned status. Never imply word-level or slide-transition synchronization from a rough topic match.
- Link timestamped video segments when verified. For gaps, expose the limitation in the UI instead of fabricating a start/end time. Provide usable slide navigation without requiring video access.
- Keep rendering separate from structured source and lesson data so citations, coverage, and corrections remain consistent.

## Build readable, rights-aware pages

- Default to a lightweight static site with responsive layout, clear navigation, deep links, and optional client-side search. Avoid unnecessary accounts, tracking, or backend services.
- Create original explanatory diagrams with labeled relationships, a caption, and a text equivalent. Mark conceptual illustrations as such; do not present invented measurements as data. Check arrows, units, equations, and semantics against the source.
- Use semantic headings, descriptive links, keyboard navigation, visible focus, sufficient contrast, accessible math, alt text, and no color-only encoding. Ensure diagrams and tables remain readable on small screens.
- Link to copyrighted sources by default. Public availability is not redistribution permission. Record licenses and attribution; reproduce slides, figures, or long excerpts only within applicable permissions and policy. Do not bundle entire source decks or transcripts merely because they are downloadable.

## Validate before delivery or publication

- Run available build, lint, and content checks. Check internal links, stable anchors, duplicate IDs, missing references, manifest totals, and nonempty lesson sections. Separate verified from untested external links.
- Audit all core claims and a representative sample of slide notes, equations, diagrams, and timestamp mappings against original sources. Increase coverage when errors appear. Do not claim exhaustive review after sampling.
- Inspect desktop and mobile renders, keyboard interaction, overflow, search, and navigation. Report actual checks and unresolved issues rather than assuming that compilation proves usability.
- Present a reviewable preview or artifact, scope/coverage, source limitations, rights caveats, and validation results. Honor any review-before-publish request; obtain any required approval before deployment or audience changes.
- Deliver the verified artifact or accessible link and state exactly what is completed, missing, and published versus only prepared. Preserve source manifests and structured content for later corrections.

