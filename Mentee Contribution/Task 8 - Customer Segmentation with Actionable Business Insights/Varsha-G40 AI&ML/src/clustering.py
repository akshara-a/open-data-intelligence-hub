# ==========================================
# Customer Segmentation using K-Means
# ==========================================

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

# ------------------------------------------
# Load Dataset
# ------------------------------------------

df = pd.read_csv("data/rfm_features.csv")

print("=" * 60)
print("CUSTOMER SEGMENTATION")
print("=" * 60)

print("\nDataset Shape:")
print(df.shape)

# ------------------------------------------
# Select Features
# ------------------------------------------

cluster_features = df[
    [
        "R",
        "F",
        "M",
        "Income",
        "Age"
    ]
]

# ------------------------------------------
# Scale Features
# ------------------------------------------

scaler = StandardScaler()

scaled_features = scaler.fit_transform(cluster_features)

print("\nFeature Scaling Completed")

# ------------------------------------------
# Elbow Method
# ------------------------------------------

inertia = []

for k in range(1,11):

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    model.fit(scaled_features)

    inertia.append(model.inertia_)

plt.figure(figsize=(8,5))

plt.plot(range(1,11), inertia, marker="o")

plt.title("Elbow Method")

plt.xlabel("Number of Clusters")

plt.ylabel("Inertia")

plt.grid(True)

plt.show()

# ------------------------------------------
# Silhouette Score
# ------------------------------------------

print("\nSilhouette Scores")

scores = []

for k in range(2,11):

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    labels = model.fit_predict(scaled_features)

    score = silhouette_score(
        scaled_features,
        labels
    )

    scores.append(score)

    print(f"k={k}  Score={score:.3f}")

# ------------------------------------------
# Final Model
# ------------------------------------------

kmeans = KMeans(
    n_clusters=5,
    random_state=42,
    n_init=10
)

df["Cluster"] = kmeans.fit_predict(scaled_features)

print("\nCluster Labels Added")

print(df["Cluster"].value_counts())

# ------------------------------------------
# PCA Visualization
# ------------------------------------------

pca = PCA(n_components=2)

pca_data = pca.fit_transform(scaled_features)

plt.figure(figsize=(8,6))

plt.scatter(
    pca_data[:,0],
    pca_data[:,1],
    c=df["Cluster"]
)

plt.title("Customer Segments")

plt.xlabel("PCA Component 1")

plt.ylabel("PCA Component 2")

plt.show()

# ------------------------------------------
# Save Customer Segments
# ------------------------------------------

df.to_csv(
    "reports/customer_segments.csv",
    index=False
)

print("\nCustomer Segments Saved Successfully!")