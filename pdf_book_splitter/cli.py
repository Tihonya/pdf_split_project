#!/usr/bin/env python3
# Модуль CLI: інтерфейс командного рядка для утиліти розбиття та очищення PDF
import click

from .splitter import split_pdf
from .cleaner import clean_pdfs


@click.group()
def cli():
    """CLI-утиліта для розбиття та очищення PDF-книг."""
    pass


# Команда pdfsplit: розбиває PDF за рівнями закладок
@cli.command()
@click.argument("input_pdf", type=click.Path(exists=True, dir_okay=False))
@click.option(
    "--levels",
    "-l",
    multiple=True,
    type=int,
    help="Bookmark levels to split (e.g., --levels 1 2 3). Default: all levels.",
)
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(file_okay=False),
    default="output",
    show_default=True,
    help="Directory to save split PDFs.",
)
@click.option(
    "--duplicate-boundaries",
    type=click.Choice(["none", "start", "end", "both"], case_sensitive=False),
    default="both",
    show_default=True,
    help="Handle boundary pages: none|start|end|both.",
)
@click.option(
    "--log-file",
    type=click.Path(dir_okay=False),
    default=None,
    help="Optional log file path for split process.",
)
def pdfsplit(input_pdf, levels, output_dir, duplicate_boundaries, log_file):
    """
    Розбиває PDF-файл на частини за ієрархією закладок.
    """
    lvl_list = list(levels) if levels else None
    split_pdf(
        input_path=input_pdf,
        output_dir=output_dir,
        levels=lvl_list,
        duplicate=duplicate_boundaries,
        log_file=log_file,
    )


@cli.command()
@click.argument("pdf_paths", nargs=-1, type=click.Path(exists=True, dir_okay=False))
@click.option(
    "--threshold",
    "-t",
    type=float,
    default=16.0,
    show_default=True,
    help="Font size threshold to detect headings for cleaning.",
)
@click.option(
    "--log-file",
    type=click.Path(dir_okay=False),
    default=None,
    help="Optional log file path for clean process.",
)
# Команда pdfclean: очищує раніше розбиті PDF від повторних заголовків
def pdfclean(pdf_paths, threshold, log_file):
    """
    Очищує split PDF-файли, видаляючи повторні заголовки та колонтитули.
    """
    clean_pdfs(paths=list(pdf_paths), threshold=threshold, log_file=log_file)


if __name__ == "__main__":
    cli()