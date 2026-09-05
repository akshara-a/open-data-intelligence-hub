import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# ============================================================
# 1. LOAD DATA
# ============================================================

df = pd.read_csv("data/processed_feedback.csv")

print("=" * 70)
print("CUSTOMER FEEDBACK SENTIMENT MODEL EVALUATION")
print("=" * 70)

print("\nDataset shape:")
print(df.shape)


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
# 4. LOAD TRAINED MODEL AND VECTORIZER
# ============================================================

model = joblib.load(
    "models/sentiment_model.pkl"
)

vectorizer = joblib.load(
    "models/tfidf_vectorizer.pkl"
)


# ============================================================
# 5. CONVERT TEST TEXT INTO TF-IDF
# ============================================================

X_test_tfidf = vectorizer.transform(X_test)


# ============================================================
# 6. PREDICTION
# ============================================================

y_pred = model.predict(X_test_tfidf)


# ============================================================
# 7. ACCURACY
# ============================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

print("\n" + "=" * 70)
print("ACCURACY")
print("=" * 70)

print(f"\nAccuracy: {accuracy:.2%}")


# ============================================================
# 8. CLASSIFICATION REPORT
# ============================================================

print("\n" + "=" * 70)
print("CLASSIFICATION REPORT")
print("=" * 70)

print(
    classification_report(
        y_test,
        y_pred
    )
)


# ============================================================
# 9. CONFUSION MATRIX
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

print("\n" + "=" * 70)
print("CONFUSION MATRIX")
print("=" * 70)

print("\nLabels:")
print(labels)

print("\nMatrix:")
print(cm)


# ============================================================
# 10. INTERPRETATION
# ============================================================

print("\n" + "=" * 70)
print("EVALUATION SUMMARY")
print("=" * 70)

print("\nThe model was evaluated using:")
print("- Accuracy")
print("- Precision")
print("- Recall")
print("- F1-score")
print("- Confusion Matrix")

print("\nEvaluation completed successfully!")