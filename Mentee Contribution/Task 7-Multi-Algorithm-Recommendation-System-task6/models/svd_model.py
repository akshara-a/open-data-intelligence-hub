from pathlib import Path
import pandas as pd

from surprise import Dataset
from surprise import Reader
from surprise import SVD

# --------------------------
# Load Dataset
# --------------------------

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

# --------------------------
# Train SVD Model
# --------------------------

model = SVD()

model.fit(trainset)

# --------------------------
# Recommendation Function
# --------------------------

def recommend_products(username, top_n=5):

    products = ratings["product_name"].unique()

    predictions = []

    for product in products:

        prediction = model.predict(username, product)

        predictions.append(
            (product, prediction.est)
        )

    predictions.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return predictions[:top_n]

# --------------------------
# Test
# --------------------------

if __name__ == "__main__":

    sample_user = ratings["user"].iloc[0]

    print(f"\nRecommendations for: {sample_user}\n")

    recommendations = recommend_products(sample_user)

    for product, score in recommendations:
        print(f"{product} ---> Predicted Rating: {score:.2f}")