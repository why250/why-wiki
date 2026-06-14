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

### 2. 验证 Python 环境（多版本探测）

**必须遍历所有可用的 Python 安装，而非仅检查默认 `python`。** Windows 系统常同时安装多个 Python 版本，默认版本未必是配置了 marker 的那个。

#### 2.1 发现所有 Python 安装

```bash
where python 2>&1  # Windows: 列出 PATH 中所有 python.exe
ls "C:/Users/$USER/AppData/Local/Programs/Python/Python*/python.exe" 2>&1  # 常见安装位置
```

记录所有找到的 Python 解释器的完整路径。

#### 2.2 逐个检查，找到可用环境

对每个解释器，按优先级检查：

```
1. torch CUDA 可用？ → 首选（GPU 加速）
2. marker-pdf + torch 可 import？ → 次选（CPU fallback）
3. 跳过 →
```

```bash
# 以完整路径调用每个 Python 解释器：
"C:/path/to/python.exe" -c "import torch; print('CUDA:', torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A')"
"C:/path/to/python.exe" -c "from marker.converters.pdf import PdfConverter; print('marker ok')"
```

#### 2.3 选择环境

- **GPU 环境优先** — 标记为本次转换使用的解释器
- 如果所有环境都不可用 → 向用户确认是否需要安装依赖
- **不要在不同解释器之间混用包**
- 后续所有转换命令均使用选定的解释器**完整路径**

---

### 3. 执行转换

**使用步骤 2 选定的解释器完整路径执行。** 以下示例中 `python` 指代已选定的解释器。

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

### 4. 提示下一步

转换完成后，告诉用户：

```
PDF 已转换为 raw/paper/<pdf-basename>/<pdf-basename>.md
如需纳入 wiki，运行 ingest 技能处理该 .md 文件。
```

**不要自动触发 ingest。** 让用户先确认转换质量。

---

## Verification

- [ ] `.md` 文件已在 `raw/paper/<pdf-basename>/` 子文件夹中生成
- [ ] `.md` 文件内容可读、结构完整（标题层级、段落、表格）
- [ ] 如转换了页码范围，确认内容范围正确
- [ ] `_meta.json` 和图片文件同步生成（如有）
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
