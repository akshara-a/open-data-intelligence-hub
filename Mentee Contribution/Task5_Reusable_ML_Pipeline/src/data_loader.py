import pandas as pd


def load_data():

    df = pd.read_csv(
        "data/WA_Fn-UseC_-Telco-Customer-Churn.csv"
    )

    return df