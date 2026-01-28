from dataclasses import dataclass, field
from typing import Optional
import uuid

import textwrap



@dataclass
class Book:
    title: str
    author: str
    genre: Optional[str] = None
    publication_year: Optional[int] = None
    page_count: Optional[int] = None
    average_rating: Optional[float] = None
    ratings_count: Optional[int] = None
    price_usd: Optional[float] = None
    publisher: Optional[str] = None
    language: Optional[str] = None
    format: Optional[str] = None
    in_print: Optional[bool] = None
    sales_millions: Optional[float] = None
    last_checkout: Optional[str] = None
    available: Optional[bool] = None
    book_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def check_out(self):
        if not self.available:
            raise Exception("Book is already checked out")        
        self.available = False

    def check_in(self):
        if self.available:
            raise Exception("Book is already available")
        self.available = True

    @classmethod
    def from_dict(cls, data: dict) -> "Book":
        return cls(**data) # kwargs - key with arguments
    
    def to_dict(self) -> dict:
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "publication_year": self.publication_year,
            "page_count": self.page_count,
            "average_rating": self.average_rating,
            "ratings_count": self.ratings_count,
            "price_usd": self.price_usd,
            "publisher": self.publisher,
            "language": self.language,
            "format": self.format,
            "in_print": self.in_print,
            "sales_millions": self.sales_millions,
            "last_checkout": self.last_checkout,
            "available": self.available
        }
    
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):

        status = (
            "Not Available"
            if not self.available
            else "Available in print" if self.in_print
            else "Available"
        )

        return textwrap.dedent(f"""
                ****** {self.title} by {self.author} ******
                Genre: {self.genre}
                Published: {self.publication_year} by {self.publisher}
                Number of pages: {self.page_count}
                Format: {self.format}
                Language: {self.language}
                Rating: {self.average_rating} out of 5.0 - {self.ratings_count} reviews
                Sales: {self.sales_millions}M copies
                Availability: {status}
                Last Checked out: {self.last_checkout}
                Price: ${self.price_usd}
                ~~~~~ Book ID: {self.book_id} ~~~~~
                """)