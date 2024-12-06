import pandas as pd
import numpy as np
from sqlconnect import *  # Ensure this contains the `add_book` function

# Read the CSV file
file_path = 'Books_df.csv'  # Replace with your CSV file path
data = pd.read_csv(file_path)
data['No. of People rated'] = data['No. of People rated'].fillna(0).astype(int)  # Handle missing values for ratings


# Clean and extract the required columns
extracted_data = data[['Rating','No. of People rated']]
i=1
maxuim = np.max(extracted_data['No. of People rated'])

# Get the current date
# day = datetime.now().date()

# Loop through rows in DataFrame and call add_book
for _, row in extracted_data.iterrows():
    rating,NumPeople = row['Rating'], row['No. of People rated']
    quntity =int((rating/5)*(NumPeople/maxuim)*1000) 
    sell_book(i,quntity)
    i+=1