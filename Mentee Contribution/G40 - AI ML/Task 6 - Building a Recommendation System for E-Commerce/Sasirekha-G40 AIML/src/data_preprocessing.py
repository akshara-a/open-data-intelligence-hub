import pandas as pd

def load_dataset(path):
    return pd.read_csv(path)

def save_dataset(df, path):
    df.to_csv(path, index=False)
    print(f"Dataset saved to: {path}")

