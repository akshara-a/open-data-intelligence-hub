"""Data loading and preprocessing utilities for customer segmentation."""

from pathlib import Path
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler


NUMERIC_FEATURES = [
    "Age",
    "AnnualIncome",
    "TotalSpending",
    "PurchaseFrequency",
    "AverageOrderValue",
    "DaysSinceLastPurchase",
    "WebsiteVisits",
    "DiscountUsage",
    "CustomerRating",
]

CATEGORICAL_FEATURES = ["Gender", "ProductCategory"]


def load_data(path: str | Path) -> pd.DataFrame:
    """Load customer data from CSV."""
    return pd.read_csv(path)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Basic cleaning: remove duplicate rows and handle missing values."""
    result = df.copy()
    result = result.drop_duplicates()

    for column in NUMERIC_FEATURES:
        if column in result.columns:
            result[column] = result[column].fillna(result[column].median())

    for column in CATEGORICAL_FEATURES:
        if column in result.columns:
            result[column] = result[column].fillna(result[column].mode()[0])

    return result


def build_preprocessor() -> ColumnTransformer:
    """Create preprocessing pipeline for mixed numeric/categorical features."""
    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERIC_FEATURES),
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
        ]
    )


def prepare_clustering_data(df: pd.DataFrame):
    """Return customer IDs and transformed features for clustering."""
    customer_ids = df["CustomerID"].copy()
    preprocessor = build_preprocessor()
    X = preprocessor.fit_transform(df)
    return customer_ids, X, preprocessor
