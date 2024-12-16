import tkinter as tk
from tkinter import messagebox, simpledialog
from Data.sqlconnect import sell_book


class SellBook:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)

        tk.Label(self.frame, text="Book ID",
                 font=("Times New Roman", 14, "bold")).grid(row=0, column=0, padx=15, pady=10)
        tk.Label(self.frame, text="Quantity",
                 font=("Times New Roman", 14, "bold")).grid(row=1, column=0, padx=15, pady=10)

        self.book_id_entry = tk.Entry(self.frame)
        self.book_id_entry.grid(row=0, column=1, padx=15, pady=10)

        self.quantity_entry2 = tk.Entry(self.frame)
        self.quantity_entry2.grid(row=1, column=1, padx=15, pady=10)

        self.sell_book_btn = tk.Button(self.frame, text="Sell Book", command=self.on_sell_book,
                                       font=("Times New Roman", 13, "bold"),
                                       activebackground="blue", activeforeground="white",
                                       highlightthickness=0)
        self.sell_book_btn.grid(row=2, columnspan=2, pady=10)

    def on_sell_book(self):
        book_id = self.book_id_entry.get()
        quantity2 = self.quantity_entry2.get()

        if book_id and quantity2:
            try:
                # Ask the user for an optional rating
                rating = simpledialog.askstring(
                    "Rate Book",
                    "Optional: Rate this book (1-5) or leave empty to skip:",
                    parent=self.frame
                )

                if rating:
                    try:
                        rating = float(rating)
                        if rating < 1 or rating > 5:
                            raise ValueError("Rating must be between 1 and 5.")
                    except ValueError:
                        messagebox.showerror("Error", "Rating must be a number between 1 and 5.")
                        return

                # Call sell_book with the optional rating
                sell_book(int(book_id), int(quantity2), rating if rating else None)
                messagebox.showinfo("Success", "Book sold successfully!")
                self.book_id_entry.delete(0, tk.END)
                self.quantity_entry2.delete(0, tk.END)
            except ValueError as e:
                messagebox.showerror("Input Error", str(e))
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    def get_frame(self):
        return self.frame
