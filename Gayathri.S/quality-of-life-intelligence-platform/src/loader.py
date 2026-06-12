import polars as pl

df = pl.read_csv(
    "data1/world_happiness.csv"
)

print(df.head())