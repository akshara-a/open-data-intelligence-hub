"""
Clustering Module
==================
Implements K-Means clustering for customer segmentation.
Includes Elbow Method, Silhouette Score analysis, PCA visualization,
and segment profiling.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
import os


def select_clustering_features(df):
    """
    Select and return the features used for clustering (RFM-based approach).
    Features: DaysSinceLastPurchase (Recency), PurchaseFrequency (Frequency),
              TotalSpending (Monetary), AverageOrderValue, WebsiteVisits, DiscountUsage
    """
    feature_cols = ['DaysSinceLastPurchase', 'PurchaseFrequency', 'TotalSpending',
                    'AverageOrderValue', 'WebsiteVisits', 'DiscountUsage', 'CustomerRating']
    feature_cols = [c for c in feature_cols if c in df.columns]
    print(f"Clustering features selected: {feature_cols}")
    return feature_cols


def scale_clustering_features(df, feature_cols):
    """Scale the clustering features using StandardScaler."""
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[feature_cols])
    print(f"Scaled {len(feature_cols)} features for clustering")
    return X_scaled, scaler


def elbow_method(X_scaled, k_range=range(2, 11), save_path=None):
    """
    Run the Elbow Method to determine the optimal number of clusters.
    """
    inertias = []
    for k in k_range:
        kmeans = KMeans(n_clusters=k, init='k-means++', n_init=10,
                        max_iter=300, random_state=42)
        kmeans.fit(X_scaled)
        inertias.append(kmeans.inertia_)
        print(f"  K={k}: Inertia = {kmeans.inertia_:,.2f}")

    if save_path:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(list(k_range), inertias, 'bo-', linewidth=2, markersize=8)
        ax.set_title('Elbow Method - Optimal Number of Clusters', fontweight='bold')
        ax.set_xlabel('Number of Clusters (K)')
        ax.set_ylabel('Inertia (Within-Cluster Sum of Squares)')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        print(f"Saved: {save_path}")

    return inertias


def silhouette_analysis(X_scaled, k_range=range(2, 11), save_path=None):
    """
    Compute silhouette scores for different values of K.
    Returns the optimal K (highest silhouette score).
    """
    scores = []
    for k in k_range:
        kmeans = KMeans(n_clusters=k, init='k-means++', n_init=10,
                        max_iter=300, random_state=42)
        labels = kmeans.fit_predict(X_scaled)
        score = silhouette_score(X_scaled, labels)
        scores.append(score)
        print(f"  K={k}: Silhouette Score = {score:.4f}")

    optimal_k = list(k_range)[np.argmax(scores)]
    best_score = max(scores)
    print(f"\n  Optimal K = {optimal_k} (Silhouette Score = {best_score:.4f})")

    if save_path:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(list(k_range), scores, 'rs-', linewidth=2, markersize=8)
        ax.axvline(x=optimal_k, color='green', linestyle='--', linewidth=1.5,
                   label=f'Optimal K = {optimal_k}')
        ax.set_title('Silhouette Score Analysis', fontweight='bold')
        ax.set_xlabel('Number of Clusters (K)')
        ax.set_ylabel('Silhouette Score')
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        print(f"Saved: {save_path}")

    return optimal_k, scores


def fit_kmeans(X_scaled, n_clusters, random_state=42):
    """Fit the final K-Means model with the optimal number of clusters."""
    kmeans = KMeans(n_clusters=n_clusters, init='k-means++', n_init=10,
                    max_iter=300, random_state=random_state)
    labels = kmeans.fit_predict(X_scaled)
    final_score = silhouette_score(X_scaled, labels)
    print(f"\nFinal K-Means: K={n_clusters}, Silhouette Score={final_score:.4f}")
    return kmeans, labels


def plot_clusters_pca(X_scaled, labels, n_clusters, save_path=None):
    """Visualize clusters using PCA (2D projection)."""
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    fig, ax = plt.subplots(figsize=(10, 8))
    colors = ['#2196F3', '#4CAF50', '#FF9800', '#E91E63', '#9C27B0',
              '#00BCD4', '#FF5722', '#607D8B']
    for i in range(n_clusters):
        mask = labels == i
        ax.scatter(X_pca[mask, 0], X_pca[mask, 1],
                   c=colors[i % len(colors)], label=f'Cluster {i}',
                   alpha=0.6, s=50, edgecolors='w', linewidth=0.5)

    ax.set_title('Customer Clusters - PCA Visualization', fontweight='bold')
    ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0] * 100:.1f}% variance)')
    ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1] * 100:.1f}% variance)')
    ax.legend(title='Cluster')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved: {save_path}")
    plt.close(fig)


def plot_cluster_counts(labels, save_path=None):
    """Plot the number of customers in each cluster."""
    unique, counts = np.unique(labels, return_counts=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['#2196F3', '#4CAF50', '#FF9800', '#E91E63', '#9C27B0',
              '#00BCD4', '#FF5722', '#607D8B']
    bars = ax.bar([f'Cluster {i}' for i in unique], counts,
                  color=[colors[i % len(colors)] for i in unique],
                  edgecolor='white', linewidth=1.5)

    for bar, count in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5,
                str(count), ha='center', fontweight='bold', fontsize=12)

    ax.set_title('Number of Customers per Cluster', fontweight='bold')
    ax.set_xlabel('Cluster')
    ax.set_ylabel('Number of Customers')
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved: {save_path}")
    plt.close(fig)


def profile_segments(df, labels, feature_cols):
    """
    Create segment profiles by computing mean values per cluster.
    Returns a summary DataFrame with segment characteristics.
    """
    df_clustered = df.copy()
    df_clustered['Cluster'] = labels

    # Profile with key metrics
    profile_cols = ['Age', 'AnnualIncome', 'TotalSpending', 'PurchaseFrequency',
                    'AverageOrderValue', 'DaysSinceLastPurchase', 'WebsiteVisits',
                    'DiscountUsage', 'CustomerRating']
    profile_cols = [c for c in profile_cols if c in df_clustered.columns]

    segment_profile = df_clustered.groupby('Cluster')[profile_cols].mean().round(2)
    segment_profile['CustomerCount'] = df_clustered.groupby('Cluster')['Cluster'].count()
    segment_profile['TotalRevenue'] = df_clustered.groupby('Cluster')['TotalSpending'].sum()
    segment_profile['RevenueContribution%'] = (
        (segment_profile['TotalRevenue'] / segment_profile['TotalRevenue'].sum()) * 100
    ).round(2)

    print("\n--- Segment Profiles ---")
    print(segment_profile.to_string())

    return segment_profile, df_clustered


def assign_segment_names(segment_profile):
    """
    Assign meaningful business names to each cluster based on its characteristics.
    """
    names = {}
    for cluster_id in segment_profile.index:
        row = segment_profile.loc[cluster_id]
        spending = row.get('TotalSpending', 0)
        frequency = row.get('PurchaseFrequency', 0)
        recency = row.get('DaysSinceLastPurchase', 999)
        discount = row.get('DiscountUsage', 0)

        # Compute relative positions within the profiles
        all_spending = segment_profile['TotalSpending']
        all_freq = segment_profile['PurchaseFrequency']
        all_recency = segment_profile['DaysSinceLastPurchase']
        all_discount = segment_profile['DiscountUsage']

        # Assign names based on characteristics
        if spending >= all_spending.quantile(0.75) and frequency >= all_freq.quantile(0.75):
            names[cluster_id] = "High-Value Loyal Customers"
        elif recency <= all_recency.quantile(0.25) and frequency <= all_freq.quantile(0.50):
            names[cluster_id] = "New and Promising Customers"
        elif discount >= all_discount.quantile(0.75):
            names[cluster_id] = "Discount-Driven Customers"
        elif recency >= all_recency.quantile(0.75) and spending >= all_spending.quantile(0.25):
            names[cluster_id] = "At-Risk Customers"
        else:
            names[cluster_id] = "Low-Engagement Customers"

    # Ensure uniqueness by appending cluster number if duplicates exist
    seen = {}
    for k, v in names.items():
        if v in seen:
            names[k] = f"{v} (Group {k})"
        else:
            seen[v] = k

    print("\n--- Segment Names ---")
    for k, v in names.items():
        print(f"  Cluster {k}: {v}")

    return names


def run_clustering(df, images_dir, outputs_dir):
    """
    Run the full clustering pipeline.
    Returns the clustered dataframe, segment profiles, and segment names.
    """
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(outputs_dir, exist_ok=True)

    print("\n" + "=" * 60)
    print("CLUSTERING - CUSTOMER SEGMENTATION")
    print("=" * 60)

    # Step 1: Select features
    feature_cols = select_clustering_features(df)

    # Step 2: Scale features
    X_scaled, scaler = scale_clustering_features(df, feature_cols)

    # Step 3: Elbow Method
    print("\n--- Elbow Method ---")
    elbow_method(X_scaled, save_path=os.path.join(images_dir, 'elbow_method.png'))

    # Step 4: Silhouette Analysis
    print("\n--- Silhouette Analysis ---")
    optimal_k, scores = silhouette_analysis(
        X_scaled, save_path=os.path.join(images_dir, 'silhouette_scores.png')
    )

    # Use optimal_k but ensure we get at least 4 clusters for meaningful segments
    # If silhouette suggests 2, we use 5 for business relevance
    n_clusters = max(optimal_k, 4)
    if optimal_k < 4:
        # Recheck silhouette for 4 and 5
        sil_4 = scores[2]  # index for k=4
        sil_5 = scores[3]  # index for k=5
        n_clusters = 5 if sil_5 > sil_4 * 0.9 else 4
        print(f"\n  Adjusted to K={n_clusters} for business relevance "
              f"(silhouette suggested K={optimal_k})")

    # Step 5: Fit final model
    kmeans, labels = fit_kmeans(X_scaled, n_clusters)

    # Step 6: Visualize
    plot_clusters_pca(X_scaled, labels, n_clusters,
                      save_path=os.path.join(images_dir, 'customer_clusters.png'))
    plot_cluster_counts(labels, save_path=os.path.join(images_dir, 'cluster_counts.png'))

    # Step 7: Profile segments
    segment_profile, df_clustered = profile_segments(df, labels, feature_cols)
    segment_names = assign_segment_names(segment_profile)

    # Step 8: Save outputs
    df_clustered.to_csv(os.path.join(outputs_dir, 'clustered_customers.csv'), index=False)
    print(f"Saved: {os.path.join(outputs_dir, 'clustered_customers.csv')}")

    # Customer segments summary with names
    segment_profile['SegmentName'] = segment_profile.index.map(segment_names)
    segment_profile.to_csv(os.path.join(outputs_dir, 'customer_segments.csv'))
    print(f"Saved: {os.path.join(outputs_dir, 'customer_segments.csv')}")

    print("\nClustering complete!")
    return df_clustered, segment_profile, segment_names, kmeans, scaler


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data", "customer_data.csv")
    images_dir = os.path.join(base_dir, "images")
    outputs_dir = os.path.join(base_dir, "outputs")
    df = pd.read_csv(data_path)
    run_clustering(df, images_dir, outputs_dir)
