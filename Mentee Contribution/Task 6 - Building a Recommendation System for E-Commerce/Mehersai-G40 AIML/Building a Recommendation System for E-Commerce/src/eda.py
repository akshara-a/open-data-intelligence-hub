import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


PLOTS_DIRECTORY = "outputs/plots"


def save_plot(file_name):
    """
    Save the current plot and close the figure.
    """

    os.makedirs(
        PLOTS_DIRECTORY,
        exist_ok=True
    )

    file_path = os.path.join(
        PLOTS_DIRECTORY,
        file_name
    )

    plt.tight_layout()

    plt.savefig(
        file_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Saved plot: {file_path}")


def perform_eda(df):
    """
    Perform exploratory data analysis
    on the processed e-commerce dataset.
    """

    print("\n" + "=" * 60)
    print("EXPLORATORY DATA ANALYSIS")
    print("=" * 60)


    # -------------------------------------------------
    # 1. Rating Distribution
    # -------------------------------------------------

    plt.figure(figsize=(8, 5))

    sns.countplot(
        data=df,
        x="rating"
    )

    plt.title("Customer Rating Distribution")

    plt.xlabel("Rating")
    plt.ylabel("Number of Sessions")

    save_plot(
        "01_rating_distribution.png"
    )


    # -------------------------------------------------
    # 2. Purchase Distribution
    # -------------------------------------------------

    plt.figure(figsize=(7, 5))

    sns.countplot(
        data=df,
        x="purchased"
    )

    plt.title("Purchase Status Distribution")

    plt.xlabel("Purchase Status")
    plt.ylabel("Number of Sessions")

    plt.xticks(
        [0, 1],
        ["Not Purchased", "Purchased"]
    )

    save_plot(
        "02_purchase_distribution.png"
    )


    # -------------------------------------------------
    # 3. Average Rating by Product Category
    # -------------------------------------------------

    category_rating = (
        df.groupby("product_category")["rating"]
        .mean()
        .reset_index()
    )

    plt.figure(figsize=(10, 6))

    sns.barplot(
        data=category_rating,
        x="product_category",
        y="rating"
    )

    plt.title(
        "Average Rating by Product Category"
    )

    plt.xlabel("Product Category Code")
    plt.ylabel("Average Rating")

    save_plot(
        "03_average_rating_by_category.png"
    )


    # -------------------------------------------------
    # 4. Browsing Time vs Purchase
    # -------------------------------------------------

    plt.figure(figsize=(8, 5))

    sns.boxplot(
        data=df,
        x="purchased",
        y="time_on_site_sec"
    )

    plt.title(
        "Browsing Time by Purchase Status"
    )

    plt.xlabel("Purchase Status")
    plt.ylabel("Time on Site (Seconds)")

    plt.xticks(
        [0, 1],
        ["Not Purchased", "Purchased"]
    )

    save_plot(
        "04_browsing_time_vs_purchase.png"
    )


    # -------------------------------------------------
    # 5. Cart Addition vs Purchase Rate
    # -------------------------------------------------

    cart_purchase_rate = (
        df.groupby("added_to_cart")["purchased"]
        .mean()
        .mul(100)
        .reset_index()
    )

    plt.figure(figsize=(7, 5))

    sns.barplot(
        data=cart_purchase_rate,
        x="added_to_cart",
        y="purchased"
    )

    plt.title(
        "Purchase Rate by Cart Addition"
    )

    plt.xlabel("Added to Cart")
    plt.ylabel("Purchase Rate (%)")

    plt.xticks(
        [0, 1],
        ["No", "Yes"]
    )

    save_plot(
        "05_cart_addition_vs_purchase.png"
    )


    # -------------------------------------------------
    # 6. Discount vs Purchase Rate
    # -------------------------------------------------

    discount_purchase_rate = (
        df.groupby("discount_applied")["purchased"]
        .mean()
        .mul(100)
        .reset_index()
    )

    plt.figure(figsize=(7, 5))

    sns.barplot(
        data=discount_purchase_rate,
        x="discount_applied",
        y="purchased"
    )

    plt.title(
        "Purchase Rate by Discount Usage"
    )

    plt.xlabel("Discount Applied")
    plt.ylabel("Purchase Rate (%)")

    plt.xticks(
        [0, 1],
        ["No Discount", "Discount Applied"]
    )

    save_plot(
        "06_discount_vs_purchase.png"
    )


    # -------------------------------------------------
    # 7. Revenue Distribution
    # -------------------------------------------------

    plt.figure(figsize=(9, 5))

    sns.histplot(
        data=df,
        x="revenue",
        bins=40,
        kde=True
    )

    plt.title("Revenue Distribution")

    plt.xlabel("Revenue")
    plt.ylabel("Frequency")

    save_plot(
        "07_revenue_distribution.png"
    )


    # -------------------------------------------------
    # 8. Correlation Heatmap
    # -------------------------------------------------

    correlation_columns = [
        "unit_price",
        "quantity",
        "discount_percent",
        "revenue",
        "pages_viewed",
        "time_on_site_sec",
        "added_to_cart",
        "purchased",
        "cart_abandoned",
        "rating",
        "engagement_score"
    ]

    correlation_matrix = (
        df[correlation_columns]
        .corr()
    )

    plt.figure(figsize=(12, 8))

    sns.heatmap(
        correlation_matrix,
        annot=True,
        fmt=".2f"
    )

    plt.title(
        "Correlation Between E-Commerce Features"
    )

    save_plot(
        "08_correlation_heatmap.png"
    )


    # -------------------------------------------------
    # Business Summary
    # -------------------------------------------------

    print("\nEDA SUMMARY")
    print("-" * 60)

    purchase_rate = (
        df["purchased"].mean() * 100
    )

    average_rating = df["rating"].mean()

    average_revenue = df["revenue"].mean()

    cart_purchase_rate_value = (
        df.loc[
            df["added_to_cart"] == 1,
            "purchased"
        ].mean() * 100
    )

    no_cart_purchase_rate_value = (
        df.loc[
            df["added_to_cart"] == 0,
            "purchased"
        ].mean() * 100
    )

    discount_purchase_rate_value = (
        df.loc[
            df["discount_applied"] == 1,
            "purchased"
        ].mean() * 100
    )

    no_discount_purchase_rate_value = (
        df.loc[
            df["discount_applied"] == 0,
            "purchased"
        ].mean() * 100
    )


    print(
        f"Overall Purchase Rate: "
        f"{purchase_rate:.2f}%"
    )

    print(
        f"Average Customer Rating: "
        f"{average_rating:.2f}"
    )

    print(
        f"Average Revenue per Session: "
        f"{average_revenue:.2f}"
    )

    print(
        f"Purchase Rate After Cart Addition: "
        f"{cart_purchase_rate_value:.2f}%"
    )

    print(
        f"Purchase Rate Without Cart Addition: "
        f"{no_cart_purchase_rate_value:.2f}%"
    )

    print(
        f"Purchase Rate With Discount: "
        f"{discount_purchase_rate_value:.2f}%"
    )

    print(
        f"Purchase Rate Without Discount: "
        f"{no_discount_purchase_rate_value:.2f}%"
    )


    print("\nExploratory data analysis completed.")