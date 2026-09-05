import pandas as pd
import joblib
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay


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
# 5. CONVERT TEST DATA TO TF-IDF
# ============================================================

X_test_tfidf = vectorizer.transform(
    X_test
)


# ============================================================
# 6. PREDICT
# ============================================================

y_pred = model.predict(
    X_test_tfidf
)


# ============================================================
# 7. CONFUSION MATRIX
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


print("=" * 60)
print("CONFUSION MATRIX")
print("=" * 60)

print("\nLabels:")
print(labels)

print("\nMatrix:")
print(cm)


# ============================================================
# 8. CREATE VISUALIZATION
# ============================================================

display = ConfusionMatrixDisplay(

    confusion_matrix=cm,

    display_labels=labels
)


display.plot()


plt.title(
    "Customer Feedback Sentiment - Confusion Matrix"
)

plt.xlabel(
    "Predicted Sentiment"
)

plt.ylabel(
    "Actual Sentiment"
)


# ============================================================
# 9. SAVE IMAGE
# ============================================================

plt.savefig(
    "confusion_matrix.png",
    dpi=300,
    bbox_inches="tight"
)


print("\nConfusion matrix image saved successfully!")

print(
    "File: confusion_matrix.png"
)


# Display graph

plt.show()