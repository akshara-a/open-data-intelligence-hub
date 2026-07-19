import numpy as np
import pandas as pd
from pathlib import Path


def generate_synthetic_data(output_dir: str | Path | None = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    output_dir = Path(output_dir or Path(__file__).resolve().parent.parent / "data")
    output_dir.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(42)
    n_customers = 500

    customer_ids = [f"C{idx:03d}" for idx in range(1, n_customers + 1)]

    age = rng.integers(18, 70, size=n_customers)
    gender = rng.choice(["Female", "Male", "Other"], size=n_customers, p=[0.5, 0.45, 0.05])
    annual_income = np.clip(rng.normal(65000, 22000, size=n_customers), 18000, 180000).round(2)
    purchase_frequency = np.clip(rng.poisson(4.2, size=n_customers) + 1, 1, 25)
    avg_order_value = np.clip(rng.normal(95, 28, size=n_customers), 25, 500).round(2)
    website_visits = np.clip(rng.poisson(22, size=n_customers) + 5, 5, 400)
    discount_usage = np.clip(rng.beta(2, 5, size=n_customers), 0.0, 0.7).round(3)
    customer_rating = np.clip(rng.normal(4.1, 0.5, size=n_customers), 2.0, 5.0).round(2)
    product_categories = rng.choice(
        ["Electronics", "Fashion", "Home", "Sports", "Beauty"],
        size=n_customers,
        p=[0.28, 0.24, 0.2, 0.16, 0.12],
    )

    base_engagement = 0.45 + 0.004 * purchase_frequency + 0.0006 * annual_income / 1000 - 0.08 * discount_usage
    purchase_likelihood = (base_engagement + rng.normal(0, 0.1, size=n_customers)).clip(0, 1)
    purchase_likelihood = (purchase_likelihood > 0.58).astype(int)

    customer_df = pd.DataFrame(
        {
            "CustomerID": customer_ids,
            "Age": age,
            "Gender": gender,
            "AnnualIncome": annual_income,
            "PurchaseFrequency": purchase_frequency,
            "AverageOrderValue": avg_order_value,
            "WebsiteVisits": website_visits,
            "DiscountUsage": discount_usage,
            "CustomerRating": customer_rating,
            "ProductCategory": product_categories,
            "PurchaseLikelihood": purchase_likelihood,
        }
    )

    customer_df["TotalSpending"] = (
        customer_df["PurchaseFrequency"] * customer_df["AverageOrderValue"] * (1 - 0.35 * customer_df["DiscountUsage"])
    ).round(2)
    customer_df["DaysSinceLastPurchase"] = np.clip(
        30 + (12 - customer_df["PurchaseFrequency"]) * 8 + rng.integers(5, 60, size=n_customers), 5, 360
    )

    reference_date = pd.Timestamp("2026-06-30")
    records = []
    order_counter = 1
    for _, row in customer_df.iterrows():
        freq = int(row["PurchaseFrequency"])
        days_since_last = int(row["DaysSinceLastPurchase"])
        last_order_date = reference_date - pd.Timedelta(days=days_since_last)
        dates = []
        current_date = last_order_date
        for _ in range(freq):
            dates.append(current_date)
            current_date = current_date - pd.Timedelta(days=int(rng.integers(7, 45)))
        dates = sorted(dates)
        for idx, order_date in enumerate(dates):
            amount = row["AverageOrderValue"] * (1 + rng.uniform(-0.2, 0.25))
            if rng.random() < 0.12:
                amount *= 0.85
            if idx == len(dates) - 1 and row["DiscountUsage"] > 0.35:
                amount *= 1 - 0.15 * row["DiscountUsage"]
            records.append(
                {
                    "CustomerID": row["CustomerID"],
                    "OrderID": f"O{order_counter:05d}",
                    "OrderDate": order_date,
                    "Amount": round(amount, 2),
                    "ProductCategory": row["ProductCategory"],
                    "DiscountApplied": bool(rng.random() < row["DiscountUsage"]),
                }
            )
            order_counter += 1

    transactions_df = pd.DataFrame(records)
    transactions_df = transactions_df.sort_values(["CustomerID", "OrderDate"]).reset_index(drop=True)

    customer_df.to_csv(output_dir / "customer_data.csv", index=False)
    transactions_df.to_csv(output_dir / "transactions.csv", index=False)
    return customer_df, transactions_df


if __name__ == "__main__":
    generate_synthetic_data()
