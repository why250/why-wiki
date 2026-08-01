# Skill: Preprocess PDF

> **Created:** 2026-06-07
> **Updated:** 2026-07-21
> **Origin:** 扩展 wiki 项目的源文件处理能力 — 支持 PDF 二进制文件，通过 marker 转为 Markdown 后再走 ingest 流程

---

## What this skill is for

当用户在 `raw/` 中放入 PDF 文件时，使用本技能将 PDF 预处理为 Markdown。转换产物写入 PDF 同级目录，之后即可用 `ingest` 技能正常处理。

**本技能只做一件事：PDF → Markdown 转换。** 不涉及 wiki 页面创建、实体提取或索引更新。

---

## Prerequisites

- [ ] PDF 文件已放入 `raw/` 的某个子目录（如 `raw/paper/`、`raw/articles/`）
- [ ] 本机已初始化 marker 环境（见步骤 0）；或用户明确要求现在初始化
- [ ] 已阅读 `schema.md`（了解项目约定）

---

## Steps

### 0. 解析 marker 环境（先读缓存，失败再初始化）

**不要每次手动遍历本机 Python。** 使用脚本读写机器本地配置：

| 文件 | 是否入库 | 作用 |
|------|---------|------|
| `.claude/marker-env.local.json` | 否（gitignore） | 缓存：python 绝对路径、GPU、marker/torch 版本 |
| `.venv-marker/` | 否（gitignore） | 仅在本机找不到可用 marker 时才创建的专用 venv |

从**仓库根目录**执行：

```bash
python .claude/skills/scripts/setup_marker_env.py resolve
```

- 成功 → stdout 只有一行：可用解释器的**绝对路径**。后续所有转换都用这个路径（下文记为 `$MARKER_PYTHON`）。
- 失败（无配置 / 路径失效）→ 走 **0b 初始化**，不要自行 `where python` 扫全盘。

默认 `resolve` **只校验路径存在**（秒级）。需要完整缓存或怀疑环境坏了时：

```bash
python .claude/skills/scripts/setup_marker_env.py resolve --json
python .claude/skills/scripts/setup_marker_env.py resolve --verify   # 慢：重新 import marker/torch
python .claude/skills/scripts/setup_marker_env.py doctor             # 刷新 GPU/版本并写回配置
```

#### 0b. 新设备 / 首次使用：初始化

marker + torch 体积大、安装慢。**默认策略：先复用，找不到再新建。**

直接跑（agent 默认命令）：

```bash
python .claude/skills/scripts/setup_marker_env.py setup
```

脚本会按顺序：

1. 若 `.venv-marker/` 已有可用 marker → 绑定，不重装
2. 否则扫描本机 Python，绑定已能 `import marker` 的环境（**CUDA 优先**于 CPU）
3. 都没有 → 才创建 `.venv-marker/` 并 `pip install marker-pdf`（会很慢，属预期）

可选参数：

```bash
# 只要 GPU：优先复用已有 CUDA marker；没有再装 GPU torch + marker
python .claude/skills/scripts/setup_marker_env.py setup --cuda cu124

# 强制新建/重建项目 venv（跳过复用，会重新下载）
python .claude/skills/scripts/setup_marker_env.py setup --force-venv
python .claude/skills/scripts/setup_marker_env.py setup --force-venv --cuda cu124

# 手动指定绑定某个解释器（不扫描）
python .claude/skills/scripts/setup_marker_env.py setup --use-existing "C:/Path/to/python.exe"

# 指定解释器且允许往里装 marker
python .claude/skills/scripts/setup_marker_env.py setup --use-existing "C:/Path/to/python.exe" --install-into-existing
```

初始化成功后会写入 `.claude/marker-env.local.json`，并打印 python / GPU / 版本摘要。然后重新 `resolve` 取得 `$MARKER_PYTHON`。

**环境异常时刷新探测（不重装）：**

```bash
python .claude/skills/scripts/setup_marker_env.py doctor
```

**Gotcha:**
- 配置与 venv 是**机器本地**的，勿提交 git；skill 与脚本可分享，环境需每人/每机跑一次 `setup`。
- `setup` 默认会探测多个解释器（每个要 import torch/marker，可能数分钟）；这只发生在初始化，日常转换只跑 `resolve`。
- 优先 Python **3.11–3.13**；3.14+ 常因 Pillow 与 marker 不兼容失败。
- **不要在不同解释器之间混用包**；转换命令始终用 `$MARKER_PYTHON` 完整路径。
- 不要把「推荐新建 venv」当成默认——除非用户明确要求隔离，或本机确实没有 marker。
---

### 1. 确认转换范围

向用户确认：
- PDF 文件的完整路径
- 转换范围：全文 / 指定页码范围（1-based）/ 某章节

**Gotcha:** 如果用户给的页码是书本页码（1-based），转换到 marker 的 `page_range` 时需要 `-1`（marker 使用 0-based 索引）。

---

### 2. 执行转换

**使用步骤 0 得到的 `$MARKER_PYTHON`。** 默认非 LLM 路径；仅当用户明确要求且本地模型支持 `vision` 时才启用 Ollama。

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
import os

pdf_path = "raw/paper/example.pdf"
output_dir = "raw/paper/example"  # 目标输出目录

os.makedirs(output_dir, exist_ok=True)

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

# 直接调用 save_output()，手动指定输出路径和文件名
# 跳过 get_output_folder() — 它会在 output_dir 下额外嵌套一层 PDF 文件名
save_output(rendered, output_dir, "example")
# 产物: raw/paper/example/example.md
#       raw/paper/example/example_meta.json
#       raw/paper/example/_page_X_Figure_Y.jpeg
```

**页码范围转换：**
```python
config_parser = ConfigParser(
    {
        "output_format": "markdown",
        "output_dir": "raw/paper/example",  # 目标输出目录
        "page_range": "74-77",  # 0-based: 书本 75-78 页
    }
)
# 其余代码同上（converter 创建 + save_output 直接调用）
# save_output(rendered, "raw/paper/example", "example")
```

调用方式示例（PowerShell）：

```powershell
& "$MARKER_PYTHON" -c @"
# ... 上文转换代码 ...
"@
```

---

### 3. 提示下一步

转换完成后，告诉用户：

```
PDF 已转换为 raw/paper/<pdf-basename>/<pdf-basename>.md
如需纳入 wiki，运行 ingest 技能处理该 .md 文件。
```

**不要自动触发 ingest。** 让用户先确认转换质量。

---

## Verification

- [ ] `resolve` 能打印有效 `$MARKER_PYTHON`（或本次刚完成 `setup`）
- [ ] `.md` 文件已在 `raw/paper/<pdf-basename>/` 子文件夹中生成
- [ ] `.md` 文件内容可读、结构完整（标题层级、段落、表格）
- [ ] 如转换了页码范围，确认内容范围正确
- [ ] `_meta.json` 和图片文件同步生成（如有）
- [ ] 原始 PDF 未被修改

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `No marker env config found` | 新机器未初始化 | 跑 `setup`（会先复用再考虑新建） |
| `Configured python missing` | 换机 / 卸载了 Python | 重新 `setup` |
| `Configured python failed marker import` / doctor 失败 | 环境被改坏 | `doctor`；仍失败则 `setup`；要强制重装用 `--force-venv` |
| `ModuleNotFoundError: pydantic` / marker | 绑错解释器或未安装 | `setup` 自动找可用环境，或 `--use-existing PATH --install-into-existing` |
| Pillow 编译失败 (Python 3.14) | marker 与 3.14 不兼容 | 用 3.11–3.13；必要时 `--force-venv --python PATH` |
| CUDA torch 安装失败 | `--cuda` tag 与驱动不匹配 | 换 `cu121`/`cu124`/`cu126`，或去掉 `--cuda` 用 CPU |
| `setup` 很慢但在 Probing | 正在 import 多个解释器 | 正常；找到后会复用且不重装。日常请用 `resolve` |
| 中文 PDF 转换质量差 | marker 默认模型对中文支持有限 | 提示用户考虑多语言配置 |
| 转换后 .md 空白或乱码 | PDF 可能是扫描版 | 检查是否有文本层；扫描版需 OCR |

---

## Related

- 环境脚本: `.claude/skills/scripts/setup_marker_env.py`
- 下一步技能: `.claude/skills/ingest.md`
- 大书分章摄入: `.claude/skills/ingest-book.md`
- Schema: `schema.md`
- 规则: `.claude/rules/always.md`
