# ==========================================================
# STEP 8 : MODEL COMPARISON
# ==========================================================

import pandas as pd
import joblib

from sklearn.metrics import (
    accuracy_score,
    r2_score,
    silhouette_score
)

print("=" * 60)
print("MODEL COMPARISON")
print("=" * 60)

# ----------------------------------------------------------
# Load Dataset
# ----------------------------------------------------------

df = pd.read_csv("data/processed_ecommerce.csv")

print("\nDataset Loaded Successfully")
print("Shape :", df.shape)

# ----------------------------------------------------------
# Load Models
# ----------------------------------------------------------

ridge_model = joblib.load("models/ridge_model.pkl")
logistic_model = joblib.load("models/logistic_model.pkl")
kmeans_model = joblib.load("models/kmeans_model.pkl")

print("\nAll Models Loaded Successfully")

# ==========================================================
# Ridge Regression
# ==========================================================

ridge_features = [

    "unit_price",
    "quantity",
    "discount_percent",
    "discount_amount",
    "revenue",
    "pages_viewed",
    "time_on_site_sec",
    "added_to_cart",
    "device_type",
    "user_type",
    "marketing_channel",
    "product_category",
    "payment_method",
    "visit_day",
    "visit_month",
    "visit_weekday",
    "visit_season",
    "session_duration_bucket",
    "location"

]

X_reg = df[ridge_features]
y_reg = df["rating"]

ridge_prediction = ridge_model.predict(X_reg)

ridge_score = r2_score(y_reg, ridge_prediction)

# ==========================================================
# Logistic Regression
# ==========================================================

classification_features = [

    "device_type",
    "user_type",
    "marketing_channel",
    "product_category",
    "unit_price",
    "quantity",
    "discount_percent",
    "discount_amount",
    "revenue",
    "pages_viewed",
    "time_on_site_sec",
    "added_to_cart",
    "rating",
    "payment_method",
    "visit_day",
    "visit_month",
    "visit_weekday",
    "visit_season",
    "session_duration_bucket",
    "location"

]

X_cls = df[classification_features]
y_cls = df["purchased"]

cls_prediction = logistic_model.predict(X_cls)

classification_score = accuracy_score(
    y_cls,
    cls_prediction
)

# ==========================================================
# KMeans
# ==========================================================

cluster_features = [

    "pages_viewed",
    "time_on_site_sec",
    "quantity",
    "revenue",
    "rating",
    "added_to_cart"

]

X_cluster = df[cluster_features]

clusters = kmeans_model.predict(X_cluster)

cluster_score = silhouette_score(
    X_cluster,
    clusters
)

# ==========================================================
# Comparison Table
# ==========================================================

results = pd.DataFrame({

    "Model":[

        "Ridge Regression",

        "Logistic Regression",

        "KMeans Clustering"

    ],

    "Metric":[

        "R² Score",

        "Accuracy",

        "Silhouette Score"

    ],

    "Score":[

        round(ridge_score,4),

        round(classification_score,4),

        round(cluster_score,4)

    ]

})

print("\n")
print(results)

# ==========================================================
# Best Model
# ==========================================================

best = results.iloc[
    results["Score"].idxmax()
]

print("\n===============================")
print("BEST MODEL")
print("===============================")

print("Model :", best["Model"])
print("Metric :", best["Metric"])
print("Score :", best["Score"])

# ==========================================================
# Save Results
# ==========================================================

results.to_csv(
    "data/model_comparison.csv",
    index=False
)

print("\nComparison Saved Successfully")

print("Location : data/model_comparison.csv")

print("\nSTEP 8 COMPLETED SUCCESSFULLY")