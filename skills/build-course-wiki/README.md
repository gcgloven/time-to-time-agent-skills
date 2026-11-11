# Build Course Wiki

[← Skill catalog](../../README.md#skill-catalog)

![Lecture slides, video, and transcript sources become an organized, source-linked learning wiki.](../../assets/build-course-wiki.webp)

Turn lecture slides, readings, and authentic video transcripts into a source-grounded wiki or curated learning webpage through the full pipeline:

1. Inventory, extract, and normalize the data with provenance.
2. Synthesize summaries, concepts, detailed notes, diagrams, and review material.
3. Define the information architecture, UI, content presentation, and interaction states.
4. Implement the responsive, accessible wiki or curated webpage.
5. Verify evidence, rendered pages, and interactions; deliver a reviewable result before any authorized publication.

For slide-based learning, define coordinated slide/notes navigation and add video alignment only when supported by evidence. Choose the layout and output format from the learning goal rather than forcing every source set into one template.

The workflow is course-, framework-, and host-independent. Missing transcripts stay visibly missing; approximate alignment is labeled; source coverage and validation are reported honestly. Public source availability is not permission to republish full decks or transcripts.

- [Skill instructions](SKILL.md)
- [Content and evidence contract](references/content-contract.md)
- [UI and presentation contract](references/ui-presentation-contract.md)
- [Overview and background](https://gcgloven.github.io/knowledge/build-course-wiki/)

## Install

Review the instructions first. This skill contains instructions and a reference document, not an executable site generator.

From your intended project directory:

```sh
npx skills add gcgloven/time-to-time-agent-skills --skill build-course-wiki
```

Choose the target agent in the prompts. For Codex explicitly:

```sh
npx skills add gcgloven/time-to-time-agent-skills --skill build-course-wiki -a codex
```

For manual installation, copy this complete folder, including `references/` and `agents/`, to your agent's skills directory. The project-local Codex destination is `.agents/skills/build-course-wiki/`. Do not overwrite an existing installation without review or backup.

See the [collection installation guide](../../README.md#install-a-skill) for runtime requirements, scope, discovery, and supported-client documentation.

## Example request

> Use build-course-wiki to create a self-learning wiki from these lecture PDFs and official video links. Start with lectures 1–3. Extract and synthesize the sources, define the UI and content presentation, then implement a responsive wiki with brief summaries, concept diagrams, coordinated slide/notes navigation, review questions, and a source coverage page. Use actual transcripts only; show any gaps. Prepare a reviewable preview before publishing.

Provide the course/version, source files or URLs, target audience, depth, and destination when known.

## Requirements and boundaries

- PDF extraction, transcription, browsing, coding, and hosting tools depend on the agent environment and are not bundled here.
- Use actual accessible sources. If a transcript is unavailable, keep the notes slide-grounded and disclose the gap.
- Review source rights before reproducing slides, figures, or transcript excerpts.
- Building a preview does not authorize publishing it or changing its audience.
- Validate source coverage, links, accessibility, and the rendered result before delivery.

## Files

- `SKILL.md`: portable workflow instructions.
- `references/content-contract.md`: evidence schema and review cases.
- `agents/openai.yaml`: optional display metadata for compatible clients.
- `references/ui-presentation-contract.md`: UI definition, presentation patterns, and visual/interaction QA.
- `README.md`: this human-facing guide.

The illustration remains at its existing repository asset URL so older links continue to work; it is not required to run the skill.

