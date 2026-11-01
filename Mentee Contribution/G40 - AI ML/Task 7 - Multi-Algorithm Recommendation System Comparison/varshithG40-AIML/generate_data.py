"""Generate a synthetic e-commerce dataset for the recommendation system project."""

import numpy as np
import pandas as pd
from pathlib import Path

RANDOM_STATE = 42
N_ROWS = 5000
CATEGORIES = ["Electronics", "Clothing", "Home", "Books", "Sports", "Beauty"]


def generate_ecommerce_data(n_rows: int = N_ROWS, seed: int = RANDOM_STATE) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    user_ids = rng.integers(1, 501, size=n_rows)
    product_ids = rng.integers(1, 201, size=n_rows)
    categories = rng.choice(CATEGORIES, size=n_rows)

    price = np.round(rng.uniform(10, 500, size=n_rows), 2)
    num_views = rng.integers(1, 50, size=n_rows)
    time_spent = np.round(rng.uniform(5, 300, size=n_rows), 1)
    previous_purchases = rng.integers(0, 30, size=n_rows)
    cart_status = rng.integers(0, 2, size=n_rows)

    category_effect = np.array([CATEGORIES.index(c) * 0.15 for c in categories])
    rating = (
        2.5
        + 0.4 * np.log1p(num_views)
        + 0.003 * time_spent
        + 0.02 * previous_purchases
        + 0.3 * cart_status
        - 0.001 * price
        + category_effect
        + rng.normal(0, 0.6, size=n_rows)
    )
    rating = np.clip(np.round(rating, 1), 1.0, 5.0)

    purchase_prob = (
        0.05
        + 0.25 * cart_status
        + 0.08 * (rating / 5)
        + 0.004 * time_spent
        + 0.01 * previous_purchases
        - 0.0008 * price
    )
    purchase_prob = np.clip(purchase_prob, 0.02, 0.95)
    purchase_status = rng.binomial(1, purchase_prob)

    df = pd.DataFrame(
        {
            "User_ID": user_ids,
            "Product_ID": product_ids,
            "Product_Category": categories,
            "Rating": rating,
            "Price": price,
            "Purchase_Status": purchase_status,
            "Number_of_Views": num_views,
            "Cart_Status": cart_status,
            "Time_Spent": time_spent,
            "Previous_Purchases": previous_purchases,
        }
    )

    # Inject realistic missing values (~2%)
    for col in ["Rating", "Time_Spent", "Price"]:
        mask = rng.random(n_rows) < 0.02
        df.loc[mask, col] = np.nan

    # Add a few duplicates
    dup_indices = rng.choice(n_rows, size=15, replace=False)
    df = pd.concat([df, df.iloc[dup_indices]], ignore_index=True)

    return df


if __name__ == "__main__":
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)
    dataset = generate_ecommerce_data()
    output_path = data_dir / "ecommerce_data.csv"
    dataset.to_csv(output_path, index=False)
    print(f"Dataset saved to {output_path}")
    print(f"Shape: {dataset.shape}")
    print(dataset.head())
