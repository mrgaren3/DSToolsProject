from functions import *
import tkinter as tk

class Analysis:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)

        self.analysis_btn = tk.Button(self.frame, text="Analyze Books", command=on_analyze_books,
                                      font=("Times New Roman", 13, "bold"),
                                      activebackground="blue", activeforeground="white",
                                      highlightthickness=0)
        self.analysis_btn.pack(pady=20)

        self.recommend_btn = tk.Button(self.frame, text="Recommend Book", command=on_recommend_book,
                                       font=("Times New Roman", 13, "bold"),
                                       activebackground="blue", activeforeground="white",
                                       highlightthickness=0)
        self.recommend_btn.pack(pady=10)

    def get_frame(self):
        return self.frame
