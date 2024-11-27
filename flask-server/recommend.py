from flask import Flask
import pandas as pd 
import pyterrier as pt 
import numpy as np
from scipy.sparse.linalg import svds
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
import operator

app = Flask(__name__)
@app.route("/recommend")

def recommend():
    #Change to your JDK path
    return "hello world"

if __name__ == "__main__":
    app.run(debug=True)