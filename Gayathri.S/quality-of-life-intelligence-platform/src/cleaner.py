import polars as pl

df = pl.read_csv("data1/world_happiness.csv")
print(df.null_count())
df = df.drop_nulls()
print(df.shape)