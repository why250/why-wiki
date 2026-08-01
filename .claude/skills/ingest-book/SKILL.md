---
name: ingest-book
description: "Process a large multi-chapter PDF book in a knowledge wiki by confirming page ranges, converting each chapter separately with Marker, ingesting chapters incrementally, and creating a book hub page. Use when a book is too large to process as one source or when a user asks to ingest selected book chapters."
---

# Ingest a book

Read `schema.md`, `.claude/rules/always.md`, `.claude/rules/wiki.md`,
`preprocess-pdf/SKILL.md`, and `ingest-source/SKILL.md` before beginning.

## Workflow

1. Ask for the chapters to process: title, start page, and end page. Confirm
   whether these are printed-book pages or PDF pages.
2. Inspect the PDF's front matter to determine the offset. Convert printed
   page `N` to Marker's zero-based PDF index with
   `pdf_page = N + offset - 1`, then show the final ranges for confirmation.
3. For each confirmed chapter, convert only that range. Store its output at
   `raw/book/<pdf-basename>/<chapter-title>/<chapter-title>.md`.
4. Ingest chapters one at a time using `ingest-source`. Create chapter sources
   as `wiki/sources/<book-slug>-ch-NN-<chapter-slug>.md`, adding the `book`,
   `chapter`, and `venue: "Book Chapter"` fields. Search before creating pages
   so cross-chapter entities and concepts stay deduplicated.
5. Give a short progress update after every completed chapter. On interruption,
   inspect `wiki/log.md` and resume at the next unlogged chapter.
6. Create `wiki/sources/<book-slug>.md` as a hub with bibliographic metadata,
   the chapter index, book-level themes, and recurring concepts. Index and log
   all newly created pages.

## Verify

- Chapter ranges and generated Markdown match the intended content.
- All chapter sources point to the hub and no entity or concept was needlessly
  duplicated.
- The hub links every ingested chapter; all pages are indexed and logged.
