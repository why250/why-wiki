# Skill: Ingest Book

> **Created:** 2026-06-08
> **Origin:** 大型参考书（300+ 页）一次性 ingest 导致 token 爆炸——每章本质上是独立论文，应按章拆分处理

---

## What this skill is for

当用户在 `raw/` 中放入大型多章节 PDF 参考书时，使用本技能按章节拆分处理。每章独立转换（marker `page_range`）、独立摄入（ingest），最后创建一个书籍 hub 页链接所有章节。

**本技能解决的核心问题：** 全书一次性摄入消耗 150K+ tokens；分章摄入每章仅 15-30K tokens。

---

## Prerequisites

- [ ] PDF 书籍已放入 `raw/` 子目录（如 `raw/books/`）
- [ ] Python 环境中已安装 `marker-pdf`（参见 `preprocess-pdf.md`）
- [ ] 已阅读 `schema.md`（了解页面格式约定）
- [ ] 已阅读 `preprocess-pdf.md`（了解页码范围转换 recipe）

---

## Steps

### Phase 1 — 提取目录 (TOC)

**目标：** 获取章节标题和起始页码，让用户确认章节划分。

**1a. 转换目录页**

提取 PDF 前 15 页（覆盖目录部分）：
```python
config_parser = ConfigParser(
    {
        "output_format": "markdown",
        "output_dir": "raw/books/book-slug",
        "page_range": "0-14",  # 前 15 页
    }
)
```

如果 15 页不够（目录很长），根据实际情况增加。

**1b. 解析章节列表**

从 toc.md 中提取章节标题和起始页码。常见的目录格式：
- `Chapter 1  Introduction .............. 3`
- `第 1 章  引言 ...................... 5`
- `1. Overview ........................ 7`

**Gotcha:** PDF 实际页码和书本页码可能偏移——前言/目录可能用罗马数字（i, ii, iii...）。需要对比 PDF 前几页的实际页码号（通常在页脚）与 TOC 中标注的页码，计算偏移量。

**1c. 呈现给用户确认**

以表格形式列出所有检测到的章节：
```
| # | 章节标题 | 书本页码 | PDF页码 |
|---|---------|---------|--------|
| 1 | Introduction | p1 | p13 |
| 2 | Background  | p15 | p27 |
...
```
等待用户确认（可以删减、调整、补充）。用户也可以指定只处理某些章节。

---

### Phase 2 — 逐章转换

**目标：** 对每一章，使用 marker 将对应页码范围转为独立 .md 文件。

遍历用户确认的章节列表：

```python
# 对每一章
chapter_pdf_range = f"{start_page}-{end_page}"  # 0-based
output_dir = f"raw/books/{book_slug}"

config_parser = ConfigParser(
    {
        "output_format": "markdown",
        "output_dir": output_dir,
        "page_range": chapter_pdf_range,
    }
)
# ... 标准转换代码，见 preprocess-pdf.md
```

**产物命名：** `<book-slug>/ch-NN-<chapter-slug>.md`
- `NN`：两位数字章节号（01, 02, ...）
- `chapter-slug`：简短的英文 slug（如 `intro`, `background`, `noise-analysis`）

**Gotcha:** marker 转换每一章都需要时间（每章 ~30-90 秒）。这是正常的——总时间 = 章数 × 单章转换时间，但换来了后续每章 ingest 的低 token 消耗。

---

### Phase 3 — 逐章摄入

**目标：** 对每章 .md 运行标准 ingest 流程，创建 source 页、实体/概念页。

对每一章，执行标准 ingest（参考 `ingest.md`）：

1. 读取该章的 .md 文件
2. 提取实体、概念、关键主张
3. 创建 `wiki/sources/<book-slug>-ch-NN-<slug>.md`
4. 创建/更新实体页和概念页

**章节 source 页 frontmatter 特殊字段：**
```yaml
---
type: source
title: "Book Title — Chapter NN: Chapter Title"
book: "[[book-slug]]"    # 指向书籍 hub 页
chapter: NN               # 章节编号
authors: [Author Name]
year: YYYY
url: ""
venue: "Book Chapter"
tags: []
related: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**跨章节概念去重：** 后续章节 ingest 时，先检查 `wiki/index.md` 中是否已有相关实体/概念页：
- 已存在 → 更新该页面（追加新章节的发现，不重复创建）
- 不存在 → 正常创建

**自动连续处理：** 所有章节连续转换+摄入，中间不暂停。只在中途出错时才中断，等待用户决策（跳过该章 / 重试 / 终止）。

每章完成后输出简短进度：
```
[3/12] Chapter 3: Noise Analysis → 已摄入，2 个新概念，1 个实体
```

---

### Phase 4 — 创建书籍 Hub 页

**目标：** 创建全书总览 source 页，作为所有章节的入口。

创建 `wiki/sources/<book-slug>.md`：

```yaml
---
type: source
title: "Full Book Title"
authors: [Author Name]
year: YYYY
url: ""
venue: "Publisher Name"
tags: []
related: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# Book Title

## 书籍信息

- **作者**：...
- **出版年份**：...
- **出版社**：...
- **章节数**：N

## 章节索引

- [[book-slug-ch-01-intro]] — 第 1 章：Introduction
- [[book-slug-ch-02-background]] — 第 2 章：Background
- ...

## 全书主题

（简要概述全书覆盖的主要领域——从各章 source 页的核心要点中提炼）

## 跨章节概念

（列出在全书中反复出现的关键概念，链接到概念页）
```

---

## Verification

- [ ] TOC 解析正确，章节页码对应实际 PDF 页面
- [ ] 每章 .md 文件已生成且内容可读
- [ ] 每章 source 页已创建，frontmatter 含 `book` 和 `chapter` 字段
- [ ] 实体/概念页在章节间没有重复创建
- [ ] 书籍 hub 页链接了所有已摄入章节
- [ ] `wiki/index.md` 中列出了所有新页面
- [ ] `wiki/log.md` 记录了每章的摄入条目

---

## Interruption Recovery

如果处理到第 N 章时中断，恢复流程：
1. 检查 `wiki/log.md`，找到最后成功摄入的章节
2. 从下一章继续
3. 已完成章节的 .md 文件无需重新转换

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| TOC 解析失败 | 目录格式不规则（扫描版、非标准排版） | 让用户手动提供章节和页码范围 |
| 页码偏移不一致 | 前言用罗马数字，正文用阿拉伯数字 | 对比 TOC 页码和 PDF 实际页码计算偏移量 |
| 某章转换质量差 | 该章含大量图表或特殊排版 | 对该章重试或让用户决定是否跳过 |
| 跨章节概念重复创建 | ingest 时未检查已有概念页 | Phase 3 中必须先 search 已有页面再创建 |

---

## Related

- PDF 转换: `.claude/skills/preprocess-pdf.md`
- 标准摄入: `.claude/skills/ingest.md`
- Schema: `schema.md`
- 规则: `.claude/rules/wiki.md`
