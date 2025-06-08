# … існуючі імпорти …
from PyPDF2 import PdfReader
from typing import List, Dict

def load_bookmarks_from_pdf(pdf_path: str) -> List[Dict]:
    reader = PdfReader(pdf_path)
    try:
        outlines = reader.outline
    except AttributeError:
        outlines = reader.outlines

    def recurse(items, level=1):
        result = []
        for item in items:
            if isinstance(item, list):
                result += recurse(item, level + 1)
            else:
                try:
                    page_num = reader.get_destination_page_number(item)
                except Exception:
                    page_num = item.page_number
                result.append({
                    "title": item.title,
                    "page": page_num,
                    "level": level
                })
        return result

    return recurse(outlines)

def extract_bookmarks(bookmarks, level: int):
    return [bm for bm in bookmarks if bm["level"] == level]
