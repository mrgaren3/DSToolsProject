import sqlite3
from tkinter import messagebox
from datetime import datetime
import matplotlib.pyplot as plt


def connect_db():
    return sqlite3.connect("bookstore2.db")

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS "Book" (
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "name" TEXT,
        "author" TEXT,
        "date" DATE,
        "price" REAL,
        "quantity" INTEGER,
        "type" TEXT,
        "sold" INTEGER DEFAULT 0 ,
        "efficiency" REAL DEFAULT 0
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
def add_book(title, author, price, purchase_date, quantity,Booktype):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Book (name, author, date, price, quantity, type) VALUES (?, ?, ?, ?, ?, ?)",
                   (title, author, purchase_date, price, quantity,Booktype))
    conn.commit()
    conn.close()
    # messagebox.showinfo("Success", "Book added successfully!")


# Functionality for selling a book
def sell_book(book_id, quantity):
    date = datetime.today().date()
    conn = connect_db()
    cursor = conn.cursor()
    current_quantity = get_book_quantity(book_id)

    # Check if there is enough stock to sell
    if current_quantity is not None and current_quantity >= quantity:
        new_quantity = current_quantity - quantity

        cursor.execute("INSERT INTO Sell (book_id, quantity, date) VALUES (?, ?, ?)", (book_id, quantity, date))
        cursor.execute("UPDATE Book SET quantity = ?,sold =sold + ?  WHERE id = ?", (new_quantity,quantity,book_id))
        conn.commit()
        # cursor.execute("SELECT efficiency,date FROM Book")
        # books = cursor.fetchall()
        # effec = books[0]/(date.day-books[1].days)
        # cursor.execute("UPDATE Book SET efficiency = ?  WHERE id = ?", (effec, book_id))
        # conn.commit()
        conn.close()
        # messagebox.showinfo("Success", "Book sale recorded successfully!")
    else:
        messagebox.showinfo("Input Error","Not enough stock available.")

def get_book_quantity(book_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT quantity FROM Book WHERE id = ?", (book_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# Functionality for book analysis
def analyze_books():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT Book.name, SUM(Sell.quantity) 
    FROM Sell
    JOIN Book ON Sell.book_id = Book.id
    GROUP BY Sell.book_id
    ORDER BY SUM(Sell.quantity) DESC
    """)
    books = cursor.fetchall()
    conn.close()

    titles, quantities = zip(*books) if books else ([], [])

    # Plotting the sales data
    plt.figure(figsize=(10, 6))
    plt.bar(titles, quantities, color='blue')
    plt.xlabel('Book Title')
    plt.ylabel('Total Quantity Sold')
    plt.title('Book Sales Analysis')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# Function to recommend a book (simple logic: recommend the one with highest sales)
def recommend_book():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT Book.name, SUM(Sell.quantity) 
    FROM Sell
    JOIN Book ON Sell.book_id = Book.id
    GROUP BY Sell.book_id
    ORDER BY SUM(Sell.quantity) DESC
    LIMIT 1
    """)
    recommendation = cursor.fetchone()
    conn.close()

    if recommendation:
        book_title = recommendation[0]
        messagebox.showinfo("Book Recommendation", f"We recommend the book: {book_title}")
    else:
        messagebox.showinfo("No Data", "No sales data available for recommendations.")

# Function to fetch and display book data in a table
def fetch_books():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, author, quantity, date, price, type, sold,efficiency FROM Book")
    books = cursor.fetchall()
    conn.close()
    return books
