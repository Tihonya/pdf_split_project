import os
import logging

import fitz

LOGGER = logging.getLogger(__name__)

# Модуль очищення PDF частин від повторних заголовків та колонтитулів


def clean_pdfs(
    paths: list[str],
    threshold: float = 16.0,
    log_file: str | None = None,
) -> None:
    # Очищує PDF-файли, видаляючи текст до/після заголовків на початку та в кінці документа
    from .utils import setup_logging

    if log_file:
        setup_logging(log_file)

    for path in paths:
        doc = fitz.open(path)
        if doc.page_count == 0:
            LOGGER.warning(f"No pages to clean in '{path}'")
            doc.close()
            continue

        page0 = doc.load_page(0)
        blocks = page0.get_text("dict").get("blocks", [])
        first_y = None
        for block in blocks:
            if block.get("type") != 0:
                continue
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    if span.get("size", 0) >= threshold:
                        y0 = span["bbox"][1]
                        if first_y is None or y0 < first_y:
                            first_y = y0
        if first_y:
            rect = fitz.Rect(0, 0, page0.rect.width, first_y)
            page0.add_redact_annot(rect, fill=(1, 1, 1))
            page0.apply_redactions()

        page_last = doc.load_page(doc.page_count - 1)
        blocks = page_last.get_text("dict").get("blocks", [])
        last_y = None
        max_y1 = -1
        for block in blocks:
            if block.get("type") != 0:
                continue
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    if span.get("size", 0) >= threshold:
                        y1 = span["bbox"][3]
                        if y1 > max_y1:
                            max_y1 = y1
                            last_y = y1
        if last_y:
            rect = fitz.Rect(0, last_y, page_last.rect.width, page_last.rect.height)
            page_last.add_redact_annot(rect, fill=(1, 1, 1))
            page_last.apply_redactions()

        base, ext = os.path.splitext(path)
        clean_path = f"{base}_clean{ext}"
        doc.save(clean_path)
        LOGGER.info(f"Cleaned '{path}' -> '{clean_path}'")
        doc.close()