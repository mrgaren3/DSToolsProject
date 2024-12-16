import seaborn as sns
import pandas as pd
from Data.sqlconnect import *

def load_data():
    try:
        df = pd.read_csv('Data/Books_df.csv')
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
    genre_counts = df['Main Genre'].value_counts()
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


def on_analyze_books():
    analyze_books()


def on_recommend_book():
    recommend_book()

