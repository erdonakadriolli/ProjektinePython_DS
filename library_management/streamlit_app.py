import streamlit as st
import requests

st.title("Library Management System")

menu = ["Add Book", "View Books"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Book":
    st.subheader("Add a New Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    isbn = st.text_input("ISBN")
    quantity = st.number_input("Quantity", min_value=1, step=1)
    if st.button("Add Book"):
        book = {"title": title, "author": author, "isbn": isbn, "quantity": quantity}
        response = requests.post("http://127.0.0.1:8000/add_book/", json=book)
        if response.status_code == 200:
            st.success("Book added successfully!")
        else:
            st.error(response.json()["detail"])

elif choice == "View Books":
    st.subheader("View All Books")
    response = requests.get("http://127.0.0.1:8000/view_books/")
    if response.status_code == 200:
        books = response.json()
        for book in books:
            st.write(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, ISBN: {book[3]}, Quantity: {book[4]}")
    else:
        st.error("Failed to fetch books.")