# CLAUDE.md — Wiki Router

> **This file is a router, not a knowledge base.**
> Do NOT add conventions, workflows, or rules here.
> Every piece of knowledge lives exactly once (SSOT).

---

## Step 1 — Read First (Always)

Before any task, read:
- `schema.md` — page types, frontmatter, naming conventions, cross-referencing rules
- `.claude/rules/always.md` — non-negotiable constraints for every session

---

## Step 2 — Identify Task Domain

| Task type | Load these docs |
|-----------|----------------|
| Ingest a new source | `.claude/skills/ingest.md` + `wiki/index.md` |
| Ingest a book | `.claude/skills/ingest-book.md` |
| Answer a question | `wiki/index.md` → drill into relevant pages |
| Health check / lint | `.claude/skills/lint.md` |
| Create a wiki page | `schema.md` (frontmatter + naming) + `.claude/rules/wiki.md` |
| Update wiki pages | `wiki/index.md` + `.claude/rules/wiki.md` |
| Preprocess a PDF | `.claude/skills/preprocess-pdf.md` |
| Record architecture decision | `docs/decisions.md` (append) |
| Unknown / ambiguous | Ask the user before loading anything |

**Rule: Load only what the task requires. Do not preload all docs.**

---

## Step 3 — Apply Rules

All rules live in `.claude/rules/`.

| Rule file | When it applies |
|-----------|----------------|
| `always.md` | Every task, no exceptions |
| `wiki.md` | Any wiki page creation, edit, or cross-reference |

---

## Step 4 — Use Skills (SOPs)

Before executing a known workflow, check `.claude/skills/` first.

| Skill | When to use |
|-------|-------------|
| `ingest.md` | User adds a source to `raw/` and asks to process it |
| `ingest-book.md` | User adds a large multi-chapter PDF book to `raw/` |
| `preprocess-pdf.md` | User adds a PDF to `raw/` and needs it converted to Markdown first |
| `lint.md` | User asks for a health check or periodic maintenance |

If a matching skill exists → follow it exactly.
If no skill exists → execute, then propose creating one after.

---

## Step 5 — After Task Completion

Ask yourself:

1. Did new facts about the wiki emerge?
   → Update the relevant page in `wiki/`

2. Did we encounter a constraint that should always be enforced?
   → Propose adding to `.claude/rules/`

3. Did we complete a repeatable workflow?
   → Propose adding to `.claude/skills/`

4. Did we make a non-obvious architectural decision about the wiki itself?
   → Append to `docs/decisions.md`

---

## Directory Map

```
CLAUDE.md                       ← you are here (router only)
README.md                       ← human-facing entry point
schema.md                       ← SSOT for conventions and page formats
purpose.md                      ← project goals and scope

wiki/
  index.md                      ← catalog of all pages (read first on every query)
  log.md                        ← chronological operation log
  overview.md                   ← high-level project summary
  entities/ concepts/ sources/  ← knowledge pages
  queries/ comparisons/ synthesis/

raw/                            ← immutable source documents

.claude/
  rules/
    always.md                   ← loaded every session, keep it short
    wiki.md                     ← wiki editing and cross-referencing rules
  skills/
    ingest.md                   ← SOP: ingesting a raw source
    ingest-book.md              ← SOP: ingesting a multi-chapter book chapter-by-chapter
    preprocess-pdf.md           ← SOP: converting PDF to Markdown before ingest
    lint.md                     ← SOP: wiki health check
    _template.md                ← copy this when creating a new skill

docs/
  decisions.md                  ← ADR log for wiki architecture decisions
```

---

## SSOT Principle

Every fact exists in **exactly one place**.

- `CLAUDE.md` → links to `schema.md`, `rules/`, `skills/` — does not duplicate
- `schema.md` → defines conventions (the *what*)
- `skills/` → defines workflows (the *how*)
- `rules/` → defines constraints (the *must/must-not*)

If two files say the same thing, one of them is wrong.

---

## What NOT to put in this file

- ❌ Page type definitions → `schema.md`
- ❌ Frontmatter format → `schema.md`
- ❌ Naming conventions → `schema.md`
- ❌ Ingest workflow steps → `.claude/skills/ingest.md`
- ❌ Lint workflow steps → `.claude/skills/lint.md`
- ❌ Cross-referencing rules → `.claude/rules/wiki.md`
- ❌ Architecture decisions → `docs/decisions.md`
