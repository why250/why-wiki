# Skill: Preprocess PDF

> **Created:** 2026-06-07
> **Origin:** 扩展 wiki 项目的源文件处理能力 — 支持 PDF 二进制文件，通过 marker 转为 Markdown 后再走 ingest 流程

---

## What this skill is for

当用户在 `raw/` 中放入 PDF 文件时，使用本技能将 PDF 预处理为 Markdown。转换产物写入 PDF 同级目录，之后即可用 `ingest` 技能正常处理。

**本技能只做一件事：PDF → Markdown 转换。** 不涉及 wiki 页面创建、实体提取或索引更新。

---

## Prerequisites

- [ ] PDF 文件已放入 `raw/` 的某个子目录（如 `raw/paper/`、`raw/articles/`）
- [ ] Python 环境中已安装 `marker-pdf` 及其依赖
- [ ] 已阅读 `schema.md`（了解项目约定）

---

## Steps

### 1. 确认转换范围

向用户确认：
- PDF 文件的完整路径
- 转换范围：全文 / 指定页码范围（1-based）/ 某章节

**Gotcha:** 如果用户给的页码是书本页码（1-based），转换到 marker 的 `page_range` 时需要 `-1`（marker 使用 0-based 索引）。

---

### 2. 验证 Python 环境

在将执行转换的 Python 解释器中依次运行：

```bash
python -c "import sys; print(sys.executable)"
python -m pip show marker-pdf
python -c "import marker, pydantic, pdftext, surya, cv2"
```

如果任一 import 失败：
- 确认当前 `python` 指向的是安装了 `marker-pdf` 的解释器
- 不要在不同解释器之间混用包

---

### 3. 执行转换

**默认使用非 LLM 路径。** 只有用户明确要求时才启用 Ollama 增强，且本地模型必须支持 `vision`。

**仅预览（不写文件）：**
```python
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered

pdf_path = "raw/paper/example.pdf"

converter = PdfConverter(
    artifact_dict=create_model_dict(),
)
rendered = converter(pdf_path)
markdown_text, ext, images = text_from_rendered(rendered)
# markdown_text: Markdown 文本
# rendered.metadata: 后续写为 _meta.json 的数据
```

**全文转换：**
```python
from marker.config.parser import ConfigParser
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import save_output

pdf_path = "raw/paper/example.pdf"
output_dir = "raw/paper"  # 与 PDF 同目录

config_parser = ConfigParser(
    {
        "output_format": "markdown",
        "output_dir": output_dir,
    }
)

converter = PdfConverter(
    config=config_parser.generate_config_dict(),
    artifact_dict=create_model_dict(),
    processor_list=config_parser.get_processors(),
    renderer=config_parser.get_renderer(),
    llm_service=config_parser.get_llm_service(),
)

rendered = converter(pdf_path)
out_folder = config_parser.get_output_folder(pdf_path)
save_output(rendered, out_folder, config_parser.get_base_filename(pdf_path))
```

**页码范围转换：**
```python
config_parser = ConfigParser(
    {
        "output_format": "markdown",
        "output_dir": "raw/paper",
        "page_range": "74-77",  # 0-based: 书本 75-78 页
    }
)
# 其余代码同上
```

**默认使用非 LLM 转换路径。** 除非用户明确要求本地 Ollama 增强，否则不启用。

---

### 4. 确认输出

`save_output()` 会在 PDF 同级目录生成：

```
raw/paper/
├── example.pdf          ← 原始 PDF（不动）
├── example.md           ← 转换后的 Markdown（可被 ingest 读取）
├── example_meta.json    ← 元数据（辅助）
└── example_images/      ← 提取的图片（如有）
```

**Gotcha:** 如果 PDF 同级目录已存在同名 `.md`，`save_output()` 会覆盖。如有疑虑，先提示用户。

`_meta.json` 包含检测到的目录结构、每页提取统计、文本提取方式（如 `surya`）、debug 数据路径。返回结果时优先给出 `.md` 路径，`_meta.json` 作为可选辅助信息。

---

### 5. 提示下一步

转换完成后，告诉用户：

```
PDF 已转换为 raw/paper/example.md
如需纳入 wiki，运行 ingest 技能处理该 .md 文件。
```

**不要自动触发 ingest。** 让用户先确认转换质量。

---

## Verification

- [ ] `.md` 文件已在 PDF 同级目录生成
- [ ] `.md` 文件内容可读、结构完整（标题层级、段落、表格）
- [ ] 如转换了页码范围，确认内容范围正确
- [ ] `_meta.json` 和 images 目录同步生成（如有）
- [ ] 原始 PDF 未被修改

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `ModuleNotFoundError: pydantic` | 当前 Python 解释器未安装 marker-pdf | 检查 `python -c "import sys; print(sys.executable)"`，在正确的环境中安装 |
| `where python` 和实际环境不一致 | Windows 多 Python 版本 | 使用完整路径调用目标解释器 |
| Pillow 编译失败 (Python 3.14) | marker 依赖 `Pillow<11`，与 Python 3.14 不兼容 | 优先使用已验证的 Python 环境，或降级到 3.12/3.13 |
| 中文 PDF 转换质量差 | marker 默认模型对中文支持有限 | 提示用户考虑使用支持多语言的配置选项 |
| 转换后 .md 空白或乱码 | PDF 可能是扫描版（图片型） | 检查 PDF 是否包含可提取文本层；扫描版需 OCR |

---

## Related

- 下一步技能: `.claude/skills/ingest.md`
- 大书分章摄入: `.claude/skills/ingest-book.md`（处理 300+ 页参考书的正确方式——按章节拆分，避免 token 爆炸）
- Schema: `schema.md`
- 规则: `.claude/rules/always.md`
