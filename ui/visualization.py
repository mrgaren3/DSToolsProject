from functions import *
import tkinter as tk

class Visualization:
    def __init__(self,parent):
        self.frame = tk.Frame(parent)

        tk.Label(self.frame, text="Choose a Visualization", font=("Times New Roman", 16, "bold")).pack(
            pady=10)

        tk.Button(self.frame, text="Rating Distribution", command=show_rating_distribution,
                  font=("Times New Roman", 13, "bold"),
                  activebackground="blue", activeforeground="white", highlightthickness=0).pack(pady=5)
        tk.Button(self.frame, text="Top Authors", command=show_top_authors,
                  font=("Times New Roman", 13, "bold"),
                  activebackground="blue", activeforeground="white", highlightthickness=0).pack(pady=5)
        tk.Button(self.frame, text="Genre Count", command=show_genre_count,
                  font=("Times New Roman", 13, "bold"),
                  activebackground="blue", activeforeground="white", highlightthickness=0).pack(pady=5)
        tk.Button(self.frame, text="Price Distribution", command=show_price_distribution,
                  font=("Times New Roman", 13, "bold"),
                  activebackground="blue", activeforeground="white", highlightthickness=0).pack(pady=5)

    def get_frame(self):
        return self.frame