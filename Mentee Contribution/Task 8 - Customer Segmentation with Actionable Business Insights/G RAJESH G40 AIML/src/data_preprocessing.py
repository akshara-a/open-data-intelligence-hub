import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

def preprocess_data(file_path):
    # Load data
    df = pd.read_csv(file_path)

    # Handle missing values
    df["Satisfaction Level"] = df["Satisfaction Level"].fillna(df["Satisfaction Level"].mode()[0])

    # Convert categorical columns
    categorical_cols = ["Gender", "City", "Membership Type", "Satisfaction Level"]

    encoder = LabelEncoder()
    for col in categorical_cols:
        df[col] = encoder.fit_transform(df[col])

    # Convert boolean column
    df["Discount Applied"] = df["Discount Applied"].astype(int)

    # Scale numeric features
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df)

    return df, scaled_data