from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity


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

TOP_K = 5

RANDOM_STATE = 42

SVD_COMPONENTS = 50


# --------------------------------------------------
# DATA LOADING
# --------------------------------------------------

def load_data(file_path):
    """Load the e-commerce dataset."""

    return pd.read_csv(
        file_path
    )


# --------------------------------------------------
# INTERACTION SCORE
# --------------------------------------------------

def create_interaction_scores(df):
    """Create implicit customer-product interaction scores."""

    interaction_df = df[
        [
            "customer_id",
            "product_id",
            "added_to_cart",
            "purchased",
        ]
    ].copy()

    interaction_df["interaction_score"] = (
        1
        + (interaction_df["added_to_cart"] * 2)
        + (interaction_df["purchased"] * 4)
    )

    return interaction_df


# --------------------------------------------------
# LEAVE-ONE-PURCHASE-OUT SPLIT
# --------------------------------------------------

def create_evaluation_split(interaction_df):
    """Hold out one purchased product per eligible customer."""

    purchased_df = interaction_df[
        interaction_df["purchased"] == 1
    ].copy()

    customer_purchase_counts = (
        purchased_df
        .groupby("customer_id")["product_id"]
        .nunique()
    )

    eligible_customers = (
        customer_purchase_counts[
            customer_purchase_counts >= 2
        ]
        .index
    )

    print(
        "\n--- EVALUATION ELIGIBILITY ---"
    )

    print(
        "Customers with at least 2 unique purchases:",
        len(eligible_customers),
    )

    rng = np.random.default_rng(
        RANDOM_STATE
    )

    test_records = []

    rows_to_remove = []

    for customer_id in eligible_customers:

        customer_purchases = (
            purchased_df[
                purchased_df["customer_id"]
                == customer_id
            ]
        )

        unique_products = (
            customer_purchases["product_id"]
            .unique()
        )

        held_out_product = int(
            rng.choice(
                unique_products
            )
        )

        held_out_rows = (
            interaction_df[
                (
                    interaction_df["customer_id"]
                    == customer_id
                )
                & (
                    interaction_df["product_id"]
                    == held_out_product
                )
            ]
            .index
            .tolist()
        )

        rows_to_remove.extend(
            held_out_rows
        )

        test_records.append(
            {
                "customer_id": customer_id,
                "held_out_product": held_out_product,
            }
        )

    train_interactions = (
        interaction_df
        .drop(
            index=rows_to_remove
        )
        .copy()
    )

    test_df = pd.DataFrame(
        test_records
    )

    return (
        train_interactions,
        test_df,
    )


# --------------------------------------------------
# AGGREGATE INTERACTIONS
# --------------------------------------------------

def aggregate_interactions(interaction_df):
    """Aggregate repeated customer-product interactions."""

    return (
        interaction_df
        .groupby(
            [
                "customer_id",
                "product_id",
            ],
            as_index=False,
        )
        .agg(
            interaction_score=(
                "interaction_score",
                "sum",
            )
        )
    )


# --------------------------------------------------
# INTERACTION MATRIX
# --------------------------------------------------

def create_interaction_matrix(aggregated_interactions):
    """Create customer-product interaction matrix."""

    return (
        aggregated_interactions
        .pivot(
            index="customer_id",
            columns="product_id",
            values="interaction_score",
        )
        .fillna(0)
    )


# --------------------------------------------------
# POPULARITY MODEL
# --------------------------------------------------

def train_popularity_model(aggregated_interactions):
    """Rank products using total interaction strength."""

    return (
        aggregated_interactions
        .groupby("product_id")[
            "interaction_score"
        ]
        .sum()
        .sort_values(
            ascending=False
        )
    )


def recommend_popularity(
    customer_id,
    interaction_matrix,
    popular_products,
    top_k,
):
    """Generate popularity-based recommendations."""

    if customer_id in interaction_matrix.index:

        interacted_products = (
            interaction_matrix
            .loc[customer_id]
        )

        interacted_products = (
            interacted_products[
                interacted_products > 0
            ]
            .index
        )

    else:

        interacted_products = []

    recommendations = (
        popular_products
        .drop(
            labels=interacted_products,
            errors="ignore",
        )
        .head(top_k)
        .index
        .tolist()
    )

    return recommendations


# --------------------------------------------------
# ITEM-BASED COLLABORATIVE FILTERING
# --------------------------------------------------

def train_item_cf(interaction_matrix):
    """Calculate item-item cosine similarity."""

    product_customer_matrix = (
        interaction_matrix.T
    )

    similarity_matrix = cosine_similarity(
        product_customer_matrix
    )

    item_similarity = pd.DataFrame(
        similarity_matrix,
        index=product_customer_matrix.index,
        columns=product_customer_matrix.index,
    )

    return item_similarity


def recommend_item_cf(
    customer_id,
    interaction_matrix,
    item_similarity,
    popular_products,
    top_k,
):
    """Generate item-based collaborative recommendations."""

    if customer_id not in interaction_matrix.index:

        return (
            popular_products
            .head(top_k)
            .index
            .tolist()
        )

    customer_interactions = (
        interaction_matrix.loc[
            customer_id
        ]
    )

    interacted_products = (
        customer_interactions[
            customer_interactions > 0
        ]
    )

    if interacted_products.empty:

        return (
            popular_products
            .head(top_k)
            .index
            .tolist()
        )

    recommendation_scores = pd.Series(
        0.0,
        index=item_similarity.index,
    )

    for (
        product_id,
        interaction_score,
    ) in interacted_products.items():

        if product_id not in item_similarity.columns:
            continue

        recommendation_scores += (
            item_similarity[product_id]
            * interaction_score
        )

    recommendation_scores = (
        recommendation_scores
        .drop(
            labels=interacted_products.index,
            errors="ignore",
        )
    )

    return (
        recommendation_scores
        .sort_values(
            ascending=False
        )
        .head(top_k)
        .index
        .tolist()
    )


# --------------------------------------------------
# SVD MODEL
# --------------------------------------------------

def train_svd_model(interaction_matrix):
    """Train Truncated SVD recommendation model."""

    max_components = min(
        interaction_matrix.shape
    ) - 1

    n_components = min(
        SVD_COMPONENTS,
        max_components,
    )

    print(
        "\nTraining Truncated SVD..."
    )

    print(
        "SVD components:",
        n_components,
    )

    svd_model = TruncatedSVD(
        n_components=n_components,
        random_state=RANDOM_STATE,
    )

    user_factors = (
        svd_model.fit_transform(
            interaction_matrix
        )
    )

    reconstructed_scores = (
        user_factors
        @ svd_model.components_
    )

    print(
        "Explained variance ratio:",
        round(
            svd_model
            .explained_variance_ratio_
            .sum(),
            4,
        ),
    )

    return (
        svd_model,
        reconstructed_scores,
    )


def recommend_svd(
    customer_id,
    interaction_matrix,
    reconstructed_scores,
    popular_products,
    top_k,
):
    """Generate SVD-based product recommendations."""

    if customer_id not in interaction_matrix.index:

        return (
            popular_products
            .head(top_k)
            .index
            .tolist()
        )

    customer_position = (
        interaction_matrix
        .index
        .get_loc(
            customer_id
        )
    )

    customer_scores = pd.Series(
        reconstructed_scores[
            customer_position
        ],
        index=interaction_matrix.columns,
    )

    interacted_products = (
        interaction_matrix
        .loc[customer_id]
    )

    interacted_products = (
        interacted_products[
            interacted_products > 0
        ]
        .index
    )

    customer_scores = (
        customer_scores
        .drop(
            labels=interacted_products,
            errors="ignore",
        )
    )

    return (
        customer_scores
        .sort_values(
            ascending=False
        )
        .head(top_k)
        .index
        .tolist()
    )


# --------------------------------------------------
# EVALUATION
# --------------------------------------------------

def evaluate_algorithm(
    algorithm_name,
    test_df,
    recommendation_function,
):
    """Evaluate a recommendation algorithm."""

    evaluation_records = []

    recommended_catalog = set()

    print(
        f"\nEvaluating {algorithm_name}..."
    )

    for row in test_df.itertuples(
        index=False
    ):

        customer_id = row.customer_id

        held_out_product = (
            row.held_out_product
        )

        recommendations = (
            recommendation_function(
                customer_id
            )
        )

        recommended_catalog.update(
            recommendations
        )

        hit = int(
            held_out_product
            in recommendations
        )

        if hit:

            rank = (
                recommendations.index(
                    held_out_product
                )
                + 1
            )

            reciprocal_rank = (
                1 / rank
            )

        else:

            rank = None

            reciprocal_rank = 0.0

        evaluation_records.append(
            {
                "customer_id": customer_id,
                "held_out_product": held_out_product,
                "recommendations": ",".join(
                    map(
                        str,
                        recommendations,
                    )
                ),
                "hit": hit,
                "rank": rank,
                "precision_at_5": (
                    hit / TOP_K
                ),
                "recall_at_5": hit,
                "reciprocal_rank": (
                    reciprocal_rank
                ),
            }
        )

    evaluation_df = pd.DataFrame(
        evaluation_records
    )

    catalog_size = len(
        interaction_matrix.columns
    )

    metrics = {
        "Algorithm": algorithm_name,
        "Hit Rate@5": (
            evaluation_df["hit"]
            .mean()
        ),
        "Precision@5": (
            evaluation_df[
                "precision_at_5"
            ]
            .mean()
        ),
        "Recall@5": (
            evaluation_df[
                "recall_at_5"
            ]
            .mean()
        ),
        "MRR@5": (
            evaluation_df[
                "reciprocal_rank"
            ]
            .mean()
        ),
        "Coverage@5": (
            len(recommended_catalog)
            / catalog_size
        ),
    }

    return (
        evaluation_df,
        metrics,
    )


# --------------------------------------------------
# DISPLAY COMPARISON
# --------------------------------------------------

def display_comparison(comparison_df):
    """Display algorithm comparison."""

    print(
        "\n--- RECOMMENDER ALGORITHM COMPARISON ---"
    )

    print(
        comparison_df.to_string(
            index=False
        )
    )

    best_algorithm = (
        comparison_df
        .sort_values(
            by=[
                "Hit Rate@5",
                "MRR@5",
            ],
            ascending=False,
        )
        .iloc[0]
    )

    print(
        "\n--- BEST RECOMMENDER ---"
    )

    print(
        "Algorithm:",
        best_algorithm["Algorithm"],
    )

    print(
        "Hit Rate@5:",
        round(
            best_algorithm[
                "Hit Rate@5"
            ],
            4,
        ),
    )

    print(
        "MRR@5:",
        round(
            best_algorithm["MRR@5"],
            4,
        ),
    )


# --------------------------------------------------
# PLOT COMPARISON
# --------------------------------------------------

def plot_comparison(comparison_df):
    """Plot recommender comparison metrics."""

    metrics_to_plot = [
        "Hit Rate@5",
        "Precision@5",
        "Recall@5",
        "MRR@5",
    ]

    plot_df = (
        comparison_df
        .set_index("Algorithm")[
            metrics_to_plot
        ]
    )

    ax = plot_df.plot(
        kind="bar",
        figsize=(10, 6),
    )

    ax.set_title(
        "Recommendation Algorithm Comparison"
    )

    ax.set_xlabel(
        "Recommendation Algorithm"
    )

    ax.set_ylabel(
        "Score"
    )

    ax.tick_params(
        axis="x",
        rotation=0,
    )

    plt.tight_layout()

    output_path = (
        FIGURE_PATH
        / "recommender_comparison.png"
    )

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    print(
        f"\nComparison figure saved: "
        f"{output_path}"
    )


# --------------------------------------------------
# SAVE RESULTS
# --------------------------------------------------

def save_results(
    comparison_df,
    popularity_evaluation,
    item_cf_evaluation,
    svd_evaluation,
):
    """Save recommendation comparison results."""

    comparison_path = (
        RESULT_PATH
        / "recommender_comparison.csv"
    )

    popularity_path = (
        RESULT_PATH
        / "popularity_evaluation.csv"
    )

    item_cf_path = (
        RESULT_PATH
        / "item_cf_evaluation.csv"
    )

    svd_path = (
        RESULT_PATH
        / "svd_evaluation.csv"
    )

    comparison_df.to_csv(
        comparison_path,
        index=False,
    )

    popularity_evaluation.to_csv(
        popularity_path,
        index=False,
    )

    item_cf_evaluation.to_csv(
        item_cf_path,
        index=False,
    )

    svd_evaluation.to_csv(
        svd_path,
        index=False,
    )

    print(
        f"\nComparison saved: "
        f"{comparison_path}"
    )

    print(
        f"Popularity evaluation saved: "
        f"{popularity_path}"
    )

    print(
        f"Item-CF evaluation saved: "
        f"{item_cf_path}"
    )

    print(
        f"SVD evaluation saved: "
        f"{svd_path}"
    )


# --------------------------------------------------
# MAIN FUNCTION
# --------------------------------------------------

def main():
    global interaction_matrix

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
        "\nCreating interaction scores..."
    )

    interaction_df = (
        create_interaction_scores(
            df
        )
    )

    (
        train_interactions,
        test_df,
    ) = create_evaluation_split(
        interaction_df
    )

    print(
        "\nTraining interactions:",
        len(train_interactions),
    )

    print(
        "Held-out test purchases:",
        len(test_df),
    )

    aggregated_interactions = (
        aggregate_interactions(
            train_interactions
        )
    )

    interaction_matrix = (
        create_interaction_matrix(
            aggregated_interactions
        )
    )

    print(
        "\nInteraction matrix shape:",
        interaction_matrix.shape,
    )

    print(
        "\nTraining popularity model..."
    )

    popular_products = (
        train_popularity_model(
            aggregated_interactions
        )
    )

    print(
        "Popularity model ready."
    )

    print(
        "\nTraining Item-Based CF..."
    )

    item_similarity = train_item_cf(
        interaction_matrix
    )

    print(
        "Item-Based CF ready."
    )

    (
        svd_model,
        reconstructed_scores,
    ) = train_svd_model(
        interaction_matrix
    )

    popularity_evaluation, popularity_metrics = (
        evaluate_algorithm(
            "Popularity-Based",
            test_df,
            lambda customer_id: recommend_popularity(
                customer_id,
                interaction_matrix,
                popular_products,
                TOP_K,
            ),
        )
    )

    item_cf_evaluation, item_cf_metrics = (
        evaluate_algorithm(
            "Item-Based CF",
            test_df,
            lambda customer_id: recommend_item_cf(
                customer_id,
                interaction_matrix,
                item_similarity,
                popular_products,
                TOP_K,
            ),
        )
    )

    svd_evaluation, svd_metrics = (
        evaluate_algorithm(
            "Truncated SVD",
            test_df,
            lambda customer_id: recommend_svd(
                customer_id,
                interaction_matrix,
                reconstructed_scores,
                popular_products,
                TOP_K,
            ),
        )
    )

    comparison_df = pd.DataFrame(
        [
            popularity_metrics,
            item_cf_metrics,
            svd_metrics,
        ]
    )

    display_comparison(
        comparison_df
    )

    plot_comparison(
        comparison_df
    )

    save_results(
        comparison_df,
        popularity_evaluation,
        item_cf_evaluation,
        svd_evaluation,
    )

    svd_model_path = (
        MODEL_PATH
        / "svd_model.pkl"
    )

    joblib.dump(
        svd_model,
        svd_model_path,
    )

    print(
        f"\nSVD model saved: "
        f"{svd_model_path}"
    )

    print(
        "\nRecommender algorithm comparison "
        "completed successfully."
    )


# --------------------------------------------------
# SCRIPT ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":
    main()