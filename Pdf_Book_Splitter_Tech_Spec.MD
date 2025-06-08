# Technical Specification (ТЗ): PDF Book Splitter & Cleaner

---
## 1. Purpose
Create a Python-based utility that automatically splits a PDF book into smaller PDFs using the document’s bookmark hierarchy (levels 1-n). The splitter must handle edge-cases where two logical sections share a single page by duplicating that boundary page into both output files. A second processing stage must trim duplicated header/tail text inside each generated part.

---
## 2. Scope & Goals
1. **Phase A – Splitter**
   * Detect bookmark (outline) entries and their levels.
   * Generate independent PDF files for every bookmark level chosen by the user (default = all levels).
   * If *end-of-section* and *start-of-section* reside on the same physical page, include that page in *both* new PDFs.
2. **Phase B – Cleaner**
   * Analyse the first & last pages of each generated PDF.
   * Remove extraneous content preceding the start heading or following the end heading.
   * Output cleaned PDFs with identical filenames plus suffix `_clean`.

---
## 3. Functional Requirements
| ID | Requirement | Priority |
|----|-------------|----------|
| F-01 | CLI command `pdfsplit <input.pdf> [--levels 1 2 3]` | MUST |
| F-02 | Detect bookmark hierarchy via `PyMuPDF` (`doc.get_toc()`) | MUST |
| F-03 | Build ordered list of (page index, level, title) | MUST |
| F-04 | For every consecutive pair of bookmarks, copy page-range `[start, end-1]` inclusive; if `start_page == end_page`, copy that page to *both* outputs | MUST |
| F-05 | Preserve original PDF metadata in each child | SHOULD |
| F-06 | Optional flag `--level N` to restrict split depth | SHOULD |
| F-07 | Optional flag `--duplicate-boundaries none|start|end|both` (default `both`) | COULD |
| F-08 | Produce log file with processed sections | SHOULD |
| F-09 | Phase B CLI: `pdfclean <folder/*pdf>` | MUST |
| F-10 | Identify heading rectangles on first page via text span size > configurable threshold (default 16 pt) | SHOULD |
| F-11 | Remove text before start rectangle and after last heading on last page | SHOULD |

---
## 4. Non-Functional Requirements
* Compatible with Python 3.9+
* Runs inside isolated **venv** with minimal dependencies: `PyMuPDF`, `click`, `rich` (logging), `pytest`.
* Process 500-page book in < 30 s on mid-range CPU.
* Memory footprint < 300 MB.
* Codebase fully type-hinted, PEP-8 compliant, ≥ 90 % unit-test coverage.

---
## 5. Architecture
```
├─ pdf_book_splitter/
│  ├─ cli.py          # entry-points using Click
│  ├─ splitter.py     # Phase A logic
│  ├─ cleaner.py      # Phase B logic
│  ├─ utils.py        # shared helpers
│  ├─ models.py       # dataclasses for Bookmark, Section
│  └─ tests/
│     ├─ test_splitter.py
│     └─ test_cleaner.py
└─ README.md          # usage & contribution guide
```

---
## 6. Detailed Algorithms
### 6.1 Splitter
1. **Load PDF** with `fitz.open()`.
2. **Extract TOC** → list of tuples `(level, title, page_idx)`.
3. **Filter levels** per CLI arg.
4. **Iterate** - for `i in range(len(nodes))`:
   * `start = nodes[i].page_idx`
   * `end   = nodes[i+1].page_idx` if exists else `doc.page_count`
   * If `start == end`: set `range_pages = [start]` else `[start, end-1]`.
   * **Insert** pages into new doc via `insert_pdf()`.
5. **Save** as `<index>_<sanitised_title>.pdf`.

### 6.2 Cleaner
1. For each PDF part:
   * Scan **first page** spans; locate first heading span (`size >= threshold`). Crop rectangle above.
   * Scan **last page** spans; locate last heading span; crop rectangle below.
2. Re-write modified pages with `page.delete_textbox(rect)`.
3. Save to `_clean.pdf`.

---
## 7. CLI Examples
```bash
# Split all levels, duplicate boundary pages
pdfsplit book.pdf

# Only top-level chapters
pdfsplit book.pdf --levels 1

# Clean previously split files
pdfclean output/chapters/*.pdf
```

---
## 8. Tests
* Unit tests with sample 10-page fixture containing nested bookmarks.
* Golden-master PDFs in `tests/data/expected/`.
* `pytest -q` integrated into CI.

---
## 9. Future Extensions (Out-of-Scope but Tracked)
* GUI wrapper (Qt) for drag-and-drop splitting.
* OCR fallback for scanned PDFs via Tesseract.
* Parallel processing of large books.

---
## 10. Acceptance Criteria
1. Running `pdfsplit` on given reference book outputs 24 PDFs exactly matching expected page ranges (verified by checksum).
2. Boundaries duplicated where shared.
3. Running `pdfclean` removes duplicated header/tail lines (visual diff).
4. All unit tests pass; linter shows zero critical warnings.

---
## 11. Glossary
* **Bookmark/Outline** – hierarchical navigation structure embedded in PDF.
* **Heading span** – text span rendered with font size above threshold, assumed to be section title.

---
*(c) 2025 — Project PDF Book Splitter*
