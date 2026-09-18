from pathlib import Path
import pandas as pd

from surprise import Dataset
from surprise import Reader
from surprise import KNNBasic

# -----------------------------
# Load Dataset
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "clean_amazon.csv"

df = pd.read_csv(DATA_PATH)

ratings = df[["user", "product_name", "rating"]].dropna()

reader = Reader(rating_scale=(1, 5))

data = Dataset.load_from_df(
    ratings[["user", "product_name", "rating"]],
    reader
)

trainset = data.build_full_trainset()

# -----------------------------
# Item-Based KNN Model
# -----------------------------

sim_options = {
    "name": "cosine",
    "user_based": False  # Item-based similarity
}

model = KNNBasic(sim_options=sim_options)

model.fit(trainset)

# -----------------------------
# Recommendation Function
# -----------------------------

def recommend_products(username, top_n=5):

    products = ratings["product_name"].unique()

    predictions = []

    for product in products:

        pred = model.predict(username, product)

        predictions.append((product, pred.est))

    predictions.sort(key=lambda x: x[1], reverse=True)

    return predictions[:top_n]

# -----------------------------
# Test
# -----------------------------

if __name__ == "__main__":

    sample_user = ratings["user"].iloc[0]

    print(f"\nRecommendations for: {sample_user}\n")

    recommendations = recommend_products(sample_user)

    for product, score in recommendations:
        print(f"{product} ---> Predicted Rating: {score:.2f}")