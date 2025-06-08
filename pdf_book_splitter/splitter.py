# Модуль логіки розбиття PDF за рівнями закладок
import os
import logging

import fitz

from .models import Bookmark, Section
from .utils import sanitize_filename


LOGGER = logging.getLogger(__name__)


def load_bookmarks(doc: fitz.Document) -> list[Bookmark]:
    # Завантажує ієрархію закладок (TOC) з документа як список об’єктів Bookmark
    toc = doc.get_toc()
    return [Bookmark(level=lv, title=title, page=pg - 1) for lv, title, pg in toc]


def build_sections(
    bookmarks: list[Bookmark],
    page_count: int,
    levels: list[int] | None = None,
    duplicate: str = "both",
) -> list[Section]:
    # Формує секції на основі закладок, враховуючи рівні та налаштування дублювання сторінок
    if levels:
        # Фільтруємо закладки за вказаними рівнями, якщо задано
        bookmarks = [bm for bm in bookmarks if bm.level in levels]

    sections: list[Section] = []
    for idx, bm in enumerate(bookmarks):
        start = bm.page
        next_page = bookmarks[idx + 1].page if idx + 1 < len(bookmarks) else None

        # Визначаємо кінцеву сторінку секції з урахуванням дублювання меж
        if next_page is None:
            end = page_count - 1
        elif start == next_page:
            # Дублювання сторінки на початку та/або в кінці розділу
            if duplicate in ("both", "start"):
                end = start
            else:
                end = start - 1
        else:
            end = next_page - 1

        if end < start:
            # Пропускаємо розділи без сторінок
            continue

        sections.append(
            Section(title=bm.title, level=bm.level, start_page=start, end_page=end)
        )

    return sections


def split_pdf(
    input_path: str,
    output_dir: str = "output",
    levels: list[int] | None = None,
    duplicate: str = "both",
    log_file: str | None = None,
) -> None:
    # Основна функція для розбиття PDF за секціями та збереження результату
    from .utils import setup_logging

    os.makedirs(output_dir, exist_ok=True)
    if log_file is None:
        log_file = os.path.join(output_dir, "pdfsplit.log")
    setup_logging(log_file)

    doc = fitz.open(input_path)
    bookmarks = load_bookmarks(doc)
    sections = build_sections(bookmarks, doc.page_count, levels, duplicate)
    metadata = doc.metadata

    for idx, sec in enumerate(sections, 1):
        new_doc = fitz.open()
        new_doc.set_metadata(metadata)
        for page_num in range(sec.start_page, sec.end_page + 1):
            new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)

        safe_title = sanitize_filename(sec.title) or f"section_{idx}"
        filename = f"{idx:02d}_{safe_title}.pdf"
        out_path = os.path.join(output_dir, filename)
        new_doc.save(out_path)
        LOGGER.info(
            f"Saved section {idx}: '{sec.title}' pages "
            f"{sec.start_page + 1}-{sec.end_page + 1} to {filename}"
        )
        new_doc.close()

    doc.close()
    LOGGER.info(
        f"Completed splitting into {len(sections)} sections. Output directory: '{output_dir}'"
    )