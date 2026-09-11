from pathlib import Path
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# -----------------------------
# Load Original Dataset
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

original_df = pd.read_csv(BASE_DIR / "data" / "clean_customers.csv")

scaled_df = pd.read_csv(BASE_DIR / "data" / "scaled_customers.csv")

# -----------------------------
# Train K-Means Model
# -----------------------------

kmeans = KMeans(
    n_clusters=5,
    random_state=42,
    n_init=10
)

clusters = kmeans.fit_predict(scaled_df)

# -----------------------------
# Add Cluster Labels
# -----------------------------

original_df["Cluster"] = clusters

# -----------------------------
# Save Clustered Dataset
# -----------------------------

OUTPUT_PATH = BASE_DIR / "outputs" / "clustered_customers.csv"

original_df.to_csv(
    OUTPUT_PATH,
    index=False
)

print("✅ Customer Segmentation Completed!")

print("\nCluster Counts")

print(original_df["Cluster"].value_counts())

# -----------------------------
# Scatter Plot
# -----------------------------

plt.figure(figsize=(10,6))

plt.scatter(
    original_df["Annual_Income"],
    original_df["Spending_Score"],
    c=original_df["Cluster"],
    cmap="viridis",
    s=70
)

plt.title("Customer Segments")

plt.xlabel("Annual Income")

plt.ylabel("Spending Score")

plt.colorbar(label="Cluster")

plt.grid(True)

plt.show()