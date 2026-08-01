---
name: ingest-source
description: "Process one Markdown source in a knowledge wiki: extract claims, create or update source, entity, and concept pages, cross-link them, and update the index and log. Use when a user adds a Markdown file under raw/ and asks to ingest, summarize, or integrate it into the wiki."
---

# Ingest a source

Read `schema.md`, `.claude/rules/always.md`, `.claude/rules/wiki.md`, and
`wiki/index.md` before editing the wiki. Process Markdown sources only; route
PDFs through `preprocess-pdf` first.

## Workflow

1. Read the source fully. Identify material claims, named entities, concepts,
   novelty, and possible conflicts with existing pages.
2. Before writing, give the user 3-5 takeaways and confirm the intended
   emphasis when it is not already clear.
3. Create `wiki/sources/<author-year-slug>.md` using the source frontmatter
   required by `schema.md`. Cover key takeaways, linked concepts, and open
   questions.
4. Search `wiki/index.md` before creating entity or concept pages. Create a
   page only for durable, reusable subjects; otherwise retain the information
   on the source page. Update existing pages rather than duplicating them.
5. Check related pages for contradictions. Document conflicts on the affected
   pages and create or update a query page that links both sources.
6. Add every new page to `wiki/index.md`, append the ingest entry to
   `wiki/log.md`, and update `wiki/overview.md` only when the high-level model
   has changed.

## Verify

- New pages have complete schema-compliant frontmatter and at least one inbound
  link.
- Source, entity, and concept pages link to one another where relevant.
- Every new wikilink resolves, and every new page is indexed and logged.
