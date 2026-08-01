#!/usr/bin/env python3
"""Convert one PDF to Markdown with Marker.

Run this script with the Python interpreter returned by setup_marker_env.py.
Page ranges use Marker's zero-based inclusive ``START-END`` convention.
"""

from __future__ import annotations

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert a PDF to Markdown with Marker.")
    parser.add_argument("pdf", type=Path, help="Source PDF path")
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Directory for Markdown, metadata, and extracted images",
    )
    parser.add_argument(
        "--name",
        help="Output basename without an extension (default: PDF filename)",
    )
    parser.add_argument(
        "--page-range",
        help="Inclusive zero-based range accepted by Marker, for example 74-77",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    pdf_path = args.pdf.resolve()
    if not pdf_path.is_file():
        raise SystemExit(f"PDF not found: {pdf_path}")

    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    # Import after parsing so `--help` works without a Marker installation.
    from marker.config.parser import ConfigParser
    from marker.converters.pdf import PdfConverter
    from marker.models import create_model_dict
    from marker.output import save_output

    config: dict[str, str] = {
        "output_format": "markdown",
        "output_dir": str(output_dir),
    }
    if args.page_range:
        config["page_range"] = args.page_range

    config_parser = ConfigParser(config)
    converter = PdfConverter(
        config=config_parser.generate_config_dict(),
        artifact_dict=create_model_dict(),
        processor_list=config_parser.get_processors(),
        renderer=config_parser.get_renderer(),
        llm_service=config_parser.get_llm_service(),
    )
    rendered = converter(str(pdf_path))
    save_output(rendered, str(output_dir), args.name or pdf_path.stem)


if __name__ == "__main__":
    main()
