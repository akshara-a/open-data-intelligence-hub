"""Utility functions for loading data and saving models/plots."""
import os
import joblib
import pandas as pd


def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def save_model(model, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model, path)


def save_dataframe(df, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
