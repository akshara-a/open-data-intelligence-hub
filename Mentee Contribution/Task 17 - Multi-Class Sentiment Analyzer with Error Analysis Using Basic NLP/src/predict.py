import os
import re
import joblib


# -----------------------------
# Project paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "sentiment_model.pkl",
)

VECTORIZER_PATH = os.path.join(
    BASE_DIR,
    "models",
    "tfidf_vectorizer.pkl",
)


# -----------------------------
# Text cleaning function
# -----------------------------
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# -----------------------------
# Load trained model
# -----------------------------
model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


# -----------------------------
# Prediction function
# -----------------------------
def predict_sentiment(text):
    cleaned_text = clean_text(text)
    features = vectorizer.transform([cleaned_text])
    prediction = model.predict(features)[0]
    return prediction


# -----------------------------
# Test predictions
# -----------------------------
test_sentences = [
    "I am very happy with this service",
    "The product is okay",
    "This is a horrible experience",
    "The delivery was excellent",
    "The application is frustrating",
]

print("\nSentiment Predictions:\n")

for sentence in test_sentences:
    result = predict_sentiment(sentence)
    print(f"{sentence} -> {result}")