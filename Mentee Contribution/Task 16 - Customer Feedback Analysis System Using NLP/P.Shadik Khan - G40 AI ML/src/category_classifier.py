import os
import sys
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from preprocessing import clean_text


def train_category_model(data_path=None):

    if data_path is None:
        base_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        data_path = os.path.join(
            base_dir,
            "data",
            "feedback.csv"
        )

    # Load dataset
    df = pd.read_csv(data_path)

    # Extract main category
    df["main_category"] = df["category"].apply(
        lambda x: str(x).split("|")[0]
    )

    # Clean text
    df["clean_feedback"] = df["feedback"].apply(
        clean_text
    )

    # Features and target
    X = df["clean_feedback"]
    y = df["main_category"]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y
    )

    # TF-IDF
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    X_train_tfidf = vectorizer.fit_transform(
        X_train
    )

    X_test_tfidf = vectorizer.transform(
        X_test
    )

    # Logistic Regression
    model = LogisticRegression(
        max_iter=1000,
        random_state=42
    )

    model.fit(
        X_train_tfidf,
        y_train
    )

    # Predictions
    y_pred = model.predict(
        X_test_tfidf
    )

    # Accuracy
    accuracy = accuracy_score(
        y_test,
        y_pred
    )

    print("=" * 60)
    print("CUSTOMER FEEDBACK CATEGORY CLASSIFICATION")
    print("=" * 60)

    print(f"\nAccuracy: {accuracy:.4f}")

    print("\nClassification Report:")

    print(
        classification_report(
            y_test,
            y_pred,
            zero_division=0
        )
    )

    print("\nConfusion Matrix:")

    print(
        confusion_matrix(
            y_test,
            y_pred,
            labels=model.classes_
        )
    )

    return model, vectorizer


def predict_category(
    feedback,
    model,
    vectorizer
):

    cleaned_feedback = clean_text(
        feedback
    )

    feedback_tfidf = vectorizer.transform(
        [cleaned_feedback]
    )

    prediction = model.predict(
        feedback_tfidf
    )

    return prediction[0]


if __name__ == "__main__":

    model, vectorizer = train_category_model()

    print("\nTesting New Customer Feedback:")

    test_feedback = [
        "My payment is failing",
        "I cannot login to my account",
        "The application is very slow",
        "Please add dark mode",
        "Customer support did not respond",
        "The application keeps crashing"
    ]

    for feedback in test_feedback:

        category = predict_category(
            feedback,
            model,
            vectorizer
        )

        print("\nFeedback:", feedback)
        print(
            "Predicted Category:",
            category
        )