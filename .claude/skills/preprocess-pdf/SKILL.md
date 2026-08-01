---
name: preprocess-pdf
description: "Convert a PDF source under raw/ into Markdown using Marker while preserving the original PDF and writing output beside it. Use when a user adds a PDF, requests PDF-to-Markdown conversion, or needs a PDF prepared before ingesting it into the wiki."
---

# Preprocess a PDF

This skill converts only. Do not ingest the output or edit the original PDF
without a separate user request.

## Workflow

1. Confirm the PDF path and whether to convert the whole document or a
   page range. Marker ranges are zero-based; translate printed-book page
   numbers only after verifying the PDF offset.
2. From the repository root, resolve the shared local Marker environment:

   ```powershell
   python .claude/skills/preprocess-pdf/scripts/setup_marker_env.py resolve
   ```

   If resolution fails, run `setup`. Use `doctor` to refresh an existing
   configuration. The local configuration and `.venv-marker/` are machine-
   specific and must not be committed.
3. Run the bundled converter with the resolved interpreter. It writes output
   directly to `raw/<category>/<pdf-basename>/` and avoids Marker's unwanted
   nested output directory:

   ```powershell
   $markerPython = python .claude/skills/preprocess-pdf/scripts/setup_marker_env.py resolve
   & $markerPython .claude/skills/preprocess-pdf/scripts/convert_pdf.py `
     raw/paper/example.pdf --output-dir raw/paper/example
   # Optional: --page-range 74-77  (zero-based and inclusive)
   ```
4. Check the Markdown, metadata, and extracted images. For a scanned or
   poorly converted PDF, report the limitation and recommend OCR or a retry.
5. Tell the user the generated Markdown path and offer `ingest-source` as the
   next step. Do not automatically start ingestion.

## Environment commands

```powershell
# First use or missing configuration; reuse an existing Marker install first.
python .claude/skills/preprocess-pdf/scripts/setup_marker_env.py setup

# Verify a configured environment, or refresh its recorded capabilities.
python .claude/skills/preprocess-pdf/scripts/setup_marker_env.py resolve --verify
python .claude/skills/preprocess-pdf/scripts/setup_marker_env.py doctor
```

## Verify

- The original PDF is unchanged.
- Markdown, `_meta.json`, and any images were created in the requested output
  directory and the converted range is correct.

## Resource

- `scripts/setup_marker_env.py` resolves or initializes the local Marker
  interpreter. Run it from the repository root.
- `scripts/convert_pdf.py` performs a full-document or selected-page
  conversion. Do not use `get_output_folder()` in replacement scripts.
