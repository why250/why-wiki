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

**不是每个名字都值得独立页面。** 先判断，再创建。标准：

- 第一作者 / 通讯作者，方向核心推动者 → 创建
- 研究机构，多篇论文的共同背景 → 创建
- 团队负责人，与其他已收录工作有关联 → 创建
- 普通合著者，仅出现一次 → **不创建**，信息留在 source page 的 `authors:` 字段即可

确定要创建时，在 `wiki/entities/<name>.md` 中写入，并通过 `[[source-slug]]` 链接回来源。更新已有 entity 时追加新来源引用。

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

### 10. Quick lint before pushing

在 commit 和 push 之前，至少检查：
- [ ] Broken wikilinks — 新页面中的 `[[...]]` 目标是否存在（有意预留的前向引用可列出但不阻塞）
- [ ] Frontmatter 完整性 — 新页面 YAML 是否包含所有必填字段
- [ ] Index 覆盖 — 新页面是否已加入 `wiki/index.md`

通过后再 push。

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
