import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

# Load dataset
df = pd.read_csv("data/sentiment_data.csv")

# Convert labels
label_map = {
    0: "negative",
    1: "neutral",
    2: "positive"
}

df["sentiment"] = df["label"].map(label_map)

# Text cleaning
def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"#\w+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

df["clean_text"] = df["text"].apply(clean_text)

# Input and target
X = df["clean_text"]
y = df["sentiment"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))

# TF-IDF Vectorization
tfidf = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2)
)

X_train_tfidf = tfidf.fit_transform(X_train)
X_test_tfidf = tfidf.transform(X_test)

print("TF-IDF training shape:", X_train_tfidf.shape)
print("TF-IDF testing shape:", X_test_tfidf.shape)
from sklearn.linear_model import LogisticRegression

# Train Logistic Regression model
model = LogisticRegression(max_iter=1000)

print("\nTraining Logistic Regression model...")

model.fit(X_train_tfidf, y_train)

print("Model training completed!")
from sklearn.metrics import accuracy_score, classification_report

# Make predictions
y_pred = model.predict(X_test_tfidf)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

print("\n" + "=" * 50)
print("MODEL EVALUATION")
print("=" * 50)

print(f"\nAccuracy: {accuracy:.4f}")
print(f"Accuracy Percentage: {accuracy * 100:.2f}%")

# Classification report
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# Create outputs folder if it doesn't exist
import os
os.makedirs("outputs", exist_ok=True)

# Confusion Matrix
ConfusionMatrixDisplay.from_predictions(
    y_test,
    y_pred,
    display_labels=["negative", "neutral", "positive"]
)

plt.title("Sentiment Analysis Confusion Matrix")
plt.tight_layout()

# Save confusion matrix
plt.savefig("outputs/confusion_matrix.png")

plt.show()

print("\nConfusion matrix saved to:")
print("outputs/confusion_matrix.png")
# ==============================
# ERROR ANALYSIS
# ==============================

import pandas as pd

# Create results DataFrame
results = pd.DataFrame({
    "text": X_test.values,
    "actual": y_test.values,
    "predicted": y_pred
})

# Find incorrect predictions
errors = results[results["actual"] != results["predicted"]]

print("\n" + "=" * 50)
print("ERROR ANALYSIS")
print("=" * 50)

print("\nTotal test samples:", len(results))
print("Correct predictions:", len(results) - len(errors))
print("Incorrect predictions:", len(errors))

# Display first 20 errors
print("\nFirst 20 incorrect predictions:")
print(errors.head(20).to_string(index=False))

# Save errors
errors.to_csv("outputs/error_analysis.csv", index=False)

print("\nError analysis saved to:")
print("outputs/error_analysis.csv")
import joblib

# Save the trained model
joblib.dump(model, "outputs/sentiment_model.pkl")

# Save the TF-IDF vectorizer
joblib.dump(tfidf, "outputs/tfidf_vectorizer.pkl")

print("\n" + "=" * 50)
print("MODEL SAVED")
print("=" * 50)

print("Model: outputs/sentiment_model.pkl")
print("Vectorizer: outputs/tfidf_vectorizer.pkl")
# ==============================
# SENTIMENT PREDICTION
# ==============================

def predict_sentiment(sentence):
    # Clean the input sentence
    cleaned = clean_text(sentence)

    # Convert text to TF-IDF
    vector = tfidf.transform([cleaned])

    # Predict sentiment
    prediction = model.predict(vector)[0]

    return prediction


print("\n" + "=" * 50)
print("SENTIMENT PREDICTION")
print("=" * 50)

# Test sentences
test_sentences = [
    "I really enjoyed this movie",
    "This product is terrible",
    "The movie was okay"
]

for sentence in test_sentences:
    result = predict_sentiment(sentence)
    print(f"\nText: {sentence}")
    print(f"Predicted Sentiment: {result}")