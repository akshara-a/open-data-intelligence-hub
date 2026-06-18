import os
import pandas as pd


def get_data_path(filename: str = 'Churn_Modelling.csv') -> str:
    return os.path.join(os.path.dirname(__file__), '..', '..', 'data', filename)


def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)
