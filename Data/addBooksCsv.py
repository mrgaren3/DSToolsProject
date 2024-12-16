import pandas as pd
import numpy as np
from sqlconnect import *  # Ensure this contains the `add_book` and `sell_book` methods

# Read the CSV file
file_path = 'Books_df.csv'  # Replace with your CSV file path
data = pd.read_csv(file_path)

# Clean and extract the required columns
data['Price'] = data['Price'].replace('[₹,]', '', regex=True).astype(float)  # Clean price column
data['No. of People rated'] = data['No. of People rated'].fillna(0).astype(int)  # Handle missing values for ratings
data['Rating'] = data['Rating'].fillna(0).astype(float)  # Handle missing values for ratings

# Extract relevant columns
extracted_data = data[['Title', 'Author', 'Main Genre', 'Price', 'Rating', 'No. of People rated']]

# Get the maximum number of people who rated for scaling quantity calculation
max_people_rated = np.max(extracted_data['No. of People rated'])

# Get the current date
day = datetime.now().date()

# Initialize book ID counter
book_id = 1

# Process each row to add books and calculate sales
for _, row in extracted_data.iterrows():
    # Extract book details
    title = row['Title']
    author = row['Author']
    genre = row['Main Genre']
    price = row['Price']
    rating = row['Rating']
    num_people_rated = row['No. of People rated']

    # Add book to the database
    add_book(title, author, price, day, 10000, genre, rating, num_people_rated)

    # Calculate quantity to sell based on rating and number of people rated
    quantity_to_sell = int((rating / 5) * (num_people_rated / max_people_rated) * 10000)

    # Sell the book
    sell_book(book_id, quantity_to_sell)

    # Increment book ID counter
    book_id += 1
