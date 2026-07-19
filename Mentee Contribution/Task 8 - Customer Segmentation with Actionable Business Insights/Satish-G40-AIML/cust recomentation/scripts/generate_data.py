"""Generate a realistic synthetic customer dataset and save as data/customer_data.csv.

Columns:
- CustomerID, Age, Gender, AnnualIncome, TotalSpending, PurchaseFrequency,
- AverageOrderValue, DaysSinceLastPurchase, WebsiteVisits, DiscountUsage,
- CustomerRating, ProductCategory, PurchaseLikelihood

Run: python scripts/generate_data.py
"""
import os
import random
import numpy as np
import pandas as pd


def generate_customer_row(i):
    customer_id = f"CUST{i:05d}"
    age = int(np.clip(np.random.normal(38, 12), 18, 80))
    gender = np.random.choice(["Male", "Female", "Other"], p=[0.48, 0.48, 0.04])
    annual_income = int(np.clip(np.random.normal(65000, 30000), 8000, 250000))
    purchase_freq = int(np.clip(np.random.poisson(12), 1, 200))
    # draw a single sample for average order value
    avg_order = round(np.clip(np.random.normal(loc=annual_income / (purchase_freq * 1.5 + 1), scale=50), 5, 5000), 2)
    total_spending = round(purchase_freq * avg_order + np.random.normal(0, 200), 2)
    days_since = int(np.clip(np.random.exponential(60), 0, 1500))
    website_visits = int(np.clip(np.random.poisson(visit_lambda := max(1, purchase_freq / 2)), 0, 500))
    discount_usage = round(np.clip(np.random.beta(2, 5) * 1.0, 0, 1), 2)
    customer_rating = int(np.clip(np.random.normal(4, 1), 1, 5))
    categories = ["Electronics", "Clothing", "Home", "Sports", "Beauty", "Books"]
    product_category = np.random.choice(categories, p=[0.2,0.2,0.18,0.15,0.15,0.12])
    # Purchase likelihood correlated with income, recency and visits
    purchase_likelihood = np.clip(0.15 + (annual_income - 20000) / 200000 + (website_visits / 100) - (days_since / 1000) + np.random.normal(0, 0.05), 0, 1)

    return {
        "CustomerID": customer_id,
        "Age": age,
        "Gender": gender,
        "AnnualIncome": annual_income,
        "TotalSpending": total_spending,
        "PurchaseFrequency": purchase_freq,
        "AverageOrderValue": avg_order,
        "DaysSinceLastPurchase": days_since,
        "WebsiteVisits": website_visits,
        "DiscountUsage": discount_usage,
        "CustomerRating": customer_rating,
        "ProductCategory": product_category,
        "PurchaseLikelihood": round(purchase_likelihood, 3),
    }


def main(n=5000, out_path="data/customer_data.csv"):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    rows = [generate_customer_row(i) for i in range(1, n + 1)]
    df = pd.DataFrame(rows)
    df.to_csv(out_path, index=False)
    print(f"Wrote {len(df)} rows to {out_path}")


if __name__ == "__main__":
    main()
