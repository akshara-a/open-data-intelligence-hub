import pandas as pd
import joblib

from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


# --------------------------------------------------
# Project paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "processed_feedback.csv"

MODEL_DIR = BASE_DIR / "models"

MODEL_PATH = MODEL_DIR / "category_model.pkl"
VECTORIZER_PATH = MODEL_DIR / "category_tfidf.pkl"


# --------------------------------------------------
# Load dataset
# --------------------------------------------------

def load_data():
    """
    Load the processed feedback dataset.
    """

    df = pd.read_csv(DATA_PATH)

    return df


# --------------------------------------------------
# Train category model
# --------------------------------------------------

def train_category_model():
    """
    Train a TF-IDF + Logistic Regression
    category classification model.
    """

    # Load dataset
    df = load_data()

    # Input
    X = df["processed_text"]

    # Target
    y = df["category"]

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

    X_train_tfidf = vectorizer.fit_transform(
        X_train
    )

    X_test_tfidf = vectorizer.transform(
        X_test
    )

    # --------------------------------------------------
    # Logistic Regression
    # --------------------------------------------------

    model = LogisticRegression(
        max_iter=1000,
        class_weight="balanced"
    )

    model.fit(
        X_train_tfidf,
        y_train
    )

    # --------------------------------------------------
    # Prediction
    # --------------------------------------------------

    predictions = model.predict(
        X_test_tfidf
    )

    # --------------------------------------------------
    # Evaluation
    # --------------------------------------------------

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    print("Category Model Results")
    print("----------------------")

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

    print("\nCategory model saved to:")
    print(MODEL_PATH)

    print("\nTF-IDF vectorizer saved to:")
    print(VECTORIZER_PATH)

    return model, vectorizer


# --------------------------------------------------
# Load trained model
# --------------------------------------------------

def load_category_model():
    """
    Load the trained category model
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
# Predict category
# --------------------------------------------------

def predict_category(
    feedback,
    model=None,
    vectorizer=None
):
    """
    Predict the category of new feedback.
    """

    from src.preprocessing import preprocess_text

    # Load model if necessary
    if model is None or vectorizer is None:

        model, vectorizer = load_category_model()

    # Preprocess feedback
    processed_text = preprocess_text(
        feedback
    )

    # Convert to TF-IDF
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

    print("Training category model...\n")

    model, vectorizer = train_category_model()

    print("\nTesting custom feedback...\n")

    test_feedback = [
        "My card payment keeps getting declined.",
        "I cannot log into my account.",
        "The application takes too long to load.",
        "The customer support team helped me quickly.",
        "The new interface is confusing.",
        "The application crashes whenever I open it.",
        "Please add dark mode to the application."
    ]

    for feedback in test_feedback:

        result = predict_category(
            feedback,
            model,
            vectorizer
        )

        print(f"Feedback: {feedback}")
        print(f"Category: {result}")
        print()