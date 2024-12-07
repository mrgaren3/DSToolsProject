from sqlconnect import *
import tkinter as tk
from tkcalendar import DateEntry  # Import the DateEntry widget
from tkinter import ttk
from tkinter import simpledialog


class BookStoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Store Management System")
        self.root.geometry("800x600")

        create_tables()

        self.tab_control = ttk.Notebook(root)

        self.add_book_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.add_book_tab, text="Add Book")
        self.setup_add_book_tab()

        # Sell Book Tab
        self.sell_book_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.sell_book_tab, text="Sell Book")
        self.setup_sell_book_tab()

        # Book Analysis Tab
        self.analysis_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.analysis_tab, text="Book Analysis")
        self.setup_analysis_tab()

        # Show Data Tab
        self.show_data_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.show_data_tab, text="Show Data")
        self.setup_show_data_tab()

        self.tab_control.pack(expand=1, fill="both")

    def setup_add_book_tab(self):
        tk.Label(self.add_book_tab, text="Title").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self.add_book_tab, text="Author").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(self.add_book_tab, text="Price").grid(row=2, column=0, padx=10, pady=5)
        tk.Label(self.add_book_tab, text="Quantity").grid(row=3, column=0, padx=10, pady=5)
        tk.Label(self.add_book_tab, text="Type").grid(row=4, column=0, padx=10, pady=5)
        tk.Label(self.add_book_tab, text="Purchase Date").grid(row=5, column=0, padx=10, pady=5)

        self.title_entry = tk.Entry(self.add_book_tab)
        self.title_entry.grid(row=0, column=1, padx=10, pady=5)

        self.author_entry = tk.Entry(self.add_book_tab)
        self.author_entry.grid(row=1, column=1, padx=10, pady=5)

        self.price_entry = tk.Entry(self.add_book_tab)
        self.price_entry.grid(row=2, column=1, padx=10, pady=5)

        self.quantity_entry = tk.Entry(self.add_book_tab)
        self.quantity_entry.grid(row=3, column=1, padx=10, pady=5)

        self.type_entry = tk.Entry(self.add_book_tab)
        self.type_entry.grid(row=4, column=1, padx=10, pady=5)

        # DateEntry widget for Purchase Date
        self.date_entry = DateEntry(self.add_book_tab, date_pattern='y-mm-dd')
        self.date_entry.grid(row=5, column=1, padx=10, pady=5)

        self.add_book_btn = tk.Button(self.add_book_tab, text="Add Book", command=self.on_add_book)
        self.add_book_btn.grid(row=6, columnspan=2, pady=10)

    def setup_sell_book_tab(self):
        tk.Label(self.sell_book_tab, text="Book ID").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self.sell_book_tab, text="Quantity").grid(row=1, column=0, padx=10, pady=5)

        self.book_id_entry = tk.Entry(self.sell_book_tab)
        self.book_id_entry.grid(row=0, column=1, padx=10, pady=5)

        self.quantity_entry2 = tk.Entry(self.sell_book_tab)
        self.quantity_entry2.grid(row=1, column=1, padx=10, pady=5)

        self.sell_book_btn = tk.Button(self.sell_book_tab, text="Sell Book", command=self.on_sell_book)
        self.sell_book_btn.grid(row=2, columnspan=2, pady=10)

    def setup_analysis_tab(self):
        self.analysis_btn = tk.Button(self.analysis_tab, text="Analyze Books", command=self.on_analyze_books)
        self.analysis_btn.pack(pady=20)

        self.recommend_btn = tk.Button(self.analysis_tab, text="Recommend Book", command=self.on_recommend_book)
        self.recommend_btn.pack(pady=10)

    def setup_show_data_tab(self):
        # Search bar
        search_frame = tk.Frame(self.show_data_tab)
        search_frame.pack(fill="x", pady=5)

        tk.Label(search_frame, text="Search By:").pack(side="left", padx=5)

        self.search_field = ttk.Combobox(
            search_frame,
            values=[
                "ID", "Title", "Author", "Quantity", "Date", "Price", "Type", "Sold",
                "Efficiency", "Rating", "Num People Rated"
            ],
            state="readonly"
        )
        self.search_field.set("Title")  # Default field to search by
        self.search_field.pack(side="left", padx=5)

        tk.Label(search_frame, text="Search:").pack(side="left", padx=5)

        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side="left", padx=5, fill="x", expand=True)

        self.search_button = tk.Button(search_frame, text="Search", command=self.on_specific_search)
        self.search_button.pack(side="left", padx=5)

        self.clear_search_button = tk.Button(search_frame, text="Clear", command=self.refresh_data)
        self.clear_search_button.pack(side="left", padx=5)

        # Treeview
        self.tree = ttk.Treeview(
            self.show_data_tab,
            columns=(
                "ID", "Title", "Author", "Quantity", "Date", "Price", "Type",
                "Sold", "Efficiency", "Rating", "Num People Rated"
            ),
            show="headings"
        )
        self.tree.heading("ID", text="ID", command=lambda: self.sort_column("ID", False))
        self.tree.heading("Title", text="Title", command=lambda: self.sort_column("Title", False))
        self.tree.heading("Author", text="Author", command=lambda: self.sort_column("Author", False))
        self.tree.heading("Quantity", text="Quantity", command=lambda: self.sort_column("Quantity", False))
        self.tree.heading("Date", text="Date", command=lambda: self.sort_column("Date", False))
        self.tree.heading("Price", text="Price", command=lambda: self.sort_column("Price", False))
        self.tree.heading("Type", text="Type", command=lambda: self.sort_column("Type", False))
        self.tree.heading("Sold", text="Sold", command=lambda: self.sort_column("Sold", False))
        self.tree.heading("Efficiency", text="Efficiency", command=lambda: self.sort_column("Efficiency", False))
        self.tree.heading("Rating", text="Rating", command=lambda: self.sort_column("Rating", False))
        self.tree.heading("Num People Rated", text="Num People Rated",
                          command=lambda: self.sort_column("Num People Rated", False))

        self.tree.pack(fill="both", expand=True)

        # Load books data into the table
        self.refresh_data()

    def on_add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        price = self.price_entry.get()
        quantity = self.quantity_entry.get()
        purchase_date = self.date_entry.get_date()
        book_type =self.type_entry.get()

        if title and author and price and quantity:
            add_book(title, author, float(price), purchase_date, int(quantity),book_type)
            self.title_entry.delete(0, tk.END)
            self.author_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
            self.quantity_entry.delete(0, tk.END)
            self.type_entry.delete(0,tk.END)
        else:
            print(title,author,price,quantity,purchase_date)
            messagebox.showwarning("Input Error", "Please fill in all fields.")


    def on_sell_book(self):
        book_id = self.book_id_entry.get()
        quantity2 = self.quantity_entry2.get()

        if book_id and quantity2:
            try:
                # Ask the user for an optional rating
                rating = simpledialog.askstring(
                    "Rate Book",
                    "Optional: Rate this book (1-5) or leave empty to skip:",
                    parent=self.root,
                )

                if rating:
                    rating = float(rating)
                    if rating < 1 or rating > 5:
                        raise ValueError("Rating must be between 1 and 5.")

                # Call sell_book with the optional rating
                sell_book(int(book_id), int(quantity2), rating if rating else None)
                messagebox.showinfo("Success", "Book sold successfully!")
                self.book_id_entry.delete(0, tk.END)
                self.quantity_entry2.delete(0, tk.END)
            except ValueError as e:
                messagebox.showerror("Input Error", str(e))
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    def on_analyze_books(self):
        analyze_books()

    def on_recommend_book(self):
        recommend_book()

    def refresh_data(self):
        # Clear the search bar and reset the dropdown
        self.search_entry.delete(0, tk.END)
        self.search_field.set("Title")

        # Clear the existing rows in the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Fetch updated data and insert into the Treeview
        books = fetch_books()
        for book in books:
            self.tree.insert("", "end", values=book)

    def sort_column(self, col, reverse):
    # Retrieve all items in the Treeview
        l = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]

        # Sort based on the column data type (try to cast to int or float, fallback to string)
        try:
            l.sort(key=lambda t: float(t[0]), reverse=reverse)
        except ValueError:
            l.sort(key=lambda t: t[0], reverse=reverse)

        # Reorder the items in the Treeview
        for index, (_, k) in enumerate(l):
            self.tree.move(k, "", index)

        # Reverse sort order for the next click
        self.tree.heading(col, command=lambda: self.sort_column(col, not reverse))

    def on_search(self):
        query = self.search_entry.get().strip().lower()  # Get the search query

        if not query:
            messagebox.showinfo("Search", "Please enter a search query.")
            return

        # Fetch all books from the database
        books = fetch_books()

        # Filter books that match the query in any column
        filtered_books = [
            book for book in books if any(query in str(value).lower() for value in book)
        ]

        # Clear the existing rows in the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Display the filtered books
        for book in filtered_books:
            self.tree.insert("", "end", values=book)

        if not filtered_books:
            messagebox.showinfo("Search", "No matching results found.")

    def on_specific_search(self):
        query = self.search_entry.get().strip().lower()  # Get the search query
        field = self.search_field.get()  # Get the selected field to search by

        if not query:
            messagebox.showinfo("Search", "Please enter a search query.")
            return

        if not field:
            messagebox.showinfo("Search", "Please select a field to search.")
            return

        # Map field names to the database column indices
        field_map = {
            "ID": 0,
            "Title": 1,
            "Author": 2,
            "Quantity": 3,
            "Date": 4,
            "Price": 5,
            "Type": 6,
            "Sold": 7,
            "Efficiency": 8
        }

        # Get the corresponding column index for the selected field
        field_index = field_map[field]

        # Fetch all books from the database
        books = fetch_books()

        # Filter books where the selected field matches the query
        filtered_books = [
            book for book in books if query in str(book[field_index]).lower()
        ]

        # Clear the existing rows in the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Display the filtered books
        for book in filtered_books:
            self.tree.insert("", "end", values=book)

        if not filtered_books:
            messagebox.showinfo("Search", "No matching results found.")
