from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans

# -----------------------------
# Load Scaled Dataset
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "scaled_customers.csv"

df = pd.read_csv(DATA_PATH)

# -----------------------------
# Elbow Method
# -----------------------------

wcss = []

for k in range(1, 11):

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    model.fit(df)

    wcss.append(model.inertia_)

# -----------------------------
# Plot
# -----------------------------

plt.figure(figsize=(8,5))

plt.plot(range(1,11), wcss, marker="o")

plt.title("Elbow Method")

plt.xlabel("Number of Clusters")

plt.ylabel("WCSS")

plt.grid(True)

plt.show()