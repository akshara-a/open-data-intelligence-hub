import os
import sys
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from preprocessing import clean_text


def extract_keywords(
    feedback,
    top_n=5
):

    cleaned_feedback = clean_text(
        feedback
    )

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    tfidf_matrix = vectorizer.fit_transform(
        [cleaned_feedback]
    )

    feature_names = vectorizer.get_feature_names_out()

    scores = tfidf_matrix.toarray()[0]

    keyword_scores = list(
        zip(
            feature_names,
            scores
        )
    )

    keyword_scores.sort(
        key=lambda x: x[1],
        reverse=True
    )

    keywords = [
        keyword
        for keyword, score
        in keyword_scores[:top_n]
    ]

    return keywords


if __name__ == "__main__":

    sample_feedback = (
        "The application is very slow "
        "and payment keeps failing"
    )

    keywords = extract_keywords(
        sample_feedback,
        top_n=5
    )

    print("=" * 60)
    print("KEYWORD EXTRACTION")
    print("=" * 60)

    print("\nFeedback:")
    print(sample_feedback)

    print("\nImportant Keywords:")

    for keyword in keywords:
        print("-", keyword)