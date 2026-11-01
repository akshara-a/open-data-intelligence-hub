import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


def preprocess_data(file_path):

    # Load dataset
    df = pd.read_csv(file_path)

    print("First 5 Rows")
    print(df.head())

    print("\nDataset Shape:", df.shape)

    print("\nMissing Values")
    print(df.isnull().sum())

    # Fill missing values
    df.ffill(inplace=True)

    # Encode all categorical columns
    for column in df.select_dtypes(include=["object"]).columns:
        encoder = LabelEncoder()
        df[column] = encoder.fit_transform(df[column].astype(str))

    print("\nData Types After Encoding:")
    print(df.dtypes)

    # Features and Target
    X = df.drop("PurchaseStatus", axis=1)
    y = df["PurchaseStatus"]

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    return df, X_train, X_test, y_train, y_test