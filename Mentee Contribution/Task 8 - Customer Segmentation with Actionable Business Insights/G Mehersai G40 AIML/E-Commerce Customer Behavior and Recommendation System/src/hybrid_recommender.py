from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "Ecommerce.csv"
)

CUSTOMER_SEGMENT_PATH = (
    PROJECT_ROOT
    / "outputs"
    / "results"
    / "customer_segments.csv"
)

RESULT_PATH = (
    PROJECT_ROOT
    / "outputs"
    / "results"
)

FIGURE_PATH = (
    PROJECT_ROOT
    / "outputs"
    / "figures"
)

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "hybrid_recommender.pkl"
)


# ============================================================
# CONFIGURATION
# ============================================================

TOP_K = 5

ITEM_CF_WEIGHT = 0.55

POPULARITY_WEIGHT = 0.20

SEGMENT_WEIGHT = 0.15

HISTORY_WEIGHT = 0.10


# ============================================================
# CREATE DIRECTORIES
# ============================================================

def create_directories():
    """Create required output directories."""

    RESULT_PATH.mkdir(
        parents=True,
        exist_ok=True,
    )

    FIGURE_PATH.mkdir(
        parents=True,
        exist_ok=True,
    )

    MODEL_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )


# ============================================================
# LOAD DATA
# ============================================================

def load_data():
    """Load e-commerce and customer segment data."""

    print("Loading project data...")

    df = pd.read_csv(
        DATA_PATH
    )

    customer_segments = pd.read_csv(
        CUSTOMER_SEGMENT_PATH
    )

    print("Project data loaded successfully.")

    print(
        "E-commerce sessions:",
        len(df),
    )

    print(
        "Customer profiles:",
        len(customer_segments),
    )

    print(
        "Unique customers:",
        df["customer_id"].nunique(),
    )

    print(
        "Unique products:",
        df["product_id"].nunique(),
    )

    return (
        df,
        customer_segments,
    )


# ============================================================
# CREATE INTERACTION SCORES
# ============================================================

def create_interaction_scores(df):
    """
    Create implicit feedback interaction scores.

    View     = 1
    Cart     = 3
    Purchase = 7
    """

    print(
        "\nCreating implicit interaction scores..."
    )

    interactions = df.copy()

    interactions["interaction_score"] = 1

    interactions.loc[
        interactions["added_to_cart"] == 1,
        "interaction_score",
    ] = 3

    interactions.loc[
        interactions["purchased"] == 1,
        "interaction_score",
    ] = 7

    print(
        "\n--- INTERACTION SCORE DISTRIBUTION ---"
    )

    print(
        interactions[
            "interaction_score"
        ]
        .value_counts()
        .sort_index()
    )

    return interactions


# ============================================================
# CREATE LEAVE-ONE-PURCHASE-OUT SPLIT
# ============================================================

def create_evaluation_split(interactions):
    """
    Hold out one purchased product per eligible customer.

    Customers require at least two unique purchased products.
    """

    print(
        "\nCreating leave-one-purchase-out evaluation split..."
    )

    purchase_data = (
        interactions[
            interactions["purchased"] == 1
        ]
        .copy()
    )

    purchase_counts = (
        purchase_data
        .groupby("customer_id")[
            "product_id"
        ]
        .nunique()
    )

    eligible_customers = (
        purchase_counts[
            purchase_counts >= 2
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

    interactions = interactions.copy()

    interactions["_row_id"] = np.arange(
        len(interactions)
    )

    held_out_rows = []

    test_records = []

    for customer_id in eligible_customers:

        customer_purchases = (
            interactions[
                (
                    interactions["customer_id"]
                    == customer_id
                )
                & (
                    interactions["purchased"]
                    == 1
                )
            ]
            .sort_values(
                [
                    "visit_date",
                    "session_id",
                ]
            )
        )

        unique_purchase_products = (
            customer_purchases[
                "product_id"
            ]
            .drop_duplicates(
                keep="last"
            )
        )

        test_product = (
            unique_purchase_products.iloc[-1]
        )

        candidate_rows = (
            customer_purchases[
                customer_purchases["product_id"]
                == test_product
            ]
        )

        held_out_row = (
            candidate_rows.iloc[-1]
        )

        held_out_rows.append(
            held_out_row["_row_id"]
        )

        test_records.append(
            {
                "customer_id": customer_id,
                "product_id": test_product,
            }
        )

    train_interactions = (
        interactions[
            ~interactions["_row_id"].isin(
                held_out_rows
            )
        ]
        .drop(
            columns="_row_id"
        )
        .copy()
    )

    test_data = pd.DataFrame(
        test_records
    )

    print(
        "\nTraining interactions:",
        len(train_interactions),
    )

    print(
        "Held-out test purchases:",
        len(test_data),
    )

    return (
        train_interactions,
        test_data,
    )


# ============================================================
# CREATE INTERACTION MATRIX
# ============================================================

def create_interaction_matrix(interactions):
    """Create customer-product interaction matrix."""

    print(
        "\nCreating customer-product interaction matrix..."
    )

    aggregated = (
        interactions
        .groupby(
            [
                "customer_id",
                "product_id",
            ],
            as_index=False,
        )["interaction_score"]
        .sum()
    )

    interaction_matrix = (
        aggregated
        .pivot(
            index="customer_id",
            columns="product_id",
            values="interaction_score",
        )
        .fillna(0)
    )

    print(
        "Interaction matrix shape:",
        interaction_matrix.shape,
    )

    return interaction_matrix


# ============================================================
# ITEM SIMILARITY
# ============================================================

def calculate_item_similarity(
    interaction_matrix,
):
    """Calculate item-item cosine similarity."""

    print(
        "\nCalculating item-item cosine similarity..."
    )

    similarity = cosine_similarity(
        interaction_matrix.T
    )

    item_similarity = pd.DataFrame(
        similarity,
        index=interaction_matrix.columns,
        columns=interaction_matrix.columns,
    )

    print(
        "Item similarity matrix shape:",
        item_similarity.shape,
    )

    return item_similarity


# ============================================================
# NORMALIZE SCORE
# ============================================================

def normalize_score(score_series):
    """Min-max normalize a score series."""

    score_series = (
        score_series
        .astype(float)
        .replace(
            [
                np.inf,
                -np.inf,
            ],
            0,
        )
        .fillna(0)
    )

    minimum = score_series.min()

    maximum = score_series.max()

    if maximum == minimum:
        return pd.Series(
            0.0,
            index=score_series.index,
        )

    return (
        score_series - minimum
    ) / (
        maximum - minimum
    )


# ============================================================
# PRODUCT POPULARITY SCORE
# ============================================================

def calculate_popularity_scores(
    interactions,
    product_ids,
):
    """Calculate normalized product popularity."""

    print(
        "\nCalculating product popularity scores..."
    )

    popularity = (
        interactions
        .groupby("product_id")[
            "interaction_score"
        ]
        .sum()
        .reindex(
            product_ids,
            fill_value=0,
        )
    )

    popularity = normalize_score(
        popularity
    )

    print(
        "Popularity scores created successfully."
    )

    return popularity


# ============================================================
# PREPARE CUSTOMER SEGMENTS
# ============================================================

def prepare_customer_segments(
    customer_segments,
):
    """Prepare customer-cluster mapping."""

    required_columns = [
        "customer_id",
        "cluster",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in customer_segments.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing customer segment columns: "
            + ", ".join(missing_columns)
        )

    segment_mapping = (
        customer_segments[
            required_columns
        ]
        .drop_duplicates(
            subset="customer_id"
        )
        .set_index("customer_id")[
            "cluster"
        ]
    )

    print(
        "\nCustomer segment mapping created."
    )

    print(
        "Segment distribution:"
    )

    print(
        segment_mapping
        .value_counts()
        .sort_index()
    )

    return segment_mapping


# ============================================================
# SEGMENT PRODUCT PREFERENCE
# ============================================================

def calculate_segment_preferences(
    interactions,
    segment_mapping,
    product_ids,
):
    """
    Calculate product preference scores for each customer segment.
    """

    print(
        "\nCalculating customer segment product preferences..."
    )

    segment_interactions = (
        interactions[
            [
                "customer_id",
                "product_id",
                "interaction_score",
            ]
        ]
        .copy()
    )

    segment_interactions[
        "cluster"
    ] = (
        segment_interactions[
            "customer_id"
        ]
        .map(
            segment_mapping
        )
    )

    segment_interactions = (
        segment_interactions
        .dropna(
            subset=["cluster"]
        )
    )

    segment_interactions[
        "cluster"
    ] = (
        segment_interactions[
            "cluster"
        ]
        .astype(int)
    )

    segment_scores = {}

    for cluster in sorted(
        segment_interactions[
            "cluster"
        ].unique()
    ):

        cluster_data = (
            segment_interactions[
                segment_interactions[
                    "cluster"
                ]
                == cluster
            ]
        )

        scores = (
            cluster_data
            .groupby("product_id")[
                "interaction_score"
            ]
            .sum()
            .reindex(
                product_ids,
                fill_value=0,
            )
        )

        segment_scores[
            cluster
        ] = normalize_score(
            scores
        )

    print(
        "Segment preference scores created successfully."
    )

    return segment_scores


# ============================================================
# ITEM CF SCORE
# ============================================================

def calculate_item_cf_score(
    customer_id,
    interaction_matrix,
    item_similarity,
):
    """Calculate Item-Based CF scores for a customer."""

    product_ids = (
        interaction_matrix.columns
    )

    if (
        customer_id
        not in interaction_matrix.index
    ):
        return pd.Series(
            0.0,
            index=product_ids,
        )

    customer_vector = (
        interaction_matrix.loc[
            customer_id
        ]
    )

    interacted_items = (
        customer_vector[
            customer_vector > 0
        ]
    )

    if interacted_items.empty:
        return pd.Series(
            0.0,
            index=product_ids,
        )

    similarities = (
        item_similarity.loc[
            interacted_items.index
        ]
    )

    weighted_scores = (
        similarities.T
        .dot(
            interacted_items.values
        )
    )

    similarity_strength = (
        similarities
        .abs()
        .sum(axis=0)
        .replace(0, np.nan)
    )

    scores = (
        weighted_scores
        / similarity_strength
    )

    scores = (
        scores
        .replace(
            [
                np.inf,
                -np.inf,
            ],
            0,
        )
        .fillna(0)
        .reindex(
            product_ids,
            fill_value=0,
        )
    )

    return normalize_score(
        scores
    )


# ============================================================
# CUSTOMER HISTORY SCORE
# ============================================================

def calculate_history_score(
    customer_id,
    interaction_matrix,
):
    """
    Calculate customer historical interaction strength.

    The score captures the customer's own implicit preference
    history before filtering already-seen products.
    """

    product_ids = (
        interaction_matrix.columns
    )

    if (
        customer_id
        not in interaction_matrix.index
    ):
        return pd.Series(
            0.0,
            index=product_ids,
        )

    history_score = (
        interaction_matrix.loc[
            customer_id
        ]
        .copy()
    )

    return normalize_score(
        history_score
    )


# ============================================================
# GET SEEN PRODUCTS
# ============================================================

def get_seen_products(
    customer_id,
    interaction_matrix,
):
    """Return products already interacted with."""

    if (
        customer_id
        not in interaction_matrix.index
    ):
        return set()

    customer_vector = (
        interaction_matrix.loc[
            customer_id
        ]
    )

    return set(
        customer_vector[
            customer_vector > 0
        ]
        .index
        .tolist()
    )


# ============================================================
# ITEM-BASED CF RECOMMENDATION
# ============================================================

def recommend_item_cf(
    customer_id,
    interaction_matrix,
    item_similarity,
    top_k=5,
):
    """Generate Item-Based CF recommendations."""

    scores = calculate_item_cf_score(
        customer_id,
        interaction_matrix,
        item_similarity,
    )

    seen_products = get_seen_products(
        customer_id,
        interaction_matrix,
    )

    scores = scores.drop(
        labels=list(
            seen_products
        ),
        errors="ignore",
    )

    return (
        scores
        .sort_values(
            ascending=False
        )
        .head(top_k)
        .index
        .tolist()
    )


# ============================================================
# HYBRID RECOMMENDATION
# ============================================================

def recommend_hybrid(
    customer_id,
    interaction_matrix,
    item_similarity,
    popularity_scores,
    segment_mapping,
    segment_preferences,
    top_k=5,
):
    """Generate hybrid behavioral recommendations."""

    product_ids = (
        interaction_matrix.columns
    )

    item_cf_score = (
        calculate_item_cf_score(
            customer_id,
            interaction_matrix,
            item_similarity,
        )
    )

    popularity_score = (
        popularity_scores
        .reindex(
            product_ids,
            fill_value=0,
        )
    )

    history_score = (
        calculate_history_score(
            customer_id,
            interaction_matrix,
        )
    )

    cluster = segment_mapping.get(
        customer_id,
        None,
    )

    if (
        cluster is not None
        and not pd.isna(cluster)
        and int(cluster)
        in segment_preferences
    ):

        segment_score = (
            segment_preferences[
                int(cluster)
            ]
            .reindex(
                product_ids,
                fill_value=0,
            )
        )

    else:

        segment_score = pd.Series(
            0.0,
            index=product_ids,
        )

    hybrid_score = (
        ITEM_CF_WEIGHT
        * item_cf_score
        + POPULARITY_WEIGHT
        * popularity_score
        + SEGMENT_WEIGHT
        * segment_score
        + HISTORY_WEIGHT
        * history_score
    )

    seen_products = get_seen_products(
        customer_id,
        interaction_matrix,
    )

    hybrid_score = hybrid_score.drop(
        labels=list(
            seen_products
        ),
        errors="ignore",
    )

    recommendations = (
        hybrid_score
        .sort_values(
            ascending=False
        )
        .head(top_k)
    )

    return recommendations


# ============================================================
# EVALUATION
# ============================================================

def evaluate_recommender(
    algorithm_name,
    test_data,
    recommendation_function,
    all_products,
):
    """Evaluate recommender using Top-K metrics."""

    print(
        f"\nEvaluating {algorithm_name}..."
    )

    evaluation_records = []

    recommended_catalog = set()

    reciprocal_ranks = []

    hits = 0

    total_precision = 0

    total_recall = 0

    for row in test_data.itertuples(
        index=False
    ):

        customer_id = row.customer_id

        test_product = row.product_id

        recommendations = (
            recommendation_function(
                customer_id
            )
        )

        if isinstance(
            recommendations,
            pd.Series,
        ):
            recommended_products = (
                recommendations
                .index
                .tolist()
            )

        else:
            recommended_products = list(
                recommendations
            )

        recommended_catalog.update(
            recommended_products
        )

        hit = int(
            test_product
            in recommended_products
        )

        hits += hit

        precision = (
            hit / TOP_K
        )

        recall = hit

        total_precision += precision

        total_recall += recall

        reciprocal_rank = 0

        if hit:

            rank = (
                recommended_products
                .index(
                    test_product
                )
                + 1
            )

            reciprocal_rank = (
                1 / rank
            )

        reciprocal_ranks.append(
            reciprocal_rank
        )

        evaluation_records.append(
            {
                "customer_id": customer_id,
                "test_product": test_product,
                "recommended_products": (
                    ",".join(
                        map(
                            str,
                            recommended_products,
                        )
                    )
                ),
                "hit": hit,
                "reciprocal_rank": (
                    reciprocal_rank
                ),
            }
        )

    number_of_customers = len(
        test_data
    )

    hit_rate = (
        hits
        / number_of_customers
    )

    precision_at_k = (
        total_precision
        / number_of_customers
    )

    recall_at_k = (
        total_recall
        / number_of_customers
    )

    mrr_at_k = np.mean(
        reciprocal_ranks
    )

    coverage_at_k = (
        len(recommended_catalog)
        / len(all_products)
    )

    metrics = {
        "Algorithm": algorithm_name,
        "Hit Rate@5": hit_rate,
        "Precision@5": precision_at_k,
        "Recall@5": recall_at_k,
        "MRR@5": mrr_at_k,
        "Coverage@5": coverage_at_k,
    }

    evaluation_df = pd.DataFrame(
        evaluation_records
    )

    print(
        f"Hit Rate@5  : {hit_rate:.6f}"
    )

    print(
        f"Precision@5 : {precision_at_k:.6f}"
    )

    print(
        f"Recall@5    : {recall_at_k:.6f}"
    )

    print(
        f"MRR@5       : {mrr_at_k:.6f}"
    )

    print(
        f"Coverage@5  : {coverage_at_k:.6f}"
    )

    return (
        metrics,
        evaluation_df,
    )


# ============================================================
# PLOT COMPARISON
# ============================================================

def plot_comparison(
    comparison_df,
):
    """Plot Item-CF and Hybrid model comparison."""

    metrics = [
        "Hit Rate@5",
        "Precision@5",
        "Recall@5",
        "MRR@5",
        "Coverage@5",
    ]

    plot_df = (
        comparison_df
        .set_index("Algorithm")[
            metrics
        ]
        .T
    )

    ax = plot_df.plot(
        kind="bar",
        figsize=(11, 7),
    )

    ax.set_title(
        "Item-Based CF vs Hybrid Behavioral Recommender"
    )

    ax.set_xlabel(
        "Evaluation Metric"
    )

    ax.set_ylabel(
        "Score"
    )

    ax.set_ylim(
        0,
        1,
    )

    plt.xticks(
        rotation=45,
        ha="right",
    )

    plt.tight_layout()

    output_path = (
        FIGURE_PATH
        / "hybrid_recommender_comparison.png"
    )

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    print(
        "\nComparison figure saved:",
        output_path,
    )


# ============================================================
# MAIN
# ============================================================

def main():

    create_directories()

    (
        df,
        customer_segments,
    ) = load_data()

    interactions = (
        create_interaction_scores(
            df
        )
    )

    (
        train_interactions,
        test_data,
    ) = create_evaluation_split(
        interactions
    )

    interaction_matrix = (
        create_interaction_matrix(
            train_interactions
        )
    )

    item_similarity = (
        calculate_item_similarity(
            interaction_matrix
        )
    )

    product_ids = (
        interaction_matrix.columns
    )

    all_products = set(
        product_ids.tolist()
    )

    popularity_scores = (
        calculate_popularity_scores(
            train_interactions,
            product_ids,
        )
    )

    segment_mapping = (
        prepare_customer_segments(
            customer_segments
        )
    )

    segment_preferences = (
        calculate_segment_preferences(
            train_interactions,
            segment_mapping,
            product_ids,
        )
    )

    # --------------------------------------------------------
    # SAMPLE HYBRID RECOMMENDATIONS
    # --------------------------------------------------------

    print(
        "\n--- SAMPLE HYBRID RECOMMENDATIONS ---"
    )

    sample_customers = (
        test_data[
            "customer_id"
        ]
        .head(10)
    )

    for customer_id in sample_customers:

        recommendations = (
            recommend_hybrid(
                customer_id,
                interaction_matrix,
                item_similarity,
                popularity_scores,
                segment_mapping,
                segment_preferences,
                top_k=TOP_K,
            )
        )

        print(
            f"\nCustomer {customer_id}"
        )

        print(
            "Recommended Products:",
            recommendations.index.tolist(),
        )

        print(
            "Hybrid Scores:",
            recommendations.round(4).tolist(),
        )

    # --------------------------------------------------------
    # ITEM-BASED CF EVALUATION
    # --------------------------------------------------------

    (
        item_cf_metrics,
        item_cf_evaluation,
    ) = evaluate_recommender(
        "Item-Based CF",
        test_data,
        lambda customer_id: (
            recommend_item_cf(
                customer_id,
                interaction_matrix,
                item_similarity,
                top_k=TOP_K,
            )
        ),
        all_products,
    )

    # --------------------------------------------------------
    # HYBRID EVALUATION
    # --------------------------------------------------------

    (
        hybrid_metrics,
        hybrid_evaluation,
    ) = evaluate_recommender(
        "Hybrid Behavioral Recommender",
        test_data,
        lambda customer_id: (
            recommend_hybrid(
                customer_id,
                interaction_matrix,
                item_similarity,
                popularity_scores,
                segment_mapping,
                segment_preferences,
                top_k=TOP_K,
            )
        ),
        all_products,
    )

    # --------------------------------------------------------
    # COMPARISON
    # --------------------------------------------------------

    comparison_df = pd.DataFrame(
        [
            item_cf_metrics,
            hybrid_metrics,
        ]
    )

    print(
        "\n"
        + "=" * 70
    )

    print(
        "HYBRID RECOMMENDER COMPARISON"
    )

    print(
        "=" * 70
    )

    print(
        comparison_df.to_string(
            index=False
        )
    )

    item_hit_rate = (
        comparison_df.loc[
            comparison_df["Algorithm"]
            == "Item-Based CF",
            "Hit Rate@5",
        ]
        .iloc[0]
    )

    hybrid_hit_rate = (
        comparison_df.loc[
            comparison_df["Algorithm"]
            == "Hybrid Behavioral Recommender",
            "Hit Rate@5",
        ]
        .iloc[0]
    )

    if item_hit_rate > 0:

        hit_rate_change = (
            (
                hybrid_hit_rate
                - item_hit_rate
            )
            / item_hit_rate
        ) * 100

    else:

        hit_rate_change = np.nan

    print(
        "\n--- HYBRID IMPROVEMENT ANALYSIS ---"
    )

    print(
        "Item-Based CF Hit Rate@5:",
        f"{item_hit_rate:.6f}",
    )

    print(
        "Hybrid Hit Rate@5:",
        f"{hybrid_hit_rate:.6f}",
    )

    if not np.isnan(
        hit_rate_change
    ):

        print(
            "Relative Hit Rate Change:",
            f"{hit_rate_change:.2f}%",
        )

    if (
        hybrid_hit_rate
        > item_hit_rate
    ):

        print(
            "Result: Hybrid recommender improved Hit Rate@5."
        )

    elif (
        hybrid_hit_rate
        == item_hit_rate
    ):

        print(
            "Result: Hybrid recommender matched Item-Based CF."
        )

    else:

        print(
            "Result: Hybrid recommender did not improve Hit Rate@5."
        )

    # --------------------------------------------------------
    # SAVE RESULTS
    # --------------------------------------------------------

    comparison_output = (
        RESULT_PATH
        / "hybrid_recommender_comparison.csv"
    )

    comparison_df.to_csv(
        comparison_output,
        index=False,
    )

    item_evaluation_output = (
        RESULT_PATH
        / "hybrid_item_cf_evaluation.csv"
    )

    item_cf_evaluation.to_csv(
        item_evaluation_output,
        index=False,
    )

    hybrid_evaluation_output = (
        RESULT_PATH
        / "hybrid_evaluation.csv"
    )

    hybrid_evaluation.to_csv(
        hybrid_evaluation_output,
        index=False,
    )

    model_artifact = {
        "interaction_matrix": (
            interaction_matrix
        ),
        "item_similarity": (
            item_similarity
        ),
        "popularity_scores": (
            popularity_scores
        ),
        "segment_mapping": (
            segment_mapping
        ),
        "segment_preferences": (
            segment_preferences
        ),
        "weights": {
            "item_cf": ITEM_CF_WEIGHT,
            "popularity": POPULARITY_WEIGHT,
            "segment": SEGMENT_WEIGHT,
            "history": HISTORY_WEIGHT,
        },
        "top_k": TOP_K,
        "interaction_scores": {
            "view": 1,
            "cart": 3,
            "purchase": 7,
        },
    }

    joblib.dump(
        model_artifact,
        MODEL_PATH,
    )

    plot_comparison(
        comparison_df
    )

    print(
        "\nComparison saved:",
        comparison_output,
    )

    print(
        "Item-CF evaluation saved:",
        item_evaluation_output,
    )

    print(
        "Hybrid evaluation saved:",
        hybrid_evaluation_output,
    )

    print(
        "Hybrid model artifact saved:",
        MODEL_PATH,
    )

    print(
        "\nHybrid recommender experiment "
        "completed successfully."
    )


if __name__ == "__main__":
    main()