from sklearn.preprocessing import LabelEncoder


def preprocess(df):

    # Remove customer ID
    df = df.drop("customerID", axis=1)


    # Convert TotalCharges to numeric
    df["TotalCharges"] = (
        df["TotalCharges"]
        .replace(" ", "0")
        .astype(float)
    )


    # Encode categorical columns

    encoder = LabelEncoder()

    for column in df.select_dtypes(include="object"):

        df[column] = encoder.fit_transform(
            df[column]
        )


    # Split features and target

    X = df.drop(
        "Churn",
        axis=1
    )

    y = df["Churn"]


    return X, y