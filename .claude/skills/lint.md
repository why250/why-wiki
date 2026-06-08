# Skill: Lint (Health Check)

> **Created:** 2026-06-07
> **Origin:** LLM Wiki pattern — periodic wiki maintenance

---

## What this skill is for

Periodic health check of the entire wiki. Find issues that have accumulated: contradictions, stale claims, orphans, missing pages, broken links.

---

## Prerequisites

- [ ] `wiki/index.md` is reasonably up to date
- [ ] Enough time to do a thorough scan (not a quick 2-minute check)

---

## Steps

### 1. Scan for contradictions

Read through concept pages and entity pages looking for:
- Conflicting claims from different sources
- Claims marked as uncertain that a newer source might resolve
- For each found: flag with a "⚠ Contradiction" marker and link to a query page

### 2. Find stale claims

For each source page, check its `year` field:
- Is a newer source available that supersedes it?
- If yes, add a "⚠ May be superseded by [[newer-source]]" note

### 3. Identify orphan pages

Check `wiki/index.md` for all listed pages. For each page:
- Search for `[[page-slug]]` across other wiki files
- If no other page links to it → it's an orphan
- For each orphan: either create inbound links from relevant pages, or flag it

### 4. Spot missing pages

Look for concepts or entities mentioned across multiple pages but lacking their own page:
- Scan for repeated references to the same name/topic
- If mentioned 3+ times without a page → propose creating one

### 5. Check broken links

For every `[[wikilink]]` in the wiki:
- Verify the target page exists
- List any broken links found

### 6. Suggest new sources

Based on gaps identified:
- Propose web searches or sources that could fill knowledge gaps
- Note queries that could be answered with additional sourcing

### 7. Summarize and log

Produce a lint report:

```
## [YYYY-MM-DD] lint | Health check summary
- Contradictions found: N
- Stale claims: N
- Orphan pages: N
- Missing pages suggested: N
- Broken links: N
- Source gaps suggested: N
```

---

## Verification

- [ ] All contradictions are documented with query pages
- [ ] All broken links are either fixed or flagged
- [ ] Orphan pages have been reviewed (linked or flagged)
- [ ] Lint results are logged to `wiki/log.md`

---

## Related

- Rules: `.claude/rules/wiki.md`
- Index: `wiki/index.md`
