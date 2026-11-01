from pathlib import Path
import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = PROJECT_ROOT / "data" / "Ecommerce.csv"

CUSTOMER_SEGMENTS_PATH = (
    PROJECT_ROOT
    / "outputs"
    / "results"
    / "customer_segments.csv"
)

RESULTS_PATH = PROJECT_ROOT / "outputs" / "results"
FIGURE_PATH = PROJECT_ROOT / "outputs" / "figures"
MODEL_PATH = PROJECT_ROOT / "models"

RESULTS_PATH.mkdir(parents=True, exist_ok=True)
FIGURE_PATH.mkdir(parents=True, exist_ok=True)
MODEL_PATH.mkdir(parents=True, exist_ok=True)


# ============================================================
# CONFIGURATION
# ============================================================

TOP_K = 5

ITEM_CF_WEIGHT = 0.55
NEIGHBOR_WEIGHT = 0.25
SEGMENT_WEIGHT = 0.15
POPULARITY_WEIGHT = 0.05

NUMBER_OF_NEIGHBORS = 20

CANDIDATE_POOL_SIZE = 50

DIVERSITY_LAMBDA = 0.80

RANDOM_STATE = 42


# ============================================================
# LOAD DATA
# ============================================================

def load_data():
    """Load e-commerce and customer segment datasets."""

    print("Loading project data...")

    df = pd.read_csv(DATA_PATH)

    customer_segments = pd.read_csv(
        CUSTOMER_SEGMENTS_PATH
    )

    print("Project data loaded successfully.")

    print("E-commerce sessions:", len(df))
    print("Customer profiles:", len(customer_segments))
    print("Unique customers:", df["customer_id"].nunique())
    print("Unique products:", df["product_id"].nunique())

    return df, customer_segments


# ============================================================
# INTERACTION SCORE
# ============================================================

def create_interaction_scores(df):
    """Create implicit customer-product interaction scores."""

    print("\nCreating implicit interaction scores...")

    interactions = df.copy()

    interactions["interaction_score"] = 1

    interactions.loc[
        interactions["added_to_cart"] == 1,
        "interaction_score"
    ] = 3

    interactions.loc[
        interactions["purchased"] == 1,
        "interaction_score"
    ] = 7

    print("\n--- INTERACTION SCORE DISTRIBUTION ---")

    print(
        interactions["interaction_score"]
        .value_counts()
        .sort_index()
    )

    return interactions


# ============================================================
# EVALUATION SPLIT
# ============================================================

def create_evaluation_split(interactions):
    """
    Create leave-one-purchase-out evaluation split.

    One purchased product is held out for every customer
    with at least two unique purchased products.
    """

    print(
        "\nCreating leave-one-purchase-out evaluation split..."
    )

    purchased = interactions[
        interactions["purchased"] == 1
    ].copy()

    eligible_customers = (
        purchased.groupby("customer_id")["product_id"]
        .nunique()
    )

    eligible_customers = eligible_customers[
        eligible_customers >= 2
    ].index

    print("\n--- EVALUATION ELIGIBILITY ---")
    print(
        "Customers with at least 2 unique purchases:",
        len(eligible_customers)
    )

    test_rows = []

    for customer_id in eligible_customers:

        customer_purchases = purchased[
            purchased["customer_id"] == customer_id
        ]

        test_row = customer_purchases.iloc[-1]

        test_rows.append(
            {
                "customer_id": customer_id,
                "product_id": test_row["product_id"],
            }
        )

    test_df = pd.DataFrame(test_rows)

    training_interactions = interactions.copy()

    for row in test_df.itertuples(index=False):

        matching_rows = training_interactions[
            (
                training_interactions["customer_id"]
                == row.customer_id
            )
            & (
                training_interactions["product_id"]
                == row.product_id
            )
            & (
                training_interactions["purchased"] == 1
            )
        ]

        if not matching_rows.empty:

            remove_index = matching_rows.index[-1]

            training_interactions = (
                training_interactions.drop(
                    index=remove_index
                )
            )

    print(
        "\nTraining interactions:",
        len(training_interactions)
    )

    print(
        "Held-out test purchases:",
        len(test_df)
    )

    return training_interactions, test_df


# ============================================================
# INTERACTION MATRIX
# ============================================================

def create_interaction_matrix(interactions):
    """Create customer-product interaction matrix."""

    print(
        "\nCreating customer-product interaction matrix..."
    )

    aggregated = (
        interactions.groupby(
            ["customer_id", "product_id"]
        )["interaction_score"]
        .sum()
        .reset_index()
    )

    interaction_matrix = aggregated.pivot(
        index="customer_id",
        columns="product_id",
        values="interaction_score"
    ).fillna(0)

    print(
        "Interaction matrix shape:",
        interaction_matrix.shape
    )

    return interaction_matrix


# ============================================================
# ITEM SIMILARITY
# ============================================================

def calculate_item_similarity(interaction_matrix):
    """Calculate item-item cosine similarity."""

    print("\nCalculating item-item cosine similarity...")

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
        item_similarity.shape
    )

    return item_similarity


# ============================================================
# POPULARITY SCORE
# ============================================================

def calculate_popularity_scores(interactions):
    """Calculate normalized product popularity scores."""

    print("\nCalculating product popularity scores...")

    popularity = (
        interactions.groupby("product_id")[
            "interaction_score"
        ]
        .sum()
    )

    maximum = popularity.max()

    if maximum > 0:
        popularity = popularity / maximum

    print("Popularity scores created successfully.")

    return popularity


# ============================================================
# CUSTOMER NEIGHBORHOOD
# ============================================================

def train_customer_neighborhood(interaction_matrix):
    """Train nearest-neighbor model using customer behavior."""

    print("\nTraining customer neighborhood model...")

    neighbor_count = min(
        NUMBER_OF_NEIGHBORS + 1,
        len(interaction_matrix)
    )

    model = NearestNeighbors(
        n_neighbors=neighbor_count,
        metric="cosine",
        algorithm="brute",
    )

    model.fit(interaction_matrix.values)

    print(
        "Customer neighborhood model trained successfully."
    )

    return model


# ============================================================
# CUSTOMER SEGMENT MAPPING
# ============================================================

def create_segment_mapping(customer_segments):
    """Create customer-to-cluster mapping."""

    customer_segments["customer_id"] = (
        customer_segments["customer_id"]
        .astype(int)
    )

    segment_mapping = (
        customer_segments
        .set_index("customer_id")["cluster"]
        .to_dict()
    )

    print("\nCustomer segment mapping created.")

    print("Segment distribution:")

    print(
        customer_segments["cluster"]
        .value_counts()
        .sort_index()
    )

    return segment_mapping


# ============================================================
# SEGMENT PRODUCT PREFERENCES
# ============================================================

def calculate_segment_preferences(
    interactions,
    segment_mapping,
):
    """Calculate normalized product preferences by segment."""

    print(
        "\nCalculating customer segment product preferences..."
    )

    segment_interactions = interactions.copy()

    segment_interactions["cluster"] = (
        segment_interactions["customer_id"]
        .map(segment_mapping)
    )

    segment_interactions = segment_interactions.dropna(
        subset=["cluster"]
    )

    segment_preferences = (
        segment_interactions.groupby(
            ["cluster", "product_id"]
        )["interaction_score"]
        .sum()
        .unstack(fill_value=0)
    )

    segment_preferences = (
        segment_preferences.div(
            segment_preferences.max(axis=1),
            axis=0,
        )
        .fillna(0)
    )

    print(
        "Segment preference scores created successfully."
    )

    return segment_preferences


# ============================================================
# SCORE NORMALIZATION
# ============================================================

def normalize_scores(scores):
    """Min-max normalize recommendation scores."""

    scores = scores.astype(float)

    minimum = scores.min()
    maximum = scores.max()

    if maximum == minimum:
        return pd.Series(
            0.0,
            index=scores.index
        )

    return (
        (scores - minimum)
        / (maximum - minimum)
    )


# ============================================================
# ITEM-BASED CF SCORE
# ============================================================

def calculate_item_cf_scores(
    customer_vector,
    item_similarity,
):
    """Calculate item-based collaborative filtering scores."""

    interacted_products = customer_vector[
        customer_vector > 0
    ]

    if interacted_products.empty:

        return pd.Series(
            0.0,
            index=item_similarity.index
        )

    valid_products = [
        product_id
        for product_id in interacted_products.index
        if product_id in item_similarity.columns
    ]

    if not valid_products:

        return pd.Series(
            0.0,
            index=item_similarity.index
        )

    similarities = item_similarity[
        valid_products
    ]

    weights = interacted_products[
        valid_products
    ]

    weighted_scores = similarities.dot(
        weights.values
    )

    weight_sum = weights.sum()

    if weight_sum > 0:
        weighted_scores = (
            weighted_scores / weight_sum
        )

    return normalize_scores(weighted_scores)


# ============================================================
# CUSTOMER NEIGHBOR SCORE
# ============================================================

def calculate_neighbor_scores(
    customer_id,
    interaction_matrix,
    neighbor_model,
):
    """
    Calculate recommendation scores using behavior
    of similar customers.
    """

    product_ids = interaction_matrix.columns

    if customer_id not in interaction_matrix.index:

        return pd.Series(
            0.0,
            index=product_ids
        )

    customer_position = (
        interaction_matrix.index.get_loc(customer_id)
    )

    customer_vector = (
        interaction_matrix.iloc[
            customer_position
        ].values.reshape(1, -1)
    )

    distances, indices = (
        neighbor_model.kneighbors(
            customer_vector
        )
    )

    distances = distances.flatten()
    indices = indices.flatten()

    neighbor_scores = np.zeros(
        interaction_matrix.shape[1],
        dtype=float
    )

    total_similarity = 0.0

    for distance, neighbor_position in zip(
        distances,
        indices,
    ):

        neighbor_id = (
            interaction_matrix.index[
                neighbor_position
            ]
        )

        if neighbor_id == customer_id:
            continue

        similarity = max(
            0.0,
            1.0 - distance
        )

        if similarity <= 0:
            continue

        neighbor_vector = (
            interaction_matrix.iloc[
                neighbor_position
            ].values
        )

        neighbor_scores += (
            similarity * neighbor_vector
        )

        total_similarity += similarity

    if total_similarity > 0:

        neighbor_scores = (
            neighbor_scores / total_similarity
        )

    neighbor_scores = pd.Series(
        neighbor_scores,
        index=product_ids,
    )

    return normalize_scores(neighbor_scores)


# ============================================================
# SEGMENT SCORE
# ============================================================

def calculate_segment_scores(
    customer_id,
    product_ids,
    segment_mapping,
    segment_preferences,
):
    """Get segment-level product preference scores."""

    cluster = segment_mapping.get(customer_id)

    if (
        cluster is None
        or cluster not in segment_preferences.index
    ):

        return pd.Series(
            0.0,
            index=product_ids
        )

    return (
        segment_preferences.loc[cluster]
        .reindex(product_ids)
        .fillna(0)
    )


# ============================================================
# DIVERSIFIED RERANKING
# ============================================================

def diversified_rerank(
    candidate_scores,
    item_similarity,
    top_k=TOP_K,
):
    """
    Apply MMR-style diversified reranking.

    Balances recommendation relevance and item diversity.
    """

    selected_products = []

    remaining_products = list(
        candidate_scores.index
    )

    while (
        len(selected_products) < top_k
        and remaining_products
    ):

        best_product = None
        best_score = -np.inf

        for product_id in remaining_products:

            relevance = candidate_scores.loc[
                product_id
            ]

            if not selected_products:

                diversity_penalty = 0.0

            else:

                similarities = []

                for selected_product in selected_products:

                    if (
                        product_id
                        in item_similarity.index
                        and selected_product
                        in item_similarity.columns
                    ):

                        similarities.append(
                            item_similarity.loc[
                                product_id,
                                selected_product,
                            ]
                        )

                diversity_penalty = (
                    max(similarities)
                    if similarities
                    else 0.0
                )

            reranking_score = (
                DIVERSITY_LAMBDA * relevance
                - (
                    1 - DIVERSITY_LAMBDA
                )
                * diversity_penalty
            )

            if reranking_score > best_score:

                best_score = reranking_score
                best_product = product_id

        if best_product is None:
            break

        selected_products.append(best_product)

        remaining_products.remove(best_product)

    return selected_products


# ============================================================
# ITEM-BASED RECOMMENDATIONS
# ============================================================

def recommend_item_cf(
    customer_id,
    interaction_matrix,
    item_similarity,
    top_k=TOP_K,
):
    """Generate Item-Based CF recommendations."""

    if customer_id not in interaction_matrix.index:
        return []

    customer_vector = interaction_matrix.loc[
        customer_id
    ]

    scores = calculate_item_cf_scores(
        customer_vector,
        item_similarity,
    )

    seen_products = set(
        customer_vector[
            customer_vector > 0
        ].index
    )

    scores = scores.drop(
        labels=list(seen_products),
        errors="ignore",
    )

    return (
        scores.sort_values(
            ascending=False
        )
        .head(top_k)
        .index
        .tolist()
    )


# ============================================================
# DIVERSIFIED HYBRID RECOMMENDATIONS
# ============================================================

def recommend_diversified_hybrid(
    customer_id,
    interaction_matrix,
    item_similarity,
    neighbor_model,
    popularity_scores,
    segment_mapping,
    segment_preferences,
    top_k=TOP_K,
):
    """
    Generate diversified hybrid recommendations using:

    - Item-Based CF
    - Customer neighborhood behavior
    - Segment preferences
    - Product popularity
    - MMR-style diversified reranking
    """

    product_ids = interaction_matrix.columns

    if customer_id not in interaction_matrix.index:

        fallback = (
            popularity_scores
            .reindex(product_ids)
            .fillna(0)
            .sort_values(ascending=False)
            .head(top_k)
        )

        return fallback.index.tolist()

    customer_vector = interaction_matrix.loc[
        customer_id
    ]

    item_cf_scores = calculate_item_cf_scores(
        customer_vector,
        item_similarity,
    )

    neighbor_scores = calculate_neighbor_scores(
        customer_id,
        interaction_matrix,
        neighbor_model,
    )

    segment_scores = calculate_segment_scores(
        customer_id,
        product_ids,
        segment_mapping,
        segment_preferences,
    )

    popularity = (
        popularity_scores
        .reindex(product_ids)
        .fillna(0)
    )

    hybrid_scores = (
        ITEM_CF_WEIGHT * item_cf_scores
        + NEIGHBOR_WEIGHT * neighbor_scores
        + SEGMENT_WEIGHT * segment_scores
        + POPULARITY_WEIGHT * popularity
    )

    seen_products = set(
        customer_vector[
            customer_vector > 0
        ].index
    )

    hybrid_scores = hybrid_scores.drop(
        labels=list(seen_products),
        errors="ignore",
    )

    candidate_scores = (
        hybrid_scores.sort_values(
            ascending=False
        )
        .head(CANDIDATE_POOL_SIZE)
    )

    return diversified_rerank(
        candidate_scores,
        item_similarity,
        top_k=top_k,
    )


# ============================================================
# RECOMMENDER EVALUATION
# ============================================================

def evaluate_recommender(
    algorithm_name,
    test_df,
    recommendation_function,
    total_products,
):
    """Evaluate a recommender using Top-K metrics."""

    print(
        f"\nEvaluating {algorithm_name}..."
    )

    evaluation_rows = []

    recommended_catalog = set()

    for row in test_df.itertuples(index=False):

        customer_id = row.customer_id
        actual_product = row.product_id

        recommendations = recommendation_function(
            customer_id
        )

        recommended_catalog.update(
            recommendations
        )

        hit = int(
            actual_product in recommendations
        )

        precision = (
            hit / TOP_K
            if recommendations
            else 0.0
        )

        recall = float(hit)

        reciprocal_rank = 0.0

        if hit:

            rank = (
                recommendations.index(
                    actual_product
                )
                + 1
            )

            reciprocal_rank = 1 / rank

        evaluation_rows.append(
            {
                "customer_id": customer_id,
                "actual_product": actual_product,
                "hit": hit,
                "precision": precision,
                "recall": recall,
                "reciprocal_rank": reciprocal_rank,
            }
        )

    evaluation_df = pd.DataFrame(
        evaluation_rows
    )

    metrics = {
        "Algorithm": algorithm_name,
        "Hit Rate@5": evaluation_df[
            "hit"
        ].mean(),
        "Precision@5": evaluation_df[
            "precision"
        ].mean(),
        "Recall@5": evaluation_df[
            "recall"
        ].mean(),
        "MRR@5": evaluation_df[
            "reciprocal_rank"
        ].mean(),
        "Coverage@5": (
            len(recommended_catalog)
            / total_products
        ),
    }

    print(
        f"Hit Rate@5  : "
        f"{metrics['Hit Rate@5']:.6f}"
    )

    print(
        f"Precision@5 : "
        f"{metrics['Precision@5']:.6f}"
    )

    print(
        f"Recall@5    : "
        f"{metrics['Recall@5']:.6f}"
    )

    print(
        f"MRR@5       : "
        f"{metrics['MRR@5']:.6f}"
    )

    print(
        f"Coverage@5  : "
        f"{metrics['Coverage@5']:.6f}"
    )

    return metrics, evaluation_df


# ============================================================
# VISUALIZATION
# ============================================================

def create_comparison_figure(comparison_df):
    """Create recommender comparison visualization."""

    metric_columns = [
        "Hit Rate@5",
        "MRR@5",
        "Coverage@5",
    ]

    plot_df = (
        comparison_df
        .set_index("Algorithm")[
            metric_columns
        ]
    )

    ax = plot_df.plot(
        kind="bar",
        figsize=(11, 6),
    )

    ax.set_title(
        "Diversified Behavioral Recommender Comparison"
    )

    ax.set_xlabel("Recommendation Algorithm")
    ax.set_ylabel("Metric Value")

    plt.xticks(rotation=15)
    plt.tight_layout()

    output_path = (
        FIGURE_PATH
        / "diversified_hybrid_comparison.png"
    )

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    print(
        "\nComparison figure saved:",
        output_path
    )


# ============================================================
# MAIN
# ============================================================

def main():

    df, customer_segments = load_data()

    interactions = create_interaction_scores(df)

    (
        training_interactions,
        test_df,
    ) = create_evaluation_split(interactions)

    interaction_matrix = create_interaction_matrix(
        training_interactions
    )

    item_similarity = calculate_item_similarity(
        interaction_matrix
    )

    popularity_scores = calculate_popularity_scores(
        training_interactions
    )

    neighbor_model = train_customer_neighborhood(
        interaction_matrix
    )

    segment_mapping = create_segment_mapping(
        customer_segments
    )

    segment_preferences = (
        calculate_segment_preferences(
            training_interactions,
            segment_mapping,
        )
    )

    total_products = interaction_matrix.shape[1]

    item_cf_metrics, item_cf_evaluation = (
        evaluate_recommender(
            "Item-Based CF",
            test_df,
            lambda customer_id: recommend_item_cf(
                customer_id,
                interaction_matrix,
                item_similarity,
            ),
            total_products,
        )
    )

    diversified_metrics, diversified_evaluation = (
        evaluate_recommender(
            "Diversified Behavioral Hybrid",
            test_df,
            lambda customer_id:
            recommend_diversified_hybrid(
                customer_id,
                interaction_matrix,
                item_similarity,
                neighbor_model,
                popularity_scores,
                segment_mapping,
                segment_preferences,
            ),
            total_products,
        )
    )

    comparison_df = pd.DataFrame(
        [
            item_cf_metrics,
            diversified_metrics,
        ]
    )

    print(
        "\n"
        + "=" * 75
    )

    print(
        "DIVERSIFIED HYBRID RECOMMENDER COMPARISON"
    )

    print(
        "=" * 75
    )

    print(
        comparison_df.to_string(index=False)
    )

    baseline_hit_rate = item_cf_metrics[
        "Hit Rate@5"
    ]

    diversified_hit_rate = diversified_metrics[
        "Hit Rate@5"
    ]

    if baseline_hit_rate > 0:

        hit_rate_change = (
            (
                diversified_hit_rate
                - baseline_hit_rate
            )
            / baseline_hit_rate
            * 100
        )

    else:
        hit_rate_change = 0.0

    baseline_mrr = item_cf_metrics["MRR@5"]

    diversified_mrr = diversified_metrics[
        "MRR@5"
    ]

    if baseline_mrr > 0:

        mrr_change = (
            (
                diversified_mrr
                - baseline_mrr
            )
            / baseline_mrr
            * 100
        )

    else:
        mrr_change = 0.0

    print("\n--- IMPROVEMENT ANALYSIS ---")

    print(
        "Item-Based CF Hit Rate@5:",
        f"{baseline_hit_rate:.6f}"
    )

    print(
        "Diversified Hybrid Hit Rate@5:",
        f"{diversified_hit_rate:.6f}"
    )

    print(
        "Relative Hit Rate Change:",
        f"{hit_rate_change:.2f}%"
    )

    print(
        "\nItem-Based CF MRR@5:",
        f"{baseline_mrr:.6f}"
    )

    print(
        "Diversified Hybrid MRR@5:",
        f"{diversified_mrr:.6f}"
    )

    print(
        "Relative MRR Change:",
        f"{mrr_change:.2f}%"
    )

    print(
        "\nDiversified Hybrid Coverage@5:",
        f"{diversified_metrics['Coverage@5']:.6f}"
    )

    create_comparison_figure(
        comparison_df
    )

    comparison_output = (
        RESULTS_PATH
        / "diversified_hybrid_comparison.csv"
    )

    item_cf_output = (
        RESULTS_PATH
        / "diversified_item_cf_evaluation.csv"
    )

    diversified_output = (
        RESULTS_PATH
        / "diversified_hybrid_evaluation.csv"
    )

    model_output = (
        MODEL_PATH
        / "diversified_hybrid_recommender.pkl"
    )

    comparison_df.to_csv(
        comparison_output,
        index=False
    )

    item_cf_evaluation.to_csv(
        item_cf_output,
        index=False
    )

    diversified_evaluation.to_csv(
        diversified_output,
        index=False
    )

    model_artifact = {
        "interaction_matrix": interaction_matrix,
        "item_similarity": item_similarity,
        "neighbor_model": neighbor_model,
        "popularity_scores": popularity_scores,
        "segment_mapping": segment_mapping,
        "segment_preferences": segment_preferences,
        "weights": {
            "item_cf": ITEM_CF_WEIGHT,
            "customer_neighbor": NEIGHBOR_WEIGHT,
            "segment": SEGMENT_WEIGHT,
            "popularity": POPULARITY_WEIGHT,
        },
        "diversity_lambda": DIVERSITY_LAMBDA,
        "candidate_pool_size": CANDIDATE_POOL_SIZE,
        "top_k": TOP_K,
    }

    with open(
        model_output,
        "wb"
    ) as file:

        pickle.dump(
            model_artifact,
            file
        )

    print(
        "\nComparison saved:",
        comparison_output
    )

    print(
        "Item-CF evaluation saved:",
        item_cf_output
    )

    print(
        "Diversified hybrid evaluation saved:",
        diversified_output
    )

    print(
        "Diversified hybrid model saved:",
        model_output
    )

    print(
        "\nDiversified hybrid recommender "
        "experiment completed successfully."
    )


if __name__ == "__main__":
    main()