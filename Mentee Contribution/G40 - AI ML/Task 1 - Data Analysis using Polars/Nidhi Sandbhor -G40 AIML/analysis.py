import pandas as pd

df = pd.read_csv(
    "Data/Domestic Tourism-Accommodation.csv",
    encoding="latin1"
)

print(df.head())
print(df.columns)
print(df.shape)
print(df.tail())
print(df.iloc[0:20])
print(df.iloc[8:16])
print(df.iloc[11])