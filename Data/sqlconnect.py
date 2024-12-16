import sqlite3
from tkinter import messagebox
from datetime import datetime


def connect_db():
    return sqlite3.connect("Data/bookstore.db")

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS "Book" (
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "Title" TEXT,
        "Author" TEXT,
        "date" DATE,
        "Price" REAL,
        "quantity" INTEGER,
        "Main_Genre" TEXT,
        "sold" INTEGER DEFAULT 0,
        "efficiency" REAL DEFAULT 0,
        "Rating" REAL DEFAULT 0,  -- Add rating column with default value 0
        "No_of_People_rated" INTEGER DEFAULT 0 -- Add num_people_rated column with default value 0
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS "Sell" (
        "book_id" INTEGER,
        "quantity" INTEGER,
        "date" DATE,
        FOREIGN KEY("book_id") REFERENCES "Book"("id")
    );
    """)
    conn.commit()
    conn.close()


# Functionality for adding a book
def add_book(title, author, price, purchase_date, quantity, book_type, rating=0, num_people_rated=0):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Book (Title, Author, date, Price, quantity, Main_Genre, Rating, No_of_People_rated)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (title, author, purchase_date, price, quantity, book_type, rating, num_people_rated))
    conn.commit()
    conn.close()
    # messagebox.showinfo("Success", "Book added successfully!")


# Functionality for selling a book
def sell_book(book_id, quantity, user_rating=None):
    date = datetime.today().date()
    conn = connect_db()
    cursor = conn.cursor()
    current_quantity = get_book_quantity(book_id)

    # Fetch current rating and the number of people who rated the book
    cursor.execute("SELECT Rating, No_of_People_rated FROM Book WHERE id = ?", (book_id,))
    result = cursor.fetchone()
    if result:
        current_rating, num_people_rated = result
    else:
        messagebox.showinfo("Error", "Book not found.")
        conn.close()
        return

    # Check if there is enough stock to sell
    if current_quantity is not None and current_quantity >= quantity:
        new_quantity = current_quantity - quantity

        # Insert the sale record
        cursor.execute("INSERT INTO Sell (book_id, quantity, date) VALUES (?, ?, ?)", (book_id, quantity, date))

        # Update the book quantity and sold count
        cursor.execute(
            "UPDATE Book SET quantity = ?, sold = sold + ? WHERE id = ?",
            (new_quantity, quantity, book_id),
        )

        # Update rating if the user provides one
        if user_rating is not None:
            new_num_people_rated = num_people_rated + 1
            new_rating = ((current_rating * num_people_rated) + user_rating) / new_num_people_rated
            cursor.execute(
                "UPDATE Book SET Rating = ?, No_of_People_rated = ? WHERE id = ?",
                (new_rating, new_num_people_rated, book_id),
            )

        conn.commit()
        conn.close()
        # messagebox.showinfo("Success", "Book sale recorded successfully!")
    else:
        conn.close()
        messagebox.showinfo("Input Error", "Not enough stock available.")

def get_book_quantity(book_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT quantity FROM Book WHERE id = ?", (book_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


# Function to fetch and display book data in a table
def fetch_books():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, Title, Author, quantity, date, Price, Main_Genre, sold, efficiency, Rating, No_of_People_rated
    FROM Book
    """)
    books = cursor.fetchall()
    conn.close()
    return books

def get_book_title(book_id):
    conn = connect_db()
    cursor = conn.cursor()
    book_id = int(book_id)
    cursor.execute("SELECT Title FROM Book WHERE id = ?", (book_id,))
    result = cursor.fetchone()
    return result[0] if result else None
