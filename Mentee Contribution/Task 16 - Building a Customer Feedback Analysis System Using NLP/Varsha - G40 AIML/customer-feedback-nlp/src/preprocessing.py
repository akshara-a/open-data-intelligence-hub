import pandas as pd
import re


def clean_text(text):
    """
    Clean customer review text.
    """
    text = str(text)

    # Convert to lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)

    # Remove special characters and numbers
    text = re.sub(r"[^a-zA-Z\s]", "", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


# Load original dataset
df = pd.read_csv("data/Customer_Sentiment.csv")

print("Original dataset shape:", df.shape)

# Clean review text
df["cleaned_text"] = df["review_text"].apply(clean_text)

# Remove empty reviews if any
df = df[df["cleaned_text"].str.strip() != ""]

# Display examples
print("\nOriginal vs Cleaned Text:")
print(
    df[["review_text", "cleaned_text", "sentiment"]]
    .head(10)
    .to_string(index=False)
)

# Save processed dataset
df.to_csv("data/processed_feedback.csv", index=False)

print("\nPreprocessing completed successfully!")
print("Processed dataset shape:", df.shape)
print("Saved to: data/processed_feedback.csv")