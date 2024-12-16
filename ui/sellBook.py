import ttkbootstrap as tk
from tkinter import messagebox, simpledialog, Listbox
from Data.sqlconnect import sell_book, get_book_title  # Add a function to fetch book title
from functions import content_based_system


class SellBook:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)

        # Using pack for all widgets within this frame
        self.frame.pack(padx=50, pady=50, fill="both", expand=True)

        # Book ID label and entry
        self.book_id_label = tk.Label(self.frame, text="Book ID", font=("Times New Roman", 14, "bold"))
        self.book_id_label.pack(padx=15, pady=10)

        self.book_id_entry = tk.Entry(self.frame)
        self.book_id_entry.pack(padx=15, pady=10)

        # Quantity label and entry
        self.quantity_label = tk.Label(self.frame, text="Quantity", font=("Times New Roman", 14, "bold"))
        self.quantity_label.pack(padx=15, pady=10)

        self.quantity_entry2 = tk.Entry(self.frame)
        self.quantity_entry2.pack(padx=15, pady=10)

        # Sell book button
        self.sell_book_btn = tk.Button(self.frame, text="Sell Book", command=self.on_sell_book, bootstyle="success")
        self.sell_book_btn.pack(pady=10)

        # Recommendations button
        self.recommend_btn = tk.Button(self.frame, text="Get Recommendations", command=self.show_recommendations,
                                       bootstyle="success")
        self.recommend_btn.pack(pady=10)

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

    def show_recommendations(self):
        book_id = self.book_id_entry.get()

        if not book_id:
            messagebox.showwarning("Input Error", "Please enter a Book ID to get recommendations.")
            return

        try:
            # Fetch the book title using the book ID
            book_title = get_book_title(int(book_id))

            if not book_title:
                messagebox.showerror("Error", "No book found with the given ID.")
                return

            # Call the content-based system
            recommendations = content_based_system(book_title)

            # Create a new window to display recommendations
            rec_window = tk.Toplevel(self.frame)
            rec_window.title("Book Recommendations")

            # Display the chosen book title
            tk.Label(rec_window, text=f"Recommendations for: '{book_title}'", font=("Arial", 14, "bold")).pack(pady=10)

            # Add a listbox to display recommended books
            listbox = Listbox(rec_window, width=150, height=10)
            listbox.pack(pady=10)

            for book, score in recommendations:
                listbox.insert(tk.END, f"{book} (Score: {score:.4f})")

            # Add a close button
            tk.Button(rec_window, text="Close", command=rec_window.destroy).pack(pady=10)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
