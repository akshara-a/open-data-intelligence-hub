from sklearn.preprocessing import LabelEncoder

def feature_engineering(df):

    le = LabelEncoder()

    for col in df.select_dtypes(include=['object']).columns:
        df[col] = le.fit_transform(df[col].astype(str))

    return df