# Always Rules

> Core constraints loaded every session. Keep this file short — every line here costs attention on every task.

---

## Hard stops — ask before proceeding

- Do not delete or modify files in `raw/` — sources are immutable
- Do not remove entries from `wiki/log.md` — log is append-only
- Do not expose secrets, tokens, or credentials in wiki pages

## Wiki discipline

- Every new wiki page MUST have complete YAML frontmatter per `schema.md`
- Every new page MUST be added to `wiki/index.md` immediately
- Every operation MUST be logged to `wiki/log.md` with `## [YYYY-MM-DD] <action> | <detail>` format
- Use `[[page-slug]]` wikilinks for ALL cross-references — no bare text links between wiki pages

## Source handling

- Raw sources are immutable — summarize them in `wiki/sources/`, never edit the originals
- When a source contradicts existing wiki content, flag it explicitly — never silently overwrite

## SSOT

- `schema.md` is the single source of truth for page formats and conventions
- `CLAUDE.md` is a router only — do not store knowledge there
- Do not duplicate information across files; link instead

---

> This file should stay under 50 lines. Move anything longer to a specific rule file.
