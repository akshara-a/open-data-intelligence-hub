import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

def load_and_clean_data(file_path):
    """
    Loads dataset, removes duplicate records, drops CustomerID, and returns cleaned DataFrame.
    """
    df = pd.read_csv(file_path)
    initial_rows = len(df)
    
    # Remove duplicate rows
    df = df.drop_duplicates()
    dedup_rows = len(df)
    print(f"[Data Preprocessing] Loaded {initial_rows} rows. Removed {initial_rows - dedup_rows} duplicate rows.")
    
    # Separate features and target
    if "CustomerID" in df.columns:
        df_model = df.drop(columns=["CustomerID"])
    else:
        df_model = df.copy()

    X = df_model.drop(columns=["Purchase"])
    y = df_model["Purchase"]
    
    return df, X, y

def get_feature_types(X):
    """
    Identifies numerical and categorical features.
    """
    categorical_cols = X.select_dtypes(include=["object", "category"]).columns.tolist()
    numerical_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
    return numerical_cols, categorical_cols

def build_preprocessor(numerical_cols, categorical_cols):
    """
    Constructs Scikit-Learn ColumnTransformer pipeline to prevent data leakage.
    """
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler())
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, numerical_cols),
            ("categorical", categorical_pipeline, categorical_cols)
        ]
    )
    return preprocessor

def split_data(X, y, test_size=0.20, random_state=42):
    """
    Performs stratified train-test split to preserve target class proportions.
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    print(f"[Data Preprocessing] Train set: {X_train.shape[0]} samples | Test set: {X_test.shape[0]} samples")
    return X_train, X_test, y_train, y_test
