import pandas as pd
import numpy as np
from scipy.sparse import coo_matrix

def load_and_clean_data():
    books_df = pd.read_csv('data/Books.csv')
    ratings_df = pd.read_csv('data/Ratings.csv')
    
    # Clean 'Year-Of-Publication' column
    books_df['Year-Of-Publication'] = pd.to_numeric(books_df['Year-Of-Publication'], errors='coerce')
    books_df = books_df.dropna(subset=['Year-Of-Publication'])
    books_df['Year-Of-Publication'] = books_df['Year-Of-Publication'].astype(int)
    
    return books_df, ratings_df

def prepare_fp_growth_data(books_df, ratings_df):
    df = pd.merge(ratings_df, books_df[['ISBN', 'Book-Title', 'Image-URL-M']], on='ISBN', how='inner')
    df = df.drop_duplicates(['User-ID', 'Book-Title'])
    df['Book-Rating'] = df['Book-Rating'].apply(lambda x: 1 if x > 0 else 0)
    
    user_ids = pd.Categorical(df['User-ID']).codes
    book_titles = pd.Categorical(df['Book-Title']).codes
    
    sparse_matrix = coo_matrix(
        (df['Book-Rating'], (user_ids, book_titles)),
        shape=(len(np.unique(user_ids)), len(np.unique(book_titles)))
    ).tocsr()
    
    transactions = []
    for user_row in sparse_matrix:
        books = user_row.indices
        transactions.append(books.tolist())
        
    book_titles = pd.Categorical(df['Book-Title']).categories
    transactions_with_titles = [[book_titles[i] for i in transaction] for transaction in transactions]
    
    return transactions_with_titles, book_titles, df
