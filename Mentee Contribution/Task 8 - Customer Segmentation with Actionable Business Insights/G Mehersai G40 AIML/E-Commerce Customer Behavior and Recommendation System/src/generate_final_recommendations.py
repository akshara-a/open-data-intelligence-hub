from pathlib import Path
import pickle

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "Ecommerce.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "outputs"
    / "results"
)

MODEL_DIR = (
    PROJECT_ROOT
    / "models"
)

FINAL_RECOMMENDATIONS_PATH = (
    OUTPUT_DIR
    / "final_recommendations.csv"
)

FINAL_RECOMMENDER_PATH = (
    MODEL_DIR
    / "final_item_cf_recommender.pkl"
)


# ============================================================
# CONFIGURATION
# ============================================================

TOP_K = 5

VIEW_SCORE = 1
CART_SCORE = 3
PURCHASE_SCORE = 7


# ============================================================
# LOAD DATA
# ============================================================

def load_data():
    print("Loading e-commerce dataset...")

    ecommerce_df = pd.read_csv(
        DATA_PATH
    )

    print("Dataset loaded successfully.")
    print(
        "Dataset shape:",
        ecommerce_df.shape
    )

    print(
        "Unique customers:",
        ecommerce_df[
            "customer_id"
        ].nunique()
    )

    print(
        "Unique products:",
        ecommerce_df[
            "product_id"
        ].nunique()
    )

    return ecommerce_df


# ============================================================
# CREATE IMPLICIT INTERACTION SCORES
# ============================================================

def create_interaction_scores(
    ecommerce_df,
):
    print(
        "\nCreating implicit interaction scores..."
    )

    interaction_df = ecommerce_df.copy()

    interaction_df[
        "interaction_score"
    ] = np.select(
        [
            interaction_df[
                "purchased"
            ].eq(1),
            interaction_df[
                "added_to_cart"
            ].eq(1),
        ],
        [
            PURCHASE_SCORE,
            CART_SCORE,
        ],
        default=VIEW_SCORE,
    )

    print(
        "\n--- INTERACTION SCORE DISTRIBUTION ---"
    )

    print(
        interaction_df[
            "interaction_score"
        ].value_counts().sort_index()
    )

    return interaction_df


# ============================================================
# AGGREGATE CUSTOMER-PRODUCT INTERACTIONS
# ============================================================

def aggregate_interactions(
    interaction_df,
):
    print(
        "\nAggregating customer-product interactions..."
    )

    aggregated_df = (
        interaction_df.groupby(
            [
                "customer_id",
                "product_id",
            ],
            as_index=False,
        )["interaction_score"]
        .sum()
    )

    print(
        "Aggregated interactions:",
        len(aggregated_df)
    )

    return aggregated_df


# ============================================================
# CREATE INTERACTION MATRIX
# ============================================================

def create_interaction_matrix(
    aggregated_df,
):
    print(
        "\nCreating customer-product interaction matrix..."
    )

    interaction_matrix = (
        aggregated_df.pivot_table(
            index="customer_id",
            columns="product_id",
            values="interaction_score",
            fill_value=0,
        )
    )

    interaction_matrix = (
        interaction_matrix.sort_index(
            axis=0
        )
        .sort_index(
            axis=1
        )
    )

    print(
        "Interaction matrix shape:",
        interaction_matrix.shape
    )

    return interaction_matrix


# ============================================================
# CALCULATE ITEM SIMILARITY
# ============================================================

def calculate_item_similarity(
    interaction_matrix,
):
    print(
        "\nCalculating item-item cosine similarity..."
    )

    similarity_values = cosine_similarity(
        interaction_matrix.T
    )

    # Create a writable copy before modifying the diagonal
    similarity_values = np.array(
        similarity_values,
        dtype=float,
        copy=True,
    )

    np.fill_diagonal(
        similarity_values,
        0.0,
    )

    item_similarity = pd.DataFrame(
        similarity_values,
        index=interaction_matrix.columns,
        columns=interaction_matrix.columns,
    )

    print(
        "Item similarity matrix shape:",
        item_similarity.shape
    )

    return item_similarity

# ============================================================
# CALCULATE POPULAR PRODUCTS
# ============================================================

def calculate_popular_products(
    aggregated_df,
):
    print(
        "\nCalculating popular product fallback..."
    )

    popular_products = (
        aggregated_df.groupby(
            "product_id"
        )["interaction_score"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    print(
        "Popular product fallback created."
    )

    return popular_products


# ============================================================
# RECOMMEND PRODUCTS
# ============================================================

def recommend_products(
    customer_id,
    interaction_matrix,
    item_similarity,
    popular_products,
    top_k=5,
):
    customer_vector = (
        interaction_matrix.loc[
            customer_id
        ]
    )

    interacted_products = (
        customer_vector[
            customer_vector > 0
        ]
    )

    interacted_product_ids = set(
        interacted_products.index
    )

    if interacted_products.empty:
        return (
            popular_products.head(
                top_k
            )
            .index
            .tolist()
        )

    similarity_subset = (
        item_similarity.loc[
            interacted_products.index
        ]
    )

    weighted_scores = (
        similarity_subset.T
        .dot(
            interacted_products.values
        )
    )

    score_series = pd.Series(
        weighted_scores,
        index=item_similarity.columns,
        dtype=float,
    )

    score_series = (
        score_series.drop(
            labels=list(
                interacted_product_ids
            ),
            errors="ignore",
        )
        .sort_values(
            ascending=False
        )
    )

    recommendations = []

    for product_id in score_series.index:
        if (
            product_id
            not in recommendations
        ):
            recommendations.append(
                product_id
            )

        if (
            len(recommendations)
            >= top_k
        ):
            break

    if len(recommendations) < top_k:
        for product_id in (
            popular_products.index
        ):
            if (
                product_id
                not in interacted_product_ids
                and product_id
                not in recommendations
            ):
                recommendations.append(
                    product_id
                )

            if (
                len(recommendations)
                >= top_k
            ):
                break

    return recommendations


# ============================================================
# GENERATE FINAL RECOMMENDATIONS
# ============================================================

def generate_final_recommendations(
    interaction_matrix,
    item_similarity,
    popular_products,
):
    print(
        "\nGenerating Top-5 recommendations "
        "for all customers..."
    )

    recommendation_records = []

    total_customers = len(
        interaction_matrix.index
    )

    for customer_number, customer_id in enumerate(
        interaction_matrix.index,
        start=1,
    ):
        recommendations = recommend_products(
            customer_id=customer_id,
            interaction_matrix=interaction_matrix,
            item_similarity=item_similarity,
            popular_products=popular_products,
            top_k=TOP_K,
        )

        for rank, product_id in enumerate(
            recommendations,
            start=1,
        ):
            recommendation_records.append(
                {
                    "customer_id": customer_id,
                    "rank": rank,
                    "recommended_product_id": product_id,
                }
            )

        if (
            customer_number % 500 == 0
            or customer_number
            == total_customers
        ):
            print(
                "Processed customers:",
                f"{customer_number}"
                f"/{total_customers}"
            )

    recommendations_df = pd.DataFrame(
        recommendation_records
    )

    print(
        "\nFinal recommendations generated successfully."
    )

    print(
        "Recommendation records:",
        len(recommendations_df)
    )

    print(
        "Customers with recommendations:",
        recommendations_df[
            "customer_id"
        ].nunique()
    )

    print(
        "Unique recommended products:",
        recommendations_df[
            "recommended_product_id"
        ].nunique()
    )

    return recommendations_df


# ============================================================
# VALIDATE RECOMMENDATIONS
# ============================================================

def validate_recommendations(
    recommendations_df,
    interaction_matrix,
):
    print(
        "\nValidating final recommendations..."
    )

    expected_customers = len(
        interaction_matrix.index
    )

    recommended_customers = (
        recommendations_df[
            "customer_id"
        ].nunique()
    )

    recommendation_counts = (
        recommendations_df.groupby(
            "customer_id"
        ).size()
    )

    customers_with_exact_top_k = (
        recommendation_counts.eq(
            TOP_K
        ).sum()
    )

    duplicate_count = (
        recommendations_df.duplicated(
            subset=[
                "customer_id",
                "recommended_product_id",
            ]
        ).sum()
    )

    interacted_lookup = {
        customer_id: set(
            interaction_matrix.columns[
                interaction_matrix.loc[
                    customer_id
                ].values > 0
            ]
        )
        for customer_id
        in interaction_matrix.index
    }

    already_interacted_count = 0

    for row in (
        recommendations_df[
            [
                "customer_id",
                "recommended_product_id",
            ]
        ]
        .itertuples(
            index=False
        )
    ):
        if (
            row.recommended_product_id
            in interacted_lookup[
                row.customer_id
            ]
        ):
            already_interacted_count += 1

    print(
        "\n--- RECOMMENDATION VALIDATION ---"
    )

    print(
        "Expected customers:",
        expected_customers
    )

    print(
        "Customers with recommendations:",
        recommended_customers
    )

    print(
        "Customers with exactly Top-5:",
        customers_with_exact_top_k
    )

    print(
        "Duplicate customer-product recommendations:",
        duplicate_count
    )

    print(
        "Already-interacted products recommended:",
        already_interacted_count
    )

    if (
        recommended_customers
        != expected_customers
    ):
        raise ValueError(
            "Not all customers received recommendations."
        )

    if (
        customers_with_exact_top_k
        != expected_customers
    ):
        raise ValueError(
            "Some customers do not have exactly "
            f"{TOP_K} recommendations."
        )

    if duplicate_count != 0:
        raise ValueError(
            "Duplicate recommendations detected."
        )

    if already_interacted_count != 0:
        raise ValueError(
            "Previously interacted products "
            "were recommended."
        )

    print(
        "Recommendation validation passed successfully."
    )


# ============================================================
# SAVE RESULTS
# ============================================================

def save_results(
    recommendations_df,
    interaction_matrix,
    item_similarity,
    popular_products,
):
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    recommendations_df.to_csv(
        FINAL_RECOMMENDATIONS_PATH,
        index=False,
    )

    model_artifact = {
        "algorithm": "Item-Based Collaborative Filtering",
        "top_k": TOP_K,
        "interaction_matrix": interaction_matrix,
        "item_similarity": item_similarity,
        "popular_products": popular_products,
        "interaction_weights": {
            "view": VIEW_SCORE,
            "cart": CART_SCORE,
            "purchase": PURCHASE_SCORE,
        },
    }

    with open(
        FINAL_RECOMMENDER_PATH,
        "wb",
    ) as model_file:
        pickle.dump(
            model_artifact,
            model_file,
        )

    print(
        "\nFinal recommendations saved:",
        FINAL_RECOMMENDATIONS_PATH
    )

    print(
        "Final recommender artifact saved:",
        FINAL_RECOMMENDER_PATH
    )


# ============================================================
# DISPLAY SAMPLE
# ============================================================

def display_sample(
    recommendations_df,
):
    print(
        "\n--- SAMPLE FINAL RECOMMENDATIONS ---"
    )

    sample_customers = (
        recommendations_df[
            "customer_id"
        ]
        .drop_duplicates()
        .head(10)
    )

    sample_df = (
        recommendations_df[
            recommendations_df[
                "customer_id"
            ].isin(
                sample_customers
            )
        ]
    )

    print(
        sample_df.to_string(
            index=False
        )
    )


# ============================================================
# MAIN
# ============================================================

def main():
    ecommerce_df = load_data()

    interaction_df = (
        create_interaction_scores(
            ecommerce_df
        )
    )

    aggregated_df = (
        aggregate_interactions(
            interaction_df
        )
    )

    interaction_matrix = (
        create_interaction_matrix(
            aggregated_df
        )
    )

    item_similarity = (
        calculate_item_similarity(
            interaction_matrix
        )
    )

    popular_products = (
        calculate_popular_products(
            aggregated_df
        )
    )

    recommendations_df = (
        generate_final_recommendations(
            interaction_matrix,
            item_similarity,
            popular_products,
        )
    )

    validate_recommendations(
        recommendations_df,
        interaction_matrix,
    )

    display_sample(
        recommendations_df
    )

    save_results(
        recommendations_df,
        interaction_matrix,
        item_similarity,
        popular_products,
    )

    print(
        "\nFinal production recommendation "
        "generation completed successfully."
    )


if __name__ == "__main__":
    main()