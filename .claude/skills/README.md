# Project Skills

This directory contains portable, task-focused skills for maintaining this wiki.
Each skill is self-contained: `SKILL.md` defines the workflow and optional
resources live beside it. Copy an entire skill directory to another project's
`.claude/skills/` directory to share it.

## Catalog

| Skill | Purpose |
| --- | --- |
| `ingest-source/` | Turn one Markdown source into linked wiki knowledge. |
| `ingest-book/` | Convert and ingest a large PDF book chapter by chapter. |
| `lint-wiki/` | Audit wiki links, coverage, contradictions, and staleness. |
| `preprocess-pdf/` | Convert a PDF into Markdown with Marker. |

## Conventions

- Name skill directories with lowercase kebab-case.
- Put the trigger description and workflow in `SKILL.md`.
- Keep scripts in the owning skill's `scripts/` directory; keep reusable
  reference material in `references/` and output templates in `assets/`.
- Do not add a `SKILL.md` under `templates/`: templates are not runnable
  skills and should not be discovered as one.
- Start a new skill from `templates/SKILL.md.template`, then replace every
  placeholder before sharing it.
