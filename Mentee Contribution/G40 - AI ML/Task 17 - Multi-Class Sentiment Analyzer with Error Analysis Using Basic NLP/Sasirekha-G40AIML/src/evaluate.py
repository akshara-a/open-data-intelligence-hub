"""Create evaluation figures from the saved production model."""
from pathlib import Path
import json
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import ConfusionMatrixDisplay
from .model import load_model

ROOT = Path(__file__).resolve().parents[1]

def main():
    df = pd.read_csv(ROOT / "data" / "raw" / "Tweets.csv").dropna(subset=["text", "sentiment"])
    X_train, X_test, y_train, y_test = train_test_split(
        df["text"].astype(str), df["sentiment"].astype(str).str.lower().str.strip(),
        test_size=0.20, random_state=42, stratify=df["sentiment"]
    )
    model = load_model(ROOT / "models" / "sentiment_pipeline.joblib")
    pred = model.predict(X_test)

    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    ConfusionMatrixDisplay.from_predictions(
        y_test, pred, labels=model.classes_, cmap="Blues", ax=ax
    )
    ax.set_title("Sentiment Confusion Matrix")
    fig.tight_layout()
    fig.savefig(ROOT / "reports" / "figures" / "confusion_matrix.png", dpi=160)
    plt.close(fig)

    counts = df["sentiment"].value_counts().reindex(model.classes_)
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    counts.plot(kind="bar", ax=ax)
    ax.set_title("Dataset Sentiment Distribution")
    ax.set_xlabel("Sentiment")
    ax.set_ylabel("Number of tweets")
    fig.tight_layout()
    fig.savefig(ROOT / "reports" / "figures" / "sentiment_distribution.png", dpi=160)
    plt.close(fig)

if __name__ == "__main__":
    main()
