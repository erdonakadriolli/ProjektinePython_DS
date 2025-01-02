import sqlite3
from tkinter import *

# Krijimi i bazës së të dhënave
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Krijimi i tabelave
cursor.execute('''
CREATE TABLE IF NOT EXISTS Books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    isbn TEXT UNIQUE NOT NULL,
    quantity INTEGER NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Borrowing (
    borrow_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    book_id INTEGER,
    borrow_date TEXT,
    return_date TEXT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (book_id) REFERENCES Books(book_id)
)
''')

# Funksionet për menaxhimin e librave
def add_book(title, author, isbn, quantity):
    cursor.execute('''
    INSERT INTO Books (title, author, isbn, quantity)
    VALUES (?, ?, ?, ?)
    ''', (title, author, isbn, quantity))
    conn.commit()
    print("Libri u shtua me sukses!")

def update_book(book_id, title, author, isbn, quantity):
    cursor.execute('''
    UPDATE Books
    SET title = ?, author = ?, isbn = ?, quantity = ?
    WHERE book_id = ?
    ''', (title, author, isbn, quantity, book_id))
    conn.commit()
    print("Libri u përditësua me sukses!")

def delete_book(book_id):
    cursor.execute('''
    DELETE FROM Books WHERE book_id = ?
    ''', (book_id,))
    conn.commit()
    print("Libri u fshi me sukses!")

# Funksionet për menaxhimin e përdoruesve
def add_user(first_name, last_name, email):
    cursor.execute('''
    INSERT INTO Users (first_name, last_name, email)
    VALUES (?, ?, ?)
    ''', (first_name, last_name, email))
    conn.commit()
    print("Përdoruesi u shtua me sukses!")

def update_user(user_id, first_name, last_name, email):
    cursor.execute('''
    UPDATE Users
    SET first_name = ?, last_name = ?, email = ?
    WHERE user_id = ?
    ''', (first_name, last_name, email, user_id))
    conn.commit()
    print("Përdoruesi u përditësua me sukses!")

def delete_user(user_id):
    cursor.execute('''
    DELETE FROM Users WHERE user_id = ?
    ''', (user_id,))
    conn.commit()
    print("Përdoruesi u fshi me sukses!")

# Funksionet për menaxhimin e huazimeve
def borrow_book(user_id, book_id, borrow_date, return_date):
    cursor.execute('''
    INSERT INTO Borrowing (user_id, book_id, borrow_date, return_date)
    VALUES (?, ?, ?, ?)
    ''', (user_id, book_id, borrow_date, return_date))
    conn.commit()
    print("Libri u huazua me sukses!")

def return_book(borrow_id):
    cursor.execute('''
    DELETE FROM Borrowing WHERE borrow_id = ?
    ''', (borrow_id,))
    conn.commit()
    print("Libri u kthye me sukses!")

# Ndërfaqja me Tkinter
def main():
    root = Tk()
    root.title("Sistemi i Menaxhimit të Bibliotekës")

    # Shtimi i librit
    Label(root, text="Titulli").grid(row=0)
    Label(root, text="Autori").grid(row=1)
    Label(root, text="ISBN").grid(row=2)
    Label(root, text="Sasia").grid(row=3)

    title = Entry(root)
    author = Entry(root)
    isbn = Entry(root)
    quantity = Entry(root)

    title.grid(row=0, column=1)
    author.grid(row=1, column=1)
    isbn.grid(row=2, column=1)
    quantity.grid(row=3, column=1)

    Button(root, text='Shto Librin', command=lambda: add_book(title.get(), author.get(), isbn.get(), int(quantity.get()))).grid(row=4, column=1, sticky=W, pady=4)

    root.mainloop()

if __name__ == "__main__":
    main()

conn.close()