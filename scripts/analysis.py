import plotly.express as px

def create_visualizations(books_df, ratings_df, df):
    # Top 10 most rated books
    top_rated_books = df.groupby('Book-Title')['Book-Rating'].count().sort_values(ascending=False).head(10)
    fig_top_rated = px.bar(top_rated_books, x=top_rated_books.index, y='Book-Rating', 
                           title='Top 10 Most Rated Books', labels={'Book-Rating': 'Number of Ratings'})

    # Distribution of ratings
    fig_rating_dist = px.histogram(ratings_df, x='Book-Rating', nbins=10, 
                                   title='Distribution of Book Ratings',
                                   labels={'Book-Rating': 'Rating', 'count': 'Number of Ratings'})

    # Books published per year
    books_per_year = books_df['Year-Of-Publication'].value_counts().sort_index()
    fig_books_per_year = px.line(x=books_per_year.index, y=books_per_year.values, 
                                 title='Number of Books Published per Year',
                                 labels={'x': 'Year', 'y': 'Number of Books'})

    # Top 10 publishers
    top_publishers = books_df['Publisher'].value_counts().head(10)
    fig_publishers = px.pie(values=top_publishers.values, names=top_publishers.index, 
                            title='Top 10 Publishers')

    # Correlation matrix
    correlation_df = df.groupby('Book-Title')['Book-Rating'].agg(['mean', 'count']).reset_index()
    correlation_df = correlation_df.merge(books_df[['Book-Title', 'Year-Of-Publication']], on='Book-Title')
    correlation_matrix = correlation_df[['mean', 'count', 'Year-Of-Publication']].corr()

    fig_correlation = px.imshow(correlation_matrix, 
                                labels=dict(color="Correlation"),
                                title="Correlation Matrix: Rating, Count, and Publication Year")

    return fig_top_rated, fig_rating_dist, fig_books_per_year, fig_publishers, fig_correlation
