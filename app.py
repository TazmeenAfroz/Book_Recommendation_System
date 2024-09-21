import streamlit as st
from scripts.preprocessing import load_and_clean_data, prepare_fp_growth_data
from scripts.analysis import create_visualizations
from scripts.fp_growth import run_fp_growth, get_books_in_rules, get_book_recommendations, format_rules

# Set page config
st.set_page_config(page_title="Book Recommendation System", page_icon="📚", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1E3D59;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 1.8rem;
        color: #1E3D59;
        margin-bottom: 1rem;
        border-bottom: 2px solid #FF6E40;
        padding-bottom: 0.5rem;
    }
    .stat-box {
        background-color: #F5F0E1;
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    .stat-box:hover {
        transform: translateY(-5px);
    }
    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF6E40;
        margin-bottom: 0.5rem;
    }
    .stat-label {
        font-size: 1.2rem;
        color: #1E3D59;
        text-transform: uppercase;
    }
    .stButton>button {
        background-color: #FF6E40;
        color: white;
        font-weight: bold;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        border: none;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #E85A3A;
    }
    .stSelectbox {
        color: #1E3D59;
    }
    .book-image {
        width: 100%;
        max-width: 200px;
        height: auto;
        margin-bottom: 1rem;
    }
    .book-title {
        font-size: 1rem;
        font-weight: bold;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return load_and_clean_data()

@st.cache_data
def prepare_data(books_df, ratings_df):
    return prepare_fp_growth_data(books_df, ratings_df)

@st.cache_data
def get_fp_growth_results(transactions_with_titles):
    return run_fp_growth(transactions_with_titles)

def main():
    # Header
    st.markdown('<h1 class="main-header">📚 Book Recommendation System</h1>', unsafe_allow_html=True)

    # Load data
    books_df, ratings_df = load_data()

    # FP-Growth Algorithm
    transactions_with_titles, book_titles, df = prepare_data(books_df, ratings_df)
    patterns, rules = get_fp_growth_results(transactions_with_titles)

    # Filter books to only those present in the rules
    books_in_rules = get_books_in_rules(rules)
    filtered_book_titles = [book for book in book_titles if book in books_in_rules]
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="stat-box"><p class="stat-number">{}</p><p class="stat-label">Total Books</p></div>'.format(len(books_df)), unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="stat-box"><p class="stat-number">{}</p><p class="stat-label">Unique Authors</p></div>'.format(books_df['Book-Author'].nunique()), unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="stat-box"><p class="stat-number">{}</p><p class="stat-label">Unique Publishers</p></div>'.format(books_df['Publisher'].nunique()), unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="stat-box"><p class="stat-number">{}</p><p class="stat-label">Total Ratings</p></div>'.format(len(ratings_df)), unsafe_allow_html=True)

    # Visualizations
    st.markdown('<h2 class="sub-header">📊 Data Insights</h2>', unsafe_allow_html=True)
    fig_top_rated, fig_rating_dist, fig_books_per_year, fig_publishers, fig_correlation = create_visualizations(books_df, ratings_df, df)
    
    st.plotly_chart(fig_top_rated, use_container_width=True)
    st.plotly_chart(fig_rating_dist, use_container_width=True)
    st.plotly_chart(fig_books_per_year, use_container_width=True)
    st.plotly_chart(fig_publishers, use_container_width=True)
    st.plotly_chart(fig_correlation, use_container_width=True)

    # Association Rules
    st.markdown('<h2 class="sub-header">🔗 Association Rules</h2>', unsafe_allow_html=True)
    formatted_rules = format_rules(rules)
    selected_rule, confidence = st.selectbox("Select a rule to see its confidence:", formatted_rules, format_func=lambda x: x[0])
    st.write(f"Confidence of the selected rule: {confidence:.2f}")

    # Book recommendation interface
    st.markdown('<h2 class="sub-header">🎯 Book Recommendations</h2>', unsafe_allow_html=True)
    
    selected_book = st.selectbox("Select a book for recommendations:", books_in_rules)

    if st.button("Get Recommendations"):
        recommendations = get_book_recommendations(selected_book, rules, df)
        if recommendations is not None:
            st.write("Recommended books:")
            cols = st.columns(5)
            for i, (_, row) in enumerate(recommendations.iterrows()):
                if i < 5:  # Display only top 5 recommendations
                    with cols[i]:
                        st.image(row['Image-URL-M'], use_column_width=True, caption=row['Book-Title'])
        else:
            st.warning("No recommendations found for this book.")
    
    # Sidebar
    st.sidebar.title("About")
    st.sidebar.info("This is an enhanced book recommendation system using the FP-Growth algorithm. It provides data insights and personalized book recommendations based on association rules, complete with book cover images.")

# Run the Streamlit app
if __name__ == "__main__":
    main()
