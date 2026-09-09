"""
=============================================================================
NLP Assignment: Multi-Class Sentiment Analyzer with Error Analysis Using Basic NLP
=============================================================================
This script implements a complete end-to-end sentiment analysis pipeline
for 3-class classification (Positive, Neutral, Negative) using TF-IDF and
Logistic Regression, followed by rigorous Error Analysis.
"""

import os
import re
import pandas as pd
import numpy as np
import matplotlib
# Use Agg backend if running in non-interactive/headless environments
if not os.environ.get("DISPLAY") and os.name != "nt":
    matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)


def main():
    print("=" * 70)
    print("1. LOADING THE DATASET")
    print("=" * 70)
    dataset_file = "sentiment_data.csv"
    if not os.path.exists(dataset_file):
        raise FileNotFoundError(f"Could not find dataset at {dataset_file}")

    df = pd.read_csv(dataset_file)
    print("First 5 rows of the dataset:")
    print(df.head())
    print("\nDataset Shape (rows, columns):", df.shape)

    print("\n" + "=" * 70)
    print("2. CHECKING DATASET INFORMATION & MISSING VALUES")
    print("=" * 70)
    print("Column names:", list(df.columns))
    print("\nDataset Info:")
    df.info()
    print("\nMissing values per column before cleanup:")
    print(df.isnull().sum())

    # Remove missing values if any exist
    df = df.dropna().reset_index(drop=True)
    print("\nMissing values per column after dropna():")
    print(df.isnull().sum())

    print("\n" + "=" * 70)
    print("3. CHECKING SENTIMENT CLASSES & DISTRIBUTION")
    print("=" * 70)
    sentiment_classes = df["sentiment"].unique()
    print("Unique sentiment classes:", sentiment_classes)
    class_counts = df["sentiment"].value_counts()
    print("\nSentiment Class Counts:\n", class_counts)

    # Visualize and save sentiment distribution plot
    plt.figure(figsize=(7, 5))
    class_counts.plot(kind="bar", color=["#2ecc71", "#e74c3c", "#3498db"])
    plt.title("Sentiment Distribution", fontsize=14, fontweight="bold")
    plt.xlabel("Sentiment", fontsize=12)
    plt.ylabel("Number of Samples", fontsize=12)
    plt.xticks(rotation=0)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    dist_fig_path = "sentiment_distribution.png"
    plt.savefig(dist_fig_path, dpi=300)
    print(f"\n[Saved sentiment distribution plot to: {dist_fig_path}]")
    try:
        plt.show(block=False)
        plt.pause(1)
    except Exception:
        pass
    plt.close()

    print("\n" + "=" * 70)
    print("4. TEXT PREPROCESSING")
    print("=" * 70)

    def clean_text(text):
        """Cleans input text by:
        1. Converting to lowercase
        2. Removing URLs (http/https)
        3. Removing non-alphabetic characters (punctuations, numbers)
        4. Collapsing extra whitespace
        """
        if not isinstance(text, str):
            return ""
        text = text.lower()
        text = re.sub(r"http\S+", "", text)
        text = re.sub(r"[^a-z\s]", "", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    df["clean_text"] = df["text"].apply(clean_text)

    print("Sample comparison of original and cleaned text:")
    sample_df = df[["text", "clean_text"]].head(5)
    for idx, row in sample_df.iterrows():
        print(f"[{idx + 1}] Original: {row['text']}")
        print(f"    Cleaned : {row['clean_text']}\n")

    print("=" * 70)
    print("5. DEFINING INPUT AND TARGET VARIABLES")
    print("=" * 70)
    X = df["clean_text"]
    y = df["sentiment"]
    print(f"Input features count: {len(X)}")
    print(f"Target labels count  : {len(y)}")

    print("\n" + "=" * 70)
    print("6. TRAIN-TEST SPLIT (80% Train, 20% Test)")
    print("=" * 70)
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )
    print(f"Training samples: {len(X_train)} (80%)")
    print(f"Testing samples : {len(X_test)} (20%)")
    print("\nTraining class distribution:")
    print(y_train.value_counts(normalize=True).round(3))
    print("\nTesting class distribution (stratified):")
    print(y_test.value_counts(normalize=True).round(3))

    print("\n" + "=" * 70)
    print("7. TF-IDF FEATURE EXTRACTION")
    print("=" * 70)
    # Using unigrams and bigrams, up to 5000 features
    tfidf = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2)
    )

    X_train_tfidf = tfidf.fit_transform(X_train)
    X_test_tfidf = tfidf.transform(X_test)

    print("Vocabulary size:", len(tfidf.vocabulary_))
    print("Shape of X_train_tfidf:", X_train_tfidf.shape)
    print("Shape of X_test_tfidf :", X_test_tfidf.shape)
    sample_features = list(tfidf.get_feature_names_out())[:15]
    print("Sample extracted TF-IDF features (unigrams & bigrams):", sample_features)

    print("\n" + "=" * 70)
    print("8. MODEL TRAINING (LOGISTIC REGRESSION)")
    print("=" * 70)
    model = LogisticRegression(
        max_iter=1000,
        random_state=42
    )
    model.fit(X_train_tfidf, y_train)
    print("Model training complete.")
    print("Classes learned by model:", model.classes_)

    print("\n" + "=" * 70)
    print("9. PREDICTION & MODEL EVALUATION")
    print("=" * 70)
    y_pred = model.predict(X_test_tfidf)

    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.4f} ({accuracy * 100:.2f}%)\n")

    print("Classification Report:")
    print(classification_report(y_test, y_pred, digits=4))

    print("Confusion Matrix:")
    cm = confusion_matrix(y_test, y_pred, labels=model.classes_)
    cm_df = pd.DataFrame(cm, index=[f"Actual {c}" for c in model.classes_],
                         columns=[f"Pred {c}" for c in model.classes_])
    print(cm_df)

    # Plot & save Confusion Matrix
    plt.figure(figsize=(7, 6))
    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=model.classes_
    )
    disp.plot(cmap="Blues", values_format="d")
    plt.title("Confusion Matrix - Multi-Class Sentiment Classifier", fontsize=12, fontweight="bold")
    plt.tight_layout()
    cm_fig_path = "confusion_matrix.png"
    plt.savefig(cm_fig_path, dpi=300)
    print(f"\n[Saved confusion matrix plot to: {cm_fig_path}]")
    try:
        plt.show(block=False)
        plt.pause(1)
    except Exception:
        pass
    plt.close()

    print("\n" + "=" * 70)
    print("10. ERROR ANALYSIS")
    print("=" * 70)
    # Assemble results DataFrame
    results = pd.DataFrame({
        "text": X_test.values,
        "actual": y_test.values,
        "predicted": y_pred
    })

    errors = results[results["actual"] != results["predicted"]].copy()
    total_samples = len(results)
    total_errors = len(errors)
    error_rate = total_errors / total_samples

    print(f"Total test samples      : {total_samples}")
    print(f"Total incorrect predictions: {total_errors}")
    print(f"Overall Error Rate      : {error_rate:.4f} ({error_rate * 100:.2f}%)")

    print("\nError Counts by (Actual -> Predicted):")
    error_counts = errors.groupby(["actual", "predicted"]).size()
    print(error_counts)

    print("\nSample Incorrect Predictions (First 15):")
    print(errors.head(15).to_string(index=False))

    print("\n" + "-" * 70)
    print("NEUTRAL CLASS ERROR DRILL-DOWN")
    print("-" * 70)
    neutral_errors = errors[errors["actual"] == "neutral"]
    print(f"Total neutral test samples misclassified: {len(neutral_errors)}")
    if not neutral_errors.empty:
        print(neutral_errors.head(10).to_string(index=False))

    print("\n" + "-" * 70)
    print("ERROR TAXONOMY INVESTIGATION (Key Error Categories)")
    print("-" * 70)

    # 1. Negation errors
    print("\n[Type 1: Negation]")
    negation_words = r"\b(not|never|no|neither|nor|didnt|wasnt)\b"
    neg_errors = errors[errors["text"].str.contains(negation_words, regex=True)]
    print(f"Found {len(neg_errors)} negation-related errors.")
    if not neg_errors.empty:
        print(neg_errors.head(5).to_string(index=False))

    # 2. Mixed Sentiment errors
    print("\n[Type 2: Mixed Sentiment / Contrast]")
    contrast_words = r"\b(but|though|although|however|yet|despite)\b"
    mixed_errors = errors[errors["text"].str.contains(contrast_words, regex=True)]
    print(f"Found {len(mixed_errors)} mixed-sentiment contrast errors.")
    if not mixed_errors.empty:
        print(mixed_errors.head(5).to_string(index=False))

    # 3. Short Sentences
    print("\n[Type 3: Short Sentences (<= 3 words)]")
    short_errors = errors[errors["text"].apply(lambda s: len(s.split()) <= 3)]
    print(f"Found {len(short_errors)} short sentence errors.")
    if not short_errors.empty:
        print(short_errors.head(5).to_string(index=False))

    print("\n" + "=" * 70)
    print("11. REAL-TIME SENTENCE PREDICTION FUNCTION & TESTING")
    print("=" * 70)

    def predict_sentiment(sentence):
        """Predicts the sentiment of any arbitrary input sentence."""
        cleaned = clean_text(sentence)
        sentence_vec = tfidf.transform([cleaned])
        pred_label = model.predict(sentence_vec)[0]
        # Also compute prediction probabilities for rich feedback
        probs = model.predict_proba(sentence_vec)[0]
        prob_dict = {cls: round(prob, 4) for cls, prob in zip(model.classes_, probs)}
        return pred_label, prob_dict

    test_sentences = [
        "This movie was amazing and fantastic!",
        "The movie was average and ordinary.",
        "I hated the story, it was dreadful and boring.",
        "The acting was excellent.",
        "Nothing special about this movie.",
        "The movie was not bad at all, I actually liked it.",
        "The acting was good but the story was boring.",
        "Great, another boring three-hour movie to waste my Sunday.",
        "The film runs for approximately one hundred and twenty minutes."
    ]

    print(f"{'Input Sentence':<60} | {'Prediction':<10} | {'Probabilities'}")
    print("-" * 105)
    for sent in test_sentences:
        pred, probs = predict_sentiment(sent)
        prob_str = f"Neg: {probs.get('negative', 0):.2f}, Neu: {probs.get('neutral', 0):.2f}, Pos: {probs.get('positive', 0):.2f}"
        print(f"{sent[:58]:<60} | {pred:<10} | {prob_str}")

    print("\n" + "=" * 70)
    print("PIPELINE EXECUTION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
