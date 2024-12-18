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

CORS(app, resources={r"/*": {"origins": ["https://mdvmvbnt-3000.usw2.devtunnels.ms", "http://172.22.144.1:3000"]}})

#Set JDK_PATH to in your environment variables
pt.java.set_java_home(os.getenv("JDK_PATH"))
index_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "geek_index", "data.properties")
index = pt.IndexFactory.of(index_path)
bm_25 = pt.BatchRetrieve(index, wmodel="BM25")

BASE_URL = "https://www.geeksforgeeks.org"  # Base URL

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

            # Improved URL generation
            try:
                # Remove './geek/' prefix and '.html' suffix
                # Handle potential nested directories or index files
                relative_path = filename.replace('./geek/', '').replace('index.html', '').rstrip('.html')
                
                # Ensure clean URL by removing any trailing slashes
                relative_path = relative_path.rstrip('/')
                
                url = f"{BASE_URL}/{relative_path}/"
            except Exception as e:
                print(f"Error generating URL for filename {filename}: {e}")
                url = BASE_URL  # Fallback to base URL if generation fails

            search_results.append({"url": url, "title": url})

        return jsonify({"results": search_results})
    
    except Exception as e:
        print(f"Error processing search request: {str(e)}")  # Server-side logging
        return jsonify({"error": "Internal server error"}), 500


@app.route("/recommend", methods=["GET"])
def recommend():
    # Load and prepare data
    articles = pd.read_csv(os.getenv("DATA"), encoding='latin-1', nrows=10000)

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

    # Get URL from request
    input_url = request.args.get('clicked_url', '')

    # Recommend articles based on URL similarity using TF-IDF and cosine similarity
    def recommend_similar_articles(input_url, num_recommendations=5):
        """
        Recommend articles based on URL similarity using TF-IDF and cosine similarity.

        Parameters:
        input_url (str): The URL of the article to base recommendations on
        num_recommendations (int): Number of similar articles to recommend

        Returns:
        List of recommended articles with similarity scores
        """
        # Find the title corresponding to the input URL
        matching_rows = articles[articles['url'] == input_url]
        
        if matching_rows.empty:
            return []
        
        # Get the title of the input URL
        input_title = matching_rows.iloc[0]['title']
        
        # Check if title exists in the dataset
        if input_title not in titles:
            return []
        
        # Get similarities for the input title
        similarities = similarity_df.loc[input_title]
        
        # Get most similar articles (excluding the input article itself)
        similar_articles = similarities.sort_values(ascending=False)[1:num_recommendations+1]
        
        # Create recommendations list
        recommendations = []
        for title, similarity_score in similar_articles.items():
            # Find the URL for this title
            article_url = articles[articles['title'] == title]['url'].values[0]
            recommendations.append({
                'title': title,
                'url': article_url,
                'similarity_score': float(similarity_score)
            })
        
        return recommendations

    # Get recommendations based on the input URL
    recommendations = recommend_similar_articles(input_url, num_recommendations=5)

    # Return recommendations as JSON response
    return jsonify({
        "message": "Recommendations based on your selected article.",
        "recommendations": recommendations
    })

if __name__ == "__main__":
    app.run(debug=True)