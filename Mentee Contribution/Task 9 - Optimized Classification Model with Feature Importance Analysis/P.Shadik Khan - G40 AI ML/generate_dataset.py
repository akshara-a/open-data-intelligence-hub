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