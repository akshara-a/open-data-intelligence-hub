"""Keyword and phrase extraction using TF-IDF for customer feedback."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

from src.preprocessing import preprocess_text

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT_DIR / "data" / "feedback.csv"


def load_feedback_texts(data_path: str | Path = DATA_PATH) -> list[str]:
    """Load all feedback text from the dataset."""
    df = pd.read_csv(data_path)
    if "feedback" not in df.columns:
        raise ValueError("Dataset must include a 'feedback' column.")
    return df["feedback"].fillna("").astype(str).tolist()


def extract_keywords(text: str, top_n: int = 5, data_path: str | Path = DATA_PATH) -> list[str]:
    """Extract the most important keywords and phrases from a feedback sentence.

    Uses TF-IDF with unigrams and bigrams so keywords can be both single words and
    short phrases such as 'payment failed' or 'slow login'.
    """
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Please provide a valid customer feedback string.")

    feedbacks = load_feedback_texts(data_path)
    feedbacks.append(text)
    cleaned_feedbacks = [preprocess_text(item) for item in feedbacks]

    vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=5000)
    tfidf_matrix = vectorizer.fit_transform(cleaned_feedbacks)
    feature_names = vectorizer.get_feature_names_out()

    target_vector = tfidf_matrix[-1]
    scores = zip(feature_names, target_vector.toarray()[0])
    scored_terms = sorted(scores, key=lambda item: item[1], reverse=True)

    keywords = []
    for term, score in scored_terms:
        if score > 0 and term.strip():
            keywords.append(term)
        if len(keywords) >= top_n:
            break

    return keywords
