import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

from preprocessing import clean_text


def train_sentiment_model(data_path="../data/feedback.csv"):
    """
    Train a TF-IDF + Logistic Regression sentiment classifier.
    """

    # Load dataset
    df = pd.read_csv(data_path)

    # Clean feedback
    df["clean_feedback"] = df["feedback"].apply(clean_text)

    # Features and target
    X = df["clean_feedback"]
    y = df["sentiment"]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y
    )

    # TF-IDF feature extraction
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    # Train model
    model = LogisticRegression(
        max_iter=1000,
        random_state=42
    )

    model.fit(X_train_tfidf, y_train)

    # Predictions
    y_pred = model.predict(X_test_tfidf)

    # Accuracy
    accuracy = accuracy_score(y_test, y_pred)

    print("=" * 60)
    print("SENTIMENT ANALYSIS")
    print("=" * 60)

    print(f"\nAccuracy: {accuracy:.4f}")

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))

    print("\nConfusion Matrix:")
    print(confusion_matrix(
        y_test,
        y_pred,
        labels=model.classes_
    ))

    return model, vectorizer, accuracy


def predict_sentiment(
    feedback,
    model,
    vectorizer
):
    """
    Predict sentiment for new customer feedback.
    """

    cleaned_feedback = clean_text(feedback)

    feedback_tfidf = vectorizer.transform(
        [cleaned_feedback]
    )

    prediction = model.predict(
        feedback_tfidf
    )

    return prediction[0]


if __name__ == "__main__":

    model, vectorizer, accuracy = train_sentiment_model()

    print("\nTesting new customer feedback:")

    test_feedback = [
        "The application is very slow",
        "I love the new dashboard",
        "Payment keeps failing"
    ]

    for feedback in test_feedback:

        sentiment = predict_sentiment(
            feedback,
            model,
            vectorizer
        )

        print(f"\nFeedback: {feedback}")
        print(f"Predicted Sentiment: {sentiment}")