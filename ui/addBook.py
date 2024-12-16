import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from Data.sqlconnect import *
from functions import show_custom_error_dialog

class AddBook:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.frame.pack(expand=True)  # Center the frame in the parent

        # Labels
        ttk.Label(self.frame, text="Title", font=("Times New Roman", 14, "bold")).grid(row=0, column=0, padx=15, pady=10, sticky="e")
        ttk.Label(self.frame, text="Author", font=("Times New Roman", 14, "bold")).grid(row=1, column=0, padx=15, pady=10, sticky="e")
        ttk.Label(self.frame, text="Price", font=("Times New Roman", 14, "bold")).grid(row=2, column=0, padx=15, pady=10, sticky="e")
        ttk.Label(self.frame, text="Quantity", font=("Times New Roman", 14, "bold")).grid(row=3, column=0, padx=15, pady=10, sticky="e")
        ttk.Label(self.frame, text="Type", font=("Times New Roman", 14, "bold")).grid(row=4, column=0, padx=15, pady=10, sticky="e")
        ttk.Label(self.frame, text="Purchase Date", font=("Times New Roman", 14, "bold")).grid(row=5, column=0, padx=15, pady=10, sticky="e")

        # Entry Widgets
        self.title_entry = ttk.Entry(self.frame, font=("", 12))
        self.title_entry.grid(row=0, column=1, padx=15, pady=10, sticky="w")
        self.author_entry = ttk.Entry(self.frame, font=("", 12))
        self.author_entry.grid(row=1, column=1, padx=15, pady=10, sticky="w")
        self.price_entry = ttk.Entry(self.frame, font=("", 12))
        self.price_entry.grid(row=2, column=1, padx=15, pady=10, sticky="w")
        self.quantity_entry = ttk.Entry(self.frame, font=("", 12))
        self.quantity_entry.grid(row=3, column=1, padx=15, pady=10, sticky="w")
        self.type_entry = ttk.Entry(self.frame, font=("", 12))
        self.type_entry.grid(row=4, column=1, padx=15, pady=10, sticky="w")

        # Use ttkbootstrap.DateEntry instead of tkcalendar.DateEntry
        self.date_entry = ttk.DateEntry(self.frame, dateformat='%Y-%m-%d', bootstyle=PRIMARY)
        self.date_entry.grid(row=5, column=1, padx=15, pady=10, sticky="w")

        # Add Book Button
        self.add_book_btn = ttk.Button(self.frame, text="Add Book", command=self.on_add_book,
                                       bootstyle="success")
        self.add_book_btn.grid(row=6, column=0, columnspan=2, pady=10)

        # Center all grid columns
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

    def on_add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        price = self.price_entry.get()
        quantity = self.quantity_entry.get()
        purchase_date = self.date_entry.entry.get()  # Access the date
        book_type = self.type_entry.get()

        if title and author and price and quantity:
            add_book(title, author, float(price), purchase_date, int(quantity), book_type)
            self.title_entry.delete(0, ttk.END)
            self.author_entry.delete(0, ttk.END)
            self.price_entry.delete(0, ttk.END)
            self.quantity_entry.delete(0, ttk.END)
            self.type_entry.delete(0, ttk.END)
        else:
            print(title, author, price, quantity, purchase_date)
            show_custom_error_dialog(self.frame, "Please fill in all fields.")

    def get_frame(self):
        return self.frame
