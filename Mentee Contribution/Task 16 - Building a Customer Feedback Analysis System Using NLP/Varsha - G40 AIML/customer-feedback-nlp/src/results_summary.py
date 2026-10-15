# ============================================================
# CUSTOMER FEEDBACK ANALYSIS SYSTEM
# RESULTS SUMMARY
# ============================================================

import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)


# ============================================================
# 1. LOAD DATA
# ============================================================

df = pd.read_csv(
    "data/processed_feedback.csv"
)


# ============================================================
# 2. INPUT AND TARGET
# ============================================================

X = df["cleaned_text"]
y = df["sentiment"]


# ============================================================
# 3. TRAIN-TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# ============================================================
# 4. LOAD MODEL AND VECTORIZER
# ============================================================

model = joblib.load(
    "models/sentiment_model.pkl"
)

vectorizer = joblib.load(
    "models/tfidf_vectorizer.pkl"
)


# ============================================================
# 5. TF-IDF TRANSFORMATION
# ============================================================

X_test_tfidf = vectorizer.transform(
    X_test
)


# ============================================================
# 6. PREDICTION
# ============================================================

y_pred = model.predict(
    X_test_tfidf
)


# ============================================================
# 7. CALCULATE METRICS
# ============================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred,
    average="weighted"
)

recall = recall_score(
    y_test,
    y_pred,
    average="weighted"
)

f1 = f1_score(
    y_test,
    y_pred,
    average="weighted"
)


# ============================================================
# 8. CONFUSION MATRIX
# ============================================================

labels = [
    "negative",
    "neutral",
    "positive"
]

cm = confusion_matrix(
    y_test,
    y_pred,
    labels=labels
)


# ============================================================
# 9. DISPLAY RESULTS
# ============================================================

print("=" * 70)
print("CUSTOMER FEEDBACK ANALYSIS SYSTEM")
print("FINAL RESULTS SUMMARY")
print("=" * 70)


print("\nDATASET INFORMATION")
print("-" * 70)

print(
    "Total records:",
    len(df)
)

print(
    "Training records:",
    len(X_train)
)

print(
    "Testing records:",
    len(X_test)
)


print("\nSENTIMENT CLASSES")
print("-" * 70)

print(
    "Negative:",
    sum(y == "negative")
)

print(
    "Neutral:",
    sum(y == "neutral")
)

print(
    "Positive:",
    sum(y == "positive")
)


print("\nMODEL INFORMATION")
print("-" * 70)

print(
    "Feature Extraction: TF-IDF"
)

print(
    "Classifier: Logistic Regression"
)

print(
    "N-gram Range: (1, 2)"
)


print("\nEVALUATION RESULTS")
print("-" * 70)

print(
    f"Accuracy:  {accuracy:.2%}"
)

print(
    f"Precision: {precision:.2%}"
)

print(
    f"Recall:    {recall:.2%}"
)

print(
    f"F1-score:  {f1:.2%}"
)


print("\nCONFUSION MATRIX")
print("-" * 70)

print(
    "Labels:",
    labels
)

print()

print(cm)


print("\nNLP COMPONENTS")
print("-" * 70)

print(
    "1. Text preprocessing"
)

print(
    "2. TF-IDF feature extraction"
)

print(
    "3. Sentiment classification"
)

print(
    "4. Complaint category detection"
)

print(
    "5. Keyword extraction"
)

print(
    "6. Overall meaning generation"
)


print("\nFINAL STATUS")
print("-" * 70)

print(
    "Customer Feedback Analysis System completed successfully."
)

print("=" * 70)