"""
Clustering utilities: model selection (elbow + silhouette) and
final K-Means fitting for customer segmentation.
"""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA


def evaluate_k_range(X, k_range=range(2, 11), random_state=42):
    """Return inertia and silhouette score for each k in k_range."""
    results = []
    for k in k_range:
        km = KMeans(n_clusters=k, init="k-means++", n_init=10, random_state=random_state)
        labels = km.fit_predict(X)
        sil = silhouette_score(X, labels)
        results.append({"k": k, "inertia": km.inertia_, "silhouette": sil})
    return pd.DataFrame(results)


def fit_kmeans(X, n_clusters, random_state=42, **kwargs):
    km = KMeans(n_clusters=n_clusters, init="k-means++", n_init=10,
                random_state=random_state, **kwargs)
    labels = km.fit_predict(X)
    return km, labels


def project_2d(X):
    pca = PCA(n_components=2, random_state=42)
    coords = pca.fit_transform(X)
    return coords, pca


def profile_clusters(df, labels, feature_cols, revenue_col="TotalSpending"):
    """Build a per-cluster summary table: size, feature means, and
    percentage contribution to total revenue."""
    df = df.copy()
    df["Cluster"] = labels

    agg = df.groupby("Cluster")[feature_cols].mean().round(2)
    agg["CustomerCount"] = df.groupby("Cluster").size()
    agg["PctOfCustomers"] = (agg["CustomerCount"] / len(df) * 100).round(1)

    total_revenue = df[revenue_col].sum()
    revenue_by_cluster = df.groupby("Cluster")[revenue_col].sum()
    agg["RevenueContributionPct"] = (revenue_by_cluster / total_revenue * 100).round(1)

    return agg.reset_index()
