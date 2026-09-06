import pandas as pd
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# ============================================================
# 1. LOAD DATA
# ============================================================

df = pd.read_csv(
    "data/processed_feedback.csv"
)

print("=" * 70)
print("IMPROVED CUSTOMER FEEDBACK SENTIMENT ANALYSIS")
print("=" * 70)

print("\nDataset shape:")
print(df.shape)

print("\nSentiment distribution:")
print(df["sentiment"].value_counts())


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

print("\nTraining samples:")
print(len(X_train))

print("\nTesting samples:")
print(len(X_test))


# ============================================================
# 4. TF-IDF FEATURE EXTRACTION
# ============================================================

vectorizer = TfidfVectorizer(

    # Use English stop words
    stop_words="english",

    # Unigrams + bigrams
    ngram_range=(1, 2),

    # Ignore extremely rare words
    min_df=2,

    # Ignore terms appearing in more than 95% documents
    max_df=0.95,

    # Limit vocabulary size
    max_features=5000,

    # Sublinear TF scaling
    sublinear_tf=True
)


X_train_tfidf = vectorizer.fit_transform(
    X_train
)

X_test_tfidf = vectorizer.transform(
    X_test
)


print("\nTF-IDF training shape:")
print(X_train_tfidf.shape)

print("\nTF-IDF testing shape:")
print(X_test_tfidf.shape)


# ============================================================
# 5. LOGISTIC REGRESSION
# ============================================================

model = LogisticRegression(

    max_iter=2000,

    # Give balanced importance to classes
    class_weight="balanced",

    # Regularization strength
    C=1.0,

    random_state=42
)


model.fit(
    X_train_tfidf,
    y_train
)


print("\nModel training completed!")


# ============================================================
# 6. PREDICTION
# ============================================================

y_pred = model.predict(
    X_test_tfidf
)


# ============================================================
# 7. ACCURACY
# ============================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)


print("\n" + "=" * 70)
print("MODEL EVALUATION")
print("=" * 70)

print(
    f"\nAccuracy: {accuracy:.2%}"
)


# ============================================================
# 8. CLASSIFICATION REPORT
# ============================================================

print("\nClassification Report:")

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


print("\nConfusion Matrix:")

print("\nLabels:")
print(labels)

print("\nMatrix:")
print(cm)


# ============================================================
# 10. SAVE MODEL
# ============================================================

os.makedirs(
    "models",
    exist_ok=True
)


joblib.dump(
    model,
    "models/sentiment_model.pkl"
)


joblib.dump(
    vectorizer,
    "models/tfidf_vectorizer.pkl"
)


print("\n" + "=" * 70)
print("MODEL SAVED SUCCESSFULLY")
print("=" * 70)

print(
    "\nSentiment Model:"
)

print(
    "models/sentiment_model.pkl"
)


print(
    "\nTF-IDF Vectorizer:"
)

print(
    "models/tfidf_vectorizer.pkl"
)


print("\nTraining completed successfully!")