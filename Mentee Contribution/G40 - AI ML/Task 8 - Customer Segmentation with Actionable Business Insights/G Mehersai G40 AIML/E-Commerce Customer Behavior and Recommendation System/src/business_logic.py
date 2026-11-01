from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = PROJECT_ROOT / "data" / "Ecommerce.csv"

CUSTOMER_SEGMENTS_PATH = (
    PROJECT_ROOT
    / "outputs"
    / "results"
    / "customer_segments.csv"
)

CART_PREDICTIONS_PATH = (
    PROJECT_ROOT
    / "outputs"
    / "results"
    / "final_cart_conversion_predictions.csv"
)

RECOMMENDATIONS_PATH = (
    PROJECT_ROOT
    / "outputs"
    / "results"
    / "final_recommendations.csv"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "outputs"
    / "results"
    / "final_business_insights.csv"
)


def load_project_data():
    """Load datasets required by the business decision engine."""

    print("Loading project data...")

    ecommerce_df = pd.read_csv(DATA_PATH)

    customer_segments = pd.read_csv(
        CUSTOMER_SEGMENTS_PATH
    )

    cart_predictions = pd.read_csv(
        CART_PREDICTIONS_PATH
    )

    recommendations = pd.read_csv(
        RECOMMENDATIONS_PATH
    )

    print("Project data loaded successfully.")

    print(
        "E-commerce sessions:",
        len(ecommerce_df)
    )

    print(
        "Customer profiles:",
        len(customer_segments)
    )

    print(
        "Cart prediction records:",
        len(cart_predictions)
    )

    print(
        "Recommendation records:",
        len(recommendations)
    )

    return (
        ecommerce_df,
        customer_segments,
        cart_predictions,
        recommendations,
    )


def prepare_customer_segments(customer_segments):
    """Assign meaningful names to K-Means customer clusters."""

    segment_df = customer_segments.copy()

    segment_mapping = {
        0: "Low-Engagement Customers",
        1: "High-Value Purchasing Customers",
    }

    segment_df["customer_segment"] = (
        segment_df["cluster"]
        .map(segment_mapping)
    )

    return segment_df


def create_customer_behavior_summary(ecommerce_df):
    """Aggregate session behaviour at customer level."""

    print("\nCreating customer behavior summary...")

    behavior_summary = (
        ecommerce_df
        .groupby("customer_id")
        .agg(
            total_sessions=(
                "session_id",
                "count"
            ),
            total_purchases=(
                "purchased",
                "sum"
            ),
            purchase_rate=(
                "purchased",
                "mean"
            ),
            cart_add_rate=(
                "added_to_cart",
                "mean"
            ),
            cart_abandon_rate=(
                "cart_abandoned",
                "mean"
            ),
            total_revenue=(
                "revenue",
                "sum"
            ),
            avg_pages_viewed=(
                "pages_viewed",
                "mean"
            ),
            avg_time_on_site=(
                "time_on_site_sec",
                "mean"
            ),
        )
        .reset_index()
    )

    print(
        "Customer behavior summary created successfully."
    )

    return behavior_summary


def prepare_cart_conversion_scores(cart_predictions):
    """Prepare latest cart conversion score for each customer.

    The final selected cart conversion model is the
    Class-Weighted Random Forest.
    """

    print("\nPreparing cart conversion scores...")

    predictions_df = cart_predictions.copy()

    print(
        "Available prediction columns:",
        predictions_df.columns.tolist()
    )

    probability_column = (
        "class_weighted_random_forest_probability"
    )

    prediction_column = (
        "class_weighted_random_forest_prediction"
    )

    if probability_column not in predictions_df.columns:
        raise ValueError(
            "Final Class-Weighted Random Forest probability "
            "column was not found. Available columns: "
            f"{predictions_df.columns.tolist()}"
        )

    print(
        "Using final selected model probability column:",
        probability_column
    )

    if prediction_column in predictions_df.columns:
        print(
            "Using final selected model prediction column:",
            prediction_column
        )

    if "visit_date" in predictions_df.columns:
        predictions_df["visit_date"] = pd.to_datetime(
            predictions_df["visit_date"],
            format="%Y-%m-%d",
            errors="coerce",
        )

        print(
            "Invalid prediction dates:",
            predictions_df["visit_date"].isna().sum()
        )

        predictions_df = (
            predictions_df
            .sort_values(
                [
                    "customer_id",
                    "visit_date",
                    "session_id",
                ]
            )
            .groupby(
                "customer_id",
                as_index=False
            )
            .tail(1)
        )

    else:
        predictions_df = (
            predictions_df
            .groupby(
                "customer_id",
                as_index=False
            )
            .tail(1)
        )

    selected_columns = [
        "customer_id",
        probability_column,
    ]

    if prediction_column in predictions_df.columns:
        selected_columns.append(
            prediction_column
        )

    conversion_scores = predictions_df[
        selected_columns
    ].copy()

    rename_mapping = {
        probability_column:
            "cart_conversion_probability"
    }

    if prediction_column in conversion_scores.columns:
        rename_mapping[prediction_column] = (
            "cart_conversion_prediction"
        )

    conversion_scores = conversion_scores.rename(
        columns=rename_mapping
    )

    print(
        "Customer conversion scores:",
        len(conversion_scores)
    )

    print(
        "\n--- CART CONVERSION PROBABILITY SUMMARY ---"
    )

    print(
        conversion_scores[
            "cart_conversion_probability"
        ]
        .describe()
        .round(4)
    )

    if (
        "cart_conversion_prediction"
        in conversion_scores.columns
    ):
        print(
            "\n--- CART CONVERSION PREDICTION DISTRIBUTION ---"
        )

        print(
            conversion_scores[
                "cart_conversion_prediction"
            ]
            .value_counts()
            .sort_index()
        )

    return conversion_scores

def prepare_recommendations(recommendations):
    """
    Convert long-format recommendation records into one row
    per customer.

    Expected input format:
        customer_id
        rank
        recommended_product_id
        product_category

    Output format:
        customer_id
        recommended_products
    """

    print("\nPreparing recommendation data...")

    recommendations_df = recommendations.copy()

    print(
        "Available recommendation columns:",
        recommendations_df.columns.tolist()
    )

    recommendation_column = "recommended_product_id"

    if recommendation_column not in recommendations_df.columns:
        raise ValueError(
            "Could not find 'recommended_product_id'. "
            f"Available columns: "
            f"{recommendations_df.columns.tolist()}"
        )

    print(
        "Using recommendation column:",
        recommendation_column
    )

    if "rank" in recommendations_df.columns:
        recommendations_df = recommendations_df.sort_values(
            [
                "customer_id",
                "rank",
            ]
        )

    recommendation_summary = (
        recommendations_df
        .groupby(
            "customer_id",
            as_index=False
        )[recommendation_column]
        .agg(list)
    )

    recommendation_summary = recommendation_summary.rename(
        columns={
            recommendation_column:
                "recommended_products"
        }
    )

    recommendation_summary[
        "recommended_products"
    ] = (
        recommendation_summary[
            "recommended_products"
        ]
        .apply(
            lambda products: ", ".join(
                str(int(product))
                if pd.notna(product)
                else ""
                for product in products
            )
        )
    )

    print(
        "Customers with recommendation records:",
        len(recommendation_summary)
    )

    print(
        "\n--- SAMPLE CUSTOMER RECOMMENDATIONS ---"
    )

    print(
        recommendation_summary.head(10).to_string(
            index=False
        )
    )

    return recommendation_summary


def assign_business_priority(row):
    """Assign the main business objective for a customer."""

    segment = row["customer_segment"]

    conversion_probability = row[
        "cart_conversion_probability"
    ]

    cart_abandon_rate = row["cart_abandon_rate"]

    purchase_rate = row["purchase_rate"]

    if (
        segment
        == "High-Value Purchasing Customers"
        and purchase_rate >= 0.50
    ):
        return "Retention"

    if (
        cart_abandon_rate >= 0.50
        and conversion_probability >= 0.41
    ):
        return "Conversion"

    if (
        segment
        == "High-Value Purchasing Customers"
    ):
        return "Purchase Growth"

    return "Re-Engagement"


def assign_marketing_action(priority):
    """Map business priority to a marketing campaign."""

    action_mapping = {
        "Retention":
            "Loyalty Reward Campaign",

        "Conversion":
            "Cart Recovery Campaign",

        "Purchase Growth":
            "Personalized Product Campaign",

        "Re-Engagement":
            "Customer Re-Engagement Campaign",
    }

    return action_mapping[priority]


def assign_discount_strategy(priority):
    """Select a discount strategy."""

    strategy_mapping = {
        "Retention":
            "Low Discount / Premium Offer",

        "Conversion":
            "Limited-Time Checkout Incentive",

        "Purchase Growth":
            "Personalized Product Offer",

        "Re-Engagement":
            "Targeted Promotional Discount",
    }

    return strategy_mapping[priority]


def assign_recommendation_strategy(row):
    """Assign recommendation strategy based on customer segment."""

    if (
        row["customer_segment"]
        == "High-Value Purchasing Customers"
    ):
        return (
            "Personalized Item-Based "
            "Collaborative Filtering"
        )

    return (
        "Item-Based CF with Popular Product Fallback"
    )


def assign_customer_risk(row):
    """Classify customer conversion or engagement risk."""

    conversion_probability = row[
        "cart_conversion_probability"
    ]

    cart_abandon_rate = row["cart_abandon_rate"]

    if (
        conversion_probability < 0.30
        and cart_abandon_rate >= 0.50
    ):
        return "High Risk"

    if conversion_probability < 0.50:
        return "Medium Risk"

    return "Low Risk"


def calculate_business_opportunity_score(row):
    """Calculate a customer-level business opportunity score."""

    conversion_probability = row[
        "cart_conversion_probability"
    ]

    cart_abandon_rate = row["cart_abandon_rate"]

    purchase_rate = row["purchase_rate"]

    normalized_revenue = row[
        "normalized_revenue"
    ]

    score = (
        0.30 * conversion_probability
        + 0.25 * cart_abandon_rate
        + 0.20 * (1 - purchase_rate)
        + 0.25 * normalized_revenue
    )

    return round(
        score * 100,
        2
    )


def create_business_insights(
    ecommerce_df,
    customer_segments,
    cart_predictions,
    recommendations,
):
    """Create final actionable customer business insights."""

    print("\nCreating final business insights...")

    segment_df = prepare_customer_segments(
        customer_segments
    )

    behavior_df = create_customer_behavior_summary(
        ecommerce_df
    )

    conversion_df = prepare_cart_conversion_scores(
        cart_predictions
    )

    recommendation_df = prepare_recommendations(
        recommendations
    )

    business_df = segment_df.merge(
        behavior_df,
        on="customer_id",
        how="left",
        suffixes=(
            "_segment",
            "_behavior",
        ),
    )

    business_df = business_df.merge(
        conversion_df,
        on="customer_id",
        how="left",
    )

    business_df = business_df.merge(
        recommendation_df,
        on="customer_id",
        how="left",
    )

    business_df["recommended_products"] = (
        business_df["recommended_products"]
        .fillna("No recommendation available")
    )

    print("\n--- CONVERSION SCORE MERGE DEBUG ---")

    print(
        "Business rows after conversion merge:",
        len(business_df)
    )

    print(
        "Unique business customers:",
        business_df["customer_id"].nunique()
    )

    print(
        "Non-null conversion probabilities:",
        business_df[
            "cart_conversion_probability"
        ].notna().sum()
    )

    missing_conversion_scores = business_df[
        "cart_conversion_probability"
    ].isna().sum()

    print(
        "Missing conversion probabilities:",
        missing_conversion_scores
    )

    print(
        "\nCustomers without future cart conversion scores:",
        missing_conversion_scores
    )

    business_df["has_cart_conversion_score"] = (
        business_df[
            "cart_conversion_probability"
        ].notna()
    )

    business_df[
        "cart_conversion_probability"
    ] = (
        business_df[
            "cart_conversion_probability"
        ]
        .fillna(0)
    )

    if "cart_conversion_prediction" in business_df.columns:
        business_df[
            "cart_conversion_prediction"
        ] = (
            business_df[
                "cart_conversion_prediction"
            ]
            .fillna(0)
            .astype(int)
        )

    revenue_column = None

    for column in [
        "total_revenue_behavior",
        "total_revenue_segment",
        "total_revenue",
    ]:
        if column in business_df.columns:
            revenue_column = column
            break

    if revenue_column is None:
        raise ValueError(
            "Could not identify total revenue column."
        )

    max_revenue = business_df[
        revenue_column
    ].max()

    if max_revenue > 0:
        business_df["normalized_revenue"] = (
            business_df[revenue_column]
            / max_revenue
        )

    else:
        business_df["normalized_revenue"] = 0

    purchase_rate_column = None

    for column in [
        "purchase_rate_behavior",
        "purchase_rate_segment",
        "purchase_rate",
    ]:
        if column in business_df.columns:
            purchase_rate_column = column
            break

    cart_abandon_column = None

    for column in [
        "cart_abandon_rate_behavior",
        "cart_abandon_rate_segment",
        "cart_abandon_rate",
    ]:
        if column in business_df.columns:
            cart_abandon_column = column
            break

    if purchase_rate_column is None:
        raise ValueError(
            "Could not identify purchase rate column."
        )

    if cart_abandon_column is None:
        raise ValueError(
            "Could not identify cart abandon rate column."
        )

    business_df["purchase_rate"] = business_df[
        purchase_rate_column
    ]

    business_df["cart_abandon_rate"] = business_df[
        cart_abandon_column
    ]

    business_df["business_priority"] = (
        business_df.apply(
            assign_business_priority,
            axis=1,
        )
    )

    business_df["marketing_action"] = (
        business_df[
            "business_priority"
        ]
        .apply(assign_marketing_action)
    )

    business_df["discount_strategy"] = (
        business_df[
            "business_priority"
        ]
        .apply(assign_discount_strategy)
    )

    business_df["recommendation_strategy"] = (
        business_df.apply(
            assign_recommendation_strategy,
            axis=1,
        )
    )

    business_df["customer_risk"] = (
        business_df.apply(
            assign_customer_risk,
            axis=1,
        )
    )

    business_df[
        "business_opportunity_score"
    ] = business_df.apply(
        calculate_business_opportunity_score,
        axis=1,
    )

    business_df = business_df.sort_values(
        "business_opportunity_score",
        ascending=False,
    )

    print(
        "Final business insights created successfully."
    )

    return business_df


def display_business_summary(business_df):
    """Display business decision engine results."""

    print(
        "\n--- CUSTOMER SEGMENT DISTRIBUTION ---"
    )

    print(
        business_df[
            "customer_segment"
        ].value_counts()
    )

    print(
        "\n--- BUSINESS PRIORITY DISTRIBUTION ---"
    )

    print(
        business_df[
            "business_priority"
        ].value_counts()
    )

    print(
        "\n--- MARKETING ACTION DISTRIBUTION ---"
    )

    print(
        business_df[
            "marketing_action"
        ].value_counts()
    )

    print(
        "\n--- CUSTOMER RISK DISTRIBUTION ---"
    )

    print(
        business_df[
            "customer_risk"
        ].value_counts()
    )

    print(
        "\n--- BUSINESS OPPORTUNITY SCORE SUMMARY ---"
    )

    print(
        business_df[
            "business_opportunity_score"
        ]
        .describe()
        .round(2)
    )

    print(
        "\n--- TOP BUSINESS OPPORTUNITIES ---"
    )

    display_columns = [
        "customer_id",
        "customer_segment",
        "cart_conversion_probability",
        "customer_risk",
        "business_priority",
        "marketing_action",
        "discount_strategy",
        "recommendation_strategy",
        "recommended_products",
        "business_opportunity_score",
    ]

    print(
        business_df[
            display_columns
        ]
        .head(10)
        .to_string(index=False)
    )




def save_business_insights(business_df):
    """Save final business decision results."""

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    
    
    
    business_df.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print(
        f"\nFinal business insights saved: {OUTPUT_PATH}"
    )


def main():
    (
        ecommerce_df,
        customer_segments,
        cart_predictions,
        recommendations,
    ) = load_project_data()

    business_df = create_business_insights(
        ecommerce_df,
        customer_segments,
        cart_predictions,
        recommendations,
    )

    display_business_summary(
        business_df
    )

    save_business_insights(
        business_df
    )

    print(
        "\nFinal business decision engine "
        "completed successfully."
    )


if __name__ == "__main__":
    main()