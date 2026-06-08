# Wiki Rules

> Loaded when creating, editing, or cross-referencing wiki pages.
> Does NOT replace `schema.md` — this file defines constraints, schema.md defines formats.

---

## Page creation checklist

Before writing a new wiki page, verify:
- [ ] Page type matches one of the 7 types in `schema.md`
- [ ] File goes in the correct directory (`wiki/entities/`, `wiki/concepts/`, etc.)
- [ ] Filename follows `kebab-case.md` convention
- [ ] YAML frontmatter is complete (`type`, `title`, `tags`, `related`, `created`, `updated`)
- [ ] Source pages additionally have `authors`, `year`, `url`, `venue`

## Cross-referencing rules

- **Every new page must have at least one inbound link** — update at least one existing page to link to it
- **Use `[[page-slug]]` syntax** exclusively for wiki-to-wiki links
- **Source pages** must link to every entity and concept they discuss
- **Query pages** must link to all sources and concepts they draw on
- **Synthesis pages** must list all contributing sources in `related:` frontmatter
- **Entity and concept pages** must appear in `wiki/index.md`

## Index maintenance

- After creating ANY new page, add it to `wiki/index.md` under the correct type heading
- Format: `- [[page-slug]] — one-line description`
- If a page's content has significantly changed, update its index description

## Log format

- Reverse chronological (newest entry first)
- Format: `## [YYYY-MM-DD] <action> | <detail>`
- Actions: `ingest`, `query`, `lint`, `update`, `create`

## Contradiction handling

When two sources disagree:
1. Note the contradiction on BOTH the relevant concept page and entity page
2. Create or update a query page to track the open question
3. Link both conflicting sources from the query page via `[[wikilinks]]`
4. When resolved, document the resolution in a synthesis page and close the query

## What NOT to do

- ❌ Create pages without frontmatter
- ❌ Skip updating `wiki/index.md`
- ❌ Skip logging to `wiki/log.md`
- ❌ Use bare URLs instead of `[[wikilinks]]` between wiki pages
- ❌ Edit raw source files
- ❌ Silently overwrite existing claims with contradictory new information
