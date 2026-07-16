"""
Data Preprocessing Module
=========================
Handles data cleaning, encoding, scaling, and train/test splitting.
Also creates aggregated customer-level features for clustering.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import os
import warnings
warnings.filterwarnings("ignore")


def load_and_clean_data(filepath):
    """
    Load the dataset and perform basic cleaning.

    Parameters
    ----------
    filepath : str
        Path to the CSV file.

    Returns
    -------
    pd.DataFrame
        Cleaned DataFrame.
    """
    df = pd.read_csv(filepath)
    initial_shape = df.shape

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Handle missing values
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    categorical_cols = df.select_dtypes(include=["object"]).columns

    for col in numeric_cols:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].median(), inplace=True)

    for col in categorical_cols:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].mode()[0], inplace=True)

    print(f"[Preprocessing] Loaded dataset: {initial_shape}")
    print(f"[Preprocessing] After cleaning: {df.shape}")
    print(f"[Preprocessing] Missing values: {df.isnull().sum().sum()}")
    print(f"[Preprocessing] Duplicates removed: {initial_shape[0] - df.shape[0]}")

    return df


def encode_features(df):
    """
    Encode categorical features using LabelEncoder.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.

    Returns
    -------
    pd.DataFrame
        DataFrame with encoded categorical columns.
    dict
        Dictionary of LabelEncoder objects keyed by column name.
    """
    df_encoded = df.copy()
    encoders = {}

    categorical_cols = ["Category", "Gender", "Location"]
    for col in categorical_cols:
        if col in df_encoded.columns:
            le = LabelEncoder()
            df_encoded[col + "_Encoded"] = le.fit_transform(df_encoded[col])
            encoders[col] = le

    print(f"[Preprocessing] Encoded columns: {list(encoders.keys())}")
    return df_encoded, encoders


def scale_features(X_train, X_test):
    """
    Scale numerical features using StandardScaler.

    Parameters
    ----------
    X_train : pd.DataFrame or np.ndarray
        Training features.
    X_test : pd.DataFrame or np.ndarray
        Testing features.

    Returns
    -------
    np.ndarray, np.ndarray, StandardScaler
        Scaled train features, scaled test features, and the fitted scaler.
    """
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    print(f"[Preprocessing] Features scaled: {X_train.shape[1]} features")
    return X_train_scaled, X_test_scaled, scaler


def prepare_regression_data(df_encoded, test_size=0.2, random_state=42):
    """
    Prepare data for the regression task (rating prediction).

    Returns
    -------
    tuple
        (X_train, X_test, y_train, y_test, X_train_scaled, X_test_scaled, scaler, feature_names)
    """
    feature_cols = ["Price", "Browsing_Time", "Previous_Purchases",
                    "Discount_Applied", "Age", "Category_Encoded", "Total_Spending"]

    X = df_encoded[feature_cols]
    y = df_encoded["Rating"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test)

    print(f"[Preprocessing] Regression data — Train: {X_train.shape}, Test: {X_test.shape}")
    return X_train, X_test, y_train, y_test, X_train_scaled, X_test_scaled, scaler, feature_cols


def prepare_classification_data(df_encoded, test_size=0.2, random_state=42):
    """
    Prepare data for the classification task (purchase prediction).

    Returns
    -------
    tuple
        (X_train, X_test, y_train, y_test, X_train_scaled, X_test_scaled, scaler, feature_names)
    """
    feature_cols = ["Browsing_Time", "Cart_Addition", "Previous_Purchases",
                    "Rating", "Price", "Discount_Applied", "Total_Spending"]

    X = df_encoded[feature_cols]
    y = df_encoded["Purchase_Status"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test)

    print(f"[Preprocessing] Classification data — Train: {X_train.shape}, Test: {X_test.shape}")
    return X_train, X_test, y_train, y_test, X_train_scaled, X_test_scaled, scaler, feature_cols


def prepare_clustering_data(df_encoded):
    """
    Create aggregated customer-level features for clustering.

    Returns
    -------
    pd.DataFrame
        Customer-level aggregated features.
    np.ndarray
        Scaled feature array.
    StandardScaler
        Fitted scaler.
    list
        Feature names.
    """
    customer_df = df_encoded.groupby("User_ID").agg(
        Browsing_Time=("Browsing_Time", "mean"),
        Previous_Purchases=("Previous_Purchases", "mean"),
        Average_Rating=("Rating", "mean"),
        Total_Spending=("Total_Spending", "sum"),
        Cart_Addition_Count=("Cart_Addition", "sum"),
        Discount_Usage=("Discount_Applied", "mean"),
    ).reset_index()

    feature_cols = ["Browsing_Time", "Previous_Purchases", "Average_Rating",
                    "Total_Spending", "Cart_Addition_Count", "Discount_Usage"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(customer_df[feature_cols])

    print(f"[Preprocessing] Clustering data — {customer_df.shape[0]} unique customers, {len(feature_cols)} features")
    return customer_df, X_scaled, scaler, feature_cols


def preprocess_all(filepath):
    """
    Run the full preprocessing pipeline.

    Returns
    -------
    dict
        Dictionary containing all preprocessed data splits and objects.
    """
    print("\n" + "=" * 60)
    print("DATA PREPROCESSING")
    print("=" * 60)

    df = load_and_clean_data(filepath)
    df_encoded, encoders = encode_features(df)

    reg_data = prepare_regression_data(df_encoded)
    clf_data = prepare_classification_data(df_encoded)
    clust_data = prepare_clustering_data(df_encoded)

    return {
        "df": df,
        "df_encoded": df_encoded,
        "encoders": encoders,
        "regression": {
            "X_train": reg_data[0], "X_test": reg_data[1],
            "y_train": reg_data[2], "y_test": reg_data[3],
            "X_train_scaled": reg_data[4], "X_test_scaled": reg_data[5],
            "scaler": reg_data[6], "feature_names": reg_data[7],
        },
        "classification": {
            "X_train": clf_data[0], "X_test": clf_data[1],
            "y_train": clf_data[2], "y_test": clf_data[3],
            "X_train_scaled": clf_data[4], "X_test_scaled": clf_data[5],
            "scaler": clf_data[6], "feature_names": clf_data[7],
        },
        "clustering": {
            "customer_df": clust_data[0], "X_scaled": clust_data[1],
            "scaler": clust_data[2], "feature_names": clust_data[3],
        },
    }


if __name__ == "__main__":
    data = preprocess_all("data/ecommerce_data.csv")
    print("\nPreprocessing complete!")
    print(f"Regression features: {data['regression']['feature_names']}")
    print(f"Classification features: {data['classification']['feature_names']}")
    print(f"Clustering features: {data['clustering']['feature_names']}")
