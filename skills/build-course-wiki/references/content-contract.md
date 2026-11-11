# Content and evidence contract

Use these fields as a portable starting point, not a required technology stack. Omit optional fields instead of inventing values.

## Source manifest

- `source_id`: stable internal key.
- `lecture_id`, `title`, `source_type`: course page, slides, video, transcript, reading, or supplemental source.
- `url`, `version_or_date`, `retrieved_at`.
- `access_status`: available, inaccessible, missing, or not checked.
- `provenance`: official, instructor, publisher, third-party, or user-provided.
- `rights`: observed license, attribution, redistribution restrictions, or unknown. Record the rights page URL when available.
- `extraction_status`: not attempted, extracted, partial, or failed; explain gaps.
- `page_count` or `duration_seconds` when verified.
- For transcripts: `transcript_origin`, `language`, `timestamped`, `quality_notes`; never treat generated summaries as transcript sources.

## Lecture record

- Stable `lecture_id`, title, order, source IDs, prerequisite concept IDs.
- Learning objectives, executive summary, concepts, explanations, diagrams, practice questions, and optional answers.
- Claim-level citations for substantive course-specific statements, with slide/page or timestamp locators where available.
- Separate supplemental explanation from source-derived claims.
- Coverage object with selected/available/processed counts, transcript availability, known omissions, and verification scope.

## Slide record

- `slide_id`, `lecture_id`, `pdf_page` (state indexing convention), optional printed slide number.
- Title, main idea, explanation, source IDs and locators.
- Optional diagram and text equivalent, example, misconception, practice question.
- Optional video interval with start/end seconds only if verified.
- `alignment_status`: exact, approximate, unaligned, or video unavailable; include evidence or uncertainty note.

## Review cases

Exercise these cases during development as applicable:

1. Slides available, transcript inaccessible: show slide-grounded notes and the transcript gap; invent no spoken claims or timestamps.
2. Different course editions: retain separate provenance, surface mismatch, and avoid implied alignment.
3. A scanned equation or ambiguous diagram: inspect the rendered page, record uncertainty, and avoid confident OCR-based errors.
4. A source missing reuse terms: link and summarize within applicable limits rather than republishing the full material.
5. Mobile navigation and keyboard use: ensure slide anchors, menu, search, and diagram alternatives work without hover or a mouse.
6. Partial processing: show numerator and denominator, disclose sampled QA, and avoid claiming complete course coverage.
7. Review requested before publication: produce a preview/artifact without deployment or audience change until authorized.

