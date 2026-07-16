# ==========================================================
# STEP 7 : K-MEANS CLUSTERING
# Customer Segmentation
# ==========================================================

import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

print("="*60)
print("K-MEANS CLUSTERING")
print("="*60)

# ----------------------------------------------------------
# Create folders
# ----------------------------------------------------------

os.makedirs("models", exist_ok=True)
os.makedirs("images", exist_ok=True)

# ----------------------------------------------------------
# Load Dataset
# ----------------------------------------------------------

df = pd.read_csv("data/processed_ecommerce.csv")

print("\nDataset Loaded Successfully")
print("Shape :", df.shape)

# ----------------------------------------------------------
# Features for Clustering
# ----------------------------------------------------------

cluster_features = [

    "pages_viewed",
    "time_on_site_sec",
    "quantity",
    "revenue",
    "rating",
    "added_to_cart"

]

X = df[cluster_features]

print("\nFeatures Used For Clustering")
print(cluster_features)

# ----------------------------------------------------------
# Elbow Method
# ----------------------------------------------------------

print("\nCalculating Elbow Method...")

inertia = []

for k in range(1,11):

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    model.fit(X)

    inertia.append(model.inertia_)

# ----------------------------------------------------------
# Plot Elbow Graph
# ----------------------------------------------------------

plt.figure(figsize=(8,5))

plt.plot(range(1,11), inertia, marker="o")

plt.title("Elbow Method")

plt.xlabel("Number of Clusters")

plt.ylabel("Inertia")

plt.grid(True)

plt.savefig("images/elbow_method.png")

plt.show()

print("\nElbow Graph Saved")

# ----------------------------------------------------------
# Train Final Model
# ----------------------------------------------------------

best_k = 4

kmeans = KMeans(

    n_clusters=best_k,

    random_state=42,

    n_init=10

)

clusters = kmeans.fit_predict(X)

df["Cluster"] = clusters

# ----------------------------------------------------------
# Silhouette Score
# ----------------------------------------------------------

score = silhouette_score(X, clusters)

print("\nSilhouette Score :", round(score,4))

# ----------------------------------------------------------
# Cluster Counts
# ----------------------------------------------------------

print("\nCluster Counts")

print(df["Cluster"].value_counts())

# ----------------------------------------------------------
# Cluster Summary
# ----------------------------------------------------------

print("\nCluster Summary")

print(df.groupby("Cluster")[cluster_features].mean())

# ----------------------------------------------------------
# Scatter Plot
# ----------------------------------------------------------

plt.figure(figsize=(8,6))

plt.scatter(

    df["pages_viewed"],

    df["revenue"],

    c=df["Cluster"]

)

plt.xlabel("Pages Viewed")

plt.ylabel("Revenue")

plt.title("Customer Segments")

plt.savefig("images/customer_clusters.png")

plt.show()

# ----------------------------------------------------------
# Save Model
# ----------------------------------------------------------

joblib.dump(kmeans, "models/kmeans_model.pkl")

print("\nModel Saved Successfully")

print("Location : models/kmeans_model.pkl")

# ----------------------------------------------------------
# Save Dataset
# ----------------------------------------------------------

df.to_csv(

    "data/customer_segments.csv",

    index=False

)

print("\nSegmented Dataset Saved")

print("Location : data/customer_segments.csv")

print("\nSTEP 7 COMPLETED SUCCESSFULLY")