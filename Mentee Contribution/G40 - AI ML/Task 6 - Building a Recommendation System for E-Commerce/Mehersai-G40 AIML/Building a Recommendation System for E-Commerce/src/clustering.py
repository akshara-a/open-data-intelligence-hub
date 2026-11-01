import os

import matplotlib.pyplot as plt
import pandas as pd

from sklearn.cluster import KMeans

from sklearn.metrics import silhouette_score

from sklearn.preprocessing import StandardScaler


RESULTS_DIRECTORY = "outputs/results"
PLOTS_DIRECTORY = "outputs/plots"


def create_customer_features(df):
    """
    Aggregate session-level data into
    customer-level behavioral features.
    """

    print("\nCreating customer-level features...")


    customer_data = (
        df.groupby("customer_id")
        .agg(
            total_sessions=(
                "session_id",
                "count"
            ),
            average_pages_viewed=(
                "pages_viewed",
                "mean"
            ),
            average_time_on_site=(
                "time_on_site_sec",
                "mean"
            ),
            cart_addition_rate=(
                "added_to_cart",
                "mean"
            ),
            purchase_rate=(
                "purchased",
                "mean"
            ),
            total_purchases=(
                "purchased",
                "sum"
            ),
            average_rating=(
                "rating",
                "mean"
            ),
            total_revenue=(
                "revenue",
                "sum"
            ),
            average_discount=(
                "discount_percent",
                "mean"
            ),
            average_engagement=(
                "engagement_score",
                "mean"
            )
        )
        .reset_index()
    )


    print(
        f"Total Unique Customers: "
        f"{customer_data.shape[0]}"
    )


    print(
        f"Customer Features: "
        f"{customer_data.shape[1] - 1}"
    )


    return customer_data


def perform_customer_clustering(df):
    """
    Segment customers using K-Means clustering.
    """

    print("\n" + "=" * 60)
    print("CLUSTERING - CUSTOMER SEGMENTATION")
    print("=" * 60)


    customer_data = create_customer_features(
        df
    )


    clustering_features = [
        "total_sessions",
        "average_pages_viewed",
        "average_time_on_site",
        "cart_addition_rate",
        "purchase_rate",
        "total_purchases",
        "average_rating",
        "total_revenue",
        "average_discount",
        "average_engagement"
    ]


    X = customer_data[
        clustering_features
    ]


    print("\nClustering Features:")

    for feature in clustering_features:
        print(f"- {feature}")


    # Scale features
    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)


    # -------------------------------------------------
    # Elbow Method
    # -------------------------------------------------

    k_values = range(2, 11)

    inertia_values = []

    silhouette_scores = []


    print("\nK-MEANS EVALUATION")
    print("-" * 60)


    for k in k_values:

        kmeans = KMeans(
            n_clusters=k,
            init="k-means++",
            max_iter=300,
            random_state=42,
            n_init=10
        )


        cluster_labels = kmeans.fit_predict(
            X_scaled
        )


        inertia = kmeans.inertia_

        silhouette = silhouette_score(
            X_scaled,
            cluster_labels
        )


        inertia_values.append(
            inertia
        )

        silhouette_scores.append(
            silhouette
        )


        print(
            f"K = {k} | "
            f"Inertia = {inertia:.2f} | "
            f"Silhouette Score = {silhouette:.4f}"
        )


    # -------------------------------------------------
    # Elbow Plot
    # -------------------------------------------------

    os.makedirs(
        PLOTS_DIRECTORY,
        exist_ok=True
    )


    plt.figure(
        figsize=(8, 5)
    )


    plt.plot(
        list(k_values),
        inertia_values,
        marker="o"
    )


    plt.title(
        "Elbow Method for Optimal Number of Clusters"
    )

    plt.xlabel(
        "Number of Clusters (K)"
    )

    plt.ylabel(
        "Inertia"
    )


    elbow_file = os.path.join(
        PLOTS_DIRECTORY,
        "12_elbow_method.png"
    )


    plt.tight_layout()

    plt.savefig(
        elbow_file,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


    print(
        f"\nSaved plot: {elbow_file}"
    )


    # -------------------------------------------------
    # Silhouette Score Plot
    # -------------------------------------------------

    plt.figure(
        figsize=(8, 5)
    )


    plt.plot(
        list(k_values),
        silhouette_scores,
        marker="o"
    )


    plt.title(
        "Silhouette Score for Different K Values"
    )

    plt.xlabel(
        "Number of Clusters (K)"
    )

    plt.ylabel(
        "Silhouette Score"
    )


    silhouette_file = os.path.join(
        PLOTS_DIRECTORY,
        "13_silhouette_scores.png"
    )


    plt.tight_layout()

    plt.savefig(
        silhouette_file,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


    print(
        f"Saved plot: {silhouette_file}"
    )


    # -------------------------------------------------
    # Select Best K
    # -------------------------------------------------

    best_score_index = silhouette_scores.index(
        max(silhouette_scores)
    )


    best_k = list(k_values)[
        best_score_index
    ]


    best_silhouette_score = max(
        silhouette_scores
    )


    print("\nOPTIMAL CLUSTER SELECTION")
    print("-" * 60)


    print(
        f"Best Number of Clusters: {best_k}"
    )

    print(
        f"Best Silhouette Score: "
        f"{best_silhouette_score:.4f}"
    )


    # -------------------------------------------------
    # Final K-Means Model
    # -------------------------------------------------

    final_kmeans = KMeans(
        n_clusters=best_k,
        init="k-means++",
        max_iter=300,
        random_state=42,
        n_init=10
    )


    customer_data["cluster"] = (
        final_kmeans.fit_predict(
            X_scaled
        )
    )
    
        # -------------------------------------------------
    # Assign Business Segment Names
    # -------------------------------------------------

    segment_names = {
        0: "Low-Conversion Browsers",
        1: "Active High-Value Buyers"
    }


    customer_data["segment_name"] = (
        customer_data["cluster"]
        .map(segment_names)
    )


    print("\nCUSTOMER SEGMENT NAMES")
    print("-" * 60)

    print(
        customer_data[
            [
                "cluster",
                "segment_name"
            ]
        ]
        .drop_duplicates()
        .sort_values("cluster")
        .to_string(index=False)
    )


    # -------------------------------------------------
    # Cluster Summary
    # -------------------------------------------------

    cluster_summary = (
        customer_data
        .groupby("cluster")[
            clustering_features
        ]
        .mean()
        .round(2)
    )


    cluster_counts = (
        customer_data["cluster"]
        .value_counts()
        .sort_index()
    )


    print("\nCUSTOMERS PER CLUSTER")
    print("-" * 60)

    print(cluster_counts)


    print("\nCLUSTER BEHAVIOR SUMMARY")
    print("-" * 60)

    print(
        cluster_summary.to_string()
    )


    # -------------------------------------------------
    # Save Results
    # -------------------------------------------------

    os.makedirs(
        RESULTS_DIRECTORY,
        exist_ok=True
    )


    customer_file = os.path.join(
        RESULTS_DIRECTORY,
        "customer_segments.csv"
    )


    customer_data.to_csv(
        customer_file,
        index=False
    )


    cluster_summary_file = os.path.join(
        RESULTS_DIRECTORY,
        "cluster_summary.csv"
    )


    cluster_summary.to_csv(
        cluster_summary_file
    )


    print(
        f"\nCustomer segments saved to: "
        f"{customer_file}"
    )

    print(
        f"Cluster summary saved to: "
        f"{cluster_summary_file}"
    )


    # -------------------------------------------------
    # Cluster Visualization
    # -------------------------------------------------

    plt.figure(
        figsize=(9, 6)
    )


    scatter = plt.scatter(
        customer_data["purchase_rate"],
        customer_data["total_revenue"],
        c=customer_data["cluster"],
        alpha=0.6
    )


    plt.title(
        "Customer Segments by Purchase Rate and Revenue"
    )

    plt.xlabel(
        "Purchase Rate"
    )

    plt.ylabel(
        "Total Revenue"
    )


    plt.legend(
        *scatter.legend_elements(),
        title="Cluster"
    )


    cluster_plot_file = os.path.join(
        PLOTS_DIRECTORY,
        "14_customer_segments.png"
    )


    plt.tight_layout()

    plt.savefig(
        cluster_plot_file,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


    print(
        f"Saved plot: {cluster_plot_file}"
    )


    print(
        "\nCustomer clustering completed."
    )


    return (
        final_kmeans,
        scaler,
        customer_data,
        cluster_summary
    )