# ============================================
# E-Commerce Recommendation System
# ============================================

import os
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, LogisticRegression
from sklearn.cluster import KMeans
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    silhouette_score,
)
from sklearn.model_selection import GridSearchCV

import matplotlib.pyplot as plt


def generate_sample_dataset(n_users=200, n_events=2000, random_state=42):
    np.random.seed(random_state)
    user_ids = np.random.choice(range(1000, 1000 + n_users), size=n_events)
    event_types = np.random.choice(["view", "cart", "purchase"], size=n_events, p=[0.6, 0.25, 0.15])
    prices = np.round(np.random.uniform(5, 500, size=n_events), 2)
    category_codes = np.random.choice(
        ["electronics", "fashion", "beauty", "home", "sports", "toys"],
        size=n_events,
    )
    return pd.DataFrame(
        {
            "user_id": user_ids,
            "event_type": event_types,
            "price": prices,
            "category_code": category_codes,
        }
    )


def load_dataset(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)

    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        print(f"Loaded dataset from {file_path}")
    else:
        print(f"Dataset file not found: {file_path}")
        print("Generating a synthetic dataset for demonstration.")
        df = generate_sample_dataset()

    print(df.head())
    return df


def main():
    df = load_dataset("ecommerce.csv")

    # ----------------------------------------
    # Data Cleaning
    # ----------------------------------------
    df.drop_duplicates(inplace=True)
    df.ffill(inplace=True)

    # Dataset-specific column mapping
    id_col = "customer_id" if "customer_id" in df.columns else "user_id"
    price_col = "unit_price" if "unit_price" in df.columns else "price"
    category_col = "product_category" if "product_category" in df.columns else "category_code"
    purchased_col = "purchased" if "purchased" in df.columns else "event_type"
    added_to_cart_col = "added_to_cart" if "added_to_cart" in df.columns else "event_type"
    rating_col = "rating" if "rating" in df.columns else None
    time_col = "time_on_site_sec" if "time_on_site_sec" in df.columns else None
    revenue_col = "revenue" if "revenue" in df.columns else None

    # Normalize column names for downstream processing
    rename_map = {}
    if id_col != "user_id":
        rename_map[id_col] = "user_id"
        id_col = "user_id"
    if price_col != "price":
        rename_map[price_col] = "price"
        price_col = "price"
    if category_col != "category_code":
        rename_map[category_col] = "category_code"
        category_col = "category_code"

    if rename_map:
        df.rename(columns=rename_map, inplace=True)

    # ----------------------------------------
    # Feature Engineering
    # ----------------------------------------
    if purchased_col == "event_type":
        df["Purchase_Status"] = np.where(df[purchased_col] == "purchase", 1, 0)
    else:
        df["Purchase_Status"] = np.where(df[purchased_col] == 1, 1, 0)

    if added_to_cart_col == "event_type":
        df["Cart_Addition"] = np.where(df[added_to_cart_col] == "cart", 1, 0)
    else:
        df["Cart_Addition"] = np.where(df[added_to_cart_col] == 1, 1, 0)

    df["Previous_Purchases"] = df.groupby(id_col)["Purchase_Status"].cumsum()
    if revenue_col:
        df["Total_Spending"] = df.groupby(id_col)[revenue_col].cumsum()
    else:
        df["Total_Spending"] = df.groupby(id_col)["price"].cumsum()

    if rating_col is None:
        np.random.seed(42)
        df["Rating"] = np.random.randint(1, 6, len(df))
    else:
        df["Rating"] = df["rating"].astype(float)

    if time_col is None:
        df["Browsing_Time"] = np.random.randint(20, 500, len(df))
    else:
        df["Browsing_Time"] = df["time_on_site_sec"].astype(float)

    encoder = LabelEncoder()
    df["category_code"] = encoder.fit_transform(df[category_col].astype(str))

    # ============================================
    # PART A : REGRESSION
    # ============================================
    X_reg = df[
        [
            "price",
            "Browsing_Time",
            "Previous_Purchases",
            "Cart_Addition",
            "Total_Spending",
            "category_code",
        ]
    ]
    y_reg = df["Rating"]

    X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(
        X_reg, y_reg, test_size=0.2, random_state=42
    )

    scaler_reg = StandardScaler()
    X_train_reg = scaler_reg.fit_transform(X_train_reg)
    X_test_reg = scaler_reg.transform(X_test_reg)

    model = LinearRegression()
    model.fit(X_train_reg, y_train_reg)
    pred_reg = model.predict(X_test_reg)

    print("Regression Results")
    print("MAE:", mean_absolute_error(y_test_reg, pred_reg))
    print("RMSE:", np.sqrt(mean_squared_error(y_test_reg, pred_reg)))
    print("R2:", r2_score(y_test_reg, pred_reg))

    ridge = Ridge()
    ridge_params = {"alpha": [0.01, 0.1, 1, 10, 100]}
    grid_ridge = GridSearchCV(
        ridge,
        ridge_params,
        cv=5,
        scoring="neg_mean_squared_error",
    )
    grid_ridge.fit(X_train_reg, y_train_reg)
    print("Best Ridge Parameters:", grid_ridge.best_params_)

    # ============================================
    # PART B : CLASSIFICATION
    # ============================================
    X_clf = df[
        [
            "Browsing_Time",
            "Cart_Addition",
            "Previous_Purchases",
            "Rating",
            "price",
            "Total_Spending",
        ]
    ]
    y_clf = df["Purchase_Status"]

    X_train_clf, X_test_clf, y_train_clf, y_test_clf = train_test_split(
        X_clf, y_clf, test_size=0.2, random_state=42
    )

    scaler_clf = StandardScaler()
    X_train_clf = scaler_clf.fit_transform(X_train_clf)
    X_test_clf = scaler_clf.transform(X_test_clf)

    log_model = LogisticRegression(max_iter=1000)
    log_model.fit(X_train_clf, y_train_clf)

    pred_clf = log_model.predict(X_test_clf)
    prob_clf = log_model.predict_proba(X_test_clf)[:, 1]

    print("Classification Results")
    print("Accuracy:", accuracy_score(y_test_clf, pred_clf))
    print("Precision:", precision_score(y_test_clf, pred_clf, zero_division=0))
    print("Recall:", recall_score(y_test_clf, pred_clf, zero_division=0))
    print("F1:", f1_score(y_test_clf, pred_clf, zero_division=0))
    print("ROC-AUC:", roc_auc_score(y_test_clf, prob_clf))

    log_params = {
        "C": [0.01, 0.1, 1, 10],
        "solver": ["liblinear", "lbfgs"],
    }
    grid_log = GridSearchCV(
        LogisticRegression(max_iter=1000),
        log_params,
        cv=5,
        scoring="accuracy",
    )
    grid_log.fit(X_train_clf, y_train_clf)
    print("Best Logistic Regression Parameters:", grid_log.best_params_)

    # ============================================
    # PART C : CLUSTERING
    # ============================================
    cluster_data = df[
        ["Browsing_Time", "Previous_Purchases", "Rating", "Total_Spending", "Cart_Addition"]
    ]
    cluster_data_scaled = scaler_clf.fit_transform(cluster_data)

    inertia = []
    for i in range(2, 11):
        km = KMeans(n_clusters=i, random_state=42)
        km.fit(cluster_data_scaled)
        inertia.append(km.inertia_)

    plt.figure(figsize=(8, 5))
    plt.plot(range(2, 11), inertia, marker="o")
    plt.xlabel("Clusters")
    plt.ylabel("Inertia")
    plt.title("Elbow Method")
    plt.tight_layout()
    plt.show()

    kmeans = KMeans(n_clusters=4, random_state=42)
    labels = kmeans.fit_predict(cluster_data_scaled)
    df["Cluster"] = labels

    print("Silhouette Score")
    print(silhouette_score(cluster_data_scaled, labels))
    print(df["Cluster"].value_counts())

    cluster_names = {
        0: "Frequent Buyers",
        1: "Browsers",
        2: "Discount Sensitive",
        3: "High Value Customers",
    }
    df["Segment"] = df["Cluster"].map(cluster_names)

    print(df[["user_id", "Segment"]].head())
    print("\nProject Completed Successfully")


if __name__ == "__main__":
    main()
