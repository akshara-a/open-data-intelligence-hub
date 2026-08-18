import os
import joblib
import numpy as np
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


def perform_kmeans_clustering(customer_df, X_scaled_df, min_k=2, max_k=6):
    """
    Perform K-Means clustering, evaluate using Inertia and Silhouette Score,
    choose the best K, fit the final model, and return results.
    """

    print("=" * 60)
    print("K-Means Customer Segmentation")
    print("=" * 60)

    inertias = []
    silhouette_scores = []
    k_range = list(range(min_k, max_k + 1))

    # -----------------------------
    # Evaluate Different K Values
    # -----------------------------
    print("\nEvaluating K values...\n")

    for k in k_range:

        kmeans = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10,
            algorithm="lloyd"
        )

        labels = kmeans.fit_predict(X_scaled_df)

        inertias.append(kmeans.inertia_)

        sil = silhouette_score(X_scaled_df, labels)
        silhouette_scores.append(sil)

        print(
            f"K = {k} | "
            f"Inertia = {kmeans.inertia_:.2f} | "
            f"Silhouette = {sil:.4f}"
        )

    # -----------------------------
    # Select Best K
    # -----------------------------
    best_index = np.argmax(silhouette_scores)
    best_k = k_range[best_index]

    print(f"\nBest K Selected: {best_k}")

    # -----------------------------
    # Train Final Model
    # -----------------------------
    final_kmeans = KMeans(
        n_clusters=best_k,
        random_state=42,
        n_init=10,
        algorithm="lloyd"
    )

    cluster_labels = final_kmeans.fit_predict(X_scaled_df)

    customer_df = customer_df.copy()
    customer_df["Cluster"] = cluster_labels

    # -----------------------------
    # Save Model
    # -----------------------------
    os.makedirs("outputs", exist_ok=True)

    joblib.dump(final_kmeans, "outputs/kmeans_model.pkl")
    customer_df.to_csv(
        "outputs/customer_segments.csv",
        index=False
    )

    print("\nModel saved successfully.")
    print("Customer segments saved successfully.")

    # -----------------------------
    # Cluster Profiles
    # -----------------------------
    features = [
        "Number_of_Products_Viewed",
        "Number_of_Purchases",
        "Average_Rating_Given",
        "Average_Time_Spent",
        "Total_Amount_Spent",
        "Number_of_Products_Added_to_Cart"
    ]

    cluster_profiles = (
        customer_df
        .groupby("Cluster")[features]
        .mean()
        .reset_index()
    )

    cluster_sizes = (
        customer_df["Cluster"]
        .value_counts()
        .rename_axis("Cluster")
        .reset_index(name="Size")
    )

    cluster_profiles = cluster_profiles.merge(
        cluster_sizes,
        on="Cluster"
    )

    print("\nCluster Profiles")
    print("-" * 60)
    print(cluster_profiles)

    # -----------------------------
    # Assign Business Labels
    # -----------------------------
    labels = {}

    spend_rank = (
        cluster_profiles
        .sort_values("Total_Amount_Spent", ascending=False)
        ["Cluster"]
        .tolist()
    )

    views_rank = (
        cluster_profiles
        .sort_values("Number_of_Products_Viewed", ascending=False)
        ["Cluster"]
        .tolist()
    )

    cart_rank = (
        cluster_profiles
        .sort_values(
            "Number_of_Products_Added_to_Cart",
            ascending=False
        )["Cluster"]
        .tolist()
    )

    for c in range(best_k):

        if c == spend_rank[0]:
            labels[c] = "High-Value Loyalists"

        elif c == views_rank[0] and c not in labels:
            labels[c] = "Active Window Shoppers"

        elif c == spend_rank[-1]:
            labels[c] = "Occasional / Low-Value Buyers"

        elif c == cart_rank[0] and c not in labels:
            labels[c] = "Cart Enthusiasts"

        else:
            labels[c] = f"Regular Customers (Segment {c})"

    customer_df["Segment_Name"] = customer_df["Cluster"].map(labels)
    cluster_profiles["Segment_Name"] = cluster_profiles["Cluster"].map(labels)

    print("\nBusiness Segments")
    print("-" * 60)

    print(
        cluster_profiles[
            ["Cluster", "Segment_Name", "Size"]
        ]
    )

    # -----------------------------
    # Results
    # -----------------------------
    results = {
        "k_range": k_range,
        "inertias": inertias,
        "silhouette_scores": silhouette_scores,
        "best_k": best_k,
        "best_inertia": inertias[best_index],
        "best_silhouette": silhouette_scores[best_index],
        "profiles": cluster_profiles,
        "customer_data": customer_df
    }

    return final_kmeans, results