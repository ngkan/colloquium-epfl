"""Command-line entry point; no changes to the installed Colloquium package."""

import argparse
from pathlib import Path

from .builder import build_epfl


def main():
    parser = argparse.ArgumentParser(prog="epfl-slides")
    parser.add_argument("source", type=Path, help="Colloquium Markdown source")
    parser.add_argument("-o", "--output", type=Path, help="HTML output path")
    parser.add_argument("--pdf", action="store_true", help="Also export PDF with Chromium")
    args = parser.parse_args()
    try:
        output = build_epfl(args.source, args.output)
        print(f"Built {output}")
        if args.pdf:
            from colloquium.export import export_pdf

            pdf = export_pdf(str(output), str(output.with_suffix(".pdf")))
            if pdf is None:
                parser.exit(1, "PDF export failed. Install a Chromium-based browser and retry.\n")
            print(f"Exported {pdf}")
    except (ValueError, OSError) as error:
        parser.exit(1, f"epfl-slides: {error}\n")
