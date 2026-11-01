from pathlib import Path

import joblib
import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = PROJECT_ROOT / "data" / "Ecommerce.csv"

MODEL_PATH = PROJECT_ROOT / "models"

RESULT_PATH = PROJECT_ROOT / "outputs" / "results"


MODEL_PATH.mkdir(
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

TOP_N = 5

SAMPLE_CUSTOMERS = 10


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
            "product_category",
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
# INTERACTION SUMMARY
# --------------------------------------------------

def display_interaction_summary(interaction_df):
    """Display interaction dataset information."""

    print(
        "\n--- INTERACTION DATA OVERVIEW ---"
    )

    print(
        "Number of interactions:",
        len(interaction_df),
    )

    print(
        "Unique customers:",
        interaction_df["customer_id"].nunique(),
    )

    print(
        "Unique products:",
        interaction_df["product_id"].nunique(),
    )

    print(
        "\n--- INTERACTION SCORE DISTRIBUTION ---"
    )

    print(
        interaction_df["interaction_score"]
        .value_counts()
        .sort_index()
    )

    print(
        "\n--- INTERACTION SCORE DISTRIBUTION (%) ---"
    )

    print(
        interaction_df["interaction_score"]
        .value_counts(normalize=True)
        .sort_index()
        .mul(100)
        .round(2)
    )


# --------------------------------------------------
# AGGREGATE CUSTOMER-PRODUCT INTERACTIONS
# --------------------------------------------------

def aggregate_interactions(interaction_df):
    """Aggregate repeated customer-product interactions."""

    aggregated_interactions = (
        interaction_df.groupby(
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

    return aggregated_interactions


# --------------------------------------------------
# CUSTOMER-PRODUCT MATRIX
# --------------------------------------------------

def create_interaction_matrix(aggregated_interactions):
    """Create customer-product interaction matrix."""

    interaction_matrix = (
        aggregated_interactions
        .pivot(
            index="customer_id",
            columns="product_id",
            values="interaction_score",
        )
        .fillna(0)
    )

    return interaction_matrix


# --------------------------------------------------
# ITEM SIMILARITY
# --------------------------------------------------

def calculate_item_similarity(interaction_matrix):
    """Calculate product-to-product cosine similarity."""

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


# --------------------------------------------------
# POPULAR PRODUCTS
# --------------------------------------------------

def calculate_popular_products(aggregated_interactions):
    """Calculate products ranked by total interaction strength."""

    popular_products = (
        aggregated_interactions
        .groupby("product_id")[
            "interaction_score"
        ]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    return popular_products


# --------------------------------------------------
# CUSTOMER RECOMMENDATIONS
# --------------------------------------------------

def recommend_products(
    customer_id,
    interaction_matrix,
    item_similarity,
    popular_products,
    top_n=TOP_N,
):
    """Generate personalized product recommendations."""

    if customer_id not in interaction_matrix.index:

        return (
            popular_products
            .head(top_n)
            .index
            .tolist()
        )

    customer_interactions = (
        interaction_matrix.loc[customer_id]
    )

    interacted_products = (
        customer_interactions[
            customer_interactions > 0
        ]
    )

    if interacted_products.empty:

        return (
            popular_products
            .head(top_n)
            .index
            .tolist()
        )

    recommendation_scores = pd.Series(
        0.0,
        index=item_similarity.index,
    )

    for product_id, interaction_score in (
        interacted_products.items()
    ):

        product_similarity = (
            item_similarity[product_id]
        )

        recommendation_scores = (
            recommendation_scores
            + (
                product_similarity
                * interaction_score
            )
        )

    recommendation_scores = (
        recommendation_scores.drop(
            labels=interacted_products.index,
            errors="ignore",
        )
    )

    recommendations = (
        recommendation_scores
        .sort_values(
            ascending=False
        )
        .head(top_n)
        .index
        .tolist()
    )

    return recommendations


# --------------------------------------------------
# PRODUCT CATEGORY LOOKUP
# --------------------------------------------------

def create_product_category_lookup(df):
    """Create product-to-category lookup."""

    product_category_lookup = (
        df.groupby("product_id")[
            "product_category"
        ]
        .agg(
            lambda values: values.mode().iloc[0]
        )
        .to_dict()
    )

    return product_category_lookup


# --------------------------------------------------
# GENERATE SAMPLE RECOMMENDATIONS
# --------------------------------------------------

def generate_sample_recommendations(
    interaction_matrix,
    item_similarity,
    popular_products,
    product_category_lookup,
):
    """Generate recommendations for sample customers."""

    customer_ids = (
        interaction_matrix.index
        .to_series()
        .sort_values()
        .head(SAMPLE_CUSTOMERS)
        .tolist()
    )

    recommendation_records = []

    print(
        "\n--- SAMPLE CUSTOMER RECOMMENDATIONS ---"
    )

    for customer_id in customer_ids:

        recommendations = recommend_products(
            customer_id,
            interaction_matrix,
            item_similarity,
            popular_products,
            TOP_N,
        )

        print(
            f"\nCustomer {customer_id}"
        )

        print(
            f"Recommended Products: {recommendations}"
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
                    "product_category": (
                        product_category_lookup.get(
                            product_id
                        )
                    ),
                }
            )

    recommendation_df = pd.DataFrame(
        recommendation_records
    )

    return recommendation_df


# --------------------------------------------------
# DISPLAY SIMILAR PRODUCTS
# --------------------------------------------------

def display_similar_products(item_similarity):
    """Display similar products for sample items."""

    sample_products = (
        item_similarity.index[:5]
    )

    print(
        "\n--- SAMPLE SIMILAR PRODUCTS ---"
    )

    for product_id in sample_products:

        similar_products = (
            item_similarity[product_id]
            .drop(
                labels=[product_id]
            )
            .sort_values(
                ascending=False
            )
            .head(5)
        )

        print(
            f"\nProduct {product_id}"
        )

        print(
            similar_products.round(4)
        )


# --------------------------------------------------
# SAVE RESULTS
# --------------------------------------------------

def save_results(
    recommendation_df,
    popular_products,
):
    """Save recommendation results."""

    recommendation_path = (
        RESULT_PATH / "recommendations.csv"
    )

    popularity_path = (
        RESULT_PATH / "popular_products.csv"
    )

    recommendation_df.to_csv(
        recommendation_path,
        index=False,
    )

    popular_products_df = (
        popular_products
        .rename("total_interaction_score")
        .reset_index()
    )

    popular_products_df.to_csv(
        popularity_path,
        index=False,
    )

    print(
        f"\nRecommendations saved: "
        f"{recommendation_path}"
    )

    print(
        f"Popular products saved: "
        f"{popularity_path}"
    )


# --------------------------------------------------
# SAVE RECOMMENDATION OBJECTS
# --------------------------------------------------

def save_recommendation_objects(
    interaction_matrix,
    item_similarity,
    popular_products,
):
    """Save objects required by the recommendation system."""

    matrix_path = (
        MODEL_PATH / "interaction_matrix.pkl"
    )

    similarity_path = (
        MODEL_PATH / "item_similarity.pkl"
    )

    popularity_path = (
        MODEL_PATH / "popular_products.pkl"
    )

    joblib.dump(
        interaction_matrix,
        matrix_path,
    )

    joblib.dump(
        item_similarity,
        similarity_path,
    )

    joblib.dump(
        popular_products,
        popularity_path,
    )

    print(
        f"\nInteraction matrix saved: "
        f"{matrix_path}"
    )

    print(
        f"Item similarity saved: "
        f"{similarity_path}"
    )

    print(
        f"Popular products saved: "
        f"{popularity_path}"
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
        "\nCreating implicit interaction scores..."
    )

    interaction_df = create_interaction_scores(
        df
    )

    display_interaction_summary(
        interaction_df
    )

    print(
        "\nAggregating customer-product interactions..."
    )

    aggregated_interactions = (
        aggregate_interactions(
            interaction_df
        )
    )

    print(
        "Aggregated interactions:",
        len(aggregated_interactions),
    )

    print(
        "\nCreating customer-product interaction matrix..."
    )

    interaction_matrix = (
        create_interaction_matrix(
            aggregated_interactions
        )
    )

    print(
        "Interaction matrix shape:",
        interaction_matrix.shape,
    )

    print(
        "\nCalculating item-item cosine similarity..."
    )

    item_similarity = (
        calculate_item_similarity(
            interaction_matrix
        )
    )

    print(
        "Item similarity matrix shape:",
        item_similarity.shape,
    )

    popular_products = (
        calculate_popular_products(
            aggregated_interactions
        )
    )

    product_category_lookup = (
        create_product_category_lookup(
            df
        )
    )

    display_similar_products(
        item_similarity
    )

    recommendation_df = (
        generate_sample_recommendations(
            interaction_matrix,
            item_similarity,
            popular_products,
            product_category_lookup,
        )
    )

    save_results(
        recommendation_df,
        popular_products,
    )

    save_recommendation_objects(
        interaction_matrix,
        item_similarity,
        popular_products,
    )

    print(
        "\nProduct recommendation completed successfully."
    )


# --------------------------------------------------
# SCRIPT ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":
    main()