"""
Data preprocessing utilities for the customer segmentation project.
Handles missing values, outliers, encoding, and feature scaling.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


def load_data(path):
    return pd.read_csv(path)


def handle_missing_values(df):
    """Impute numeric columns with median. No categorical columns had
    missing values in this dataset, but we guard for it anyway."""
    df = df.copy()
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df[col].isna().sum() > 0:
            df[col] = df[col].fillna(df[col].median())

    categorical_cols = df.select_dtypes(include=["object"]).columns
    for col in categorical_cols:
        if df[col].isna().sum() > 0:
            df[col] = df[col].fillna(df[col].mode()[0])
    return df


def cap_outliers(df, columns, lower_q=0.01, upper_q=0.99):
    """Cap extreme values using percentile winsorization rather than
    dropping rows, so we don't lose otherwise-valid customers."""
    df = df.copy()
    for col in columns:
        lower = df[col].quantile(lower_q)
        upper = df[col].quantile(upper_q)
        df[col] = df[col].clip(lower, upper)
    return df


def encode_categoricals(df, columns):
    df = df.copy()
    df = pd.get_dummies(df, columns=columns, prefix=columns)
    return df


def add_rfm_features(df):
    """Recency is already DaysSinceLastPurchase, Frequency is
    PurchaseFrequency, Monetary is TotalSpending. We also add an
    RFM composite score using simple quantile scoring (1-4, higher
    is better) purely for reference/EDA, not as a model input."""
    df = df.copy()
    df["R_Score"] = pd.qcut(df["DaysSinceLastPurchase"], 4, labels=[4, 3, 2, 1]).astype(int)
    df["F_Score"] = pd.qcut(df["PurchaseFrequency"].rank(method="first"), 4, labels=[1, 2, 3, 4]).astype(int)
    df["M_Score"] = pd.qcut(df["TotalSpending"].rank(method="first"), 4, labels=[1, 2, 3, 4]).astype(int)
    df["RFM_Score"] = df["R_Score"] + df["F_Score"] + df["M_Score"]
    return df


def scale_features(df, columns):
    scaler = StandardScaler()
    scaled = scaler.fit_transform(df[columns])
    scaled_df = pd.DataFrame(scaled, columns=[f"{c}_scaled" for c in columns], index=df.index)
    return scaled_df, scaler


def prepare_clustering_features(df):
    """Full pipeline: clean -> cap outliers -> engineer RFM -> scale.
    Returns the cleaned full dataframe and the scaled feature matrix
    used specifically for K-Means."""
    clean = handle_missing_values(df)
    outlier_cols = ["TotalSpending", "AnnualIncome", "AverageOrderValue"]
    clean = cap_outliers(clean, outlier_cols)
    clean = add_rfm_features(clean)

    cluster_cols = [
        "DaysSinceLastPurchase", "PurchaseFrequency", "TotalSpending",
        "AverageOrderValue", "WebsiteVisits", "DiscountUsage", "CustomerRating",
    ]
    scaled_df, scaler = scale_features(clean, cluster_cols)
    return clean, scaled_df, scaler, cluster_cols
