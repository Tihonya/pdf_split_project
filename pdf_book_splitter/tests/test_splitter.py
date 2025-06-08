import os
import fitz

from pdf_book_splitter.splitter import load_bookmarks, build_sections


def test_build_sections_level2():
    # Юніт-тест перевіряє, що при рівні 2 утворюється очікувана кількість секцій із тестового PDF
    pdf_path = os.path.join(
        os.path.dirname(__file__), '..', '..',
        '30__L1_LLM_Engineers_Handbook_Master_the_art_of_engineering_large_language.pdf'
    )
    pdf_path = os.path.abspath(pdf_path)
    doc = fitz.open(pdf_path)
    bookmarks = load_bookmarks(doc)
    sections = build_sections(bookmarks, doc.page_count, levels=[2], duplicate='both')
    # В тестовому PDF має бути 6 розділів рівня 2
    assert len(sections) == 6
    doc.close()