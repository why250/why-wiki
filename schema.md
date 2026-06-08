# Wiki Schema

This document defines the conventions for this knowledge base — the *what*. For the *how*, see `.claude/skills/` (workflows) and `.claude/rules/` (constraints). `CLAUDE.md` is the router that points to all of these.

> **SSOT:** This file is the single source of truth for page formats, naming, and frontmatter. Do not duplicate this information elsewhere.

## Architecture

Three layers per the LLM Wiki pattern:

| Layer | Location | Ownership | Purpose |
|-------|----------|-----------|---------|
| Raw sources | `raw/` | Human-curated, immutable | Source of truth |
| Wiki | `wiki/` | LLM-maintained | Structured, interlinked knowledge |
| Schema | `schema.md`, `.claude/rules/`, `.claude/skills/` | Co-evolved | Conventions, constraints, and workflows |
| Router | `CLAUDE.md` | LLM entry point | Task routing — tells LLM which docs to load |

## Page Types

| Type | Directory | Purpose |
|------|-----------|---------|
| entity | `wiki/entities/` | Named things (people, tools, organizations, datasets) |
| concept | `wiki/concepts/` | Ideas, techniques, phenomena, frameworks |
| source | `wiki/sources/` | Papers, articles, talks, books, blog posts |
| query | `wiki/queries/` | Open questions under active investigation |
| comparison | `wiki/comparisons/` | Side-by-side analysis of related entities |
| synthesis | `wiki/synthesis/` | Cross-cutting summaries and conclusions |
| overview | `wiki/` | High-level project summary (one per project) |

## Naming Conventions

- Files: `kebab-case.md`
- Entities: match official name where possible (e.g., `openai.md`, `gpt-4.md`)
- Concepts: descriptive noun phrases (e.g., `chain-of-thought.md`)
- Sources: `author-year-slug.md` (e.g., `wei-2022-cot.md`)
- Book chapters: `<book-slug>-ch-NN-<chapter-slug>.md` (e.g., `razavi-analog-cmos-ch-03-noise.md`)
- Book hubs: `<book-slug>.md` (links all chapters)
- Queries: question as slug (e.g., `does-scale-improve-reasoning.md`)

## Frontmatter

All pages must include YAML frontmatter:

```yaml
---
type: entity | concept | source | query | comparison | synthesis | overview
title: Human-readable title
tags: []
related: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

Source pages also include:
```yaml
authors: []
year: YYYY
url: ""
venue: ""
```

Book chapter sources additionally include:
```yaml
book: "[[book-slug]]"   # wikilink to the book hub page
chapter: NN              # chapter number
venue: "Book Chapter"    # explicitly mark as book chapter
```

## Index Format

`wiki/index.md` lists all pages grouped by type. Each entry:
```
- [[page-slug]] — one-line description
```

The LLM updates the index on every ingest. When answering a query, the LLM reads the index first to find relevant pages, then drills into them.

## Log Format

`wiki/log.md` records activity in reverse chronological order:
```
## [YYYY-MM-DD] <action> | <detail>
```

Actions: `ingest`, `query`, `lint`, `update`, `create`

This prefix format makes the log parseable: `grep "^## \[" wiki/log.md | tail -10` gives the last 10 entries.

## Cross-referencing Rules

- Use `[[page-slug]]` syntax to link between wiki pages
- Every entity and concept should appear in `wiki/index.md`
- Queries link to the sources and concepts they draw on
- Synthesis pages cite all contributing sources via `related:`

## Workflows

Detailed step-by-step workflows live in `.claude/skills/` (SSOT):

| Workflow | Skill file | When to use |
|----------|-----------|-------------|
| Ingest a source | `.claude/skills/ingest.md` | Processing new raw sources |
| Health check / lint | `.claude/skills/lint.md` | Periodic wiki maintenance |
| Query | (inline in CLAUDE.md Step 2) | Answering questions from wiki content |

## Contradiction Handling

When sources contradict each other:
1. Note the contradiction in the relevant concept or entity page
2. Create or update a query page to track the open question
3. Link both sources from the query page
4. Resolve in a synthesis page once sufficient evidence exists

See `.claude/rules/wiki.md` for detailed constraints on contradiction handling.
