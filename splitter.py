# … існуючі імпорти …
from Test_pdf import load_bookmarks_from_pdf
from PyPDF2 import PdfWriter, PdfReader
import os

def split_pdf(pdf_path: str, output_dir: str, level: int = 2):
    os.makedirs(output_dir, exist_ok=True)
    reader = PdfReader(pdf_path)

    all_bm = load_bookmarks_from_pdf(pdf_path)
    bms = [bm for bm in all_bm if bm["level"] == level]

    for idx, bm in enumerate(bms):
        start = bm["page"]
        end = (bms[idx + 1]["page"] - 1) if idx + 1 < len(bms) else len(reader.pages) - 1

        writer = PdfWriter()
        for p in range(start, end + 1):
            writer.add_page(reader.pages[p])

        title = bm["title"]
        safe_title = "".join(c for c in title if c.isalnum() or c in (" ", "_", "-")).strip()

        out_name = f"{idx+1:02d}_{safe_title}.pdf"
        out_path = os.path.join(output_dir, out_name)
        with open(out_path, "wb") as f_out:
            writer.write(f_out)

    print(f"Збережено {len(bms)} файлів у {output_dir}/")