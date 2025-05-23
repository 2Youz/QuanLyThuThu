import json
import os
from QuanLy import Book

BOOKS_FILE = "books.json"

def load_books():
    """Load danh sách sách từ file JSON"""
    if not os.path.exists(BOOKS_FILE) or os.path.getsize(BOOKS_FILE) == 0:
        return []
    with open(BOOKS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        books = []
        for book_data in data:
            book = Book(
                book_data["BookID"],
                book_data["BookName"], 
                book_data["Author"],
                book_data["Category"],
                book_data["Quantity"]
            )
            books.append(book)
        return books

def save_books(books):
    """Lưu danh sách sách vào file JSON"""
    with open(BOOKS_FILE, "w", encoding="utf-8") as f:
        json.dump([book.to_dict() for book in books], f, indent=4, ensure_ascii=False)

def get_all_books():
    """Lấy tất cả sách"""
    return load_books()

def add_book(book):
    """Thêm sách mới"""
    books = load_books()
    for b in books:
        if b.BookID == book.BookID:
            raise ValueError("Mã sách đã tồn tại")
    books.append(book)
    save_books(books)

def update_book(book_id, new_data):
    """Cập nhật thông tin sách"""
    books = load_books()
    found = False
    for book in books:
        if book.BookID == book_id:
            book.BookName = new_data.get("BookName", book.BookName)
            book.Author = new_data.get("Author", book.Author)
            book.Category = new_data.get("Category", book.Category)
            book.Quantity = new_data.get("Quantity", book.Quantity)
            found = True
            break
    if not found:
        raise ValueError("Không tìm thấy sách")
    save_books(books)

def delete_book(book_id):
    """Xóa sách theo mã sách"""
    books = load_books()
    new_books = [book for book in books if book.BookID != book_id]
    if len(new_books) == len(books):
        raise ValueError("Không tìm thấy sách để xóa")
    save_books(new_books)