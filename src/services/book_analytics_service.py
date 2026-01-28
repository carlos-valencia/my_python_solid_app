import numpy as np
from src.domain.book import Book

# Ground rules for numpy
# 1. Keep numpy in service layer ONLY
#   - if you see numpy imports anywhere else, this is a design smell!
# 2. Notice how methods take in books, and return normal data types, NOT ndarrays
#   - this service and numpy are ISOLATED, this will keep our functions and tests clean

class BookAnalyticsService:

    def average_price(self, books: list[Book]) -> float:
        prices = np.array([b.price_usd for b in books], dtype="float")
        return float(prices.mean())

    # changed min_ratings default to 500 because max generated value is 1000
    def top_rated(self, books: list[Book], min_ratings: int = 500, limit: int = 10) -> list[Book]:
        ratings = np.array([b.average_rating for b in books])
        counts = np.array([b.ratings_count for b in books])

        # what we have now:
        # books -> book objects
        # ratings -> numbers
        # counts -> numbers
        # filtered books contains all books that have at least 1000 ratings
        mask = counts >= min_ratings
        filtered_books = np.array(books)[mask]

        # now scores is only the ratings for the filtered scores (over 1000 ratings)
        scores = ratings[mask]
        sorted_idx = np.argsort(scores)[::-1]
        return filtered_books[sorted_idx].tolist()[:limit]

    # value score = rating * log(ratings_count) / price
    def value_scores(self, books: list[Book]) -> dict[str, float]:
        ratings = np.array([b.average_rating for b in books])
        counts = np.array([b.ratings_count for b in books])
        prices = np.array([b.price_usd for b in books], dtype="float")

        scores = (ratings * np.log1p(counts)) / prices

        return {
            # zip iterates over both lists in parallel, so indexes are synced
            # zip will stop automatically if one list is shorted
            # if same key appears more than once, later entries override earlier ones
            book.book_id: float(score) 
            for book, score in zip (books, scores)
        }

    def get_medians_by_genre(self, books: list[Book]) -> dict[str, float]:

        genres = set(book.genre for book in books)
        medians_by_genre: dict[str, float] = {}

        for genre in genres:
            prices = np.array([b.price_usd for b in books if b.genre == genre], dtype="float")
            mean = float(prices.mean())
            medians_by_genre[genre] = mean

        return medians_by_genre

    def most_popular_genre(self, books: list[Book]) -> str:
        checkouts_by_genre: dict[str, int] = {}
        checkouts = np.array([b.last_checkout for b in books])

        mask = np.char.startswith(checkouts, "2026")
        filtered_books = np.array(books)[mask]

        for book in filtered_books:
            if book.genre in checkouts_by_genre:
                checkouts_by_genre[book.genre] += 1
            else:
                checkouts_by_genre[book.genre] = 1

        return max(checkouts_by_genre.keys(), key = lambda genre: checkouts_by_genre[genre])
