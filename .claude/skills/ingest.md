# Skill: Ingest Source

> **Created:** 2026-06-07
> **Origin:** LLM Wiki pattern — the most frequent and important workflow

---

## What this skill is for

Processing a new raw source: reading it, extracting knowledge, and integrating it across all relevant wiki pages. A single source typically touches 5–15 wiki pages.

---

## Prerequisites

- [ ] Source file exists in `raw/`
- [ ] **Source file is a Markdown (`.md`) file** — ingest 只处理 Markdown；PDF 等其他格式需先走对应的预处理技能（如 `.claude/skills/preprocess-pdf.md`）
- [ ] `wiki/index.md` is up to date
- [ ] Read `schema.md` for page format conventions

---

## Steps

### 1. Read and understand the source

Read the source file thoroughly. Identify:
- Named entities (people, tools, organizations, datasets)
- Key concepts, techniques, or frameworks
- Claims that may confirm or contradict existing wiki content
- What's novel vs. what's already known

### 2. Discuss with the user

Before writing anything, share 3–5 key takeaways. Ask:
- What stood out as important?
- What should be emphasized?
- Any angles or connections the user wants to highlight?

### 3. Write the source summary page

Create `wiki/sources/<author-year-slug>.md` with complete frontmatter:

```yaml
---
type: source
title: Full title
authors: [Author Name]
year: YYYY
url: ""
venue: ""
tags: []
related: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

Include sections: **核心要点** (key takeaways), **关键概念** (concepts to link), **待探究的问题** (open questions).

### 4. Create or update entity pages

For each named entity, create `wiki/entities/<name>.md` or update the existing one.
Link back to the source via `[[source-slug]]`.

### 5. Create or update concept pages

For each idea or technique, create `wiki/concepts/<concept>.md` or update the existing one.
Link back to the source and to related entities/concepts.

### 6. Check for contradictions

Search existing wiki pages for claims that conflict with the new source.
If found:
- Add a "Contradictions" section to the affected page
- Create or update a query page in `wiki/queries/`
- Link both sources from the query page

### 7. Update the index

Add every new page to `wiki/index.md` under the correct heading:
```
- [[page-slug]] — one-line description
```

### 8. Append to the log

```
## [YYYY-MM-DD] ingest | Source Title
- Created source page: [[source-slug]]
- Created/updated entities: [[entity-1]], [[entity-2]]
- Created/updated concepts: [[concept-1]], [[concept-2]]
- Cross-references added to N existing pages
```

### 9. Update the overview

If the project's high-level understanding has shifted, update `wiki/overview.md`.

---

## Verification

How to confirm this was done correctly:
- [ ] Source page exists in `wiki/sources/` with complete frontmatter
- [ ] All mentioned entities have pages in `wiki/entities/`
- [ ] All mentioned concepts have pages in `wiki/concepts/`
- [ ] `wiki/index.md` lists every new page
- [ ] `wiki/log.md` has the ingest entry in correct format
- [ ] No broken `[[wikilinks]]` to new pages

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Forgot to update index.md | Run through the new pages and add each to index |
| Source page has no inbound links | Update entity/concept pages to link back to the source |
| Missed a contradiction | Re-read the source against all related concept pages |

---

## Related

- Rules: `.claude/rules/wiki.md`
- Schema: `schema.md`
- Index: `wiki/index.md`
