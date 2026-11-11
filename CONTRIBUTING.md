# Adding a skill

This repository curates independent agent workflows. A new skill should solve a concrete task and be useful on its own, without turning the repository into an application for any one workflow.

## Folder contract

Create `skills/<skill-name>/` using a short, descriptive lowercase hyphenated name.

- **SKILL.md** is required. Include valid YAML frontmatter with `name` matching the folder and a `description` explaining what the skill does and when to use it. Write actionable instructions, boundaries, and validation steps.
- **README.md** is the human-facing guide. Explain the outcome, requirements, installation command with `--skill <skill-name>`, an example request, and limitations.
- **references/** holds supporting material the instructions link to, when needed.
- **scripts/** and **assets/** are optional. Keep skill-specific resources inside the skill folder so installation can carry them with it.
- **agents/openai.yaml** is optional client metadata. Keep its display name and default prompt consistent with the skill.

See the [Agent Skills specification](https://agentskills.io/specification) for naming and format requirements. Do not add a root `SKILL.md`; the root README is a catalog, not a combined skill.

The existing `assets/build-course-wiki.webp` path is retained for link compatibility. New skill-specific assets should live with their skill.

## Catalog and documentation

1. Add one row to the root README's skill catalog with the real skill name, concise purpose, usage-guide link, and instruction link.
2. Keep skill-specific illustrations, examples, and detailed explanations in that skill's README.
3. Document required tools or services honestly. Do not imply that a workflow bundles tools, grants permissions, or installs into every client.
4. Preserve published paths where possible. If a path changes, review both repository links and external website references.
5. Do not list placeholder or planned skills as available.

## Validation checklist

- [ ] Frontmatter parses, names are unique, and the folder matches the skill name.
- [ ] Every relative link and required supporting file resolves from the file that references it.
- [ ] The skill can be understood independently; it does not depend on unpublished personal files or private context.
- [ ] Instructions preserve user review, sharing, publishing, and access constraints.
- [ ] The usage guide includes a realistic request, requirements, and known limitations.
- [ ] CLI discovery lists the expected skill: `npx skills add ./ --list` from the repository root.
- [ ] Test installation into a disposable project for the intended client and confirm required references, scripts, and assets are included.
- [ ] Exercise a representative task and relevant failure cases; report actual checks and gaps.
- [ ] Run any checks required by the skill's scripts or implementation, if present.
- [ ] Update the catalog only for files included in the change.

Do not claim an installation or end-to-end test passed merely because the documentation was reviewed. Keep shared collection documentation concise as the catalog grows.

