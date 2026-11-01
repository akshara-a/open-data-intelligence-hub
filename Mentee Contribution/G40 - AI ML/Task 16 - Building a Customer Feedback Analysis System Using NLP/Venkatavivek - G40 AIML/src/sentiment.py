import pandas as pd
import joblib

from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report



BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "processed_feedback.csv"

MODEL_DIR = BASE_DIR / "models"

MODEL_PATH = MODEL_DIR / "sentiment_model.pkl"
VECTORIZER_PATH = MODEL_DIR / "sentiment_tfidf.pkl"




def load_data():
    """
    Load the processed feedback dataset.
    """

    df = pd.read_csv("/home/venkata/Downloads/Venkatavivek - G40 AIML/processed_feedback.csv")

    return df



def train_sentiment_model():
    """
    Train a TF-IDF + Logistic Regression
    sentiment classification model.
    """

    # Load data
    df = load_data()

    # Input
    X = df["processed_text"]

    # Target
    y = df["sentiment"]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # --------------------------------------------------
    # TF-IDF
    # --------------------------------------------------

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2)
    )

    X_train_tfidf = vectorizer.fit_transform(X_train)

    X_test_tfidf = vectorizer.transform(X_test)

    # --------------------------------------------------
    # Logistic Regression
    # --------------------------------------------------

    model = LogisticRegression(
        max_iter=1000,
        class_weight="balanced"
    )

    model.fit(X_train_tfidf, y_train)

    # --------------------------------------------------
    # Evaluation
    # --------------------------------------------------

    predictions = model.predict(X_test_tfidf)

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    print("Sentiment Model Results")
    print("-----------------------")

    print(f"Accuracy: {accuracy:.4f}")

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            predictions
        )
    )

    # --------------------------------------------------
    # Save model
    # --------------------------------------------------

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    joblib.dump(
        model,
        MODEL_PATH
    )

    joblib.dump(
        vectorizer,
        VECTORIZER_PATH
    )

    print("\nModel saved to:")
    print(MODEL_PATH)

    print("\nTF-IDF vectorizer saved to:")
    print(VECTORIZER_PATH)

    return model, vectorizer


# --------------------------------------------------
# Load trained model
# --------------------------------------------------

def load_sentiment_model():
    """
    Load the previously trained model
    and TF-IDF vectorizer.
    """

    model = joblib.load(
        MODEL_PATH
    )

    vectorizer = joblib.load(
        VECTORIZER_PATH
    )

    return model, vectorizer


# --------------------------------------------------
# Predict sentiment
# --------------------------------------------------

def predict_sentiment(
    feedback,
    model=None,
    vectorizer=None
):
    """
    Predict sentiment for new customer feedback.
    """

    # Import our preprocessing function
    from src.preprocessing import preprocess_text

    # Load model if not supplied
    if model is None or vectorizer is None:

        model, vectorizer = load_sentiment_model()

    # Preprocess new feedback
    processed_text = preprocess_text(
        feedback
    )

    # Convert text into TF-IDF
    text_tfidf = vectorizer.transform(
        [processed_text]
    )

    # Predict
    prediction = model.predict(
        text_tfidf
    )[0]

    return prediction


# --------------------------------------------------
# Test the module
# --------------------------------------------------

if __name__ == "__main__":

    print("Training sentiment model...\n")

    model, vectorizer = train_sentiment_model()

    print("\nTesting custom feedback...\n")

    test_feedback = [
        "The payment was successful and everything worked perfectly.",
        "My application keeps crashing and I am very frustrated.",
        "I want to know when my order will be delivered."
    ]

    for feedback in test_feedback:

        result = predict_sentiment(
            feedback,
            model,
            vectorizer
        )

        print(f"Feedback: {feedback}")
        print(f"Sentiment: {result}")
        print()