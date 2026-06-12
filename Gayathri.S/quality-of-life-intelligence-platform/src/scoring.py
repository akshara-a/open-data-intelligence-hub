import polars as pl

df = pl.read_csv(
    "data1/world_happiness.csv"
)

df = df.with_columns(
    (
        pl.col("Happiness Score")*0.30 +
        pl.col("GDP")*0.20 +
        pl.col("Health")*0.15 +
        pl.col("Freedom")*0.15 +
        pl.col("Social Support")*0.10 +
        pl.col("Generosity")*0.05 +
        pl.col("Corruption")*0.05
    ).alias("QoL Score")
)

print(df.head())