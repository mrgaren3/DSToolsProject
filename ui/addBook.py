import  tkinter as tk
from tkcalendar import DateEntry  # Import the DateEntry widget
from Data.sqlconnect import *
from tkinter import ttk


class AddBook:
    def __init__(self,parent):
        self.frame = tk.Frame(parent)
        tk.Label(self.frame, text="Title", font=("Times New Roman", 14, "bold")).grid(row=0, column=0, padx=15, pady=10)
        tk.Label(self.frame, text="Author", font=("Times New Roman", 14, "bold")).grid(row=1, column=0, padx=15,
                                                                                       pady=10)
        tk.Label(self.frame, text="Price", font=("Times New Roman", 14, "bold")).grid(row=2, column=0, padx=15, pady=10)
        tk.Label(self.frame, text="Quantity", font=("Times New Roman", 14, "bold")).grid(row=3, column=0, padx=15,
                                                                                         pady=10)
        tk.Label(self.frame, text="Type", font=("Times New Roman", 14, "bold")).grid(row=4, column=0, padx=15, pady=10)
        tk.Label(self.frame, text="Purchase Date", font=("Times New Roman", 14, "bold")).grid(row=5, column=0, padx=15,
                                                                                              pady=10)

        # Entry Widgets
        self.title_entry = tk.Entry(self.frame, font=("Tahoma", 12))
        self.title_entry.grid(row=0, column=1, padx=15, pady=10)
        self.author_entry = tk.Entry(self.frame, font=("Tahoma", 12))
        self.author_entry.grid(row=1, column=1, padx=15, pady=10)
        self.price_entry = tk.Entry(self.frame, font=("Tahoma", 12))
        self.price_entry.grid(row=2, column=1, padx=15, pady=10)
        self.quantity_entry = tk.Entry(self.frame, font=("Tahoma", 12))
        self.quantity_entry.grid(row=3, column=1, padx=15, pady=10)
        self.type_entry = tk.Entry(self.frame, font=("Tahoma", 12))
        self.type_entry.grid(row=4, column=1, padx=15, pady=10)
        self.date_entry = DateEntry(self.frame, date_pattern='y-mm-dd', font=("Tahoma", 12))
        self.date_entry.grid(row=5, column=1, padx=15, pady=10)

        # Add Book Button
        self.add_book_btn = tk.Button(self.frame, text="Add Book", command=self.on_add_book,
                                      font=("Times New Roman", 13, "bold"))
        self.add_book_btn.grid(row=6, column=0, columnspan=2, pady=10)

    def on_add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        price = self.price_entry.get()
        quantity = self.quantity_entry.get()
        purchase_date = self.date_entry.get_date()
        book_type = self.type_entry.get()

        if title and author and price and quantity:
            add_book(title, author, float(price), purchase_date, int(quantity), book_type)
            self.title_entry.delete(0, tk.END)
            self.author_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
            self.quantity_entry.delete(0, tk.END)
            self.type_entry.delete(0, tk.END)
        else:
            print(title, author, price, quantity, purchase_date)
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    def get_frame(self):
        return self.frame