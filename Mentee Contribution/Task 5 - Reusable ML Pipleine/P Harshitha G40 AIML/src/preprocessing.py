import pandas as pd


def preprocess_data(df):
    """
    Clean the customer churn dataset.

    Steps:
    1. Remove duplicate rows
    2. Convert TotalCharges to numeric
    3. Handle missing values
    """

    # Make a copy so the original DataFrame is not modified
    df = df.copy()

    # ---------------------------------------------------------
    # 1. Remove duplicate rows
    # ---------------------------------------------------------
    df.drop_duplicates(inplace=True)

    # ---------------------------------------------------------
    # 2. Convert TotalCharges to numeric
    # ---------------------------------------------------------
    if "TotalCharges" in df.columns:
        df["TotalCharges"] = pd.to_numeric(
            df["TotalCharges"],
            errors="coerce"
        )

    # ---------------------------------------------------------
    # 3. Handle missing values
    # ---------------------------------------------------------
    for col in df.columns:

        # Numerical columns → fill with median
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].median())

        # Categorical columns → fill with mode
        else:
            if not df[col].mode().empty:
                df[col] = df[col].fillna(df[col].mode()[0])

    return df