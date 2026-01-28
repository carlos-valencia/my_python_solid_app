from src.domain import Book
from src.repositories import BookRepository
from src.services import generate_books_json
from src.services import BookService
from src.services.book_analytics_service import BookAnalyticsService
import requests


class BookREPL:
    def __init__(self, book_svc, book_analytic_svc):
        self.running = True
        self.book_service = book_svc
        self.book_analytics_service = book_analytic_svc

    def start(self):
        print("Welcome to the Book app! Type 'help' for a list of commands.")
        while self.running:
            cmd = input(">>>").strip()
            self.handle_command(cmd)

    def handle_command(self, cmd):
        self.print_main_menu()
        if cmd == "0":
            self.running = False
            print("Goodbye")
        elif cmd == "1":
            self.get_all_records()
        elif cmd == "2":
            self.add_book()
        elif cmd == "3":
            self.remove_book()
        elif cmd == "4":
            self.update_book()
        elif cmd == "5":
            self.find_book_by_name()
        elif cmd == "6":
            self.analytics()
        elif cmd == "7":
            self.get_joke()
        else:
            print("Please use a valid command")

    def analytics(self):
        while True:
            self.print_analytics_menu()
            cmd = input(">>>").strip()
            if cmd == "0":
                print("Thanks for using analytics")
                break
            if cmd == "1":
                self.get_average_price()
            elif cmd == "2":
                self.get_top_books()
            elif cmd == "3":
                self.get_value_scores()
            elif cmd == "4":
                self.get_median_price_by_genre()
            else:
                print("Please select a valid analytics command")

    def get_median_price_by_genre(self):
        books = self.book_service.get_all_books()
        medians = self.book_analytics_service.get_medians_by_genre(books)
        print(medians)

    def print_main_menu(self):
        print("Available Commands\n"
              "[1] Get All Records"
              "[2] Add Book"
              "[3] Remove Book"
              "[4] Update Book"
              "[5] Find Book By Name"
              "[6] Analytics"
              "[0] EXIT")

    def print_analytics_menu(self):
        print("Available Analytics\n"
              "[1] Average Price\n"
              "[2] Top Books\n"
              "[3] Value Scores\n"
              "[4] Average Price by Genre\n"
              "[0] MAIN MENU")


    def update_book(self):
        pass

    def get_average_price(self):
        books = self.book_service.get_all_books()
        avg_price = self.book_analytics_service.average_price(books)
        print(f"Average Price: ${avg_price}")

    def get_top_books(self):
        books = self.book_service.get_all_books()
        top_rated_books = self.book_analytics_service.top_rated(books)
        print(top_rated_books)

    def get_value_scores(self):
        books = self.book_service.get_all_books()
        value_scores = self.book_analytics_service.value_scores(books)
        print(value_scores)

    def remove_book(self):
        query = input("Please enter book name: ")
        
        pass

    def get_joke(self):
        try:
            url = "https://api.chucknorris.io/jokes/random"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            print(response.json()["value"])
        except requests.exceptions.Timeout:
            print("Request timed out")
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Something else went wrong: {e}")

    def get_all_records(self):
        books = self.book_service.get_all_books()
        print(books)

    def add_book(self):
        try:
            print("Enter book details")
            title = input("Title: ")
            author = input("Author: ")
            book = Book(title = title, author = author)
            new_book_id = self.book_service.add_book(book)
            print(new_book_id)
        except Exception as e:
            print(f"An unexpected error has occurred: {e}")

    def find_book_by_name(self):
        query = input("Please enter book name: ")
        books = self.book_service.find_book_by_name(query)
        print(books)

if __name__ == "__main__":
    generate_books_json()
    repo = BookRepository("books.json")
    book_service = BookService(repo)
    book_analytics_service = BookAnalyticsService()
    repl = BookREPL(book_service, book_analytics_service)
    repl.start()
    