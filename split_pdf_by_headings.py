#!/usr/bin/env python3
import os
import json

from Test_pdf import load_bookmarks_from_pdf
from PyPDF2 import PdfReader, PdfWriter
from cli import parse_args


def load_config(path: str) -> dict:
    if not path:
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def split_pdf(
    pdf_path: str,
    output_dir: str = "out",
    level: int = 2
):
    all_bm = load_bookmarks_from_pdf(pdf_path)
    lvl_bm = [bm for bm in all_bm if bmlevel == level]

    os.makedirs(output_dir, exist_ok=True)
    reader = PdfReader(pdf_path)

    for idx, bm in enumerate(lvl_bm):
        start = bm.page
        end = (
            lvl_bm[idx + 1].page - 1
            if idx + 1 < len(lvl_bm)
            else len(reader.pages) - 1
    )

        writer = PdfWriter()
        for p in range(start, end + 1):
            writer.add_page(reader.pages[p])

        safe_title = "".join(
            ch for ch in bm.title if ch.isalnum() or ch in " _-"
        ).strip()
        out_name = os.path.join(output_dir, f"{safe_title}.pdf")

        with open(out_name, "wb") as out_f:
            writer.write(out_f)

def main():
    args = parse_args()
    cfg = load_config(args.config)
    pdf_path = args.input_pdf
    output_dir = args.output_dir or cfg.get("output_dir", "output")
    level = args.level if args.level is not None else cfg.get("bookmark_level", 2)

    split_pdf(
        pdf_path=pdf_path,
        output_dir=output_dir,
        level=level
    )

if __name__ == "__main__":
    main()
