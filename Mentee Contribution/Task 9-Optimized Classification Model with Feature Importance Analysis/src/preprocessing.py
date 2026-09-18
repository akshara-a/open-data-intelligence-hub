import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def load_data():

    df = pd.read_csv("data/heart.csv")

    return df



def preprocess_data():

    df = load_data()

    print(df.head())
    print(df.info())


    # Separate features and target

    X = df.drop("target", axis=1)
    y = df["target"]


    # Split data

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )


    # Scaling

    scaler = StandardScaler()

    X_train = scaler.fit_transform(X_train)

    X_test = scaler.transform(X_test)


    return X_train, X_test, y_train, y_test, scaler



if __name__ == "__main__":

    preprocess_data()