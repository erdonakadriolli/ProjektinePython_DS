from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Books (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        isbn TEXT UNIQUE NOT NULL,
        quantity INTEGER NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        quantity = request.form['quantity']
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Books WHERE isbn = ?', (isbn,))
        if cursor.fetchone():
            return "Gabim: ISBN ekziston tashmë!"
        else:
            cursor.execute('''
            INSERT INTO Books (title, author, isbn, quantity)
            VALUES (?, ?, ?, ?)
            ''', (title, author, isbn, quantity))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('add_book.html')

@app.route('/view')
def view_books():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Books')
    books = cursor.fetchall()
    conn.close()
    return render_template('view_books.html', books=books)

if __name__ == '__main__':
    app.run(debug=True)