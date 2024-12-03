from flask import Flask, request,jsonify
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask_cors import CORS
import pyterrier as pt
import os
from dotenv import load_dotenv

#Load environment variables
load_dotenv()

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": ["http://localhost:3000", "http://172.22.144.1:3000"]}})

#Set  JDK_PATH to in your environment variables
pt.java.set_java_home(os.getenv("JDK_PATH"))
index_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "geek_index", "data.properties")
index = pt.IndexFactory.of(index_path)
bm_25 = pt.BatchRetrieve(index, wmodel="BM25")
@app.route("/search", methods=["GET"])
def search():
    try:
        query_text = request.args.get('query', '')
        if not query_text:
            return jsonify({"error": "Query parameter is required"}), 400

        query = pd.DataFrame([["q1", query_text]], columns=["qid", "query"])
        
        results = bm_25.transform(query)

        search_results = []
        for i in range(min(10, len(results))):
            filename = index.getMetaIndex().getItem("filename", results.docid[i])
            title = index.getMetaIndex().getItem("title", results.docid[i]).strip()
            if not title:
                title = filename

            url = f"https://{filename.replace('./', '')}"
            search_results.append({"url": url, "title": title})

        return jsonify({"results": search_results})
    
    except Exception as e:
        print(f"Error processing search request: {str(e)}")  # Server-side logging
        return jsonify({"error": "Internal server error"}), 500


@app.route("/recommend", methods=["GET"])
def recommend():
    # Load and prepare data
    articles = pd.read_csv(r'C:\Users\Amrith\Documents\info376\G4GSearchRecSys\data\geeksforgeeks_articles.csv', encoding='latin-1', nrows=10000)

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