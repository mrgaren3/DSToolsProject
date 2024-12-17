import seaborn as sns
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Data.sqlconnect import *
import tkinter as tk
import matplotlib.pyplot as plt
from sqlalchemy import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import ttkbootstrap as ttk

def load_data():
    try:
        engine = create_engine('sqlite:///Data/bookstore.db')
        connection = engine.connect()
        df = pd.read_sql_table('Book', connection)
        return df
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load data: {e}")
        return pd.DataFrame()

def show_rating_distribution():
    df = load_data()
    plt.figure(figsize=(8, 6))
    sns.histplot(df['Rating'], bins=20, kde=True, color='skyblue')
    plt.title('Distribution of Book Ratings',
              fontname="Times New Roman", fontsize=20, fontweight=900)
    plt.xlabel('Rating', fontname="Times New Roman", fontweight=600, fontsize=15)
    plt.ylabel('Count', fontname="Times New Roman", fontweight=600, fontsize=15)
    plt.xticks(fontname="Tahoma", fontweight=450)
    plt.yticks(fontname="Tahoma", fontweight=450)
    plt.show()

def show_top_authors():
    df = load_data()
    top_authors = df['Author'].value_counts().head(10)
    plt.figure(figsize=(8, 6))
    sns.barplot(x=top_authors.values, y=top_authors.index, palette='viridis')
    plt.title('Top 10 Authors with Most Books',
              fontname="Times New Roman", fontsize=20, fontweight=900)
    plt.xlabel('Number of Books', fontname="Times New Roman", fontweight=600,
               fontsize=15)
    plt.ylabel('Author', fontname="Times New Roman", fontweight=600, fontsize=15, labelpad=-4)
    plt.yticks(fontsize=8, fontname="Tahoma", fontweight=450)
    plt.xticks(fontname="Tahoma", fontweight=450)
    plt.show()

def show_genre_count():
    df = load_data()
    genre_counts = df['Main_Genre'].value_counts()
    plt.figure(figsize=(8, 6))
    sns.barplot(x=genre_counts.values, y=genre_counts.index, palette='magma')
    plt.title('Book Count by Main Genre', fontsize=20, fontweight=900,
              fontname="Times New Roman")
    plt.xlabel('Number of Books', fontname="Times New Roman", fontweight=600,
               fontsize=15)
    plt.ylabel('Main Genre', fontsize=15, fontweight=600, fontname='Times New Roman', labelpad=-8)
    plt.yticks(fontsize=6, fontname="Tahoma", fontweight=450)
    plt.xticks(fontname="Tahoma", fontweight=450)
    plt.show()

def show_price_distribution():
    df = load_data()
    plt.figure(figsize=(8, 6))
    sns.histplot(df['Price'], bins=30, kde=True, color='orange')
    plt.title('Distribution of Book Prices', fontname="Times New Roman",
              fontsize=20, fontweight=900)
    plt.xlabel('Price (₹)', fontsize=15, fontweight=600, fontname="Times New Roman")
    plt.ylabel('Count', fontsize=15, fontname="Times New Roman", fontweight=600)
    plt.xticks(fontname="Tahoma", fontweight=450)
    plt.yticks(fontname="Tahoma", fontweight=450)
    plt.show()

def rfmModel():
    engine = create_engine('sqlite:///Data/bookstore.db')
    connection = engine.connect()
    df = pd.read_sql_table('Book', connection)
    data = pd.read_sql_table('Sell', connection)
    data["date"] = pd.to_datetime(data["date"])
    df["date"] = pd.to_datetime(df["date"])
    rfm_data = data.merge(df, left_on="book_id", right_on="id")
    current_date = pd.Timestamp.today()
    rfm_summary = (
        rfm_data.groupby("book_id")
        .agg(
            Recency=("date_x", lambda x: (current_date - x.max()).days),  # Recency calculation
            Frequency=("book_id", "count"),  # Frequency: Total sold per book
            Monetary=("sold", lambda x: (x * rfm_data.loc[x.index, "Price"]).sum())  # Monetary value
        )
        .reset_index()
    )

    # Merge 'title' from the 'df' DataFrame into rfm_summary based on 'book_id'
    rfm_summary = rfm_summary.merge(df[['id', 'Title']], left_on='book_id', right_on='id', how='left')

    # Debugging helper function to safely apply qcut
    def safe_qcut(series, q, labels):
        try:
            return pd.qcut(series, q=q, labels=labels, duplicates="drop")
        except ValueError:
            # Fallback: Assign the lowest rank if quantiles cannot be created
            return pd.Series([labels[-1]] * len(series), index=series.index)

    # Apply qcut safely for Recency, Frequency, and Monetary
    rfm_summary["R_rank"] = safe_qcut(rfm_summary["Recency"], q=5, labels=[4, 3, 2, 1])
    rfm_summary["F_rank"] = safe_qcut(rfm_summary["Frequency"], q=5, labels=[1, 2, 3, 4])
    rfm_summary["M_rank"] = safe_qcut(rfm_summary["Monetary"], q=5, labels=[1, 2, 3, 4])

    # Combine RFM scores into a single column
    rfm_summary["RFM_Score"] = (
            rfm_summary["R_rank"].astype(str)
            + rfm_summary["F_rank"].astype(str)
            + rfm_summary["M_rank"].astype(str)
    )

    # Assuming 'title' column exists in top_books for book titles
    top_books = rfm_summary.sort_values(by="Monetary", ascending=False).head(10)

    # Create a GUI window to display top 10 books and graph
    def show_top_books():
        # Create a new top-level window
        top_window = tk.Toplevel()
        top_window.title("Top 10 Books by Revenue")
        top_window.geometry("800x600")

        # Frame for Treeview
        tree_frame = tk.Frame(top_window)
        tree_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        # Create a Treeview widget to display the results
        columns = ("Title", "Frequency", "Revenue")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        tree.pack(fill="both", expand=True)

        # Define column headings
        tree.heading("Title", text="Book Title")
        tree.heading("Frequency", text="Frequency")
        tree.heading("Revenue", text="Revenue ($)")

        # Define column widths
        tree.column("Title", width=250)
        tree.column("Frequency", width=100, anchor="center")
        tree.column("Revenue", width=100, anchor="center")

        # Add rows to the Treeview
        for _, row in top_books.iterrows():
            tree.insert("", "end", values=(row["Title"], row["Frequency"], f"${row['Monetary']:.2f}"))

        # Create the plot
        titles = top_books["Title"]
        revenue = top_books["Monetary"]

        # Truncate book titles to the first 25 characters
        short_titles = [title[:25] for title in titles]

        # Plot revenue bar chart using plt
        plt.figure(figsize=(8, 4))
        plt.bar(short_titles, revenue, color="orange", label="Revenue")

        # Set plot labels and title
        plt.xlabel("Book Title")
        plt.ylabel("Revenue ($)")
        plt.title("Top 10 Books Revenue")
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Display the plot in a separate window
        plt.show()

        # Add a close button
        close_button = tk.Button(top_window, text="Close", command=top_window.destroy)
        close_button.pack(pady=10)

    show_top_books()
def wrap_text(text, max_length=15):
    return '\n'.join([text[i:i + max_length] for i in range(0, len(text), max_length)])

def on_popularity_book(parent_frame=None):
    # Load and process data
    df = load_data()
    popularity_df = df.copy()
    popularity_df['popularity_score'] = (popularity_df['Rating'] * popularity_df['No_of_People_rated'])
    popular_items = popularity_df.sort_values(by='popularity_score', ascending=False)

    # Select the top N popular items (e.g., top 20)
    top_n = 20
    top_popular_items = popular_items[['Title', 'popularity_score']].head(top_n)

    # Create a new window
    top_window = tk.Toplevel()
    top_window.title("Top Popular Books")
    top_window.geometry("800x600")

    # Add a heading label
    tk.Label(top_window, text="Top Popular Books", font=("Times New Roman", 16, "bold")).pack(pady=10)

    # Create a frame for the table
    table_frame = tk.Frame(top_window)
    table_frame.pack(fill="both", expand=True)

    # Create column headings
    tk.Label(table_frame, text="Title", font=("Times New Roman", 12, "bold"), width=30, anchor="w").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(table_frame, text="Popularity Score", font=("Times New Roman", 12, "bold"), width=15, anchor="center").grid(row=0, column=1, padx=10, pady=5)

    # Populate the table with book data
    for i, (title, score) in enumerate(zip(top_popular_items['Title'], top_popular_items['popularity_score'])):
        tk.Label(table_frame, text=title, font=("Times New Roman", 12), anchor="w").grid(row=i + 1, column=0, padx=10, pady=5, sticky="w")
        tk.Label(table_frame, text=round(score, 2), font=("Times New Roman", 12), anchor="center").grid(row=i + 1, column=1, padx=10, pady=5)

    # Add a close button
    close_button = tk.Button(top_window, text="Close", command=top_window.destroy)
    close_button.pack(pady=10)

def content_based_system(title):
    df =load_data()
    combined_features = df["Title"] + ' ' + df["Author"] + ' ' + df["Main_Genre"]
    vectorizer = TfidfVectorizer(stop_words='english')
    feature_vectors = vectorizer.fit_transform(combined_features)
    cosine_sim = cosine_similarity(feature_vectors, feature_vectors)

    # Get the index of the book that matches the title
    idx = df[df['Title'] == title].index[0]

    # Get the similarity scores of all books with the given book
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort books based on similarity scores in descending order
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the indices and similarity scores of the top 5 most similar books (excluding the input book)
    top_books = sim_scores[1:6]  # Skip the first one as it's the book itself

    # Retrieve book titles and their similarity scores
    recommendations = [(df.iloc[i[0]]['Title'], i[1]) for i in top_books]

    return recommendations


def show_custom_error_dialog(parent, message):
    # Create a custom error dialog with a Toplevel window
    dialog = ttk.Toplevel(parent)
    dialog.title("Input Error")
    dialog.geometry("400x200")  # Adjust the size of the dialog

    # Set the background color to red (danger style)
    dialog.configure(bg="#f8d7da")

    # Label for the error message, wrap long text within the window
    label = ttk.Label(dialog, text=message, font=("Arial", 12), wraplength=380)
    label.pack(padx=10, pady=20)

    # Button to close the dialog
    button = ttk.Button(dialog, text="Close", bootstyle="danger", command=dialog.destroy)
    button.pack(pady=10)
