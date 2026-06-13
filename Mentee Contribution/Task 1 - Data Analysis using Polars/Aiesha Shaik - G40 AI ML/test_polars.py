import polars as pl

df = pl.DataFrame({
    "Country": ["India", "USA"],
    "Value": [100, 200]
})

print(df)