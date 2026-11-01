"""K-Means clustering and cluster evaluation."""

import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


def evaluate_kmeans(X, k_values=range(2, 11), random_state=42):
    """Calculate inertia and silhouette scores for candidate cluster counts."""
    results = []

    for k in k_values:
        model = KMeans(n_clusters=k, n_init=20, random_state=random_state)
        labels = model.fit_predict(X)

        results.append({
            "k": k,
            "inertia": model.inertia_,
            "silhouette_score": silhouette_score(X, labels),
        })

    return results


def fit_kmeans(X, n_clusters: int, random_state=42):
    """Fit final K-Means model."""
    model = KMeans(
        n_clusters=n_clusters,
        n_init=20,
        max_iter=300,
        random_state=random_state,
    )
    labels = model.fit_predict(X)
    return model, labels


def profile_clusters(df, labels):
    """Create business-friendly numerical cluster profiles."""
    result = df.copy()
    result["Cluster"] = labels

    profile = (
        result.groupby("Cluster")
        .agg(
            Customers=("CustomerID", "count"),
            AvgSpending=("TotalSpending", "mean"),
            AvgPurchaseFrequency=("PurchaseFrequency", "mean"),
            AvgRecency=("DaysSinceLastPurchase", "mean"),
            AvgOrderValue=("AverageOrderValue", "mean"),
            AvgRating=("CustomerRating", "mean"),
            AvgDiscountUsage=("DiscountUsage", "mean"),
        )
        .reset_index()
    )

    total_revenue = result["TotalSpending"].sum()
    revenue_by_cluster = result.groupby("Cluster")["TotalSpending"].sum()

    profile["RevenueContributionPct"] = (
        profile["Cluster"].map(revenue_by_cluster) / total_revenue * 100
    )

    return result, profile
