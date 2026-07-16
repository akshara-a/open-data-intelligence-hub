from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "Ecommerce.csv"
)

CUSTOMER_SEGMENTS_PATH = (
    PROJECT_ROOT
    / "outputs"
    / "results"
    / "customer_segments.csv"
)

RESULTS_PATH = (
    PROJECT_ROOT
    / "outputs"
    / "results"
)

FIGURE_PATH = (
    PROJECT_ROOT
    / "outputs"
    / "figures"
)

RESULTS_PATH.mkdir(
    parents=True,
    exist_ok=True,
)

FIGURE_PATH.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# CONFIGURATION
# ============================================================

TOP_K = 5

SVD_COMPONENTS = 50

NUMBER_OF_NEIGHBORS = 20

CANDIDATE_POOL_SIZE = 50

DIVERSITY_LAMBDA = 0.80

RANDOM_STATE = 42


# CURRENT HYBRID WEIGHTS

HYBRID_ITEM_WEIGHT = 0.55
HYBRID_POPULARITY_WEIGHT = 0.20
HYBRID_SEGMENT_WEIGHT = 0.15
HYBRID_HISTORY_WEIGHT = 0.10


# DIVERSIFIED BEHAVIORAL HYBRID WEIGHTS

DIVERSIFIED_ITEM_WEIGHT = 0.55
DIVERSIFIED_NEIGHBOR_WEIGHT = 0.25
DIVERSIFIED_SEGMENT_WEIGHT = 0.15
DIVERSIFIED_POPULARITY_WEIGHT = 0.05


# ============================================================
# LOAD DATA
# ============================================================

def load_data():
    """Load e-commerce and customer segment data."""

    print("Loading project data...")

    df = pd.read_csv(DATA_PATH)

    customer_segments = pd.read_csv(
        CUSTOMER_SEGMENTS_PATH
    )

    print("Project data loaded successfully.")

    print(
        "E-commerce sessions:",
        len(df)
    )

    print(
        "Customer profiles:",
        len(customer_segments)
    )

    print(
        "Unique customers:",
        df["customer_id"].nunique()
    )

    print(
        "Unique products:",
        df["product_id"].nunique()
    )

    return df, customer_segments


# ============================================================
# PREPARE TEMPORAL DATA
# ============================================================

def prepare_temporal_data(df):
    """
    Convert visit dates to datetime and create deterministic
    chronological ordering.
    """

    print(
        "\nPreparing temporal interaction data..."
    )

    temporal_df = df.copy()

    temporal_df["visit_date"] = pd.to_datetime(
        temporal_df["visit_date"],
        errors="coerce",
    )

    invalid_dates = (
        temporal_df["visit_date"]
        .isna()
        .sum()
    )

    print(
        "Invalid visit dates:",
        invalid_dates
    )

    if invalid_dates > 0:

        temporal_df = temporal_df.dropna(
            subset=["visit_date"]
        )

    temporal_df = (
        temporal_df.sort_values(
            [
                "customer_id",
                "visit_date",
                "session_id",
            ]
        )
        .reset_index(drop=True)
    )

    print(
        "Temporal ordering completed."
    )

    print(
        "Dataset date range:",
        temporal_df["visit_date"].min(),
        "to",
        temporal_df["visit_date"].max(),
    )

    return temporal_df


# ============================================================
# CREATE INTERACTION SCORES
# ============================================================

def create_interaction_scores(df):
    """Create implicit interaction scores."""

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
        interactions["interaction_score"]
        .value_counts()
        .sort_index()
    )

    return interactions


# ============================================================
# STANDARDIZED TEMPORAL HOLDOUT
# ============================================================

def create_temporal_holdout(interactions):
    """
    Hold out the latest unique purchased product for each
    customer with at least two unique purchased products.
    """

    print(
        "\nCreating standardized temporal "
        "leave-one-purchase-out split..."
    )

    purchased = interactions[
        interactions["purchased"] == 1
    ].copy()

    unique_purchase_counts = (
        purchased.groupby(
            "customer_id"
        )["product_id"]
        .nunique()
    )

    eligible_customers = (
        unique_purchase_counts[
            unique_purchase_counts >= 2
        ]
        .index
    )

    print(
        "\n--- EVALUATION ELIGIBILITY ---"
    )

    print(
        "Customers with at least 2 unique purchases:",
        len(eligible_customers)
    )

    test_rows = []

    remove_indices = []

    for customer_id in eligible_customers:

        customer_purchases = purchased[
            purchased["customer_id"]
            == customer_id
        ].copy()

        customer_purchases = (
            customer_purchases.sort_values(
                [
                    "visit_date",
                    "session_id",
                ]
            )
        )

        latest_product = (
            customer_purchases.iloc[-1][
                "product_id"
            ]
        )

        latest_product_rows = (
            customer_purchases[
                customer_purchases["product_id"]
                == latest_product
            ]
        )

        latest_row = (
            latest_product_rows.iloc[-1]
        )

        test_rows.append(
            {
                "customer_id": int(
                    customer_id
                ),
                "product_id": int(
                    latest_product
                ),
                "visit_date": latest_row[
                    "visit_date"
                ],
                "session_id": int(
                    latest_row["session_id"]
                ),
            }
        )

        remove_indices.extend(
            interactions[
                (
                    interactions["customer_id"]
                    == customer_id
                )
                & (
                    interactions["product_id"]
                    == latest_product
                )
            ].index.tolist()
        )

    test_df = pd.DataFrame(
        test_rows
    )

    training_interactions = (
        interactions.drop(
            index=remove_indices
        )
        .copy()
    )

    print(
        "\nTraining interactions:",
        len(training_interactions)
    )

    print(
        "Held-out test purchases:",
        len(test_df)
    )

    print(
        "Removed customer-product interaction rows:",
        len(remove_indices)
    )

    print(
        "\nTest purchase date range:",
        test_df["visit_date"].min(),
        "to",
        test_df["visit_date"].max(),
    )

    print(
        "\n--- SAMPLE TEMPORAL HOLDOUT ---"
    )

    print(
        test_df.head(10).to_string(
            index=False
        )
    )

    return (
        training_interactions,
        test_df,
    )


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
            [
                "customer_id",
                "product_id",
            ]
        )["interaction_score"]
        .sum()
        .reset_index()
    )

    interaction_matrix = (
        aggregated.pivot(
            index="customer_id",
            columns="product_id",
            values="interaction_score",
        )
        .fillna(0)
    )

    interaction_matrix.index = (
        interaction_matrix.index.astype(int)
    )

    interaction_matrix.columns = (
        interaction_matrix.columns.astype(int)
    )

    print(
        "Interaction matrix shape:",
        interaction_matrix.shape
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
        item_similarity.shape
    )

    return item_similarity


# ============================================================
# POPULARITY
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
        interactions.groupby(
            "product_id"
        )["interaction_score"]
        .sum()
        .reindex(
            product_ids,
            fill_value=0,
        )
        .astype(float)
    )

    maximum = popularity.max()

    if maximum > 0:

        popularity = (
            popularity / maximum
        )

    print(
        "Popularity scores created successfully."
    )

    return popularity


# ============================================================
# SEGMENT MAPPING
# ============================================================

def create_segment_mapping(
    customer_segments,
):
    """Create customer-to-cluster mapping."""

    customer_segments = (
        customer_segments.copy()
    )

    customer_segments["customer_id"] = (
        customer_segments["customer_id"]
        .astype(int)
    )

    segment_mapping = (
        customer_segments
        .set_index(
            "customer_id"
        )["cluster"]
        .to_dict()
    )

    print(
        "\nCustomer segment mapping created."
    )

    print(
        "Segment distribution:"
    )

    print(
        customer_segments["cluster"]
        .value_counts()
        .sort_index()
    )

    return segment_mapping


# ============================================================
# SEGMENT PREFERENCES
# ============================================================

def calculate_segment_preferences(
    interactions,
    segment_mapping,
    product_ids,
):
    """Calculate product preferences by segment."""

    print(
        "\nCalculating segment product preferences..."
    )

    segment_interactions = (
        interactions.copy()
    )

    segment_interactions["cluster"] = (
        segment_interactions["customer_id"]
        .map(segment_mapping)
    )

    segment_interactions = (
        segment_interactions.dropna(
            subset=["cluster"]
        )
    )

    segment_preferences = (
        segment_interactions.groupby(
            [
                "cluster",
                "product_id",
            ]
        )["interaction_score"]
        .sum()
        .unstack(fill_value=0)
        .reindex(
            columns=product_ids,
            fill_value=0,
        )
        .astype(float)
    )

    row_maximum = (
        segment_preferences.max(axis=1)
        .replace(0, 1)
    )

    segment_preferences = (
        segment_preferences.div(
            row_maximum,
            axis=0,
        )
    )

    print(
        "Segment preference scores created successfully."
    )

    return segment_preferences


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_scores(scores):
    """Min-max normalize scores."""

    scores = scores.astype(float)

    minimum = scores.min()
    maximum = scores.max()

    if maximum == minimum:

        return pd.Series(
            0.0,
            index=scores.index,
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
    """Calculate Item-Based CF recommendation scores."""

    interacted_products = customer_vector[
        customer_vector > 0
    ]

    if interacted_products.empty:

        return pd.Series(
            0.0,
            index=item_similarity.index,
        )

    valid_products = [
        product_id
        for product_id
        in interacted_products.index
        if product_id
        in item_similarity.columns
    ]

    if not valid_products:

        return pd.Series(
            0.0,
            index=item_similarity.index,
        )

    similarity_scores = (
        item_similarity[
            valid_products
        ]
    )

    weights = (
        interacted_products[
            valid_products
        ]
    )

    scores = similarity_scores.dot(
        weights.values
    )

    weight_sum = weights.sum()

    if weight_sum > 0:

        scores = (
            scores / weight_sum
        )

    return normalize_scores(scores)


# ============================================================
# POPULARITY RECOMMENDER
# ============================================================

def recommend_popularity(
    customer_id,
    interaction_matrix,
    popularity_scores,
    top_k=TOP_K,
):
    """Generate popularity-based recommendations."""

    scores = popularity_scores.copy()

    if customer_id in interaction_matrix.index:

        customer_vector = (
            interaction_matrix.loc[
                customer_id
            ]
        )

        seen_products = (
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
# ITEM-BASED CF RECOMMENDER
# ============================================================

def recommend_item_cf(
    customer_id,
    interaction_matrix,
    item_similarity,
    popularity_scores,
    top_k=TOP_K,
):
    """Generate Item-Based CF recommendations."""

    if customer_id not in interaction_matrix.index:

        return recommend_popularity(
            customer_id,
            interaction_matrix,
            popularity_scores,
            top_k,
        )

    customer_vector = (
        interaction_matrix.loc[
            customer_id
        ]
    )

    scores = calculate_item_cf_scores(
        customer_vector,
        item_similarity,
    )

    seen_products = (
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
# SVD MODEL
# ============================================================

def train_svd(interaction_matrix):
    """Train Truncated SVD recommender."""

    print(
        "\nTraining Truncated SVD..."
    )

    max_components = min(
        interaction_matrix.shape
    ) - 1

    number_of_components = min(
        SVD_COMPONENTS,
        max_components,
    )

    svd = TruncatedSVD(
        n_components=number_of_components,
        random_state=RANDOM_STATE,
    )

    customer_factors = svd.fit_transform(
        interaction_matrix.values
    )

    reconstructed_scores = (
        customer_factors
        @ svd.components_
    )

    print(
        "SVD components:",
        number_of_components
    )

    print(
        "Explained variance ratio:",
        round(
            svd.explained_variance_ratio_.sum(),
            4,
        )
    )

    return svd, reconstructed_scores


# ============================================================
# SVD RECOMMENDER
# ============================================================

def recommend_svd(
    customer_id,
    interaction_matrix,
    reconstructed_scores,
    popularity_scores,
    top_k=TOP_K,
):
    """Generate Truncated SVD recommendations."""

    if customer_id not in interaction_matrix.index:

        return recommend_popularity(
            customer_id,
            interaction_matrix,
            popularity_scores,
            top_k,
        )

    customer_position = (
        interaction_matrix.index.get_loc(
            customer_id
        )
    )

    scores = pd.Series(
        reconstructed_scores[
            customer_position
        ],
        index=interaction_matrix.columns,
    )

    customer_vector = (
        interaction_matrix.loc[
            customer_id
        ]
    )

    seen_products = (
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
# CURRENT HYBRID
# ============================================================

def recommend_current_hybrid(
    customer_id,
    interaction_matrix,
    item_similarity,
    popularity_scores,
    segment_mapping,
    segment_preferences,
    top_k=TOP_K,
):
    """Generate current hybrid recommendations."""

    product_ids = (
        interaction_matrix.columns
    )

    if customer_id not in interaction_matrix.index:

        return recommend_popularity(
            customer_id,
            interaction_matrix,
            popularity_scores,
            top_k,
        )

    customer_vector = (
        interaction_matrix.loc[
            customer_id
        ]
    )

    item_scores = calculate_item_cf_scores(
        customer_vector,
        item_similarity,
    )

    popularity = (
        popularity_scores
        .reindex(product_ids)
        .fillna(0)
    )

    cluster = segment_mapping.get(
        customer_id
    )

    if (
        cluster is not None
        and cluster
        in segment_preferences.index
    ):

        segment_scores = (
            segment_preferences.loc[
                cluster
            ]
            .reindex(product_ids)
            .fillna(0)
        )

    else:

        segment_scores = pd.Series(
            0.0,
            index=product_ids,
        )

    history_scores = normalize_scores(
        customer_vector
        .reindex(product_ids)
        .fillna(0)
    )

    hybrid_scores = (
        HYBRID_ITEM_WEIGHT
        * item_scores
        + HYBRID_POPULARITY_WEIGHT
        * popularity
        + HYBRID_SEGMENT_WEIGHT
        * segment_scores
        + HYBRID_HISTORY_WEIGHT
        * history_scores
    )

    seen_products = (
        customer_vector[
            customer_vector > 0
        ].index
    )

    hybrid_scores = hybrid_scores.drop(
        labels=list(seen_products),
        errors="ignore",
    )

    return (
        hybrid_scores.sort_values(
            ascending=False
        )
        .head(top_k)
        .index
        .tolist()
    )


# ============================================================
# CUSTOMER NEIGHBORHOOD
# ============================================================

def train_customer_neighborhood(
    interaction_matrix,
):
    """Train customer nearest-neighbor model."""

    print(
        "\nTraining customer neighborhood model..."
    )

    neighbor_count = min(
        NUMBER_OF_NEIGHBORS + 1,
        len(interaction_matrix),
    )

    model = NearestNeighbors(
        n_neighbors=neighbor_count,
        metric="cosine",
        algorithm="brute",
    )

    model.fit(
        interaction_matrix.values
    )

    print(
        "Customer neighborhood model trained successfully."
    )

    return model


# ============================================================
# NEIGHBOR SCORE
# ============================================================

def calculate_neighbor_scores(
    customer_id,
    interaction_matrix,
    neighbor_model,
):
    """Calculate similar-customer recommendation scores."""

    product_ids = (
        interaction_matrix.columns
    )

    if customer_id not in interaction_matrix.index:

        return pd.Series(
            0.0,
            index=product_ids,
        )

    customer_position = (
        interaction_matrix.index.get_loc(
            customer_id
        )
    )

    customer_vector = (
        interaction_matrix.iloc[
            customer_position
        ]
        .values
        .reshape(1, -1)
    )

    distances, indices = (
        neighbor_model.kneighbors(
            customer_vector
        )
    )

    scores = np.zeros(
        interaction_matrix.shape[1],
        dtype=float,
    )

    total_similarity = 0.0

    for distance, neighbor_position in zip(
        distances.flatten(),
        indices.flatten(),
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
            1.0 - distance,
        )

        if similarity <= 0:
            continue

        neighbor_vector = (
            interaction_matrix.iloc[
                neighbor_position
            ].values
        )

        scores += (
            similarity
            * neighbor_vector
        )

        total_similarity += similarity

    if total_similarity > 0:

        scores = (
            scores
            / total_similarity
        )

    return normalize_scores(
        pd.Series(
            scores,
            index=product_ids,
        )
    )


# ============================================================
# DIVERSIFIED RERANKING
# ============================================================

def diversified_rerank(
    candidate_scores,
    item_similarity,
    top_k=TOP_K,
):
    """Apply MMR-style diversified reranking."""

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

            relevance = (
                candidate_scores.loc[
                    product_id
                ]
            )

            if not selected_products:

                diversity_penalty = 0.0

            else:

                similarities = [
                    item_similarity.loc[
                        product_id,
                        selected_product,
                    ]
                    for selected_product
                    in selected_products
                    if (
                        product_id
                        in item_similarity.index
                        and selected_product
                        in item_similarity.columns
                    )
                ]

                diversity_penalty = (
                    max(similarities)
                    if similarities
                    else 0.0
                )

            reranking_score = (
                DIVERSITY_LAMBDA
                * relevance
                - (
                    1
                    - DIVERSITY_LAMBDA
                )
                * diversity_penalty
            )

            if reranking_score > best_score:

                best_score = reranking_score
                best_product = product_id

        if best_product is None:
            break

        selected_products.append(
            best_product
        )

        remaining_products.remove(
            best_product
        )

    return selected_products


# ============================================================
# DIVERSIFIED HYBRID
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
    """Generate diversified behavioral hybrid recommendations."""

    product_ids = (
        interaction_matrix.columns
    )

    if customer_id not in interaction_matrix.index:

        return recommend_popularity(
            customer_id,
            interaction_matrix,
            popularity_scores,
            top_k,
        )

    customer_vector = (
        interaction_matrix.loc[
            customer_id
        ]
    )

    item_scores = calculate_item_cf_scores(
        customer_vector,
        item_similarity,
    )

    neighbor_scores = (
        calculate_neighbor_scores(
            customer_id,
            interaction_matrix,
            neighbor_model,
        )
    )

    popularity = (
        popularity_scores
        .reindex(product_ids)
        .fillna(0)
    )

    cluster = segment_mapping.get(
        customer_id
    )

    if (
        cluster is not None
        and cluster
        in segment_preferences.index
    ):

        segment_scores = (
            segment_preferences.loc[
                cluster
            ]
            .reindex(product_ids)
            .fillna(0)
        )

    else:

        segment_scores = pd.Series(
            0.0,
            index=product_ids,
        )

    hybrid_scores = (
        DIVERSIFIED_ITEM_WEIGHT
        * item_scores
        + DIVERSIFIED_NEIGHBOR_WEIGHT
        * neighbor_scores
        + DIVERSIFIED_SEGMENT_WEIGHT
        * segment_scores
        + DIVERSIFIED_POPULARITY_WEIGHT
        * popularity
    )

    seen_products = (
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
        top_k,
    )


# ============================================================
# EVALUATION
# ============================================================

def evaluate_recommender(
    algorithm_name,
    test_df,
    recommendation_function,
    total_products,
):
    """Evaluate recommender using standardized Top-K metrics."""

    print(
        f"\nEvaluating {algorithm_name}..."
    )

    evaluation_rows = []

    recommended_catalog = set()

    for row in test_df.itertuples(
        index=False
    ):

        customer_id = int(
            row.customer_id
        )

        actual_product = int(
            row.product_id
        )

        recommendations = (
            recommendation_function(
                customer_id
            )
        )

        recommendations = [
            int(product_id)
            for product_id
            in recommendations
        ]

        recommended_catalog.update(
            recommendations
        )

        hit = int(
            actual_product
            in recommendations
        )

        precision = (
            hit / TOP_K
            if recommendations
            else 0.0
        )

        recall = float(hit)

        reciprocal_rank = 0.0

        rank = None

        if hit:

            rank = (
                recommendations.index(
                    actual_product
                )
                + 1
            )

            reciprocal_rank = (
                1 / rank
            )

        evaluation_rows.append(
            {
                "customer_id": customer_id,
                "actual_product": actual_product,
                "recommendations": str(
                    recommendations
                ),
                "hit": hit,
                "rank": rank,
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
        "Hit Rate@5": (
            evaluation_df["hit"].mean()
        ),
        "Precision@5": (
            evaluation_df[
                "precision"
            ].mean()
        ),
        "Recall@5": (
            evaluation_df[
                "recall"
            ].mean()
        ),
        "MRR@5": (
            evaluation_df[
                "reciprocal_rank"
            ].mean()
        ),
        "Coverage@5": (
            len(recommended_catalog)
            / total_products
        ),
        "Unique Recommended Products": (
            len(recommended_catalog)
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

    print(
        "Unique recommended products:",
        metrics[
            "Unique Recommended Products"
        ]
    )

    return metrics, evaluation_df


# ============================================================
# COMPARISON FIGURE
# ============================================================

def create_comparison_figure(
    comparison_df,
):
    """Create final recommender comparison figure."""

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
        figsize=(12, 7),
    )

    ax.set_title(
        "Final Standardized Recommender Evaluation"
    )

    ax.set_xlabel(
        "Recommendation Algorithm"
    )

    ax.set_ylabel(
        "Metric Value"
    )

    plt.xticks(
        rotation=20,
        ha="right",
    )

    plt.tight_layout()

    output_path = (
        FIGURE_PATH
        / "final_recommender_comparison.png"
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

    df = prepare_temporal_data(df)

    interactions = (
        create_interaction_scores(df)
    )

    (
        training_interactions,
        test_df,
    ) = create_temporal_holdout(
        interactions
    )

    interaction_matrix = (
        create_interaction_matrix(
            training_interactions
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

    popularity_scores = (
        calculate_popularity_scores(
            training_interactions,
            product_ids,
        )
    )

    segment_mapping = (
        create_segment_mapping(
            customer_segments
        )
    )

    segment_preferences = (
        calculate_segment_preferences(
            training_interactions,
            segment_mapping,
            product_ids,
        )
    )

    (
        svd_model,
        reconstructed_scores,
    ) = train_svd(
        interaction_matrix
    )

    neighbor_model = (
        train_customer_neighborhood(
            interaction_matrix
        )
    )

    total_products = (
        interaction_matrix.shape[1]
    )

    evaluation_results = []

    evaluation_files = {}


    # --------------------------------------------------------
    # POPULARITY
    # --------------------------------------------------------

    metrics, evaluation_df = (
        evaluate_recommender(
            "Popularity-Based",
            test_df,
            lambda customer_id:
            recommend_popularity(
                customer_id,
                interaction_matrix,
                popularity_scores,
            ),
            total_products,
        )
    )

    evaluation_results.append(
        metrics
    )

    evaluation_files[
        "final_popularity_evaluation.csv"
    ] = evaluation_df


    # --------------------------------------------------------
    # ITEM-BASED CF
    # --------------------------------------------------------

    metrics, evaluation_df = (
        evaluate_recommender(
            "Item-Based CF",
            test_df,
            lambda customer_id:
            recommend_item_cf(
                customer_id,
                interaction_matrix,
                item_similarity,
                popularity_scores,
            ),
            total_products,
        )
    )

    evaluation_results.append(
        metrics
    )

    evaluation_files[
        "final_item_cf_evaluation.csv"
    ] = evaluation_df


    # --------------------------------------------------------
    # TRUNCATED SVD
    # --------------------------------------------------------

    metrics, evaluation_df = (
        evaluate_recommender(
            "Truncated SVD",
            test_df,
            lambda customer_id:
            recommend_svd(
                customer_id,
                interaction_matrix,
                reconstructed_scores,
                popularity_scores,
            ),
            total_products,
        )
    )

    evaluation_results.append(
        metrics
    )

    evaluation_files[
        "final_svd_evaluation.csv"
    ] = evaluation_df


    # --------------------------------------------------------
    # CURRENT HYBRID
    # --------------------------------------------------------

    metrics, evaluation_df = (
        evaluate_recommender(
            "Hybrid Behavioral Recommender",
            test_df,
            lambda customer_id:
            recommend_current_hybrid(
                customer_id,
                interaction_matrix,
                item_similarity,
                popularity_scores,
                segment_mapping,
                segment_preferences,
            ),
            total_products,
        )
    )

    evaluation_results.append(
        metrics
    )

    evaluation_files[
        "final_hybrid_evaluation.csv"
    ] = evaluation_df


    # --------------------------------------------------------
    # DIVERSIFIED HYBRID
    # --------------------------------------------------------

    metrics, evaluation_df = (
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

    evaluation_results.append(
        metrics
    )

    evaluation_files[
        "final_diversified_evaluation.csv"
    ] = evaluation_df


    # ========================================================
    # FINAL COMPARISON
    # ========================================================

    comparison_df = pd.DataFrame(
        evaluation_results
    )

    comparison_df = (
        comparison_df.sort_values(
            [
                "Hit Rate@5",
                "MRR@5",
            ],
            ascending=False,
        )
        .reset_index(drop=True)
    )

    print(
        "\n"
        + "=" * 100
    )

    print(
        "FINAL STANDARDIZED RECOMMENDER COMPARISON"
    )

    print(
        "=" * 100
    )

    print(
        comparison_df.to_string(
            index=False
        )
    )

    best_model = (
        comparison_df.iloc[0]
    )

    print(
        "\n--- FINAL BEST RECOMMENDER ---"
    )

    print(
        "Algorithm:",
        best_model["Algorithm"]
    )

    print(
        "Hit Rate@5:",
        f"{best_model['Hit Rate@5']:.6f}"
    )

    print(
        "Precision@5:",
        f"{best_model['Precision@5']:.6f}"
    )

    print(
        "Recall@5:",
        f"{best_model['Recall@5']:.6f}"
    )

    print(
        "MRR@5:",
        f"{best_model['MRR@5']:.6f}"
    )

    print(
        "Coverage@5:",
        f"{best_model['Coverage@5']:.6f}"
    )

    print(
        "Unique Recommended Products:",
        int(
            best_model[
                "Unique Recommended Products"
            ]
        )
    )


    # ========================================================
    # SAVE RESULTS
    # ========================================================

    comparison_output = (
        RESULTS_PATH
        / "final_recommender_comparison.csv"
    )

    holdout_output = (
        RESULTS_PATH
        / "final_recommender_holdout.csv"
    )

    comparison_df.to_csv(
        comparison_output,
        index=False,
    )

    test_df.to_csv(
        holdout_output,
        index=False,
    )

    for (
        file_name,
        evaluation_df,
    ) in evaluation_files.items():

        evaluation_df.to_csv(
            RESULTS_PATH / file_name,
            index=False,
        )

    create_comparison_figure(
        comparison_df
    )

    print(
        "\nFinal comparison saved:",
        comparison_output
    )

    print(
        "Standardized holdout saved:",
        holdout_output
    )

    print(
        "\nFinal standardized recommender "
        "evaluation completed successfully."
    )


if __name__ == "__main__":
    main()