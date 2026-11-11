# Time-to-Time Agent Skills

A growing curation of useful agent and subagent skills, collected from time to time.

Each skill is an independent workflow with its own instructions, usage guide, and supporting resources. This repository is the collection, not a single-purpose tool. Choose the skills that fit your work.

## Skill catalog

| Skill | What it helps with | Guide | Instructions |
| --- | --- | --- | --- |
| Build Course Wiki | Extract and synthesize course sources, define the UI, and deliver a verified wiki or curated webpage. | [Usage and installation](skills/build-course-wiki/README.md) | [SKILL.md](skills/build-course-wiki/SKILL.md) |

The catalog lists only skills available in this repository today. New skills belong alongside existing ones under `skills/`.

<a id="build-course-wiki"></a>

For the wiki workflow, see the [Build Course Wiki guide](skills/build-course-wiki/README.md).

## Install a skill

Review the selected skill's instructions and requirements before installing. Skills guide an agent; they do not supply every tool, service, or permission a task may need.

### Skills CLI

List available skills without installing them:

```sh
npx skills add gcgloven/time-to-time-agent-skills --list
```

Install a specific skill by its catalog name. For example:

```sh
npx skills add gcgloven/time-to-time-agent-skills --skill build-course-wiki
```

Choose your agent in the prompts, or append `-a codex` to target Codex. Installation is project-local by default; add `-g` only for a user-wide installation. Run project-local commands from the intended project directory.

The CLI currently requires Node.js 22.20 or later. Syntax and paths were checked against the official [CLI reference](https://github.com/vercel-labs/skills/blob/main/docs/commands.md), [agent paths](https://github.com/vercel-labs/skills/blob/main/docs/agents.md), and [runtime requirement](https://github.com/vercel-labs/skills/blob/main/package.json) on 2026-11-11. This is direct installation from GitHub, not a claim of marketplace listing or approval.

### Manual installation

1. Use **Code → Download ZIP** and extract it, or clone this repository:
   ```sh
   git clone https://github.com/gcgloven/time-to-time-agent-skills.git
   ```
2. Copy the complete `skills/<skill-name>/` folder into your agent's supported skills directory, including any references, scripts, assets, and agent metadata. Do not copy only `SKILL.md`.
3. For project-local Codex use, copy it to `.agents/skills/<skill-name>/`. Review or back up an existing installation before replacing it.
4. Follow your client's refresh instructions, then ask it to use the selected skill by name.

See each skill's guide for a concrete example and requirements. A GitHub download does not automatically install skills into a hosted ChatGPT account.

## Use a skill

Open its guide, provide the requested inputs, and ask your agent to use the skill's name. Review its planned actions and outputs; installing a skill does not grant publishing, sharing, or account access permissions.

<a id="example-request"></a>

[Build Course Wiki example request](skills/build-course-wiki/README.md#example-request)

## Layout

```text
README.md                         Collection overview and catalog
CONTRIBUTING.md                   How to add and validate a skill
skills/
  build-course-wiki/
    README.md                     Skill overview, installation, and examples
    SKILL.md                      Portable agent instructions
    agents/openai.yaml            Optional client display metadata
    references/content-contract.md
    references/ui-presentation-contract.md
assets/
  build-course-wiki.webp           Existing illustration URL, kept stable
```

Skill instructions follow the [Agent Skills format](https://agentskills.io/specification). Client-specific metadata stays with its skill; the collection has no root `SKILL.md` that would merge every workflow into one.

## Add another skill

See [Contributing](CONTRIBUTING.md) for the folder contract and validation checklist. Keep new skills independent and add a catalog entry only when their files are present.

