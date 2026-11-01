"""
Data Generation Module
======================
Generates a synthetic e-commerce dataset with ~5,000 records containing
realistic correlations between customer behavior and purchase patterns.
"""

import numpy as np
import pandas as pd
import os


def generate_ecommerce_data(n_records=5000, random_state=42, output_dir="data"):
    """
    Generate a synthetic e-commerce dataset with realistic feature correlations.

    Parameters
    ----------
    n_records : int
        Number of records to generate (default: 5000).
    random_state : int
        Random seed for reproducibility.
    output_dir : str
        Directory to save the generated CSV file.

    Returns
    -------
    pd.DataFrame
        The generated dataset.
    """
    np.random.seed(random_state)

    # --- User and Product IDs ---
    n_users = 800
    n_products = 200
    user_ids = np.random.randint(1, n_users + 1, size=n_records)
    product_ids = np.random.randint(1, n_products + 1, size=n_records)

    # --- Product Categories ---
    categories = ["Electronics", "Clothing", "Books", "Home & Kitchen",
                   "Sports", "Beauty", "Toys", "Grocery"]
    category = np.random.choice(categories, size=n_records)

    # --- Price (varies by category) ---
    category_price_map = {
        "Electronics": (200, 800),
        "Clothing": (20, 150),
        "Books": (5, 50),
        "Home & Kitchen": (30, 300),
        "Sports": (25, 200),
        "Beauty": (10, 100),
        "Toys": (10, 80),
        "Grocery": (3, 50),
    }
    price = np.array([
        np.random.uniform(*category_price_map[c]) for c in category
    ]).round(2)

    # --- Customer Demographics ---
    age = np.random.randint(18, 70, size=n_records)
    gender = np.random.choice(["Male", "Female", "Other"], size=n_records, p=[0.48, 0.48, 0.04])
    locations = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
                 "Philadelphia", "San Antonio", "San Diego", "Dallas", "Austin"]
    location = np.random.choice(locations, size=n_records)

    # --- Browsing Time (minutes) — influenced by age and category ---
    base_browse = np.random.exponential(scale=10, size=n_records)
    # Younger users browse slightly more
    age_factor = 1 + (35 - age) * 0.005
    browsing_time = (base_browse * age_factor).clip(0.5, 60).round(1)

    # --- Previous Purchases ---
    previous_purchases = np.random.poisson(lam=5, size=n_records).clip(0, 30)

    # --- Discount Applied ---
    discount_applied = np.random.choice([0, 1], size=n_records, p=[0.55, 0.45])

    # --- Cart Addition (influenced by browsing time and discount) ---
    cart_prob = 0.15 + 0.008 * browsing_time + 0.12 * discount_applied
    cart_prob = cart_prob.clip(0, 0.95)
    cart_addition = np.array([np.random.binomial(1, p) for p in cart_prob])

    # --- Purchase Status (influenced by cart, discount, browsing, previous purchases) ---
    purchase_prob = (
        0.05
        + 0.35 * cart_addition
        + 0.08 * discount_applied
        + 0.003 * browsing_time
        + 0.01 * previous_purchases
        - 0.0003 * price
    )
    purchase_prob = purchase_prob.clip(0.02, 0.95)
    purchase_status = np.array([np.random.binomial(1, p) for p in purchase_prob])

    # --- Rating (influenced by purchase, discount, price satisfaction) ---
    base_rating = np.random.normal(loc=3.5, scale=0.8, size=n_records)
    rating_adj = (
        0.3 * purchase_status
        + 0.2 * discount_applied
        - 0.001 * price
        + 0.01 * previous_purchases
    )
    rating = (base_rating + rating_adj).clip(1.0, 5.0).round(1)

    # --- Total Spending (correlated with previous purchases and price) ---
    total_spending = (
        previous_purchases * np.random.uniform(20, 80, size=n_records)
        + purchase_status * price * np.random.uniform(0.8, 1.2, size=n_records)
    ).round(2)

    # --- Build DataFrame ---
    df = pd.DataFrame({
        "User_ID": user_ids,
        "Product_ID": product_ids,
        "Category": category,
        "Price": price,
        "Rating": rating,
        "Browsing_Time": browsing_time,
        "Previous_Purchases": previous_purchases,
        "Cart_Addition": cart_addition,
        "Purchase_Status": purchase_status,
        "Age": age,
        "Gender": gender,
        "Location": location,
        "Discount_Applied": discount_applied,
        "Total_Spending": total_spending,
    })

    # --- Save to CSV ---
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, "ecommerce_data.csv")
    df.to_csv(filepath, index=False)
    print(f"[Data Generation] Dataset generated: {df.shape[0]} records, {df.shape[1]} columns")
    print(f"[Data Generation] Saved to: {filepath}")
    print(f"[Data Generation] Purchase rate: {purchase_status.mean():.2%}")
    print(f"[Data Generation] Average rating: {rating.mean():.2f}")

    return df


if __name__ == "__main__":
    df = generate_ecommerce_data()
    print("\nSample records:")
    print(df.head(10).to_string(index=False))
    print(f"\nDataset shape: {df.shape}")
    print(f"\nColumn dtypes:\n{df.dtypes}")
