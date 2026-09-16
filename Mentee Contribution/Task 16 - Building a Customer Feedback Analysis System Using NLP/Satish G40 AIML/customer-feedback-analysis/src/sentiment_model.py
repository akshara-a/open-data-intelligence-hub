"""Sentiment classification model for customer feedback."""

from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from src.preprocessing import preprocess_text

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT_DIR / "data" / "feedback.csv"
MODEL_PATH = ROOT_DIR / "models" / "sentiment_model.pkl"


def load_sentiment_dataset(data_path: str | Path = DATA_PATH) -> pd.DataFrame:
    """Load and prepare the sentiment dataset."""
    df = pd.read_csv(data_path)

    required_columns = {"feedback", "sentiment"}
    missing = required_columns.difference(df.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")

    df = df.copy()
    df["feedback_clean"] = df["feedback"].apply(preprocess_text)
    return df


def build_sentiment_pipeline() -> Pipeline:
    """Create a TF-IDF + Logistic Regression pipeline for sentiment classification."""
    return Pipeline(
        steps=[
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=5000)),
            ("classifier", LogisticRegression(max_iter=1000, random_state=42)),
        ]
    )


def train_sentiment_model(data_path: str | Path = DATA_PATH, model_path: str | Path = MODEL_PATH) -> dict:
    """Train the sentiment model, evaluate it, and save it to disk."""
    df = load_sentiment_dataset(data_path)

    X = df["feedback_clean"]
    y = df["sentiment"].astype(str)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = build_sentiment_pipeline()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, average="weighted", zero_division=0),
        "recall": recall_score(y_test, y_pred, average="weighted", zero_division=0),
        "f1": f1_score(y_test, y_pred, average="weighted", zero_division=0),
        "classification_report": classification_report(y_test, y_pred),
        "confusion_matrix": confusion_matrix(y_test, y_pred),
    }

    model_path = Path(model_path)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)

    return metrics


def load_sentiment_model(model_path: str | Path = MODEL_PATH):
    """Load a saved sentiment model."""
    return joblib.load(model_path)


def predict_sentiment(text: str, model_path: str | Path = MODEL_PATH) -> str:
    """Predict the sentiment label for a single feedback string."""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Please provide a valid customer feedback string.")

    model = load_sentiment_model(model_path)
    cleaned_text = preprocess_text(text)
    prediction = model.predict([cleaned_text])[0]
    return str(prediction).lower()
