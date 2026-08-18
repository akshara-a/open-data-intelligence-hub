import os
import numpy as np
import pandas as pd

def generate_ecommerce_dataset(num_samples=1500, random_state=42):
    """
    Generates a realistic synthetic e-commerce customer purchase dataset.
    """
    np.random.seed(random_state)

    customer_ids = [f"CUST_{1000 + i}" for i in range(num_samples)]
    ages = np.random.randint(18, 70, size=num_samples)
    genders = np.random.choice(["Female", "Male", "Other"], size=num_samples, p=[0.52, 0.45, 0.03])
    locations = np.random.choice(["North America", "Europe", "Asia-Pacific", "Latin America", "Middle East"], size=num_samples, p=[0.40, 0.30, 0.18, 0.08, 0.04])
    device_types = np.random.choice(["Mobile", "Desktop", "Tablet"], size=num_samples, p=[0.55, 0.35, 0.10])
    traffic_sources = np.random.choice(["Search Engine", "Social Media", "Email", "Direct", "Advertisement"], size=num_samples, p=[0.35, 0.25, 0.15, 0.15, 0.10])
    
    pages_viewed = np.random.poisson(lam=6, size=num_samples) + 1
    time_on_site = np.round(np.random.exponential(scale=8.0, size=num_samples) + 0.5, 2)
    products_viewed = np.minimum(pages_viewed, np.random.randint(1, 15, size=num_samples))
    
    # Cart items correlated with pages viewed
    cart_items = np.clip(np.random.binomial(n=pages_viewed, p=0.3), 0, 10)
    
    previous_purchases = np.random.negative_binomial(n=2, p=0.4, size=num_samples)
    avg_order_value = np.where(previous_purchases > 0, np.round(np.random.gamma(shape=3.0, scale=30.0, size=num_samples), 2), 0.0)
    
    discount_used = np.random.choice([0, 1], size=num_samples, p=[0.65, 0.35])
    email_clicked = np.random.choice([0, 1], size=num_samples, p=[0.75, 0.25])
    ad_clicked = np.random.choice([0, 1], size=num_samples, p=[0.70, 0.30])
    
    review_score_viewed = np.round(np.random.uniform(2.5, 5.0, size=num_samples), 1)
    days_since_last_visit = np.random.randint(1, 90, size=num_samples)
    session_count = np.random.poisson(lam=4, size=num_samples) + 1

    # Probability of purchase based on key features
    logit = (
        -3.2
        + 0.65 * cart_items
        + 0.25 * previous_purchases
        + 0.08 * time_on_site
        + 0.12 * pages_viewed
        + 0.45 * discount_used
        + 0.35 * email_clicked
        - 0.02 * days_since_last_visit
        + 0.30 * (device_types == "Desktop").astype(int)
        + np.random.normal(0, 0.5, size=num_samples)
    )
    
    prob = 1 / (1 + np.exp(-logit))
    purchase = (prob > 0.5).astype(int)

    df = pd.DataFrame({
        "CustomerID": customer_ids,
        "Age": ages,
        "Gender": genders,
        "Location": locations,
        "DeviceType": device_types,
        "TrafficSource": traffic_sources,
        "PagesViewed": pages_viewed,
        "TimeOnSite": time_on_site,
        "ProductsViewed": products_viewed,
        "CartItems": cart_items,
        "PreviousPurchases": previous_purchases,
        "AverageOrderValue": avg_order_value,
        "DiscountUsed": discount_used,
        "EmailClicked": email_clicked,
        "AdClicked": ad_clicked,
        "ReviewScoreViewed": review_score_viewed,
        "DaysSinceLastVisit": days_since_last_visit,
        "SessionCount": session_count,
        "Purchase": purchase
    })

    # Introduce minor missing values & duplicates to showcase realistic data cleaning
    missing_indices_num = np.random.choice(num_samples, size=15, replace=False)
    df.loc[missing_indices_num, "AverageOrderValue"] = np.nan
    
    missing_indices_time = np.random.choice(num_samples, size=10, replace=False)
    df.loc[missing_indices_time, "TimeOnSite"] = np.nan
    
    missing_indices_cat = np.random.choice(num_samples, size=8, replace=False)
    df.loc[missing_indices_cat, "Gender"] = np.nan

    # Add 5 duplicate rows
    duplicates = df.iloc[:5].copy()
    df = pd.concat([df, duplicates], ignore_index=True)

    return df

if __name__ == "__main__":
    output_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, "ecommerce_customer_data.csv")
    
    df = generate_ecommerce_dataset()
    df.to_csv(file_path, index=False)
    print(f"Dataset successfully created at '{file_path}' with shape {df.shape}.")
    print(f"Target distribution:\n{df['Purchase'].value_counts(normalize=True)}")
