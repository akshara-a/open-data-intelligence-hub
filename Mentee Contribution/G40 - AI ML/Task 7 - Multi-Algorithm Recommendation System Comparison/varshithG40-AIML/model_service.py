"""Model service for the recommendation system web interface."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

RANDOM_STATE = 42
BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "data" / "ecommerce_data.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
MODELS_DIR = BASE_DIR / "models"
RESULTS_PATH = OUTPUT_DIR / "model_results.json"

CATEGORIES = ["Electronics", "Clothing", "Home", "Books", "Sports", "Beauty"]

CLUSTER_LABELS = {
    0: ("Active Buyers", "Frequent viewers with solid purchase activity."),
    1: ("Window Shoppers", "Browse often but purchase less — good retargeting candidates."),
    2: ("High-Value Customers", "Top spenders and purchasers — loyalty program targets."),
    3: ("Regular Buyers", "Steady mid-tier customers with consistent spend."),
    4: ("Engaged Browsers", "High time-on-site, moderate purchases."),
    5: ("Occasional Buyers", "Lower engagement — win-back campaigns recommended."),
}

REGRESSION_FEATURES = [
    "Price", "Product_Category", "Number_of_Views",
    "Cart_Status", "Time_Spent", "Previous_Purchases",
]
CLASSIFICATION_FEATURES = REGRESSION_FEATURES + ["Rating"]
CLUSTER_FEATURES = [
    "products_viewed", "num_purchases", "avg_rating",
    "avg_time_spent", "total_spent", "cart_additions",
]


@dataclass
class RecommendationEngine:
    category_encoder: LabelEncoder
    regression_scaler: StandardScaler
    classification_scaler: StandardScaler
    cluster_scaler: StandardScaler
    regression_model: GradientBoostingRegressor
    classification_model: LogisticRegression
    cluster_model: KMeans
    customer_segments: pd.DataFrame
    raw_data: pd.DataFrame
    results: dict


def preprocess(df: pd.DataFrame, encoder: LabelEncoder | None = None) -> tuple[pd.DataFrame, LabelEncoder]:
    df = df.copy().drop_duplicates()
    numeric_cols = ["Rating", "Price", "Number_of_Views", "Time_Spent", "Previous_Purchases"]
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())

    if encoder is None:
        encoder = LabelEncoder()
        encoder.fit(CATEGORIES)
    df["Product_Category"] = encoder.transform(df["Product_Category"])
    return df, encoder


def build_customer_features(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("User_ID").agg(
        products_viewed=("Number_of_Views", "sum"),
        num_purchases=("Purchase_Status", "sum"),
        avg_rating=("Rating", "mean"),
        avg_time_spent=("Time_Spent", "mean"),
        total_spent=("Price", lambda x: (x * df.loc[x.index, "Purchase_Status"]).sum()),
        cart_additions=("Cart_Status", "sum"),
    ).reset_index()


def train_and_save_models() -> RecommendationEngine:
    MODELS_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)

    raw = pd.read_csv(DATA_PATH)
    df, encoder = preprocess(raw)

    # Regression
    X_reg = df[REGRESSION_FEATURES]
    y_reg = df["Rating"]
    X_reg_train, _, y_reg_train, _ = train_test_split(
        X_reg, y_reg, test_size=0.2, random_state=RANDOM_STATE
    )
    reg_scaler = StandardScaler()
    X_reg_train_s = reg_scaler.fit_transform(X_reg_train)
    reg_model = GradientBoostingRegressor(n_estimators=100, random_state=RANDOM_STATE)
    reg_model.fit(X_reg_train_s, y_reg_train)

    # Classification
    X_clf = df[CLASSIFICATION_FEATURES]
    y_clf = df["Purchase_Status"]
    X_clf_train, _, y_clf_train, _ = train_test_split(
        X_clf, y_clf, test_size=0.2, random_state=RANDOM_STATE, stratify=y_clf
    )
    clf_scaler = StandardScaler()
    X_clf_train_s = clf_scaler.fit_transform(X_clf_train)
    clf_model = GridSearchCV(
        LogisticRegression(random_state=RANDOM_STATE),
        param_grid={
            "C": [0.01, 0.1, 1, 10],
            "solver": ["liblinear", "lbfgs"],
            "max_iter": [100, 200, 500],
        },
        cv=5,
        scoring="f1",
    )
    clf_model.fit(X_clf_train_s, y_clf_train)
    best_clf = clf_model.best_estimator_

    # Clustering
    customer = build_customer_features(df)
    X_clust = customer[CLUSTER_FEATURES]
    clust_scaler = StandardScaler()
    X_clust_s = clust_scaler.fit_transform(X_clust)
    n_clusters = 6
    if RESULTS_PATH.exists():
        with open(RESULTS_PATH) as f:
            saved = json.load(f)
        n_clusters = saved.get("clustering", {}).get("K-Means", {}).get("n_clusters", 6)
    cluster_model = KMeans(n_clusters=n_clusters, random_state=RANDOM_STATE, n_init=10)
    labels = cluster_model.fit_predict(X_clust_s)
    customer["KMeans_Cluster"] = labels
    customer.to_csv(OUTPUT_DIR / "customer_segments.csv", index=False)

    engine = RecommendationEngine(
        category_encoder=encoder,
        regression_scaler=reg_scaler,
        classification_scaler=clf_scaler,
        cluster_scaler=clust_scaler,
        regression_model=reg_model,
        classification_model=best_clf,
        cluster_model=cluster_model,
        customer_segments=customer,
        raw_data=raw,
        results=json.loads(RESULTS_PATH.read_text()) if RESULTS_PATH.exists() else {},
    )

    joblib.dump(engine, MODELS_DIR / "engine.pkl")
    return engine


def load_engine() -> RecommendationEngine:
    model_path = MODELS_DIR / "engine.pkl"
    if model_path.exists():
        return joblib.load(model_path)
    return train_and_save_models()


def encode_category(encoder: LabelEncoder, category: str) -> int:
    if category not in encoder.classes_:
        raise ValueError(f"Unknown category: {category}")
    return int(encoder.transform([category])[0])


def predict_rating(engine: RecommendationEngine, inputs: dict) -> float:
    category = encode_category(engine.category_encoder, inputs["product_category"])
    row = pd.DataFrame([{
        "Price": inputs["price"],
        "Product_Category": category,
        "Number_of_Views": inputs["number_of_views"],
        "Cart_Status": inputs["cart_status"],
        "Time_Spent": inputs["time_spent"],
        "Previous_Purchases": inputs["previous_purchases"],
    }])
    scaled = engine.regression_scaler.transform(row)
    rating = float(engine.regression_model.predict(scaled)[0])
    return round(np.clip(rating, 1.0, 5.0), 2)


def predict_purchase(engine: RecommendationEngine, inputs: dict) -> tuple[int, float]:
    category = encode_category(engine.category_encoder, inputs["product_category"])
    row = pd.DataFrame([{
        "Price": inputs["price"],
        "Product_Category": category,
        "Number_of_Views": inputs["number_of_views"],
        "Cart_Status": inputs["cart_status"],
        "Time_Spent": inputs["time_spent"],
        "Previous_Purchases": inputs["previous_purchases"],
        "Rating": inputs["rating"],
    }])
    scaled = engine.classification_scaler.transform(row)
    pred = int(engine.classification_model.predict(scaled)[0])
    prob = float(engine.classification_model.predict_proba(scaled)[0][1])
    return pred, round(prob, 4)


def get_customer_segment(engine: RecommendationEngine, user_id: int) -> dict | None:
    match = engine.customer_segments[engine.customer_segments["User_ID"] == user_id]
    if match.empty:
        return None
    row = match.iloc[0]
    cluster = int(row["KMeans_Cluster"])
    label, desc = CLUSTER_LABELS.get(cluster, (f"Cluster {cluster}", "Custom segment"))
    return {
        "user_id": user_id,
        "cluster": cluster,
        "label": label,
        "description": desc,
        "products_viewed": round(row["products_viewed"], 1),
        "num_purchases": int(row["num_purchases"]),
        "avg_rating": round(row["avg_rating"], 2),
        "avg_time_spent": round(row["avg_time_spent"], 1),
        "total_spent": round(row["total_spent"], 2),
        "cart_additions": int(row["cart_additions"]),
    }


def predict_segment_from_behavior(engine: RecommendationEngine, behavior: dict) -> dict:
    row = np.array([[
        behavior["products_viewed"], behavior["num_purchases"], behavior["avg_rating"],
        behavior["avg_time_spent"], behavior["total_spent"], behavior["cart_additions"],
    ]])
    scaled = engine.cluster_scaler.transform(row)
    cluster = int(engine.cluster_model.predict(scaled)[0])
    label, desc = CLUSTER_LABELS.get(cluster, (f"Cluster {cluster}", "Custom segment"))
    return {"cluster": cluster, "label": label, "description": desc}
