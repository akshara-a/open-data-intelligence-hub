import os

import pandas as pd


RESULTS_DIRECTORY = "outputs/results"


REGRESSION_FEATURES = [
    "unit_price",
    "quantity",
    "discount_percent",
    "pages_viewed",
    "time_on_site_sec",
    "added_to_cart",
    "product_category",
    "device_type",
    "user_type",
    "engagement_score"
]


CLASSIFICATION_FEATURES = [
    "device_type",
    "user_type",
    "marketing_channel",
    "product_category",
    "unit_price",
    "quantity",
    "discount_percent",
    "pages_viewed",
    "time_on_site_sec",
    "added_to_cart",
    "visit_day",
    "visit_month",
    "visit_weekday",
    "visit_season",
    "discount_applied",
    "engagement_score"
]


def get_customer_segment(
    customer_id,
    customer_segments
):
    """
    Return the identified segment
    for a customer.
    """

    customer_record = customer_segments[
        customer_segments["customer_id"]
        == customer_id
    ]


    if customer_record.empty:
        raise ValueError(
            f"Customer ID {customer_id} "
            "was not found in customer segments."
        )


    if "segment_name" in customer_record.columns:

        segment_name = (
            customer_record["segment_name"]
            .iloc[0]
        )

    else:

        cluster = int(
            customer_record["cluster"]
            .iloc[0]
        )


        segment_names = {
            0: "Low-Conversion Browsers",
            1: "Active High-Value Buyers"
        }


        segment_name = segment_names.get(
            cluster,
            "Unknown Segment"
        )


    return segment_name


def get_segment_weights(segment_name):
    """
    Return recommendation weights based
    on customer segment.
    """

    if segment_name == "Low-Conversion Browsers":

        return {
            "purchase_weight": 0.70,
            "rating_weight": 0.30
        }


    if segment_name == "Active High-Value Buyers":

        return {
            "purchase_weight": 0.40,
            "rating_weight": 0.60
        }


    return {
        "purchase_weight": 0.50,
        "rating_weight": 0.50
    }


def create_product_profiles(df):
    """
    Create one representative feature profile
    for each product.
    """

    product_profiles = (
        df.groupby("product_id")
        .agg(
            product_category=(
                "product_category",
                "first"
            ),
            unit_price=(
                "unit_price",
                "mean"
            ),
            quantity=(
                "quantity",
                "mean"
            ),
            discount_percent=(
                "discount_percent",
                "mean"
            ),
            added_to_cart=(
                "added_to_cart",
                "mean"
            ),
            average_rating=(
                "rating",
                "mean"
            ),
            purchase_rate=(
                "purchased",
                "mean"
            )
        )
        .reset_index()
    )


    return product_profiles


def create_customer_profile(
    customer_id,
    df
):
    """
    Create a behavioral profile for
    the selected customer.
    """

    customer_history = df[
        df["customer_id"] == customer_id
    ]


    if customer_history.empty:
        raise ValueError(
            f"Customer ID {customer_id} "
            "was not found in the dataset."
        )


    customer_profile = {
        "device_type": (
            customer_history["device_type"]
            .mode()
            .iloc[0]
        ),
        "user_type": (
            customer_history["user_type"]
            .mode()
            .iloc[0]
        ),
        "marketing_channel": (
            customer_history[
                "marketing_channel"
            ]
            .mode()
            .iloc[0]
        ),
        "pages_viewed": (
            customer_history["pages_viewed"]
            .mean()
        ),
        "time_on_site_sec": (
            customer_history[
                "time_on_site_sec"
            ]
            .mean()
        ),
        "visit_day": (
            customer_history["visit_day"]
            .mode()
            .iloc[0]
        ),
        "visit_month": (
            customer_history["visit_month"]
            .mode()
            .iloc[0]
        ),
        "visit_weekday": (
            customer_history["visit_weekday"]
            .mode()
            .iloc[0]
        ),
        "visit_season": (
            customer_history["visit_season"]
            .mode()
            .iloc[0]
        )
    }


    return customer_profile


def generate_recommendations(
    customer_id,
    df,
    rating_model,
    purchase_model,
    customer_segments,
    top_n=5
):
    """
    Generate Top-N product recommendations
    for a customer.
    """

    print("\n" + "=" * 60)
    print("SHOP SENSE AI - PRODUCT RECOMMENDATIONS")
    print("=" * 60)


    segment_name = get_customer_segment(
        customer_id,
        customer_segments
    )


    weights = get_segment_weights(
        segment_name
    )


    print(
        f"\nCustomer ID      : {customer_id}"
    )

    print(
        f"Customer Segment : {segment_name}"
    )

    print(
        "Purchase Weight  : "
        f"{weights['purchase_weight']:.0%}"
    )

    print(
        "Rating Weight    : "
        f"{weights['rating_weight']:.0%}"
    )


    customer_profile = create_customer_profile(
        customer_id,
        df
    )


    product_profiles = create_product_profiles(
        df
    )


    customer_history = df[
        df["customer_id"] == customer_id
    ]


    purchased_products = set(
        customer_history.loc[
            customer_history["purchased"] == 1,
            "product_id"
        ]
    )


    candidate_products = product_profiles[
        ~product_profiles["product_id"]
        .isin(purchased_products)
    ].copy()


    print(
        f"Previously Purchased Products: "
        f"{len(purchased_products)}"
    )

    print(
        f"Candidate Products            : "
        f"{len(candidate_products)}"
    )


    # Add customer behavioral information
    # to every candidate product.

    for feature, value in customer_profile.items():

        candidate_products[feature] = value


    candidate_products["discount_applied"] = (
        candidate_products["discount_percent"] > 0
    ).astype(int)


    candidate_products["engagement_score"] = (
        candidate_products["pages_viewed"]
        *
        candidate_products["time_on_site_sec"]
    )


    # K-Means and historical EDA showed that
    # cart activity strongly relates to purchase.

    candidate_products["added_to_cart"] = (
        candidate_products["added_to_cart"]
        >= 0.50
    ).astype(int)


    # -------------------------------------------------
    # Predict Ratings
    # -------------------------------------------------

    rating_features = candidate_products[
        REGRESSION_FEATURES
    ]


    candidate_products["predicted_rating"] = (
        rating_model.predict(
            rating_features
        )
    )


    candidate_products["predicted_rating"] = (
        candidate_products["predicted_rating"]
        .clip(1, 5)
    )


    candidate_products[
        "normalized_rating"
    ] = (
        candidate_products["predicted_rating"]
        / 5.0
    )


    # -------------------------------------------------
    # Predict Purchase Probability
    # -------------------------------------------------

    purchase_features = candidate_products[
        CLASSIFICATION_FEATURES
    ]


    candidate_products[
        "purchase_probability"
    ] = (
        purchase_model.predict_proba(
            purchase_features
        )[:, 1]
    )


    # -------------------------------------------------
    # Recommendation Score
    # -------------------------------------------------

    candidate_products[
        "recommendation_score"
    ] = (
        (
            candidate_products[
                "purchase_probability"
            ]
            *
            weights["purchase_weight"]
        )
        +
        (
            candidate_products[
                "normalized_rating"
            ]
            *
            weights["rating_weight"]
        )
    )


    recommendations = (
        candidate_products
        .sort_values(
            by="recommendation_score",
            ascending=False
        )
        .head(top_n)
        .copy()
    )


    recommendations[
        "purchase_probability_percent"
    ] = (
        recommendations["purchase_probability"]
        * 100
    )


    recommendations[
        "recommendation_score_percent"
    ] = (
        recommendations["recommendation_score"]
        * 100
    )


    output_columns = [
        "product_id",
        "product_category",
        "unit_price",
        "predicted_rating",
        "purchase_probability_percent",
        "recommendation_score_percent"
    ]


    recommendations = recommendations[
        output_columns
    ]


    recommendations = recommendations.round(
        {
            "unit_price": 2,
            "predicted_rating": 2,
            "purchase_probability_percent": 2,
            "recommendation_score_percent": 2
        }
    )


    print("\nTOP PRODUCT RECOMMENDATIONS")
    print("-" * 60)


    print(
        recommendations.to_string(
            index=False
        )
    )


    os.makedirs(
        RESULTS_DIRECTORY,
        exist_ok=True
    )


    recommendation_file = os.path.join(
        RESULTS_DIRECTORY,
        f"recommendations_customer_{customer_id}.csv"
    )


    recommendations.to_csv(
        recommendation_file,
        index=False
    )


    print(
        f"\nRecommendations saved to: "
        f"{recommendation_file}"
    )


    return recommendations


def run_recommendation_engine(
    df,
    rating_model,
    purchase_model,
    customer_segments,
    top_n=5
):
    """
    Run the recommendation engine for
    example customers from each segment.
    """

    print("\n" + "=" * 60)
    print("SHOP SENSE AI - RECOMMENDATION ENGINE")
    print("=" * 60)


    example_customers = (
        customer_segments
        .groupby("segment_name")[
            "customer_id"
        ]
        .first()
    )


    all_recommendations = {}


    for segment_name, customer_id in (
        example_customers.items()
    ):

        print(
            f"\nGenerating recommendations for "
            f"{segment_name}..."
        )


        recommendations = generate_recommendations(
            customer_id=customer_id,
            df=df,
            rating_model=rating_model,
            purchase_model=purchase_model,
            customer_segments=customer_segments,
            top_n=top_n
        )


        all_recommendations[
            customer_id
        ] = recommendations


    print("\n" + "=" * 60)
    print("RECOMMENDATION ENGINE COMPLETED")
    print("=" * 60)


    return all_recommendations