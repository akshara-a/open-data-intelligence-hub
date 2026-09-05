import joblib


# ============================================================
# LOAD MODEL AND VECTORIZER
# ============================================================

model = joblib.load(
    "models/sentiment_model.pkl"
)

vectorizer = joblib.load(
    "models/tfidf_vectorizer.pkl"
)


# ============================================================
# TEST FEEDBACK
# ============================================================

test_feedback = [

    "I am very happy with the product",

    "I absolutely love this product",

    "This product is excellent",

    "The product is terrible and stopped working",

    "I am extremely disappointed",

    "The product is okay, nothing special",

    "The delivery was very fast",

    "The product quality is very poor",

    "I am satisfied with my purchase",

    "Payment failed and my money was deducted",

    "I want a refund for this product",

    "Please add dark mode to the application",

    "Customer support did not respond",

    "The application keeps crashing"
]


# ============================================================
# PREDICTION
# ============================================================

print("=" * 70)
print("CUSTOMER FEEDBACK SENTIMENT TESTING")
print("=" * 70)


for feedback in test_feedback:

    # Convert feedback to TF-IDF
    text_tfidf = vectorizer.transform(
        [feedback]
    )

    # Predict sentiment
    prediction = model.predict(
        text_tfidf
    )[0]

    # Prediction probabilities
    probabilities = model.predict_proba(
        text_tfidf
    )

    confidence = probabilities.max()

    print("\nFeedback:")
    print(feedback)

    print("\nPredicted Sentiment:")
    print(prediction)

    print("\nConfidence:")
    print(f"{confidence:.2%}")

    print("\n" + "-" * 70)


print("\n")
print("=" * 70)
print("SENTIMENT TESTING COMPLETED")
print("=" * 70)