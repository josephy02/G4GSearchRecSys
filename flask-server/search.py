from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import pyterrier as pt
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Initialize index once
pt.java.set_java_home("C:\\Users\\Amrith\\.jdks\\temurin-11.0.16.1")
index_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "geek_index", "data.properties")
index = pt.IndexFactory.of(index_path)
bm_25 = pt.BatchRetrieve(index, wmodel="BM25")

@app.route("/search")
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

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == "__main__":
    app.run(debug=True)