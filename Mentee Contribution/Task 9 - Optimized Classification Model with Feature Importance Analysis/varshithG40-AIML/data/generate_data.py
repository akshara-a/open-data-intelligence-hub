"""
Generate synthetic e-commerce customer data with realistic distributions
and meaningful correlations between features and purchase outcome.
"""
import numpy as np
import pandas as pd
import os

def generate_ecommerce_data(n_samples=5000, random_state=42):
    np.random.seed(random_state)
    
    # --- Demographics ---
    customer_id = [f"CUST-{i:05d}" for i in range(1, n_samples + 1)]
    age = np.clip(np.random.normal(35, 12, n_samples), 18, 75).astype(int)
    gender = np.random.choice(["Male", "Female"], n_samples, p=[0.52, 0.48])
    location = np.random.choice(
        ["Urban", "Suburban", "Rural"], n_samples, p=[0.55, 0.30, 0.15]
    )
    
    # --- Device & Traffic ---
    device_type = np.random.choice(
        ["Desktop", "Mobile", "Tablet"], n_samples, p=[0.40, 0.48, 0.12]
    )
    traffic_source = np.random.choice(
        ["Organic Search", "Paid Search", "Social Media", "Email", "Direct", "Referral"],
        n_samples, p=[0.30, 0.20, 0.18, 0.15, 0.10, 0.07]
    )
    
    # --- Browsing Behavior ---
    pages_viewed = np.random.poisson(6, n_samples) + 1
    time_on_site = np.clip(np.random.exponential(15, n_samples) + pages_viewed * 2, 1, 120).round(1)
    products_viewed = np.random.poisson(8, n_samples) + 1
    cart_items = np.random.choice(range(0, 8), n_samples, p=[0.45, 0.25, 0.15, 0.07, 0.04, 0.02, 0.01, 0.01])
    
    # --- History & Engagement ---
    previous_purchases = np.random.poisson(3, n_samples)
    average_order_value = np.clip(np.random.lognormal(3.5, 0.8, n_samples), 10, 2000).round(2)
    discount_used = np.random.choice([0, 1], n_samples, p=[0.60, 0.40])
    email_clicked = np.random.choice([0, 1], n_samples, p=[0.65, 0.35])
    ad_clicked = np.random.choice([0, 1], n_samples, p=[0.70, 0.30])
    review_score_viewed = np.clip(np.random.normal(4.0, 0.8, n_samples), 1.0, 5.0).round(1)
    days_since_last_visit = np.clip(np.random.exponential(20, n_samples), 0, 365).round(0).astype(int)
    session_count = np.random.poisson(5, n_samples) + 1
    
    # --- Purchase Probability (logistic model with meaningful coefficients) ---
    # Create a linear combination that drives purchase probability
    logit = (
        -7.0                                           # base intercept (keeps ~30% positive)
        + 3.5 * (cart_items / 7)                       # more cart items -> much more likely
        + 2.5 * (previous_purchases / 10)              # repeat customers more likely
        + 3.0 * (np.clip(time_on_site, 0, 60) / 60)   # more time -> much more likely
        + 1.5 * discount_used                          # discount seekers more likely
        + 1.3 * email_clicked                          # engaged via email
        + 1.2 * (pages_viewed / 20)                    # more browsing
        + 1.5 * (products_viewed / 25)                 # more products viewed
        + 0.8 * (session_count / 15)                   # frequent visitors
        - 1.0 * (days_since_last_visit / 100)          # long absence -> less likely
        + 0.5 * (review_score_viewed / 5)              # higher reviews = slightly more likely
        + np.random.normal(0, 0.2, n_samples)          # low noise
    )
    
    # Add some interaction effects
    logit += 0.8 * (cart_items > 0) * (time_on_site > 10)  # cart + time interaction
    logit += 0.6 * (previous_purchases > 3) * email_clicked # history + email interaction
    logit += 0.5 * (products_viewed > 10) * (time_on_site > 20) # products + time interaction
    
    # Convert to probability
    prob = 1 / (1 + np.exp(-logit))
    
    # Generate purchase outcome
    purchase = (np.random.random(n_samples) < prob).astype(int)
    
    # --- Introduce a few missing values (~1-2% per column) ---
    for col in ["time_on_site", "review_score_viewed", "average_order_value"]:
        mask = np.random.random(n_samples) < 0.015
        # We'll handle these in the notebook; for now insert NaN
        locals()[col] = locals()[col].astype(float) if col != "time_on_site" else locals()[col]
    
    df = pd.DataFrame({
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
    })
    
    # Inject some missing values
    n_missing = int(n_samples * 0.015)
    for col in ["TimeOnSite", "ReviewScoreViewed", "AverageOrderValue", "PagesViewed"]:
        idx = np.random.choice(n_samples, n_missing, replace=False)
        df.loc[idx, col] = np.nan
    
    return df


if __name__ == "__main__":
    df = generate_ecommerce_data()
    
    output_path = os.path.join(os.path.dirname(__file__), "ecommerce_customer_data.csv")
    df.to_csv(output_path, index=False)
    
    print(f"Dataset generated: {output_path}")
    print(f"Shape: {df.shape}")
    print(f"Purchase rate: {df['Purchase'].mean():.2%}")
    print(f"Missing values:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
