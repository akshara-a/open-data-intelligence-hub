"""
Generate a synthetic e-commerce dataset matching the columns specified in the
mini-project brief. No real dataset was provided, so we simulate one with
realistic, correlated relationships so the downstream models have genuine
signal to learn (rather than pure noise).
"""

import numpy as np
import pandas as pd

RNG = np.random.default_rng(42)
N = 6000

categories = ["Electronics", "Fashion", "Home & Kitchen", "Beauty", "Sports", "Books"]
category_price_mult = {"Electronics": 2.2, "Fashion": 0.8, "Home & Kitchen": 1.1,
                        "Beauty": 0.6, "Sports": 1.0, "Books": 0.3}

user_ids = RNG.integers(1000, 1000 + N // 3, size=N)  # some users appear multiple times
product_ids = RNG.integers(5000, 5000 + N // 4, size=N)
product_category = RNG.choice(categories, size=N)

base_price = RNG.gamma(shape=2.0, scale=15, size=N) + 5
price = np.round(base_price * np.array([category_price_mult[c] for c in product_category]), 2)

previous_purchases = RNG.poisson(lam=3.5, size=N)
num_views = RNG.poisson(lam=6, size=N) + 1
time_spent = np.round(np.clip(RNG.normal(loc=3 + 0.4 * np.log1p(num_views), scale=1.5, size=N), 0.2, None), 2)  # minutes

# Cart status more likely with more views/time spent
cart_logit = -2.0 + 0.15 * num_views + 0.3 * time_spent - 0.01 * price
cart_prob = 1 / (1 + np.exp(-cart_logit))
cart_status = (RNG.random(N) < cart_prob).astype(int)

# Rating depends on price-value, previous purchases (loyalty), time spent (engagement)
rating_signal = (
    3.2
    + 0.35 * cart_status
    + 0.05 * np.log1p(previous_purchases)
    + 0.08 * np.log1p(time_spent)
    - 0.004 * price
    + RNG.normal(0, 0.6, size=N)
)
rating = np.clip(np.round(rating_signal), 1, 5).astype(int)

# Purchase status depends on cart status, rating, previous purchases, views
purchase_logit = (
    -3.0
    + 1.8 * cart_status
    + 0.35 * (rating - 3)
    + 0.12 * previous_purchases
    + 0.05 * num_views
    - 0.005 * price
)
purchase_prob = 1 / (1 + np.exp(-purchase_logit))
purchase_status = (RNG.random(N) < purchase_prob).astype(int)

df = pd.DataFrame({
    "User_ID": user_ids,
    "Product_ID": product_ids,
    "Product_Category": product_category,
    "Rating": rating,
    "Price": price,
    "Purchase_Status": purchase_status,
    "Number_of_Views": num_views,
    "Cart_Status": cart_status,
    "Time_Spent": time_spent,
    "Previous_Purchases": previous_purchases,
})

# Inject a small amount of realistic messiness: missing values + duplicates
missing_idx = RNG.choice(df.index, size=int(0.02 * N), replace=False)
df.loc[missing_idx, "Time_Spent"] = np.nan
missing_idx2 = RNG.choice(df.index, size=int(0.01 * N), replace=False)
df.loc[missing_idx2, "Rating"] = np.nan

dup_rows = df.sample(n=40, random_state=1)
df = pd.concat([df, dup_rows], ignore_index=True)

df.to_csv("/home/claude/project/ecommerce_dataset.csv", index=False)
print(df.shape)
print(df.head())
print(df.isna().sum())
