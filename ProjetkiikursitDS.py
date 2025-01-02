import sqlite3
from tkinter import *
from tkinter import messagebox

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

def add_book(title, author, isbn, quantity):
    try:
        cursor.execute('SELECT * FROM Books WHERE isbn = ?', (isbn,))
        if cursor.fetchone():
            messagebox.showerror("Gabim", "ISBN ekziston tashmë!")
        else:
            cursor.execute('''
            INSERT INTO Books (title, author, isbn, quantity)
            VALUES (?, ?, ?, ?)
            ''', (title, author, isbn, quantity))
            conn.commit()
            messagebox.showinfo("Sukses", "Libri u shtua me sukses!")
            cursor.execute('SELECT * FROM Books WHERE isbn = ?', (isbn,))
            book = cursor.fetchone()
            print("Libri i shtuar:", book)
    except sqlite3.IntegrityError:
        messagebox.showerror("Gabim", "ISBN ekziston tashmë!")


def main():
    root = Tk()
    root.title("Sistemi i Menaxhimit të Bibliotekës")

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