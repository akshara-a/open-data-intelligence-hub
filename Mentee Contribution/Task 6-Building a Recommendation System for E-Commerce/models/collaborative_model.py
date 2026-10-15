import pandas as pd
from surprise import Dataset, Reader, KNNBasic
import pickle
import os

# -----------------------------
# Load Ratings Dataset
# -----------------------------
# Expected columns:
# user_id, product_id, rating

ratings = pd.read_csv("data/ratings.csv")

print("Ratings Dataset Shape:", ratings.shape)
print(ratings.head())

# -----------------------------
# Prepare Surprise Dataset
# -----------------------------
reader = Reader(rating_scale=(1, 5))

data = Dataset.load_from_df(
    ratings[["user_id", "product_id", "rating"]],
    reader
)

trainset = data.build_full_trainset()

# -----------------------------
# Train KNN Model
# -----------------------------
sim_options = {
    "name": "cosine",
    "user_based": True
}

model = KNNBasic(sim_options=sim_options)

model.fit(trainset)

# -----------------------------
# Save Model
# -----------------------------
os.makedirs("models", exist_ok=True)

with open("models/collaborative_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("\nCollaborative model saved successfully!")