from dataclasses import dataclass

# Моделі даних для закладок та секцій PDF

@dataclass
# Представлення закладки з рівнем, назвою та номером сторінки
class Bookmark:
    level: int
    title: str
    page: int

@dataclass
# Представлення секції з назвою, рівнем та діапазоном сторінок
class Section:
    title: str
    level: int
    start_page: int
    end_page: int