import os
import sys
import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# Allow importing preprocessing.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from preprocessing import preprocess_feedback_dataframe


DATA_PATH = "data/feedback.csv"
MODEL_PATH = "models"


def train_classifier(texts, labels, model_name):
    """
    Train a TF-IDF + Logistic Regression classifier.
    """

    X_train, X_test, y_train, y_test = train_test_split(
        texts,
        labels,
        test_size=0.25,
        random_state=42,
        stratify=labels
    )

    pipeline = Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                ngram_range=(1, 2),
                max_features=1000
            )
        ),
        (
            "classifier",
            LogisticRegression(
                max_iter=1000
            )
        )
    ])

    pipeline.fit(X_train, y_train)

    predictions = pipeline.predict(X_test)

    print(f"\n===== {model_name.upper()} MODEL =====")
    print("Accuracy:", accuracy_score(y_test, predictions))
    print("\nClassification Report:")
    print(classification_report(y_test, predictions, zero_division=0))

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, predictions))

    return pipeline


def main():
    os.makedirs(MODEL_PATH, exist_ok=True)

    data = pd.read_csv(DATA_PATH)
    data = preprocess_feedback_dataframe(data)

    sentiment_model = train_classifier(
        data["cleaned_text"],
        data["sentiment"],
        "sentiment"
    )

    category_model = train_classifier(
        data["cleaned_text"],
        data["category"],
        "category"
    )

    joblib.dump(
        sentiment_model,
        os.path.join(MODEL_PATH, "sentiment_model.pkl")
    )

    joblib.dump(
        category_model,
        os.path.join(MODEL_PATH, "category_model.pkl")
    )

    print("\nModels saved successfully in the models folder.")


if __name__ == "__main__":
    main()