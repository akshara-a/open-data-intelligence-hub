from pathlib import Path

import numpy as np
import pandas as pd


# ---------------------------------------------------------
# PROJECT PATHS
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = PROJECT_ROOT / "data" / "Ecommerce.csv"

OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "ecommerce_historical_features.csv"
)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

def load_data(file_path):
    """Load the original e-commerce session dataset."""

    print("Loading dataset...")

    df = pd.read_csv(file_path)

    print("Dataset loaded successfully.")
    print("Dataset shape:", df.shape)

    return df


# ---------------------------------------------------------
# PREPARE TEMPORAL DATA
# ---------------------------------------------------------

def prepare_temporal_data(df):
    """Convert dates and order customer sessions chronologically."""

    print("\nPreparing temporal session data...")

    df = df.copy()

    df["visit_date"] = pd.to_datetime(
        df["visit_date"],
        format="%d-%m-%Y",
        errors="coerce"
    )

    invalid_dates = df["visit_date"].isna().sum()

    print("Invalid visit dates:", invalid_dates)

    if invalid_dates > 0:
        print("Removing rows with invalid visit dates...")

        df = df.dropna(
            subset=["visit_date"]
        ).copy()

    # Stable ordering is important when multiple sessions
    # occur on the same date.
    df = df.sort_values(
        by=[
            "customer_id",
            "visit_date",
            "session_id"
        ]
    ).reset_index(drop=True)

    print("Temporal ordering completed.")

    return df


# ---------------------------------------------------------
# HISTORICAL COUNT FEATURES
# ---------------------------------------------------------

def create_historical_count_features(df):
    """Create customer-history count features using past sessions only."""

    print("\nCreating historical count features...")

    customer_group = df.groupby(
        "customer_id",
        sort=False
    )

    df["previous_sessions"] = (
        customer_group.cumcount()
    )

    df["previous_purchases"] = (
        customer_group["purchased"]
        .cumsum()
        - df["purchased"]
    )

    df["previous_cart_adds"] = (
        customer_group["added_to_cart"]
        .cumsum()
        - df["added_to_cart"]
    )

    df["previous_cart_abandonments"] = (
        customer_group["cart_abandoned"]
        .cumsum()
        - df["cart_abandoned"]
    )

    print("Historical count features created.")

    return df


# ---------------------------------------------------------
# HISTORICAL RATE FEATURES
# ---------------------------------------------------------

def create_historical_rate_features(df):
    """Create historical behavioral rates from previous sessions."""

    print("\nCreating historical rate features...")

    safe_previous_sessions = (
        df["previous_sessions"]
        .replace(0, np.nan)
    )

    df["historical_purchase_rate"] = (
        df["previous_purchases"]
        / safe_previous_sessions
    )

    df["historical_cart_add_rate"] = (
        df["previous_cart_adds"]
        / safe_previous_sessions
    )

    df["historical_abandon_rate"] = (
        df["previous_cart_abandonments"]
        / safe_previous_sessions
    )

    rate_columns = [
        "historical_purchase_rate",
        "historical_cart_add_rate",
        "historical_abandon_rate",
    ]

    df[rate_columns] = (
        df[rate_columns]
        .fillna(0)
    )

    print("Historical rate features created.")

    return df


# ---------------------------------------------------------
# HISTORICAL AVERAGE FEATURES
# ---------------------------------------------------------

def create_historical_average_features(df):
    """Create expanding customer averages using past sessions only."""

    print("\nCreating historical average features...")

    historical_columns = {
        "pages_viewed": "avg_previous_pages_viewed",
        "time_on_site_sec": "avg_previous_time_on_site",
        "discount_percent": "avg_previous_discount",
        "unit_price": "avg_previous_unit_price",
    }

    for source_column, new_column in historical_columns.items():

        cumulative_sum = (
            df.groupby(
                "customer_id",
                sort=False
            )[source_column]
            .cumsum()
            - df[source_column]
        )

        denominator = (
            df["previous_sessions"]
            .replace(0, np.nan)
        )

        df[new_column] = (
            cumulative_sum
            / denominator
        ).fillna(0)

    print("Historical average features created.")

    return df


# ---------------------------------------------------------
# RECENCY FEATURE
# ---------------------------------------------------------

def create_recency_feature(df):
    """Calculate days since the customer's previous visit."""

    print("\nCreating customer recency feature...")

    df["previous_visit_date"] = (
        df.groupby(
            "customer_id",
            sort=False
        )["visit_date"]
        .shift(1)
    )

    df["days_since_last_visit"] = (
        df["visit_date"]
        - df["previous_visit_date"]
    ).dt.days

    df["days_since_last_visit"] = (
        df["days_since_last_visit"]
        .fillna(-1)
    )

    print("Recency feature created.")

    return df


# ---------------------------------------------------------
# CUSTOMER-PRODUCT HISTORY
# ---------------------------------------------------------

def create_customer_product_history(df):
    """Count prior interactions between a customer and product."""

    print("\nCreating customer-product history...")

    df["previous_product_interactions"] = (
        df.groupby(
            [
                "customer_id",
                "product_id"
            ],
            sort=False
        )
        .cumcount()
    )

    print("Customer-product history created.")

    return df


# ---------------------------------------------------------
# VALIDATE TEMPORAL FEATURES
# ---------------------------------------------------------

def validate_features(df):
    """Validate historical features and inspect generated values."""

    historical_features = [
        "previous_sessions",
        "previous_purchases",
        "previous_cart_adds",
        "previous_cart_abandonments",
        "historical_purchase_rate",
        "historical_cart_add_rate",
        "historical_abandon_rate",
        "avg_previous_pages_viewed",
        "avg_previous_time_on_site",
        "avg_previous_discount",
        "avg_previous_unit_price",
        "days_since_last_visit",
        "previous_product_interactions",
    ]

    print("\n--- HISTORICAL FEATURE SUMMARY ---")

    print(
        df[historical_features]
        .describe()
        .T
        .round(4)
    )

    print("\n--- MISSING VALUES ---")

    print(
        df[historical_features]
        .isna()
        .sum()
    )

    print("\n--- SAMPLE CUSTOMER HISTORY ---")

    customer_counts = (
        df["customer_id"]
        .value_counts()
    )

    eligible_customers = (
        customer_counts[
            customer_counts >= 4
        ]
        .index
    )

    if len(eligible_customers) > 0:

        sample_customer = eligible_customers[0]

        sample_columns = [
            "customer_id",
            "session_id",
            "visit_date",
            "purchased",
            "added_to_cart",
            "cart_abandoned",
            "previous_sessions",
            "previous_purchases",
            "historical_purchase_rate",
            "previous_cart_adds",
            "historical_cart_add_rate",
            "previous_cart_abandonments",
            "historical_abandon_rate",
            "days_since_last_visit",
        ]

        print("Sample Customer:", sample_customer)

        print(
            df.loc[
                df["customer_id"] == sample_customer,
                sample_columns
            ].to_string(index=False)
        )

    return historical_features


# ---------------------------------------------------------
# SAVE FEATURE DATASET
# ---------------------------------------------------------

def save_dataset(df):
    """Save the feature-engineered temporal dataset."""

    print("\nSaving feature-engineered dataset...")

    output_df = df.drop(
        columns=["previous_visit_date"],
        errors="ignore"
    )

    output_df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print(
        "Feature dataset saved:",
        OUTPUT_PATH
    )

    print(
        "Final dataset shape:",
        output_df.shape
    )


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():

    df = load_data(DATA_PATH)

    df = prepare_temporal_data(df)

    df = create_historical_count_features(df)

    df = create_historical_rate_features(df)

    df = create_historical_average_features(df)

    df = create_recency_feature(df)

    df = create_customer_product_history(df)

    historical_features = validate_features(df)

    save_dataset(df)

    print("\n--- CREATED HISTORICAL FEATURES ---")

    for feature in historical_features:
        print("-", feature)

    print(
        "\nHistorical feature engineering completed successfully."
    )


if __name__ == "__main__":
    main()