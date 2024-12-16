import seaborn as sns
import pandas as pd
from Data.sqlconnect import *
import tkinter as tk
import matplotlib.pyplot as plt
from sqlalchemy import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import difflib

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
    pass

def on_popularity_book(parent_frame):
    df = load_data()
    popularity_df = df.copy()
    popularity_df['popularity_score'] = (popularity_df['Rating'] * popularity_df['No_of_People_rated'])
    popular_items = popularity_df.sort_values(by='popularity_score', ascending=False)

    # Select the top N popular items (e.g., top 20)
    top_n = 20
    top_popular_items = popular_items[['Title', 'popularity_score']].head(top_n)

    # Clear the frame to refresh the content
    for widget in parent_frame.winfo_children():
        widget.destroy()

    # Add a heading label
    tk.Label(parent_frame, text="Top Popular Books", font=("Times New Roman", 16, "bold")).pack(pady=10)

    # Create a frame for the table
    table_frame = tk.Frame(parent_frame)
    table_frame.pack(fill="both", expand=True)

    # Create column headings
    tk.Label(table_frame, text="Title", font=("Times New Roman", 12, "bold"), width=30, anchor="w").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(table_frame, text="Popularity Score", font=("Times New Roman", 12, "bold"), width=15, anchor="center").grid(row=0, column=1, padx=10, pady=5)

    # Populate the table with book data
    for i, (title, score) in enumerate(zip(top_popular_items['Title'], top_popular_items['popularity_score'])):
        tk.Label(table_frame, text=title, font=("Times New Roman", 12), anchor="w").grid(row=i + 1, column=0, padx=10, pady=5, sticky="w")
        tk.Label(table_frame, text=round(score, 2), font=("Times New Roman", 12), anchor="center").grid(row=i + 1, column=1, padx=10, pady=5)

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

import ttkbootstrap as bk

def show_custom_error_dialog(parent, message):
    # Create a custom error dialog with a Toplevel window
    dialog = bk.Toplevel(parent)
    dialog.title("Input Error")
    dialog.geometry("400x200")  # Adjust the size of the dialog

    # Set the background color to red (danger style)
    dialog.configure(bg="#f8d7da")

    # Label for the error message, wrap long text within the window
    label = bk.Label(dialog, text=message, font=("Arial", 12), wraplength=380)
    label.pack(padx=10, pady=20)

    # Button to close the dialog
    button = bk.Button(dialog, text="Close", bootstyle="danger", command=dialog.destroy)
    button.pack(pady=10)