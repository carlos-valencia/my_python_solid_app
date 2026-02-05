import json
from src.domain import Book
from src.repositories.book_repository_protocol import BookRepositoryProtocol


class BookRepository(BookRepositoryProtocol):
    def __init__(self, filepath: str = "book.json"):
        self.filepath = filepath

    def get_all_books(self) -> list[Book]:
        with open(self.filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Book.from_dict(item) for item in data]

    def add_book(self, book: Book) -> str:
        books = self.get_all_books()
        books.append(book)

        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump([item.to_dict() for item in books], f, indent=2)
        return book.book_id

    def find_book_by_name(self, query):
        books = self.get_all_books()
        return [b for b in books if b.title == query]

    def remove_book(self, book: Book) -> bool:
        books = self.get_all_books()
        books.remove(book)

        if book in books:
            return False

        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump([item.to_dict() for item in books], f, indent=2)

        return True

    def update_book(self, book: Book, updates: dict[str: int]) -> bool:

        try:
            books = self.get_all_books()
            for field, value in updates.items():
                setattr(book, field, value)

            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump([item.to_dict() for item in books], f, indent=2)
                
            return True
        except Exception:
            return False
