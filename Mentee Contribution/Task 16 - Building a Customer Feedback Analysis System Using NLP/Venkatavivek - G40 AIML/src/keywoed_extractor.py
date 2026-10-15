import pandas as pd

from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer


# --------------------------------------------------
# Project paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "processed_feedback.csv"


# --------------------------------------------------
# Load data
# --------------------------------------------------

def load_data():

    df = pd.read_csv(DATA_PATH)

    return df


# --------------------------------------------------
# Train TF-IDF
# --------------------------------------------------

def create_tfidf():

    df = load_data()

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2)
    )

    tfidf_matrix = vectorizer.fit_transform(
        df["processed_text"]
    )

    feature_names = vectorizer.get_feature_names_out()

    return vectorizer, tfidf_matrix, feature_names


# --------------------------------------------------
# Extract keywords
# --------------------------------------------------

def extract_keywords(text, top_n=5):

    vectorizer, _, _ = create_tfidf()

    tfidf_vector = vectorizer.transform(
        [text]
    )

    feature_names = vectorizer.get_feature_names_out()

    scores = tfidf_vector.toarray()[0]

    keyword_scores = list(
        zip(feature_names, scores)
    )

    keyword_scores = sorted(
        keyword_scores,
        key=lambda x: x[1],
        reverse=True
    )

    keywords = [
        word
        for word, score in keyword_scores[:top_n]
        if score > 0
    ]

    return keywords


# --------------------------------------------------
# Extract keywords from already processed text
# --------------------------------------------------

def extract_keywords_from_processed_text(
    processed_text,
    top_n=5
):

    vectorizer, _, _ = create_tfidf()

    vector = vectorizer.transform(
        [processed_text]
    )

    feature_names = vectorizer.get_feature_names_out()

    scores = vector.toarray()[0]

    keyword_scores = list(
        zip(feature_names, scores)
    )

    keyword_scores.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return keyword_scores[:top_n]


# --------------------------------------------------
# Test
# --------------------------------------------------

if __name__ == "__main__":

    feedback = (
        "The payment page is extremely slow "
        "and the transaction keeps failing."
    )

    keywords = extract_keywords(
        feedback,
        top_n=5
    )

    print("Feedback:")
    print(feedback)

    print("\nImportant keywords:")

    for keyword in keywords:
        print("-", keyword)