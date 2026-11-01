import os

import pandas as pd
# pyrefly: ignore [missing-import]
from transformers import pipeline


MODEL_NAME = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"


def analyze_sentiments(input_path, output_path):
    """Analyze sentiment of text data using a pretrained Transformer."""

    print(f"Loading data from {input_path}...")

    try:
        df = pd.read_csv(input_path)
    except FileNotFoundError:
        print(f"Error: Could not find {input_path}")
        return

    if "text" not in df.columns:
        print("Error: Input CSV must contain a 'text' column.")
        return

    print("Loading sentiment analysis pipeline...")
    print(f"Using model: {MODEL_NAME}")

    sentiment_pipeline = pipeline(
        "sentiment-analysis",
        model=MODEL_NAME
    )

    print("Analyzing sentiments...")

    results = sentiment_pipeline(df["text"].tolist())

    df["label"] = [result["label"] for result in results]
    df["score"] = [result["score"] for result in results]

    # Ensure the output directory exists
    output_dir = os.path.dirname(output_path)

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    print(f"Saving results to {output_path}...")

    df.to_csv(output_path, index=False)

    print("Done!")


if __name__ == "__main__":
    base_dir = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    input_file = os.path.join(
        base_dir,
        "data",
        "sample_texts.csv"
    )

    output_file = os.path.join(
        base_dir,
        "results",
        "sentiment_results.csv"
    )

    analyze_sentiments(input_file, output_file)