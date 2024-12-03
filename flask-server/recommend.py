from flask import Flask, jsonify
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

@app.route("/recommend", methods=["GET"])
def recommend():
    # Load and prepare data
    articles = pd.read_csv(r'../data/geeksforgeeks_articles.csv', encoding='latin-1', nrows=10000)

    # Remove duplicates and reset index
    articles = articles.drop_duplicates(subset=['url', 'title']).reset_index(drop=True)

    # Store original titles and URLs after duplicate removal
    titles = articles['title'].values
    urls = articles['url'].values

    # Create TF-IDF vectorizer
    tfidf = TfidfVectorizer(stop_words='english')

    # Create TF-IDF matrix for titles
    title_tfidf_matrix = tfidf.fit_transform(titles)

    # Calculate similarity matrix
    similarity_matrix = cosine_similarity(title_tfidf_matrix)

    # Create DataFrame for similarity matrix with proper indices
    similarity_df = pd.DataFrame(
        similarity_matrix,
        index=titles,
        columns=titles
    )

    # Recommend articles based on title similarity using TF-IDF and cosine similarity
    def recommend_similar_articles(title, num_recommendations=5):
        """
        Recommend articles based on title similarity using TF-IDF and cosine similarity.

        Parameters:
        title (str): The title of the article to base recommendations on
        num_recommendations (int): Number of similar articles to recommend

        Returns:
        DataFrame: Recommended articles with similarity scores
        """
        # Check if title exists in the dataset
        if title not in titles:
            raise ValueError("Title not found in dataset")
        
        # Get similarities for the input title
        similarities = similarity_df.loc[title]
        
        # Get most similar articles (excluding the input article itself)
        similar_articles = similarities.sort_values(ascending=False)[1:num_recommendations+1]
        
        # Create recommendations dataframe
        recommendations = pd.DataFrame({
            'title': similar_articles.index,
            'similarity_score': similar_articles.values
        })
        
        # Add URLs to recommendations
        recommendations = recommendations.merge(
            articles[['title', 'url']],
            on='title',
            how='left'
        )
        
        return recommendations.sort_values('similarity_score', ascending=False).to_dict(orient="records")

    # Example usage - Get example recommendations
    example_title = titles[0]  # Get the first title as an example
    recommendations = recommend_similar_articles(example_title, num_recommendations=5)

    # Return recommendations as JSON response
    return jsonify({
        "message": "Recommendations based on your query.",
        "recommendations": recommendations
    })

if __name__ == "__main__":
    app.run(debug=True)
