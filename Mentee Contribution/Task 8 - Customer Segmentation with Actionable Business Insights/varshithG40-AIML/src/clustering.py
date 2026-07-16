from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


def evaluate_kmeans(features: pd.DataFrame, k_range: list[int] | range | None = None) -> dict:
    if k_range is None:
        k_range = range(2, 8)

    inertia_values = []
    silhouette_values = []
    for k in k_range:
        model = KMeans(n_clusters=k, random_state=42, n_init=15)
        labels = model.fit_predict(features)
        inertia_values.append(model.inertia_)
        silhouette_values.append(silhouette_score(features, labels))

    return {"k_range": list(k_range), "inertia": inertia_values, "silhouette": silhouette_values}


def fit_kmeans(features: pd.DataFrame, n_clusters: int) -> tuple[KMeans, pd.Series]:
    model = KMeans(n_clusters=n_clusters, random_state=42, n_init=15)
    labels = model.fit_predict(features)
    return model, pd.Series(labels, name="Cluster", index=features.index)


def profile_clusters(df: pd.DataFrame, cluster_labels: pd.Series) -> pd.DataFrame:
    cluster_df = df.copy()
    cluster_df["Cluster"] = cluster_labels.astype(int)
    summary = (
        cluster_df.groupby("Cluster")
        .agg(
            CustomerCount=("CustomerID", "count"),
            AvgSpending=("TotalSpending", "mean"),
            AvgFrequency=("PurchaseFrequency", "mean"),
            AvgRecency=("DaysSinceLastPurchase", "mean"),
            AvgOrderValue=("AverageOrderValue", "mean"),
            AvgRating=("CustomerRating", "mean"),
            AvgDiscountUsage=("DiscountUsage", "mean"),
            RevenueContribution=("TotalSpending", "sum"),
        )
        .round(2)
    )
    summary["RevenueShare"] = (summary["RevenueContribution"] / summary["RevenueContribution"].sum() * 100).round(2)
    return summary


def assign_segment_names(summary: pd.DataFrame) -> pd.DataFrame:
    summary = summary.copy()
    labels = []
    for _, row in summary.iterrows():
        if row["AvgRecency"] < 50 and row["AvgFrequency"] > 6:
            labels.append("High-Value Loyal")
        elif row["AvgRecency"] < 80 and row["AvgFrequency"] > 3:
            labels.append("Promising Repeat Buyers")
        elif row["AvgDiscountUsage"] > 0.3:
            labels.append("Discount-Driven")
        elif row["AvgRecency"] > 140:
            labels.append("At-Risk Inactive")
        else:
            labels.append("Low-Engagement")
    summary["Segment"] = labels
    return summary


def reduce_dimensions(features: pd.DataFrame, n_components: int = 2) -> pd.DataFrame:
    pca = PCA(n_components=n_components, random_state=42)
    reduced = pca.fit_transform(features)
    return pd.DataFrame(reduced, columns=[f"PC{i+1}" for i in range(n_components)], index=features.index)
