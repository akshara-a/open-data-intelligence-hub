from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = PROJECT_ROOT / "data" / "Ecommerce.csv"

MODEL_PATH = PROJECT_ROOT / "models"

FIGURE_PATH = PROJECT_ROOT / "outputs" / "figures"

RESULT_PATH = PROJECT_ROOT / "outputs" / "results"


MODEL_PATH.mkdir(
    parents=True,
    exist_ok=True,
)

FIGURE_PATH.mkdir(
    parents=True,
    exist_ok=True,
)

RESULT_PATH.mkdir(
    parents=True,
    exist_ok=True,
)


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

RANDOM_STATE = 42

MIN_CLUSTERS = 2

MAX_CLUSTERS = 8


CUSTOMER_FEATURES = [
    "total_sessions",
    "purchase_rate",
    "total_purchases",
    "total_revenue",
    "avg_order_value",
    "avg_pages_viewed",
    "avg_time_on_site",
    "avg_discount",
    "cart_add_rate",
    "cart_abandon_rate",
]


# --------------------------------------------------
# DATA LOADING
# --------------------------------------------------

def load_data(file_path):
    """Load the e-commerce dataset."""

    return pd.read_csv(
        file_path
    )


# --------------------------------------------------
# CUSTOMER PROFILE CREATION
# --------------------------------------------------

def create_customer_profiles(df):
    """Aggregate session data into customer profiles."""

    customer_profiles = (
        df.groupby("customer_id")
        .agg(
            total_sessions=(
                "session_id",
                "count",
            ),
            purchase_rate=(
                "purchased",
                "mean",
            ),
            total_purchases=(
                "purchased",
                "sum",
            ),
            total_revenue=(
                "revenue",
                "sum",
            ),
            avg_pages_viewed=(
                "pages_viewed",
                "mean",
            ),
            avg_time_on_site=(
                "time_on_site_sec",
                "mean",
            ),
            avg_discount=(
                "discount_percent",
                "mean",
            ),
            cart_add_rate=(
                "added_to_cart",
                "mean",
            ),
            cart_abandon_rate=(
                "cart_abandoned",
                "mean",
            ),
        )
        .reset_index()
    )

    customer_profiles[
        "avg_order_value"
    ] = (
        customer_profiles["total_revenue"]
        / customer_profiles["total_purchases"]
        .replace(0, pd.NA)
    )

    customer_profiles[
        "avg_order_value"
    ] = (
        customer_profiles["avg_order_value"]
        .fillna(0)
    )

    customer_profiles = customer_profiles[
        [
            "customer_id",
            *CUSTOMER_FEATURES,
        ]
    ]

    return customer_profiles


# --------------------------------------------------
# CUSTOMER PROFILE SUMMARY
# --------------------------------------------------

def display_customer_summary(customer_profiles):
    """Display customer profile information."""

    print(
        "\n--- CUSTOMER PROFILE OVERVIEW ---"
    )

    print(
        "Number of customers:",
        len(customer_profiles),
    )

    print(
        "Number of clustering features:",
        len(CUSTOMER_FEATURES),
    )

    print(
        "\nCustomer features:"
    )

    for feature in CUSTOMER_FEATURES:
        print(
            f"- {feature}"
        )

    print(
        "\n--- CUSTOMER PROFILE SUMMARY ---"
    )

    print(
        customer_profiles[
            CUSTOMER_FEATURES
        ]
        .describe()
        .T
        .round(2)
    )

    print(
        "\n--- MISSING VALUES ---"
    )

    print(
        customer_profiles[
            CUSTOMER_FEATURES
        ]
        .isnull()
        .sum()
    )


# --------------------------------------------------
# FEATURE SCALING
# --------------------------------------------------

def scale_customer_features(customer_profiles):
    """Standardize customer clustering features."""

    X = customer_profiles[
        CUSTOMER_FEATURES
    ].copy()

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(
        X
    )

    return X_scaled, scaler


# --------------------------------------------------
# CLUSTER EVALUATION
# --------------------------------------------------

def evaluate_cluster_numbers(X_scaled):
    """Evaluate K-Means for different cluster counts."""

    cluster_results = []

    print(
        "\n--- K-MEANS CLUSTER EVALUATION ---"
    )

    for k in range(
        MIN_CLUSTERS,
        MAX_CLUSTERS + 1,
    ):

        model = KMeans(
            n_clusters=k,
            random_state=RANDOM_STATE,
            n_init=10,
        )

        cluster_labels = model.fit_predict(
            X_scaled
        )

        score = silhouette_score(
            X_scaled,
            cluster_labels,
        )

        inertia = model.inertia_

        cluster_results.append(
            {
                "k": k,
                "silhouette_score": score,
                "inertia": inertia,
            }
        )

        print(
            f"K = {k} | "
            f"Silhouette Score = {score:.4f} | "
            f"Inertia = {inertia:.2f}"
        )

    cluster_results_df = pd.DataFrame(
        cluster_results
    )

    return cluster_results_df


# --------------------------------------------------
# BEST CLUSTER SELECTION
# --------------------------------------------------

def select_best_k(cluster_results):
    """Select K with the highest silhouette score."""

    best_row = cluster_results.loc[
        cluster_results[
            "silhouette_score"
        ].idxmax()
    ]

    best_k = int(
        best_row["k"]
    )

    best_score = best_row[
        "silhouette_score"
    ]

    print(
        "\n--- BEST CLUSTER CONFIGURATION ---"
    )

    print(
        "Best K:",
        best_k,
    )

    print(
        f"Best Silhouette Score: "
        f"{best_score:.4f}"
    )

    return best_k


# --------------------------------------------------
# FINAL K-MEANS MODEL
# --------------------------------------------------

def train_final_model(X_scaled, best_k):
    """Train final K-Means model."""

    model = KMeans(
        n_clusters=best_k,
        random_state=RANDOM_STATE,
        n_init=10,
    )

    cluster_labels = model.fit_predict(
        X_scaled
    )

    return model, cluster_labels


# --------------------------------------------------
# CLUSTER ANALYSIS
# --------------------------------------------------

def analyze_clusters(
    customer_profiles,
    cluster_labels,
):
    """Analyze customer cluster characteristics."""

    customer_profiles = (
        customer_profiles.copy()
    )

    customer_profiles[
        "cluster"
    ] = cluster_labels
    
    segment_mapping = {
    0: "Low-Conversion Customers",
    1: "High-Value Customers",
}

    customer_profiles["segment_name"] = (
    customer_profiles["cluster"]
    .map(segment_mapping)
    )

    print(
        "\n--- CLUSTER DISTRIBUTION ---"
    )

    cluster_distribution = (
        customer_profiles["cluster"]
        .value_counts()
        .sort_index()
    )

    print(
        cluster_distribution
    )

    print(
        "\n--- CLUSTER DISTRIBUTION (%) ---"
    )

    cluster_percentage = (
        customer_profiles["cluster"]
        .value_counts(normalize=True)
        .sort_index()
        .mul(100)
        .round(2)
    )

    print(
        cluster_percentage
    )

    print(
        "\n--- CLUSTER PROFILE SUMMARY ---"
    )

    cluster_summary = (
        customer_profiles
        .groupby("cluster")[
            CUSTOMER_FEATURES
        ]
        .mean()
        .round(2)
    )

    print(
        cluster_summary.to_string()
    )

    return (
        customer_profiles,
        cluster_summary,
    )


# --------------------------------------------------
# SILHOUETTE SCORE PLOT
# --------------------------------------------------

def plot_cluster_scores(cluster_results):
    """Plot silhouette scores for cluster counts."""

    plt.figure(
        figsize=(8, 5)
    )

    plt.plot(
        cluster_results["k"],
        cluster_results[
            "silhouette_score"
        ],
        marker="o",
    )

    plt.title(
        "K-Means Silhouette Score"
    )

    plt.xlabel(
        "Number of Clusters (K)"
    )

    plt.ylabel(
        "Silhouette Score"
    )

    plt.xticks(
        cluster_results["k"]
    )

    plt.tight_layout()

    output_path = (
        FIGURE_PATH / "kmeans_scores.png"
    )

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    print(
        f"\nCluster score figure saved: "
        f"{output_path}"
    )


# --------------------------------------------------
# PCA CLUSTER VISUALIZATION
# --------------------------------------------------

def plot_customer_clusters(
    X_scaled,
    cluster_labels,
):
    """Visualize customer clusters using PCA."""

    pca = PCA(
        n_components=2
    )

    X_pca = pca.fit_transform(
        X_scaled
    )

    pca_df = pd.DataFrame(
        {
            "PCA1": X_pca[:, 0],
            "PCA2": X_pca[:, 1],
            "Cluster": cluster_labels,
        }
    )

    plt.figure(
        figsize=(9, 7)
    )

    scatter = plt.scatter(
        pca_df["PCA1"],
        pca_df["PCA2"],
        c=pca_df["Cluster"],
        alpha=0.6,
    )

    plt.title(
        "Customer Segments using PCA"
    )

    plt.xlabel(
        "Principal Component 1"
    )

    plt.ylabel(
        "Principal Component 2"
    )

    plt.legend(
        *scatter.legend_elements(),
        title="Cluster",
    )

    plt.tight_layout()

    output_path = (
        FIGURE_PATH / "customer_clusters.png"
    )

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    print(
        f"Customer cluster figure saved: "
        f"{output_path}"
    )

    return pca


# --------------------------------------------------
# SAVE RESULTS
# --------------------------------------------------

def save_results(
    customer_profiles,
    cluster_summary,
    cluster_results,
):
    """Save clustering results."""

    customer_path = (
        RESULT_PATH / "customer_segments.csv"
    )

    summary_path = (
        RESULT_PATH / "cluster_summary.csv"
    )

    score_path = (
        RESULT_PATH / "kmeans_scores.csv"
    )

    customer_profiles.to_csv(
        customer_path,
        index=False,
    )

    cluster_summary.to_csv(
        summary_path,
    )

    cluster_results.to_csv(
        score_path,
        index=False,
    )

    print(
        f"\nCustomer segments saved: "
        f"{customer_path}"
    )

    print(
        f"Cluster summary saved: "
        f"{summary_path}"
    )

    print(
        f"K-Means scores saved: "
        f"{score_path}"
    )


# --------------------------------------------------
# SAVE MODELS
# --------------------------------------------------

def save_models(
    model,
    scaler,
    pca,
):
    """Save clustering models and preprocessing objects."""

    model_path = (
        MODEL_PATH / "kmeans_model.pkl"
    )

    scaler_path = (
        MODEL_PATH / "customer_scaler.pkl"
    )

    pca_path = (
        MODEL_PATH / "customer_pca.pkl"
    )

    joblib.dump(
        model,
        model_path,
    )

    joblib.dump(
        scaler,
        scaler_path,
    )

    joblib.dump(
        pca,
        pca_path,
    )

    print(
        f"\nK-Means model saved: "
        f"{model_path}"
    )

    print(
        f"Scaler saved: "
        f"{scaler_path}"
    )

    print(
        f"PCA model saved: "
        f"{pca_path}"
    )


# --------------------------------------------------
# MAIN FUNCTION
# --------------------------------------------------

def main():
    print(
        "Loading dataset..."
    )

    df = load_data(
        DATA_PATH
    )

    print(
        "Dataset loaded successfully."
    )

    print(
        "Dataset shape:",
        df.shape
    )

    print(
        "\nCreating customer profiles..."
    )

    customer_profiles = (
        create_customer_profiles(
            df
        )
    )

    print(
        "Customer profiles created successfully."
    )

    display_customer_summary(
        customer_profiles
    )

    print(
        "\nScaling customer features..."
    )

    (
        X_scaled,
        scaler,
    ) = scale_customer_features(
        customer_profiles
    )

    print(
        "Feature scaling completed."
    )

    cluster_results = (
        evaluate_cluster_numbers(
            X_scaled
        )
    )

    best_k = select_best_k(
        cluster_results
    )

    print(
        "\nTraining final K-Means model..."
    )

    (
        model,
        cluster_labels,
    ) = train_final_model(
        X_scaled,
        best_k,
    )

    print(
        "Final K-Means model trained successfully."
    )

    (
        customer_profiles,
        cluster_summary,
    ) = analyze_clusters(
        customer_profiles,
        cluster_labels,
    )

    plot_cluster_scores(
        cluster_results
    )

    pca = plot_customer_clusters(
        X_scaled,
        cluster_labels,
    )

    save_results(
        customer_profiles,
        cluster_summary,
        cluster_results,
    )

    save_models(
        model,
        scaler,
        pca,
    )

    print(
        "\nCustomer segmentation completed successfully."
    )


# --------------------------------------------------
# SCRIPT ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":
    main()