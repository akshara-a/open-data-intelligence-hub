"""Data loading and preprocessing routines."""
from typing import Tuple
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


def load_and_preprocess(path: str) -> Tuple[pd.DataFrame, pd.DataFrame, Pipeline]:
    df = pd.read_csv(path)
    # Basic cleaning: drop duplicates
    df = df.drop_duplicates(subset=["CustomerID"]).reset_index(drop=True)

    # Feature engineering: create binary label for high purchase likelihood
    df["HighPurchase"] = (df["PurchaseLikelihood"] >= 0.5).astype(int)

    # Columns
    numeric_features = ["Age", "AnnualIncome", "PurchaseFrequency", "AverageOrderValue", "DaysSinceLastPurchase", "WebsiteVisits", "DiscountUsage", "CustomerRating", "TotalSpending"]
    categorical_features = ["Gender", "ProductCategory"]

    # Preprocessing pipeline
    numeric_transformer = Pipeline(steps=[("scaler", StandardScaler())])
    categorical_transformer = Pipeline(steps=[("ohe", OneHotEncoder(handle_unknown="ignore"))])

    preprocessor = ColumnTransformer(transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features),
    ])

    X = df[numeric_features + categorical_features].copy()
    y_reg = df["TotalSpending"].copy()
    y_clf = df["HighPurchase"].copy()

    return X, {"regression": y_reg, "classification": y_clf, "raw": df}, preprocessor
