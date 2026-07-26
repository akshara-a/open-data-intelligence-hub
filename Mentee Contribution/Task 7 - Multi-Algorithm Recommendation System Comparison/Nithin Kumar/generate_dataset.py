import pandas as pd
import numpy as np
import os

# Reproducible random data
np.random.seed(42)

# Number of records
n = 1500

# Generate e-commerce data
user_ids = np.random.randint(1001, 1301, n)
product_ids = np.random.randint(2001, 2101, n)

categories = np.random.choice(
    ["Electronics", "Fashion", "Home", "Books", "Beauty"],
    n
)

price = np.round(np.random.uniform(100, 5000, n), 2)
views = np.random.randint(1, 30, n)
cart_status = np.random.randint(0, 2, n)
time_spent = np.round(np.random.uniform(1, 30, n), 2)
previous_purchases = np.random.randint(0, 20, n)

# Create rating with some relationship to customer behaviour
rating = (
    1.5
    + (views * 0.04)
    + (time_spent * 0.05)
    + (previous_purchases * 0.04)
    + (cart_status * 0.3)
    + np.random.normal(0, 0.5, n)
)

rating = np.clip(rating, 1, 5)
rating = np.round(rating, 1)

# Purchase probability based on behaviour
purchase_score = (
    (views * 0.08)
    + (time_spent * 0.10)
    + (previous_purchases * 0.10)
    + (cart_status * 1.5)
    + (rating * 0.5)
    - 4.5
)

purchase_probability = 1 / (1 + np.exp(-purchase_score))

purchase_status = np.random.binomial(
    1,
    np.clip(purchase_probability, 0, 1)
)

# Total amount spent for clustering
total_amount_spent = np.round(
    previous_purchases * np.random.uniform(200, 2000, n),
    2
)

# Build DataFrame
df = pd.DataFrame({
    "UserID": user_ids,
    "ProductID": product_ids,
    "ProductCategory": categories,
    "Price": price,
    "NumberOfViews": views,
    "CartStatus": cart_status,
    "TimeSpent": time_spent,
    "PreviousPurchases": previous_purchases,
    "Rating": rating,
    "PurchaseStatus": purchase_status,
    "TotalAmountSpent": total_amount_spent
})

# Create data directory if necessary
os.makedirs("data", exist_ok=True)

# Save dataset
file_path = "data/ecommerce_recommendation_data.csv"
df.to_csv(file_path, index=False)

print("=" * 60)
print("TASK 7 - E-COMMERCE DATASET GENERATED SUCCESSFULLY")
print("=" * 60)
print(f"Dataset Shape: {df.shape}")
print(f"Dataset saved to: {file_path}")

print("\nFirst 5 rows:")
print(df.head())

print("\nColumns:")
print(df.columns.tolist())

print("\nPurchase Distribution:")
print(df["PurchaseStatus"].value_counts())

print("\nDataset generation completed successfully!")