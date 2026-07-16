"""
Clustering Model Module — Part C
==================================
Implements K-Means Clustering to segment customers based on
their aggregated shopping behavior.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples
from sklearn.decomposition import PCA
import os
import warnings
warnings.filterwarnings("ignore")


def find_optimal_k(X_scaled, k_range=range(2, 11)):
    """
    Find the optimal number of clusters using Elbow Method and Silhouette Analysis.

    Returns
    -------
    dict
        Dictionary containing inertias and silhouette scores for each k.
    """
    results = {"k": [], "inertia": [], "silhouette": []}

    for k in k_range:
        kmeans = KMeans(n_clusters=k, init="k-means++", n_init=10,
                        max_iter=300, random_state=42)
        labels = kmeans.fit_predict(X_scaled)
        results["k"].append(k)
        results["inertia"].append(kmeans.inertia_)
        results["silhouette"].append(silhouette_score(X_scaled, labels))

    return results


def train_kmeans(X_scaled, n_clusters=4, random_state=42):
    """Train a K-Means model with the specified number of clusters."""
    model = KMeans(n_clusters=n_clusters, init="k-means++", n_init=10,
                   max_iter=300, random_state=random_state)
    labels = model.fit_predict(X_scaled)

    metrics = {
        "Inertia": model.inertia_,
        "Silhouette_Score": silhouette_score(X_scaled, labels),
        "n_clusters": n_clusters,
    }

    return model, labels, metrics


def profile_clusters(customer_df, labels, feature_names):
    """
    Create a profile summary for each cluster.

    Returns
    -------
    pd.DataFrame
        Cluster profiles with mean feature values.
    """
    df = customer_df.copy()
    df["Cluster"] = labels

    profiles = df.groupby("Cluster")[feature_names].mean().round(2)

    # Add cluster sizes
    sizes = df["Cluster"].value_counts().sort_index()
    profiles["Size"] = sizes.values
    profiles["Size_Pct"] = (sizes.values / len(df) * 100).round(1)

    return profiles


def plot_clustering_results(X_scaled, labels, customer_df, feature_names,
                             k_results, metrics, output_dir="outputs/plots"):
    """Generate and save clustering evaluation plots."""
    os.makedirs(output_dir, exist_ok=True)

    # --- 1. Elbow Method ---
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(k_results["k"], k_results["inertia"], "bo-", linewidth=2, markersize=8)
    ax1.set_xlabel("Number of Clusters (K)", fontsize=12)
    ax1.set_ylabel("Inertia", fontsize=12, color="#4C72B0")
    ax1.tick_params(axis="y", labelcolor="#4C72B0")
    ax1.set_title("Elbow Method & Silhouette Score", fontsize=14, fontweight="bold")

    ax2 = ax1.twinx()
    ax2.plot(k_results["k"], k_results["silhouette"], "rs-", linewidth=2, markersize=8)
    ax2.set_ylabel("Silhouette Score", fontsize=12, color="#C44E52")
    ax2.tick_params(axis="y", labelcolor="#C44E52")

    # Mark optimal k
    best_k_idx = np.argmax(k_results["silhouette"])
    best_k = k_results["k"][best_k_idx]
    ax2.axvline(best_k, color="green", linestyle="--", linewidth=1.5, alpha=0.7,
                label=f"Best K = {best_k}")
    ax2.legend(fontsize=11, loc="center right")

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "clustering_elbow_silhouette.png"), dpi=150)
    plt.close()

    # --- 2. PCA 2D Cluster Visualization ---
    fig, ax = plt.subplots(figsize=(10, 8))
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    scatter = ax.scatter(X_pca[:, 0], X_pca[:, 1], c=labels, cmap="tab10",
                          alpha=0.8, s=120, edgecolors="white", linewidth=0.5)
    ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)", fontsize=13)
    ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)", fontsize=13)
    ax.set_title("Customer Segments — PCA Visualization", fontsize=15, fontweight="bold")

    # Add cluster centers
    centers_pca = pca.transform(
        KMeans(n_clusters=len(set(labels)), init="k-means++", n_init=10,
               random_state=42).fit(X_scaled).cluster_centers_
    )
    ax.scatter(centers_pca[:, 0], centers_pca[:, 1], c="black", marker="X",
               s=250, linewidths=2.5, edgecolors="white", zorder=5)

    legend = ax.legend(*scatter.legend_elements(), title="Cluster", fontsize=11,
                        title_fontsize=12)
    ax.add_artist(legend)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "clustering_pca.png"), dpi=200)
    plt.close()

    # --- 3. Cluster Profile Radar/Bar Chart ---
    profiles = profile_clusters(customer_df, labels, feature_names)

    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    axes = axes.flatten()
    colors = sns.color_palette("Set2", len(profiles))

    for idx, feature in enumerate(feature_names):
        ax = axes[idx]
        bars = ax.bar(
            [f"Cluster {i}" for i in profiles.index],
            profiles[feature],
            color=colors,
            edgecolor="white",
        )
        ax.set_title(feature.replace("_", " "), fontsize=12, fontweight="bold")
        ax.set_ylabel("Mean Value", fontsize=10)
        for bar, val in zip(bars, profiles[feature]):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                    f"{val:.1f}", ha="center", va="bottom", fontsize=9)

    plt.suptitle("Cluster Profiles — Feature Comparison", fontsize=15, fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "clustering_profiles.png"), dpi=150)
    plt.close()

    # --- 4. Cluster Size Distribution ---
    fig, ax = plt.subplots(figsize=(8, 6))
    cluster_sizes = pd.Series(labels).value_counts().sort_index()
    bars = ax.bar(
        [f"Cluster {i}" for i in cluster_sizes.index],
        cluster_sizes.values,
        color=colors[:len(cluster_sizes)],
        edgecolor="white",
    )
    for bar, val in zip(bars, cluster_sizes.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2,
                f"{val} ({val/len(labels):.1%})", ha="center", fontsize=11, fontweight="bold")
    ax.set_xlabel("Cluster", fontsize=12)
    ax.set_ylabel("Number of Customers", fontsize=12)
    ax.set_title("Customer Segment Sizes", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "clustering_sizes.png"), dpi=150)
    plt.close()

    print("[Clustering] Saved: clustering_elbow_silhouette.png")
    print("[Clustering] Saved: clustering_pca.png")
    print("[Clustering] Saved: clustering_profiles.png")
    print("[Clustering] Saved: clustering_sizes.png")


def run_clustering(clust_data, output_dir="outputs/plots"):
    """
    Run the complete clustering pipeline.

    Parameters
    ----------
    clust_data : dict
        Preprocessed clustering data from data_preprocessing.
    output_dir : str
        Directory to save plots.

    Returns
    -------
    dict
        Dictionary containing model, labels, metrics, and profiles.
    """
    print("\n" + "=" * 60)
    print("PART C: CLUSTERING — CUSTOMER SEGMENTATION")
    print("=" * 60)

    customer_df = clust_data["customer_df"]
    X_scaled = clust_data["X_scaled"]
    feature_names = clust_data["feature_names"]

    # Find optimal K
    print("\n--- Finding Optimal Number of Clusters ---")
    k_results = find_optimal_k(X_scaled)
    for i, k in enumerate(k_results["k"]):
        print(f"  K={k}: Inertia={k_results['inertia'][i]:.1f}, "
              f"Silhouette={k_results['silhouette'][i]:.4f}")

    best_k = k_results["k"][np.argmax(k_results["silhouette"])]
    print(f"\n  -> Best K by Silhouette Score: {best_k}")

    # Train with optimal K (use 4 as default for business interpretability)
    n_clusters = 4
    print(f"\n--- Training K-Means with K={n_clusters} ---")
    model, labels, metrics = train_kmeans(X_scaled, n_clusters=n_clusters)

    print(f"  Inertia: {metrics['Inertia']:.2f}")
    print(f"  Silhouette Score: {metrics['Silhouette_Score']:.4f}")

    # Cluster profiles
    profiles = profile_clusters(customer_df, labels, feature_names)
    print("\n--- Cluster Profiles ---")
    print(profiles.to_string())

    # Business interpretation
    print("\n--- Segment Interpretation ---")
    for cluster_id in range(n_clusters):
        profile = profiles.loc[cluster_id]
        print(f"\n  Cluster {cluster_id} ({profile['Size']:.0f} customers, {profile['Size_Pct']:.1f}%):")

        # Simple heuristic-based interpretation
        if profile["Total_Spending"] > profiles["Total_Spending"].median():
            if profile["Previous_Purchases"] > profiles["Previous_Purchases"].median():
                print("    -> High-value frequent buyers")
            else:
                print("    -> High-spending occasional buyers")
        else:
            if profile["Browsing_Time"] > profiles["Browsing_Time"].median():
                print("    -> Active browsers with low purchases")
            else:
                if profile["Discount_Usage"] > profiles["Discount_Usage"].median():
                    print("    -> Discount-sensitive customers")
                else:
                    print("    -> Casual/low-engagement customers")

    # Plot results
    plot_clustering_results(
        X_scaled, labels, customer_df, feature_names,
        k_results, metrics, output_dir
    )

    return {
        "model": model,
        "labels": labels,
        "metrics": metrics,
        "profiles": profiles,
        "k_results": k_results,
    }


if __name__ == "__main__":
    from data_preprocessing import preprocess_all
    data = preprocess_all("data/ecommerce_data.csv")
    run_clustering(data["clustering"])
