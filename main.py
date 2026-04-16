from datetime import datetime, timedelta
from models.transaction import Transaction

class LibraryService:
    def __init__(self, books, users):
        self.books = books
        self.users = users
        self.transactions = []

    def add_book(self, book, user):
        if user.role != "admin":
            raise Exception("Only admin can add book")
        self.books.append(book)

    def search(self, keyword):
        return [b for b in self.books if keyword.lower() in b.title.lower()]

    def borrow(self, user, book_id):
        for book in self.books:
            if book.id == book_id and book.available:
                if not user.can_borrow():
                    return "Limit reached"
                book.available = False
                user.borrowed_books.append({
                    "book_id": book.id,
                    "date": datetime.now().isoformat()
                })
                self.transactions.append(Transaction(user.id, book.id, "borrow"))
                return "Borrowed"
        return "Not available"

    def return_book(self, user, book_id):
        for record in user.borrowed_books:
            if record["book_id"] == book_id:
                user.borrowed_books.remove(record)

                for book in self.books:
                    if book.id == book_id:
                        book.available = True

                days = (datetime.now() - datetime.fromisoformat(record["date"])).days
                fine = max(0, days - 7) * 2000

                self.transactions.append(Transaction(user.id, book_id, "return"))
                return f"Returned. Fine: {fine}"

        return "Book not found"
