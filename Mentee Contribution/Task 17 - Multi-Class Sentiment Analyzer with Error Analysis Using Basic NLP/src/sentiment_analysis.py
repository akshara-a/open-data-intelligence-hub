import os
import re
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
)


# -----------------------------
# 1. Project paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "data", "sentiment_data.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


# -----------------------------
# 2. Text cleaning function
# -----------------------------
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# -----------------------------
# 3. Load dataset
# -----------------------------
df = pd.read_csv(DATA_PATH)

df = df.dropna(subset=["text", "sentiment"])
df["clean_text"] = df["text"].apply(clean_text)

print("\nDataset shape:", df.shape)
print("\nClass distribution:")
print(df["sentiment"].value_counts())


# -----------------------------
# 4. Save sentiment distribution
# -----------------------------
plt.figure(figsize=(7, 5))
df["sentiment"].value_counts().plot(kind="bar")
plt.title("Sentiment Class Distribution")
plt.xlabel("Sentiment")
plt.ylabel("Number of Samples")
plt.tight_layout()
plt.savefig(
    os.path.join(OUTPUT_DIR, "sentiment_distribution.png")
)
plt.close()


# -----------------------------
# 5. Train-test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    df["clean_text"],
    df["sentiment"],
    test_size=0.25,
    random_state=42,
    stratify=df["sentiment"],
)


# -----------------------------
# 6. TF-IDF feature extraction
# -----------------------------
vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2),
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)


# -----------------------------
# 7. Train Logistic Regression
# -----------------------------
model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced",
)

model.fit(X_train_tfidf, y_train)


# -----------------------------
# 8. Evaluate model
# -----------------------------
y_pred = model.predict(X_test_tfidf)

accuracy = accuracy_score(y_test, y_pred)

print("\nAccuracy:", round(accuracy, 4))

report = classification_report(
    y_test,
    y_pred,
    zero_division=0,
)

print("\nClassification Report:\n")
print(report)

with open(
    os.path.join(OUTPUT_DIR, "classification_report.txt"),
    "w",
    encoding="utf-8",
) as file:
    file.write("Accuracy: " + str(round(accuracy, 4)) + "\n\n")
    file.write(report)


# -----------------------------
# 9. Confusion matrix
# -----------------------------
labels = ["negative", "neutral", "positive"]

cm = confusion_matrix(
    y_test,
    y_pred,
    labels=labels,
)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=labels,
)

disp.plot()
plt.title("Sentiment Confusion Matrix")
plt.tight_layout()
plt.savefig(
    os.path.join(OUTPUT_DIR, "confusion_matrix.png")
)
plt.close()


# -----------------------------
# 10. Error analysis
# -----------------------------
error_df = pd.DataFrame(
    {
        "text": X_test.values,
        "actual": y_test.values,
        "predicted": y_pred,
    }
)

error_df["is_error"] = (
    error_df["actual"] != error_df["predicted"]
)

errors_only = error_df[
    error_df["is_error"] == True
].copy()

errors_only.to_csv(
    os.path.join(OUTPUT_DIR, "error_analysis.csv"),
    index=False,
)

error_counts = pd.crosstab(
    error_df["actual"],
    error_df["predicted"],
)

error_counts.to_csv(
    os.path.join(OUTPUT_DIR, "error_counts.csv")
)


# -----------------------------
# 11. Save model and vectorizer
# -----------------------------
joblib.dump(
    model,
    os.path.join(MODEL_DIR, "sentiment_model.pkl"),
)

joblib.dump(
    vectorizer,
    os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl"),
)


# -----------------------------
# 12. Test new sentences
# -----------------------------
sample_sentences = [
    "I really enjoyed this amazing service",
    "The product was okay",
    "This was a terrible experience",
]

sample_cleaned = [
    clean_text(sentence)
    for sentence in sample_sentences
]

sample_features = vectorizer.transform(sample_cleaned)
sample_predictions = model.predict(sample_features)

print("\nSample Predictions:")
for sentence, prediction in zip(
    sample_sentences,
    sample_predictions,
):
    print(f"{sentence} -> {prediction}")


print("\nTraining completed successfully!")