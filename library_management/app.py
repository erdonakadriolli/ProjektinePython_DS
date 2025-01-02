from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

class Book(BaseModel):
    title: str
    author: str
    isbn: str
    quantity: int

@app.post("/add_book/")
def add_book(book: Book):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Books WHERE isbn = ?', (book.isbn,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="ISBN ekziston tashmë!")
    cursor.execute('''
    INSERT INTO Books (title, author, isbn, quantity)
    VALUES (?, ?, ?, ?)
    ''', (book.title, book.author, book.isbn, book.quantity))
    conn.commit()
    conn.close()
    return {"message": "Libri u shtua me sukses!"}

@app.get("/view_books/")
def view_books():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Books')
    books = cursor.fetchall()
    conn.close()
    return bookspp