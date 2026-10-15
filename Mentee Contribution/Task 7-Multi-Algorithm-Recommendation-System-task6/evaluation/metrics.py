import time
import pandas as pd
from pathlib import Path

from surprise import Dataset
from surprise import Reader
from surprise import SVD, KNNBasic
from surprise.model_selection import train_test_split
from surprise.accuracy import rmse, mae

# -----------------------
# Load Dataset
# -----------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "clean_amazon.csv"

df = pd.read_csv(DATA_PATH)

ratings = df[["user", "product_name", "rating"]].dropna()

reader = Reader(rating_scale=(1, 5))

data = Dataset.load_from_df(
    ratings[["user", "product_name", "rating"]],
    reader
)

trainset, testset = train_test_split(data, test_size=0.2, random_state=42)

results = []

# -----------------------
# SVD
# -----------------------

start = time.time()

svd = SVD()

svd.fit(trainset)

predictions = svd.test(testset)

svd_time = time.time() - start

results.append(
    {
        "Algorithm": "SVD",
        "RMSE": rmse(predictions, verbose=False),
        "MAE": mae(predictions, verbose=False),
        "Time (s)": round(svd_time, 3)
    }
)

# -----------------------
# User KNN
# -----------------------

start = time.time()

user_knn = KNNBasic(
    sim_options={
        "name": "cosine",
        "user_based": True
    }
)

user_knn.fit(trainset)

predictions = user_knn.test(testset)

knn_user_time = time.time() - start

results.append(
    {
        "Algorithm": "User-KNN",
        "RMSE": rmse(predictions, verbose=False),
        "MAE": mae(predictions, verbose=False),
        "Time (s)": round(knn_user_time, 3)
    }
)

# -----------------------
# Item KNN
# -----------------------

start = time.time()

item_knn = KNNBasic(
    sim_options={
        "name": "cosine",
        "user_based": False
    }
)

item_knn.fit(trainset)

predictions = item_knn.test(testset)

knn_item_time = time.time() - start

results.append(
    {
        "Algorithm": "Item-KNN",
        "RMSE": rmse(predictions, verbose=False),
        "MAE": mae(predictions, verbose=False),
        "Time (s)": round(knn_item_time, 3)
    }
)

# -----------------------
# Save Results
# -----------------------

results_df = pd.DataFrame(results)

print(results_df)

results_df.to_csv(
    BASE_DIR / "evaluation" / "results.csv",
    index=False
)

print("\n✅ Results saved to evaluation/results.csv")