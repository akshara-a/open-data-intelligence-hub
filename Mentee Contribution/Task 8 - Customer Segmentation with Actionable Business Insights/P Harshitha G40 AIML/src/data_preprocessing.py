"""
Data Preprocessing Module
=========================
Handles loading, cleaning, encoding, and scaling of the customer dataset.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
import os


def load_data(filepath):
    """Load the raw customer dataset from a CSV file."""
    df = pd.read_csv(filepath)
    print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    return df


def inspect_data(df):
    """Print basic information about the dataset."""
    print("\n--- Dataset Info ---")
    print(df.info())
    print("\n--- First 5 Rows ---")
    print(df.head())
    print("\n--- Statistical Summary ---")
    print(df.describe())
    print("\n--- Missing Values ---")
    print(df.isnull().sum())
    print("\n--- Duplicate Rows ---")
    print(f"Number of duplicates: {df.duplicated().sum()}")
    return df


def handle_missing_values(df):
    """Handle missing values in the dataset."""
    # Fill numeric columns with median
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df[col].isnull().sum() > 0:
            median_val = df[col].median()
            df[col].fillna(median_val, inplace=True)
            print(f"Filled {col} missing values with median: {median_val}")

    # Fill categorical columns with mode
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        if df[col].isnull().sum() > 0:
            mode_val = df[col].mode()[0]
            df[col].fillna(mode_val, inplace=True)
            print(f"Filled {col} missing values with mode: {mode_val}")

    print(f"Missing values after handling: {df.isnull().sum().sum()}")
    return df


def remove_duplicates(df):
    """Remove duplicate rows from the dataset."""
    initial_rows = len(df)
    df = df.drop_duplicates()
    removed = initial_rows - len(df)
    if removed > 0:
        print(f"Removed {removed} duplicate rows")
    else:
        print("No duplicate rows found")
    return df


def treat_outliers(df, columns, method='iqr'):
    """
    Treat outliers using the IQR method by capping values.
    """
    for col in columns:
        if col in df.columns and df[col].dtype in [np.float64, np.int64, np.float32, np.int32]:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            outliers_count = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
            if outliers_count > 0:
                df[col] = df[col].clip(lower=lower_bound, upper=upper_bound)
                print(f"Capped {outliers_count} outliers in {col} "
                      f"[{lower_bound:.2f}, {upper_bound:.2f}]")
    return df


def encode_categorical(df):
    """
    Encode categorical variables:
    - Gender: Label Encoding (Male=1, Female=0)
    - ProductCategory: One-Hot Encoding
    """
    # Label encode Gender
    if 'Gender' in df.columns:
        le = LabelEncoder()
        df['Gender_Encoded'] = le.fit_transform(df['Gender'])
        print(f"Gender encoded: {dict(zip(le.classes_, le.transform(le.classes_)))}")

    # One-Hot encode ProductCategory
    if 'ProductCategory' in df.columns:
        dummies = pd.get_dummies(df['ProductCategory'], prefix='Category', dtype=int)
        df = pd.concat([df, dummies], axis=1)
        print(f"ProductCategory one-hot encoded into {len(dummies.columns)} columns")

    return df


def scale_features(df, feature_columns):
    """
    Scale numerical features using StandardScaler.
    Returns the scaled dataframe and the fitted scaler.
    """
    scaler = StandardScaler()
    df_scaled = df.copy()
    df_scaled[feature_columns] = scaler.fit_transform(df[feature_columns])
    print(f"Scaled {len(feature_columns)} features using StandardScaler")
    return df_scaled, scaler


def preprocess_pipeline(raw_data_path, cleaned_data_path):
    """
    Run the full preprocessing pipeline.
    Returns the cleaned dataframe and the encoded dataframe.
    """
    # Step 1: Load data
    df = load_data(raw_data_path)

    # Step 2: Inspect data
    inspect_data(df)

    # Step 3: Handle missing values
    df = handle_missing_values(df)

    # Step 4: Remove duplicates
    df = remove_duplicates(df)

    # Step 5: Treat outliers on numeric columns
    outlier_columns = ['AnnualIncome', 'TotalSpending', 'PurchaseFrequency',
                       'AverageOrderValue', 'DaysSinceLastPurchase', 'WebsiteVisits']
    df = treat_outliers(df, outlier_columns)

    # Step 6: Save cleaned data (before encoding)
    df.to_csv(cleaned_data_path, index=False)
    print(f"\nCleaned data saved to {cleaned_data_path}")

    # Step 7: Encode categorical variables
    df_encoded = encode_categorical(df)

    return df, df_encoded


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_path = os.path.join(base_dir, "data", "customer_data.csv")
    cleaned_path = os.path.join(base_dir, "data", "cleaned_customer_data.csv")
    df, df_encoded = preprocess_pipeline(raw_path, cleaned_path)
    print("\nPreprocessing complete!")
    print(f"Encoded dataframe shape: {df_encoded.shape}")
