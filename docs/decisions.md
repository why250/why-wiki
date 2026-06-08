# Architecture Decisions (ADR Log)

> Append a new entry whenever a non-obvious decision is made about the wiki itself.
> Never delete old entries — they explain why the wiki is structured the way it is.
> Format: date, decision, context, alternatives considered, consequences.

---

## Template

```
### [YYYY-MM-DD] Title of Decision

**Decision:** What we decided.

**Context:** Why we needed to decide this. What constraint or problem triggered it.

**Alternatives considered:**
- Option A — why rejected
- Option B — why rejected

**Consequences:**
- What becomes easier
- What becomes harder or is now a constraint
```

---

## Log

### [2026-06-06] Adopted LLM Wiki pattern

**Decision:** Build a personal knowledge base using the LLM Wiki pattern — LLM maintains all wiki pages, human curates sources and asks questions.

**Context:** Starting a knowledge base for deep technical research (ADC design, AI-assisted engineering, open-source hardware). Wanted a system that compounds over time rather than re-deriving knowledge on every query (vs. RAG approach).

**Alternatives considered:**
- Pure RAG (NotebookLM, ChatGPT file upload) — rejected because knowledge doesn't accumulate; every query re-discovers from raw sources
- Manual wiki (writing pages by hand) — rejected because maintenance burden grows faster than value
- Plain folder of markdown notes without LLM involvement — rejected because cross-referencing and consistency are too tedious to maintain manually

**Consequences:**
- LLM does all writing, cross-referencing, and maintenance
- Human focuses on sourcing, curation, and asking good questions
- Wiki quality depends on consistent application of schema conventions

### [2026-06-07] Adopted ai-project-template routing architecture

**Decision:** Restructured CLAUDE.md into a lightweight router, added `.claude/rules/` and `.claude/skills/` directories following the `why250/ai-project-template` pattern.

**Context:** The initial CLAUDE.md was a monolithic knowledge base — it contained conventions, workflow steps, rules, and directory maps all in one file. This violated SSOT (single source of truth) because information was duplicated between CLAUDE.md and schema.md. The ai-project-template demonstrates a cleaner separation: AGENT.md routes, rules/ constrains, skills/ standardizes.

**Alternatives considered:**
- Keep monolithic CLAUDE.md — rejected because duplication creates maintenance debt; when conventions change, both files must be updated
- Remove CLAUDE.md entirely — rejected because the LLM needs a routing entry point to know which docs to load for which task

**Consequences:**
- CLAUDE.md is now ~80 lines (was ~120 lines)
- Rules and skills are independently maintainable
- SSOT: schema.md owns conventions, rules/ owns constraints, skills/ owns workflows
- Adding a new workflow means creating one skill file, not editing CLAUDE.md
