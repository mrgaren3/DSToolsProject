from tkinter import ttk
from Data.sqlconnect import fetch_books
import tkinter as tk
from tkinter import messagebox


class ShowData:
    def __init__(self,parent):
        self.frame = tk.Frame(parent)  # Correctly initialize parent frame
        self.frame.pack(fill="both", expand=True)  # Ensure the frame expands to fill

        # Search frame
        search_frame = tk.Frame(self.frame)  # Attach to self.frame, not self.show_data_tab
        search_frame.pack(fill="x", pady=5)

        tk.Label(search_frame, text="Search By:", font=("Times New Roman", 12, "bold")).pack(side="left", padx=5)

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

        tk.Label(search_frame, text="Search:", font=("Times New Roman", 12, "bold")).pack(side="left", padx=5)

        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side="left", padx=5, fill="x", expand=True)

        self.search_button = tk.Button(search_frame, text="Search", command=self.on_specific_search,
                                       font=("Times New Roman", 13, "bold"),
                                       activebackground="blue", activeforeground="white",
                                       highlightthickness=0)
        self.search_button.pack(side="left", padx=5)

        self.clear_search_button = tk.Button(search_frame, text="Clear", command=self.refresh_data,
                                             font=("Times New Roman", 12, "bold"),
                                             activebackground="blue", activeforeground="white",
                                             highlightthickness=0)
        self.clear_search_button.pack(side="left", padx=5)

        # Treeview
        self.tree = ttk.Treeview(
            self.frame,  # Correct parent frame
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

    def get_frame(self):
        return self.frame