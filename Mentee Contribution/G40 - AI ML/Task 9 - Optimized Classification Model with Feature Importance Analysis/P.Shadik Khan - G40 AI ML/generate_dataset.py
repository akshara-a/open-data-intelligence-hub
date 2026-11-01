import numpy as np
import pandas as pd

RANDOM_STATE = 42
rng = np.random.default_rng(RANDOM_STATE)

N_CUSTOMERS = 2000

customer_id = np.arange(100001, 100001 + N_CUSTOMERS)

age = rng.integers(18, 66, N_CUSTOMERS)

gender = rng.choice(
    ["Male", "Female", "Other"],
    size=N_CUSTOMERS,
    p=[0.48, 0.48, 0.04]
)

location = rng.choice(
    ["North", "South", "East", "West", "Central"],
    size=N_CUSTOMERS
)

device_type = rng.choice(
    ["Mobile", "Desktop", "Tablet"],
    size=N_CUSTOMERS,
    p=[0.55, 0.35, 0.10]
)

traffic_source = rng.choice(
    ["Search", "Social Media", "Email", "Direct", "Advertisement"],
    size=N_CUSTOMERS,
    p=[0.30, 0.20, 0.15, 0.20, 0.15]
)

pages_viewed = rng.poisson(8, N_CUSTOMERS) + 1

time_on_site = np.round(
    rng.gamma(shape=2.5, scale=4.0, size=N_CUSTOMERS),
    2
)

products_viewed = np.maximum(
    1,
    np.round(pages_viewed * rng.uniform(0.35, 0.80, N_CUSTOMERS))
).astype(int)

cart_items = np.minimum(
    products_viewed,
    rng.poisson(1.2, N_CUSTOMERS)
)

previous_purchases = rng.poisson(1.5, N_CUSTOMERS)

average_order_value = np.round(
    np.clip(
        rng.normal(65, 25, N_CUSTOMERS)
        + previous_purchases * 8,
        15,
        250
    ),
    2
)

discount_used = rng.choice(
    [0, 1],
    size=N_CUSTOMERS,
    p=[0.65, 0.35]
)

email_clicked = rng.choice(
    [0, 1],
    size=N_CUSTOMERS,
    p=[0.72, 0.28]
)

ad_clicked = rng.choice(
    [0, 1],
    size=N_CUSTOMERS,
    p=[0.70, 0.30]
)

review_score_viewed = np.round(
    np.clip(rng.normal(4.0, 0.55, N_CUSTOMERS), 1, 5),
    2
)

days_since_last_visit = rng.integers(0, 61, N_CUSTOMERS)

session_count = rng.poisson(4, N_CUSTOMERS) + 1


# Purchase probability is influenced by meaningful
# customer-behavior variables.
logit = (
    -3.2
    + 0.075 * cart_items
    + 0.055 * previous_purchases
    + 0.035 * time_on_site
    + 0.025 * pages_viewed
    + 0.45 * discount_used
    + 0.55 * email_clicked
    + 0.30 * ad_clicked
    + 0.08 * session_count
    + 0.10 * (review_score_viewed - 3)
    - 0.018 * days_since_last_visit
)

purchase_probability = 1 / (1 + np.exp(-logit))

purchase = rng.binomial(
    1,
    purchase_probability
)


df = pd.DataFrame(
    {
        "CustomerID": customer_id,
        "Age": age,
        "Gender": gender,
        "Location": location,
        "DeviceType": device_type,
        "TrafficSource": traffic_source,
        "PagesViewed": pages_viewed,
        "TimeOnSite": time_on_site,
        "ProductsViewed": products_viewed,
        "CartItems": cart_items,
        "PreviousPurchases": previous_purchases,
        "AverageOrderValue": average_order_value,
        "DiscountUsed": discount_used,
        "EmailClicked": email_clicked,
        "AdClicked": ad_clicked,
        "ReviewScoreViewed": review_score_viewed,
        "DaysSinceLastVisit": days_since_last_visit,
        "SessionCount": session_count,
        "Purchase": purchase,
    }
)


# Add a small number of realistic missing values.
missing_columns = [
    "Age",
    "TimeOnSite",
    "AverageOrderValue",
    "Gender",
    "TrafficSource",
]

for column in missing_columns:
    missing_indices = rng.choice(
        df.index,
        size=int(N_CUSTOMERS * 0.02),
        replace=False
    )
    df.loc[missing_indices, column] = np.nan


output_path = (
    "Mentee Contribution/"
    "Task 9 - Optimized Classification Model with Feature Importance Analysis/"
    "P.Shadik Khan - G40 AI ML/data/ecommerce_customer_data.csv"
)

df.to_csv(output_path, index=False)

print("Dataset created successfully!")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")
print("\nPurchase distribution:")
print(df["Purchase"].value_counts())
print("\nPurchase percentage:")
print(df["Purchase"].value_counts(normalize=True).round(3))
print(f"\nSaved to: {output_path}")
import os

import numpy as np
import pandas as pd


def create_customer_dataset(number_of_rows: int = 1500) -> pd.DataFrame:
    """Create a sample e-commerce customer purchase dataset."""

    np.random.seed(42)

    age = np.random.randint(18, 66, number_of_rows)
    gender = np.random.choice(
        ["Male", "Female"],
        number_of_rows,
    )
    device_type = np.random.choice(
        ["Mobile", "Desktop", "Tablet"],
        number_of_rows,
        p=[0.55, 0.35, 0.10],
    )
    traffic_source = np.random.choice(
        ["Search", "Social Media", "Email", "Direct", "Advertisement"],
        number_of_rows,
    )

    pages_viewed = np.random.randint(1, 21, number_of_rows)
    time_on_site = np.round(np.random.uniform(1, 30, number_of_rows), 2)
    products_viewed = np.random.randint(1, 16, number_of_rows)
    cart_items = np.random.randint(0, 8, number_of_rows)
    previous_purchases = np.random.randint(0, 12, number_of_rows)
    average_order_value = np.round(
        np.random.uniform(200, 8000, number_of_rows),
        2,
    )
    discount_used = np.random.choice([0, 1], number_of_rows)
    email_clicked = np.random.choice([0, 1], number_of_rows)
    ad_clicked = np.random.choice([0, 1], number_of_rows)
    days_since_last_visit = np.random.randint(0, 91, number_of_rows)
    session_count = np.random.randint(1, 25, number_of_rows)

    purchase_score = (
        -4.5
        + 0.20 * pages_viewed
        + 0.12 * time_on_site
        + 0.60 * cart_items
        + 0.16 * previous_purchases
        + 0.45 * discount_used
        + 0.35 * email_clicked
        + 0.30 * ad_clicked
        - 0.018 * days_since_last_visit
    )

    purchase_probability = 1 / (1 + np.exp(-purchase_score))
    purchase = np.random.binomial(1, purchase_probability)

    data = pd.DataFrame(
        {
            "CustomerID": range(1001, 1001 + number_of_rows),
            "Age": age,
            "Gender": gender,
            "DeviceType": device_type,
            "TrafficSource": traffic_source,
            "PagesViewed": pages_viewed,
            "TimeOnSite": time_on_site,
            "ProductsViewed": products_viewed,
            "CartItems": cart_items,
            "PreviousPurchases": previous_purchases,
            "AverageOrderValue": average_order_value,
            "DiscountUsed": discount_used,
            "EmailClicked": email_clicked,
            "AdClicked": ad_clicked,
            "DaysSinceLastVisit": days_since_last_visit,
            "SessionCount": session_count,
            "Purchase": purchase,
        }
    )

    return data


if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)

    customer_data = create_customer_dataset()
    output_path = "data/customer_purchase_data.csv"

    customer_data.to_csv(output_path, index=False)

    print("Dataset created successfully.")
    print(f"Saved at: {output_path}")
    print(f"Rows: {customer_data.shape[0]}")
    print(f"Columns: {customer_data.shape[1]}")
    print(customer_data.head())
