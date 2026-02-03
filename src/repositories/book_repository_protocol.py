from typing import Protocol
from src.domain import Book

class BookRepositoryProtocol(Protocol):
    def get_all_books(self) -> list[Book]:
        ...

    def add_book(self, book: Book) -> str:
        ...

    def find_book_by_name(self, query: str) -> list[Book]:
        ...

    def remove_book(self, book: Book) -> bool:
        ...

    def check_out_book(self, book_id: str) -> Book:
        ...

    def check_in_book(self, book_id: str) -> Book:
        ...