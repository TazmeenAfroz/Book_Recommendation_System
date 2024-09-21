import pyfpgrowth

def run_fp_growth(transactions_with_titles):
    patterns = pyfpgrowth.find_frequent_patterns(transactions_with_titles, 100)
    rules = pyfpgrowth.generate_association_rules(patterns, 0.5)
    return patterns, rules

def get_books_in_rules(rules):
    books_in_rules = set()
    for rule_antecedent, _ in rules.items():
        books_in_rules.update(rule_antecedent)
    return books_in_rules

def get_book_recommendations(book_title, rules, df):
    recommendations = set()
    for rule_antecedent, rule_consequent in rules.items():
        if book_title in rule_antecedent:
            recommendations.update(rule_consequent[0])
    
    recommendations.discard(book_title)
    
    # Get book details including image URLs
    recommended_books = df[df['Book-Title'].isin(recommendations)].drop_duplicates('Book-Title')[['Book-Title', 'Image-URL-M']]
    return recommended_books if not recommended_books.empty else None

def format_rules(rules):
    formatted_rules = []
    for antecedent, (consequent, confidence) in rules.items():
        antecedent_str = ', '.join(antecedent)
        consequent_str = ', '.join(consequent)
        formatted_rules.append((f"If [{antecedent_str}], then [{consequent_str}]", confidence))
    return formatted_rules
