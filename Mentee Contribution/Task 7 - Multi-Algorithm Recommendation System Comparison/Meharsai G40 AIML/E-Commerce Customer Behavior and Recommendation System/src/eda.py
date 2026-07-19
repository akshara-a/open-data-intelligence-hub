from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = PROJECT_ROOT / "data" / "Ecommerce.csv"

FIGURE_PATH = PROJECT_ROOT / "outputs" / "figures"


# Create output directory
FIGURE_PATH.mkdir(
    parents=True,
    exist_ok=True
)


# --------------------------------------------------
# DATA LOADING
# --------------------------------------------------

def load_data(file_path):
    """Load the e-commerce dataset."""

    return pd.read_csv(file_path)


# --------------------------------------------------
# FIGURE SAVING
# --------------------------------------------------

def save_figure(filename):
    """Save the current Matplotlib figure."""

    FIGURE_PATH.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path = FIGURE_PATH / filename

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Figure saved: {output_path}")


# --------------------------------------------------
# PURCHASE DISTRIBUTION
# --------------------------------------------------

def analyze_purchase_distribution(df):
    """Analyze purchase class distribution."""

    purchase_counts = (
        df["purchased"]
        .value_counts()
        .sort_index()
    )

    print("\n--- PURCHASE DISTRIBUTION ---")

    print(purchase_counts)

    print("\n--- PURCHASE DISTRIBUTION (%) ---")

    purchase_percentage = (
        df["purchased"]
        .value_counts(normalize=True)
        .sort_index()
        .mul(100)
        .round(2)
    )

    print(purchase_percentage)

    plt.figure(
        figsize=(7, 5)
    )

    purchase_counts.plot(
        kind="bar"
    )

    plt.title(
        "Purchase Distribution"
    )

    plt.xlabel(
        "Purchase Status"
    )

    plt.ylabel(
        "Number of Sessions"
    )

    plt.xticks(
        ticks=[0, 1],
        labels=[
            "Not Purchased",
            "Purchased"
        ],
        rotation=0
    )

    save_figure(
        "purchase_dist.png"
    )


# --------------------------------------------------
# PURCHASE RATE ANALYSIS
# --------------------------------------------------

def analyze_purchase_rate(df, column, figure_name):
    """Calculate and visualize purchase rate by a feature."""

    purchase_rate = (
        df.groupby(column)["purchased"]
        .mean()
        .mul(100)
        .sort_index()
    )

    print(
        f"\n--- PURCHASE RATE BY {column.upper()} ---"
    )

    print(
        purchase_rate.round(2)
    )

    plt.figure(
        figsize=(8, 5)
    )

    purchase_rate.plot(
        kind="bar"
    )

    feature_name = (
        column
        .replace("_", " ")
        .title()
    )

    plt.title(
        f"Purchase Rate by {feature_name}"
    )

    plt.xlabel(
        feature_name
    )

    plt.ylabel(
        "Purchase Rate (%)"
    )

    plt.xticks(
        rotation=45
    )

    save_figure(
        f"purchase_{figure_name}.png"
    )


# --------------------------------------------------
# CUSTOMER BEHAVIOR ANALYSIS
# --------------------------------------------------

def analyze_behavior_by_purchase(df):
    """Compare customer behavior by purchase status."""

    behavior_columns = [
        "pages_viewed",
        "time_on_site_sec",
        "unit_price",
        "discount_percent",
        "discount_amount",
        "quantity",
    ]

    behavior_summary = (
        df.groupby("purchased")[behavior_columns]
        .mean()
        .round(2)
    )

    print(
        "\n--- BEHAVIOR SUMMARY BY PURCHASE STATUS ---"
    )

    print(
        behavior_summary
    )

    return behavior_summary


# --------------------------------------------------
# CART ANALYSIS
# --------------------------------------------------

def analyze_cart_relationship(df):
    """Analyze cart variables against purchase status."""

    added_to_cart_table = pd.crosstab(
        df["added_to_cart"],
        df["purchased"]
    )

    cart_abandoned_table = pd.crosstab(
        df["cart_abandoned"],
        df["purchased"]
    )

    print(
        "\n--- ADDED TO CART VS PURCHASED ---"
    )

    print(
        added_to_cart_table
    )

    print(
        "\n--- CART ABANDONED VS PURCHASED ---"
    )

    print(
        cart_abandoned_table
    )


# --------------------------------------------------
# POSSIBLE DATA LEAKAGE ANALYSIS
# --------------------------------------------------

def analyze_post_purchase_features(df):
    """Inspect possible post-purchase features."""

    leakage_columns = [
        "revenue",
        "revenue_normalized",
        "rating",
        "review_text",
        "review_helpful_votes",
        "payment_method",
    ]

    leakage_summary = (
        df.groupby("purchased")[leakage_columns]
        .mean()
        .round(2)
    )

    print(
        "\n--- POSSIBLE LEAKAGE FEATURE SUMMARY ---"
    )

    print(
        leakage_summary
    )

    return leakage_summary


# --------------------------------------------------
# CORRELATION ANALYSIS
# --------------------------------------------------

def analyze_numeric_correlations(df):
    """Analyze numerical correlations with purchase."""

    numeric_df = df.select_dtypes(
        include=["number"]
    )

    purchase_correlations = (
        numeric_df
        .corr()["purchased"]
        .drop("purchased")
        .sort_values(
            key=abs,
            ascending=False
        )
    )

    print(
        "\n--- CORRELATION WITH PURCHASED ---"
    )

    print(
        purchase_correlations.round(4)
    )

    top_correlations = (
        purchase_correlations
        .head(12)
    )

    plt.figure(
        figsize=(9, 6)
    )

    top_correlations.sort_values().plot(
        kind="barh"
    )

    plt.title(
        "Top Numerical Correlations with Purchase Status"
    )

    plt.xlabel(
        "Correlation"
    )

    save_figure(
        "purchase_corr.png"
    )


# --------------------------------------------------
# MAIN FUNCTION
# --------------------------------------------------

def main():
    print(
        "Project root:",
        PROJECT_ROOT
    )

    print(
        "Data path:",
        DATA_PATH
    )

    print(
        "Figure directory:",
        FIGURE_PATH
    )

    print(
        "Figure directory exists:",
        FIGURE_PATH.exists()
    )

    print(
        "\nLoading dataset..."
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

    # ----------------------------------------------
    # Purchase distribution
    # ----------------------------------------------

    analyze_purchase_distribution(
        df
    )

    # ----------------------------------------------
    # Purchase rate analysis
    # ----------------------------------------------

    categorical_features = {
        "device_type": "device",
        "user_type": "user",
        "marketing_channel": "marketing",
        "product_category": "category",
        "visit_month": "month",
        "visit_weekday": "weekday",
        "visit_season": "season",
        "session_duration_bucket": "duration",
    }

    for column, figure_name in categorical_features.items():

        analyze_purchase_rate(
            df,
            column,
            figure_name
        )

    # ----------------------------------------------
    # Customer behavior
    # ----------------------------------------------

    analyze_behavior_by_purchase(
        df
    )

    # ----------------------------------------------
    # Cart relationships
    # ----------------------------------------------

    analyze_cart_relationship(
        df
    )

    # ----------------------------------------------
    # Leakage analysis
    # ----------------------------------------------

    analyze_post_purchase_features(
        df
    )

    # ----------------------------------------------
    # Correlation analysis
    # ----------------------------------------------

    analyze_numeric_correlations(
        df
    )

    print(
        "\nEDA completed successfully."
    )

    print(
        f"Figures saved to: {FIGURE_PATH}"
    )


# --------------------------------------------------
# SCRIPT ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":
    main()