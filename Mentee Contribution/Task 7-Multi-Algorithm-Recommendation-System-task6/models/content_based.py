from pathlib import Path
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------
# Load Dataset
# -----------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "clean_amazon.csv"

df = pd.read_csv(DATA_PATH)

# Remove duplicates (one row per product)
products = df[["product_id", "product_name", "brand", "category"]].drop_duplicates()

# Fill missing values
products = products.fillna("")

# Combine text features
products["features"] = (
    products["product_name"] + " " +
    products["brand"] + " " +
    products["category"]
)

# -----------------------
# TF-IDF
# -----------------------

tfidf = TfidfVectorizer(stop_words="english")

tfidf_matrix = tfidf.fit_transform(products["features"])

# -----------------------
# Cosine Similarity
# -----------------------

similarity = cosine_similarity(tfidf_matrix)

# -----------------------
# Recommendation Function
# -----------------------

def recommend(product_name, top_n=5):

    # Check whether product exists
    matches = products[
        products["product_name"].str.lower() == product_name.lower()
    ]

    if matches.empty:
        print("Product not found!")
        return

    idx = matches.index[0]

    scores = list(enumerate(similarity[idx]))

    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    scores = scores[1:top_n+1]

    recommendations = products.iloc[[i[0] for i in scores]]

    return recommendations[["product_name", "brand", "category"]]


# -----------------------
# Test
# -----------------------

if __name__ == "__main__":

    sample_product = products.iloc[0]["product_name"]

    print("Selected Product:\n")
    print(sample_product)

    print("\nRecommended Products:\n")

    print(recommend(sample_product))