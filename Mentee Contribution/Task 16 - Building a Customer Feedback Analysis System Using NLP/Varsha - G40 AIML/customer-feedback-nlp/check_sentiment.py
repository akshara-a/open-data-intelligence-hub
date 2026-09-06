import pandas as pd

df = pd.read_csv("data/Customer_Sentiment.csv")

print("Sentiment Values:")
print(df["sentiment"].value_counts())

print("\nUnique Sentiments:")
print(df["sentiment"].unique())

print("\nReview Examples:")
print(df["review_text"].head(10))