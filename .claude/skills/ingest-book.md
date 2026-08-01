# Skill: Ingest Book

> **Created:** 2026-06-08
> **Origin:** 大型参考书（300+ 页）一次性 ingest 导致 token 爆炸——每章本质上是独立论文，应按章拆分处理

---

## What this skill is for

当用户在 `raw/` 中放入大型多章节 PDF 参考书时，使用本技能按章节拆分处理。每章独立转换（marker `page_range`）、独立摄入（ingest），最后创建一个书籍 hub 页链接所有章节。

**本技能解决的核心问题：** 全书一次性摄入消耗 150K+ tokens；分章摄入每章仅 15-30K tokens。

---

## Prerequisites

- [ ] PDF 书籍已放入 `raw/book/` 目录
- [ ] 本机 marker 环境已初始化（`preprocess-pdf.md` 步骤 0：`resolve` / 必要时 `setup`）
- [ ] 已阅读 `schema.md`（了解页面格式约定）
- [ ] 已阅读 `preprocess-pdf.md`（环境解析 + 页码范围转换 recipe）

## 输出目录约定

文件夹名与 PDF 文件名一致，放在 `raw/book/` 下：

```
raw/book/<pdf-filename>/                  ← 与 PDF 同名
├── Introduction/                          ← 每章一个文件夹，以章节标题命名
│   ├── Introduction.md                    ← Markdown（重命名后）
│   ├── Introduction_meta.json             ← 元数据（重命名后）
│   └── _page_X_Figure_Y.jpeg              ← 提取的图片
├── Background/
│   └── ...
```

> `book-slug`（wiki 页面用的缩写名）只在 wiki 中使用，`raw/` 下直接用 PDF 文件名作为文件夹名。

---

## Steps

### Phase 1 — 用户指定章节划分

**目标：** 获取用户提供的章节列表（标题 + 页码范围），作为逐章转换的输入。

**1a. 提示用户提供章节信息**

首先向用户询问此书的章节划分，给出明确格式提示：

```
请提供此书的章节划分（可指定只处理部分章节）：

| # | 章节标题 | 起始页码 | 结束页码 |
|---|---------|---------|---------|
| 1 | Introduction | 1 | 14 |
| 2 | Background  | 15 | 40 |
| 3 | CMOS DAC Architectures | 41 | 72 |
...
```

- **页码范围**：默认使用书本页码（1-based），如果是 PDF 页码请注明
- 根据章节标题自动生成 slug（简短英文标识，如 `intro`、`background`、`cmos-dac-architectures`）
- 用户可指定只处理某些章节

**1b. 确认 PDF 页码偏移**

用户提供的页码范围需要转为 marker 使用的 **0-based PDF 页码**。

- 检查 PDF 前几页的实际页码（通常在页脚），确认偏移量
- 常见情况：目录/前言用罗马数字（i, ii, iii...），正文从 p1 开始，此时 p1 可能对应 PDF 第 13 页
- 书本页码 pN → 0-based PDF 页码 = pN + offset - 1

在转换计划中列出最终的 PDF 页码范围，待用户确认：
```
| # | 章节标题 | PDF页码(0-based) |
|---|---------|------------------|
| 1 | Introduction | 12-25 |
| 2 | Background  | 26-51 |
...
```

用户确认后进入 Phase 2。

---

### Phase 2 — 逐章转换

**目标：** 对每一章，使用 marker 将对应页码范围转为独立 .md 文件。

遍历用户确认的章节列表：

```python
# 对每一章
# pdf_folder = "raw/book/<pdf-filename>"（与 PDF 同名）
chapter_pdf_range = f"{start_page}-{end_page}"  # 0-based
chapter_name = "Introduction"  # 章节标题，直接用作文件夹名和文件名
output_dir = f"{pdf_folder}/{chapter_name}"

config_parser = ConfigParser(
    {
        "output_format": "markdown",
        "output_dir": output_dir,
        "page_range": chapter_pdf_range,
    }
)
# ... 见下方 save_output 调用方式
```

**产物命名：** `raw/book/<pdf-filename>/<Chapter Title>/<Chapter Title>.md`
- `<pdf-filename>`：PDF 文件名（不含 `.pdf` 扩展名），如 `Time Interleaving DAC (TI-DAC)`
- `<Chapter Title>`：章节标题原文，直接用作文件夹名和 .md 文件名，如 `Introduction`、`Appendix A — Behavioral DAC Modeling`

**Gotcha — 跳过 `get_output_folder()`：** marker 的 `save_output(rendered, output_dir, fname_base)` 直接写入指定路径，不会自动嵌套。但旧代码模式习惯于调用 `config_parser.get_output_folder(pdf_path)`（返回 `output_dir/pdf_basename`），这才是嵌套的根源。

**正确做法：** 直接调用 `save_output()`，手动传入目标路径和文件名：

```python
converter = PdfConverter(...)
rendered = converter(pdf_path)

# 直接指定输出路径，跳过 get_output_folder()
output_dir = f"raw/book/<pdf-filename>/<Chapter Title>"
os.makedirs(output_dir, exist_ok=True)
save_output(rendered, output_dir, "<Chapter Title>")
# 产物: raw/book/<pdf-filename>/<Chapter Title>/<Chapter Title>.md
#        raw/book/<pdf-filename>/<Chapter Title>/<Chapter Title>_meta.json
#        raw/book/<pdf-filename>/<Chapter Title>/_page_X_Figure_Y.jpeg
```
无嵌套，无需重命名。

**Gotcha:** marker 转换每一章都需要时间。公式密集的章节（如 Static/Dynamic Behaviour）可能 20-30 分钟，轻量章节 1-3 分钟。总时间由最重的章节决定。

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

- [ ] 用户提供的章节页码已正确转换为 0-based PDF 页码范围
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
| 用户提供的页码与实际不符 | 书本页码与 PDF 页码有偏移（前言用罗马数字等） | 检查 PDF 前几页的实际页码号（页脚），计算偏移量并修正 |
| 转换后内容不对 | marker 页码范围（0-based）计算错误 | 核对书本页码 → 0-based PDF 页码的转换公式：`pdf_page = book_page + offset - 1` |
| 某章转换质量差 | 该章含大量图表或特殊排版 | 对该章重试或让用户决定是否跳过 |
| 跨章节概念重复创建 | ingest 时未检查已有概念页 | Phase 3 中必须先 search 已有页面再创建 |

---

## Related

- PDF 转换: `.claude/skills/preprocess-pdf.md`
- 标准摄入: `.claude/skills/ingest.md`
- Schema: `schema.md`
- 规则: `.claude/rules/wiki.md`
