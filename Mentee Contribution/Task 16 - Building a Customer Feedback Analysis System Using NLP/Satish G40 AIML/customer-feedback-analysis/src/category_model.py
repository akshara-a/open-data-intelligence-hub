"""Multi-label category classification for customer feedback."""

from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MultiLabelBinarizer

from src.preprocessing import preprocess_text

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT_DIR / "data" / "feedback.csv"
MODEL_PATH = ROOT_DIR / "models" / "category_model.pkl"
MLB_PATH = ROOT_DIR / "models" / "multilabel_binarizer.pkl"


def split_categories(categories: str | pd.Series | list) -> list[str]:
    """Convert a comma-separated category string into a clean list of labels."""
    if categories is None or (isinstance(categories, float) and pd.isna(categories)):
        return []

    if isinstance(categories, str):
        raw_values = categories.split(",")
    else:
        raw_values = categories

    cleaned_values = []
    for value in raw_values:
        item = str(value).strip().lower().replace(" ", "_")
        if item:
            cleaned_values.append(item)
    return cleaned_values


def load_category_dataset(data_path: str | Path = DATA_PATH) -> pd.DataFrame:
    """Load the category dataset and prepare multi-label labels."""
    df = pd.read_csv(data_path)
    required_columns = {"feedback", "categories"}
    missing = required_columns.difference(df.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")

    df = df.copy()
    df["feedback_clean"] = df["feedback"].apply(preprocess_text)
    df["category_list"] = df["categories"].apply(split_categories)
    return df


def build_category_pipeline() -> Pipeline:
    """Create a TF-IDF + OneVsRest Logistic Regression pipeline."""
    return Pipeline(
        steps=[
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=5000)),
            ("classifier", OneVsRestClassifier(LogisticRegression(max_iter=1000, random_state=42))),
        ]
    )


def train_category_model(
    data_path: str | Path = DATA_PATH,
    model_path: str | Path = MODEL_PATH,
    mlb_path: str | Path = MLB_PATH,
    threshold: float = 0.4,
) -> dict:
    """Train the multi-label category classifier and save the model and encoder."""
    df = load_category_dataset(data_path)
    mlb = MultiLabelBinarizer()
    y_encoded = mlb.fit_transform(df["category_list"])

    X_train, X_test, y_train, y_test = train_test_split(
        df["feedback_clean"], y_encoded, test_size=0.2, random_state=42
    )

    model = build_category_pipeline()
    model.fit(X_train, y_train)

    y_prob = model.predict_proba(X_test)
    y_pred = (y_prob >= threshold).astype(int)

    metrics = {
        "precision": precision_score(y_test, y_pred, average="micro", zero_division=0),
        "recall": recall_score(y_test, y_pred, average="micro", zero_division=0),
        "f1": f1_score(y_test, y_pred, average="micro", zero_division=0),
        "micro_f1": f1_score(y_test, y_pred, average="micro", zero_division=0),
        "macro_f1": f1_score(y_test, y_pred, average="macro", zero_division=0),
        "threshold": threshold,
    }

    Path(model_path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)
    joblib.dump(mlb, mlb_path)

    return metrics


def load_category_model(model_path: str | Path = MODEL_PATH):
    """Load the saved category classifier."""
    return joblib.load(model_path)


def load_multilabel_binarizer(mlb_path: str | Path = MLB_PATH):
    """Load the saved MultiLabelBinarizer."""
    return joblib.load(mlb_path)


def predict_categories(text: str, model_path: str | Path = MODEL_PATH, mlb_path: str | Path = MLB_PATH, threshold: float = 0.4) -> list[str]:
    """Predict one or more category labels for a single customer feedback message."""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Please provide a valid customer feedback string.")

    model = load_category_model(model_path)
    mlb = load_multilabel_binarizer(mlb_path)

    cleaned_text = preprocess_text(text)
    probabilities = model.predict_proba([cleaned_text])[0]
    predicted_indices = [idx for idx, value in enumerate(probabilities) if value >= threshold]

    if not predicted_indices:
        return []

    labels = mlb.classes_[predicted_indices]
    return [str(label) for label in labels]
