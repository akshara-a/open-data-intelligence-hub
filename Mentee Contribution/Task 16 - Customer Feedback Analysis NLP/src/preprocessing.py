import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS


def clean_text(text):
    """
    Clean customer feedback text.
    """

    text = str(text).lower()

    # Remove punctuation and special characters
    text = re.sub(r"[^a-zA-Z\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    # Remove English stop words
    words = text.split()
    words = [
        word for word in words
        if word not in ENGLISH_STOP_WORDS
    ]

    return " ".join(words)


def preprocess_feedback_dataframe(df):
    """
    Add a cleaned_text column to the dataframe.
    """

    df = df.copy()
    df["cleaned_text"] = df["feedback"].apply(clean_text)

    return df


if __name__ == "__main__":
    import pandas as pd

    data = pd.read_csv("data/feedback.csv")
    processed_data = preprocess_feedback_dataframe(data)

    print(processed_data[["feedback", "cleaned_text"]].head())