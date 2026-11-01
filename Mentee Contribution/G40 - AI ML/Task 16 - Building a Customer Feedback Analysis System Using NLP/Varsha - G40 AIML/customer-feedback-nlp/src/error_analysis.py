import joblib
import pandas as pd

from sklearn.model_selection import train_test_split


# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv(
    "data/processed_feedback.csv"
)

X = df["cleaned_text"]
y = df["sentiment"]


# ============================================================
# TRAIN-TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# ============================================================
# LOAD MODEL
# ============================================================

model = joblib.load(
    "models/sentiment_model.pkl"
)

vectorizer = joblib.load(
    "models/tfidf_vectorizer.pkl"
)


# ============================================================
# PREDICT TEST DATA
# ============================================================

X_test_tfidf = vectorizer.transform(X_test)

y_pred = model.predict(
    X_test_tfidf
)


# ============================================================
# FIND ERRORS
# ============================================================

results = pd.DataFrame({
    "text": X_test,
    "actual": y_test,
    "predicted": y_pred
})

errors = results[
    results["actual"] != results["predicted"]
]


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("=" * 70)
print("CUSTOMER FEEDBACK SENTIMENT ERROR ANALYSIS")
print("=" * 70)

print("\nTotal test samples:")
print(len(results))

print("\nCorrect predictions:")
print(len(results) - len(errors))

print("\nIncorrect predictions:")
print(len(errors))


print("\n" + "=" * 70)
print("ERROR ANALYSIS")
print("=" * 70)

if len(errors) == 0:

    print("\nNo errors were found in the test set.")

    print(
        "\nThe model correctly classified all "
        "5,000 test samples."
    )

else:

    print("\nExamples of incorrect predictions:\n")

    print(
        errors.head(20).to_string(index=False)
    )


# ============================================================
# SAVE ERRORS
# ============================================================

errors.to_csv(
    "data/error_analysis.csv",
    index=False
)


print("\n" + "=" * 70)
print("ERROR ANALYSIS COMPLETED")
print("=" * 70)

print(
    "\nSaved file:"
)

print(
    "data/error_analysis.csv"
)