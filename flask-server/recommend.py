from flask import Flask
import pandas as pd
import pyterrier as pt
import numpy as np
from scipy.sparse.linalg import svds
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
import operator
from scipy.sparse.linalg import svds


app = Flask(__name__)
@app.route("/recommend")



def recommend():
# -*- coding: utf-8 -*-
#load in data
    articles = pd.read_csv('/content/drive/MyDrive/Data/geekstest1.csv', encoding='latin-1')
    articles.head(5)

    # Check for duplicates in the index columns
    duplicates = articles.duplicated(subset=['url', 'title'], keep=False)
    if duplicates.any():
        articles = articles.groupby(['url', 'title'])['rating'].mean().reset_index()


    # Now, the pivot operation should work without errors
    u_t = articles.pivot(index='url', columns='title', values='rating').fillna(0)

    u_t.shape

    u_t.head(5)

    # Step-3: normalize ratings.
    data = u_t.values
    ratings_mean = np.mean(data,axis=1)
    normalizedRating = data - ratings_mean.reshape(-1,1)

    normalizedRating



    # Step-4: SVD (matrix factorization)
    U, sigma, Vt = svds(normalizedRating, k=100)

    # Step-5: get the diagonal entries of sigma (singular values)
    sigma = np.diag(sigma)

    # Step-6: reshape and renormalize ratings using weighted/important components/factors
    all_user_ratings = np.dot(np.dot(U,sigma), Vt) + ratings_mean.reshape(-1,1)

    # Step-7: construct a dataframe with all these user-movie ratings predictions.
    preds = pd.DataFrame(all_user_ratings, columns=u_t.columns)

    # Recommend articles for a user based on predicted ratings.
    def recommend_articles(predictions_df, user_id, articles_df, original_ratings_df, num_recs):

        # Get and sort the user's predictions
        user_row_number = user_id - 1  # user_id starts at 1, not 0
        sorted_user_predictions = predictions_df.iloc[user_row_number].sort_values(ascending=False)

        # Get the user's data and merge in article information
        user_data = original_ratings_df[original_ratings_df['user_id'] == user_id]  # Rows with user info
        user_full = user_data.merge(
            articles_df,
            how='left',
            left_on='url',  # Assuming URL links ratings to articles
            right_on='url'
        ).sort_values(['rating'], ascending=False)

        print('User {0} has already rated {1} articles.'.format(user_id, user_full.shape[0]))
        print('Recommending highest {0} predicted ratings articles not already rated.'.format(num_recs))

        # Recommend the highest predicted rating articles that the user hasn't seen yet
        recommendations = (
            articles_df[~articles_df['url'].isin(user_full['url'])]
            .merge(
                pd.DataFrame(sorted_user_predictions).reset_index(),
                how='left',
                left_on='title',  # Matching titles for predictions
                right_on='title'
            )
            .rename(columns={user_row_number: 'Predictions'})
            .sort_values('Predictions', ascending=False)
            .iloc[:num_recs, :]
        )

        return user_full, recommendations

    # What we want to do
    already_rated, recommendations = recommend_articles(preds,1,articles,ratings,10)

    already_rated.head(5)
    recommendations.head(5)

if __name__ == "__main__":
    app.run(debug=True)
