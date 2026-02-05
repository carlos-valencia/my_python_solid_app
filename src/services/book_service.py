from src.repositories import BookRepositoryProtocol
from src.domain import Book

class BookService:
    def __init__(self, repo: BookRepositoryProtocol):
        self.repo = repo

    def get_all_books(self) -> list[Book]:
        return self.repo.get_all_books()

    def add_book(self, book: Book) -> str:
        return self.repo.add_book(book)

    def find_book_by_name(self, query: str) -> list[Book]:
        if not isinstance(query, str):
            raise TypeError("Expected str, got something else")
        return self.repo.find_book_by_name(query)

    def remove_book(self, book: Book) -> bool:
        return self.repo.remove_book(book)

    def update_book(self, book: Book, updates: dict[str: int]) -> dict[str: list[str]]:

        result = {
            "updated": [],
            "invalid": []
        }

        for field, value in updates.items():
            # if value is an int, we need to validate
            if isinstance(value, int):
                # if value is int, we want it to be positive at least
                if(value < 0):
                    result["invalid"].append(field)
                    updates.pop(field)
                else:
                    result["updated"].append(field)
            # if not an int, it's a str, we take as is
            else:
                result["updated"].append(field)

        if self.repo.update_book(book, updates):
            return result
        else:
            return {}
