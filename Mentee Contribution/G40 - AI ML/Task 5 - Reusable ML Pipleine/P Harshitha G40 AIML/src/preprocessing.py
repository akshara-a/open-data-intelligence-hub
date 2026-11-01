import pandas as pd

def preprocess_data(df):

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Convert TotalCharges to numeric
    if 'TotalCharges' in df.columns:
        df['TotalCharges'] = pd.to_numeric(
            df['TotalCharges'],
            errors='coerce'
        )

    # Fill missing values
    for col in df.columns:

        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].median())

        else:
            df[col] = df[col].fillna(df[col].mode()[0])

    return df