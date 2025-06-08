# PDF Book Splitter & Cleaner

Утиліта для розбиття PDF-книг за рівнями закладок та очищення частин від повторних заголовків.

## Встановлення

```bash
pip install -r requirements.txt
```

## Використання

```bash
# Розбиття за всіма рівнями закладок (дублювання кордонів за замовчуванням)
pdfsplit 30__L1_LLM_Engineers_Handbook_Master_the_art_of_engineering_large_language.pdf

# Розбиття тільки топ-рівня закладок
pdfsplit 30__L1_LLM_Engineers_Handbook_Master_the_art_of_engineering_large_language.pdf --levels 1

# Очищення раніше розбитих PDF
pdfclean output/*.pdf
```

## Додаткові інструкції

### Активація віртуального оточення та встановлення залежностей

```bash
# Перевірте, що перебуваєте в корені проекту та активуйте venv
source venv/bin/activate

# Оновіть pip та встановіть залежності
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### Запуск розбиття PDF

```bash
# Розбиття за рівнями закладок
python -m pdf_book_splitter.cli pdfsplit \
    <шлях_до_PDF> \
    --levels 1 2 \
    --duplicate-boundaries both \
    --output-dir output_dir \
    --log-file split.log
```

### Очищення розбитих PDF

```bash
# Видалення повторних заголовків та колонтитулів
python -m pdf_book_splitter.cli pdfclean \
    output_dir/*.pdf \
    --threshold 16.0 \
    --log-file clean.log
```

### Юніт-тести

```bash
pytest -q
```

## Структура проекту

- **pdf_book_splitter/** — пакет з основними модулями:
- `splitter.py` — логіка розбиття PDF за закладками.
- `cleaner.py` — логіка очищення PDF від повторних заголовків.
- `cli.py` — інтерфейс командного рядка.
- `utils.py`, `models.py` — допоміжні модулі та моделі даних.
- **tests/** — юніт-тести для `pdf_book_splitter`.
- **requirements.txt** — перелік залежностей.
- **Pdf_Book_Splitter_Tech_Spec.MD** — технічне завдання.