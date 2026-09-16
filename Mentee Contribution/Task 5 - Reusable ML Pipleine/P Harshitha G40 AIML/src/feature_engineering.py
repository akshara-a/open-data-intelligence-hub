import pandas as pd


def feature_engineering(df):
    """
    Perform feature engineering and categorical encoding
    for the customer churn dataset.

    The encoding is deterministic so that the same category
    always receives the same numerical value during training
    and prediction.
    """

    # Work on a copy
    df = df.copy()

    # ---------------------------------------------------------
    # Remove customerID
    # ---------------------------------------------------------
    if "customerID" in df.columns:
        df.drop("customerID", axis=1, inplace=True)

    # ---------------------------------------------------------
    # Gender
    # ---------------------------------------------------------
    if "gender" in df.columns:
        df["gender"] = df["gender"].map({
            "Female": 0,
            "Male": 1
        })

    # ---------------------------------------------------------
    # Yes / No columns
    # ---------------------------------------------------------
    binary_columns = [
        "Partner",
        "Dependents",
        "PhoneService",
        "PaperlessBilling"
    ]

    for column in binary_columns:
        if column in df.columns:
            df[column] = df[column].map({
                "No": 0,
                "Yes": 1
            })

    # ---------------------------------------------------------
    # Multiple Lines
    # ---------------------------------------------------------
    if "MultipleLines" in df.columns:
        df["MultipleLines"] = df["MultipleLines"].map({
            "No": 0,
            "No phone service": 1,
            "Yes": 2
        })

    # ---------------------------------------------------------
    # Internet Service
    # ---------------------------------------------------------
    if "InternetService" in df.columns:
        df["InternetService"] = df["InternetService"].map({
            "DSL": 0,
            "Fiber optic": 1,
            "No": 2
        })

    # ---------------------------------------------------------
    # Internet-dependent services
    # ---------------------------------------------------------
    service_columns = [
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "StreamingTV",
        "StreamingMovies"
    ]

    for column in service_columns:
        if column in df.columns:
            df[column] = df[column].map({
                "No": 0,
                "No internet service": 1,
                "Yes": 2
            })

    # ---------------------------------------------------------
    # Contract
    # ---------------------------------------------------------
    if "Contract" in df.columns:
        df["Contract"] = df["Contract"].map({
            "Month-to-month": 0,
            "One year": 1,
            "Two year": 2
        })

    # ---------------------------------------------------------
    # Payment Method
    # ---------------------------------------------------------
    if "PaymentMethod" in df.columns:
        df["PaymentMethod"] = df["PaymentMethod"].map({
            "Bank transfer (automatic)": 0,
            "Credit card (automatic)": 1,
            "Electronic check": 2,
            "Mailed check": 3
        })

    # ---------------------------------------------------------
    # Convert feature columns to numeric
    # ---------------------------------------------------------
    feature_columns = [
        "gender",
        "SeniorCitizen",
        "Partner",
        "Dependents",
        "tenure",
        "PhoneService",
        "MultipleLines",
        "InternetService",
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "StreamingTV",
        "StreamingMovies",
        "Contract",
        "PaperlessBilling",
        "PaymentMethod",
        "MonthlyCharges",
        "TotalCharges"
    ]

    for column in feature_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    # ---------------------------------------------------------
    # Final safety check
    # ---------------------------------------------------------
    if df[feature_columns].isnull().any().any():

        missing_columns = df[feature_columns].columns[
            df[feature_columns].isnull().any()
        ].tolist()

        raise ValueError(
            "Missing values found after feature engineering "
            f"in columns: {missing_columns}"
        )

    return df