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
        print("Welcome to the Book app!")
        while self.running:
            self.print_main_menu()
            cmd = input(">>>").strip()
            self.handle_command(cmd)

    def handle_command(self, cmd):
        if cmd == "0":
            self.running = False
            print("Goodbye")
        elif cmd == "1":
            self.get_all_records()
        elif cmd == "2":
            self.update_book()
        elif cmd == "3":
            self.add_book()
        elif cmd == "4":
            self.remove_book()
        elif cmd == "5":
            self.update_book()
        elif cmd == "6":
            self.find_book_by_name()
        elif cmd == "7":
            self.analytics()
        elif cmd == "8":
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
            elif cmd == "5":
                self.most_popular_genre()
            else:
                print("Please select a valid analytics command")

    def get_median_price_by_genre(self):
        books = self.book_service.get_all_books()
        medians = self.book_analytics_service.get_medians_by_genre(books)
        print(medians)

    def print_main_menu(self):
        print(
            "Available Commands\n"
            "[1] Print All Records\n"
            "[2] Check out/Check in Book\n"
            "[3] Add Book\n"
            "[4] Remove Book\n"
            "[5] Update Book\n"
            "[6] Find Book By Name\n"
            "[7] Analytics\n"
            "[8] Get Joke\n"
            "[0] EXIT\n"
        )

    def print_analytics_menu(self):
        print(
            "Available Analytics\n"
            "[1] Average Price\n"
            "[2] Top Books\n"
            "[3] Value Scores\n"
            "[4] Average Price by Genre\n"
            "[5] Most Popular Genre of the Year\n"
            "[0] MAIN MENU\n"
        )

    def most_popular_genre(self):
        books = self.book_service.get_all_books()
        print(self.book_analytics_service.most_popular_genre(books))

    def update_book(self):
        query = input("Please enter book name: ")
        book_choice = self.get_book_choice(query)
        
        updates = {}

        new_title = input("Enter new book title: ")
        new_author = input("Enter new author: ")
        new_pub_year = self.get_int("Enter new publication year: ")
        new_page_count = self.get_int("Enter new page count: ")

        if new_title:
            updates["title"] = new_title

        if new_author:
            updates["author"] = new_author

        if new_pub_year:
            updates["publication_year"] = new_pub_year

        if new_page_count:
            updates["page_count"] = new_page_count

        update_result = self.book_service.update_book(book_choice, updates)

        for status, field_list in update_result.items():
            print(f"{status}: {field}" for field in field_list)

    def get_int(self, query: str) -> int:
        while True:
            try:
                int_input = int(input(query))
                return int_input
            except TypeError as e:
                print(e)


    def get_book_choice(self, query: str) -> Book:
        books = self.book_service.find_book_by_name(query)

        # list is empty - no such books of that title
        if not books:
            print(f"No books found with the title {query}")
            return None

        # more than one found, give user chance to choose one (by index)
        if len(books) > 1:
            print("Multiple entries found with that name, select one")
            print(*(f"[{i}] {book.title} - {book.author}"
                    for i, book in enumerate(books, start=1)), sep="\n")
            choice = self.get_choice_int(len(books), True)
            return books[choice]

        # only one in list, returns index 0
        return books[0]

    def remove_book(self):
        query = input("Please enter book name: ")
        book_choice = self.get_book_choice(query)

        if book_choice:
            print(f"{book_choice.title} has been removed"
                  if self.book_service.remove_book(book_choice)
                  else "An unexpected error has occurred")

    def get_choice_int(self, length: int, adjust: bool) -> int:
        while True:
            try:
                choice = int(input("Enter selection: "))
                if choice - 1 < 0 or choice - 1 >= length:
                    raise IndexError("Index out of bounds.")
                
                # adjust == True: we adjust the value for list index
                # adjust == False: we return as is
                return choice - 1 if adjust else choice
            except TypeError:
                print("Something went wrong, please try again.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
            except IndexError as ie:
                print(f"{ie} Please enter a choice in the range of 1 and {length}")

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
            book = Book(title=title, author=author)
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
