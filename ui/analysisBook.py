from functions import *

class Analysis:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.frame.pack(fill="both", expand=True)

        # Buttons for analysis
        self.analysis_btn = tk.Button(self.frame, text="RFM", command=rfmModel,
                                      font=("Times New Roman", 13, "bold"),
                                      activebackground="blue", activeforeground="white",
                                      highlightthickness=0)
        self.analysis_btn.pack(pady=20)

        self.popularity_btn = tk.Button(self.frame, text="Popularity Book", command=self.show_popularity,
                                        font=("Times New Roman", 13, "bold"),
                                        activebackground="blue", activeforeground="white",
                                        highlightthickness=0)
        self.popularity_btn.pack(pady=10)

        # Frame to display results
        self.results_frame = tk.Frame(self.frame)
        self.results_frame.pack(fill="both", expand=True, padx=10, pady=10)


    def show_popularity(self):
        on_popularity_book(self.results_frame)

    def get_frame(self):
        return self.frame
