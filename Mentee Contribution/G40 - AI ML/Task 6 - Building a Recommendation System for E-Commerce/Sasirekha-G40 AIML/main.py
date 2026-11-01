from src.data_preprocessing import load_dataset

df = load_dataset("data/processed/ecommerce_encoded.csv")

print(df.head())
