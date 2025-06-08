import logging

from rich.logging import RichHandler

# Утилітні функції: налаштування логування та обробка імен файлів


def setup_logging(log_file: str = None, level: str = "INFO") -> None:
    # Налаштовує логування з Rich та файловим хендлером
    handlers = [RichHandler()]
    if log_file:
        file_handler = logging.FileHandler(log_file)
        handlers.append(file_handler)
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s: %(message)s",
        handlers=handlers,
    )


def sanitize_filename(name: str) -> str:
    # Очищає назву для безпечного використання в іменах файлів
    return "".join(c for c in name if c.isalnum() or c in " _-").strip()