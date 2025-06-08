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