---
name: lint-wiki
description: "Audit a knowledge wiki for broken wikilinks, orphan pages, missing high-value pages, contradictions, stale claims, and research gaps. Use when a user asks for a wiki health check, lint, maintenance audit, or cleanup plan."
---

# Lint the wiki

Read `schema.md`, `.claude/rules/always.md`, `.claude/rules/wiki.md`, and
`wiki/index.md` before auditing.

## Workflow

1. Verify every `[[wikilink]]` resolves to a page and list failures.
2. Find indexed pages with no inbound wikilinks. Add relevant links or flag
   them for review; do not invent a connection.
3. Identify concepts and entities mentioned repeatedly without a dedicated
   page. Propose candidates that appear in at least three relevant places.
4. Compare claims across related source, entity, and concept pages. Flag
   contradictions and stale claims; record unresolved conflicts in query pages
   only after sufficient evidence is available.
5. Identify source gaps that would materially improve the wiki.
6. Report counts and findings, then append the lint summary to `wiki/log.md`.
   Fix only the issues the user authorized; otherwise leave an actionable list.

## Verify

- The report separates confirmed issues from proposals.
- Fixed links, orphan decisions, and contradiction records follow the wiki
  rules; the result is logged in reverse chronological order.
