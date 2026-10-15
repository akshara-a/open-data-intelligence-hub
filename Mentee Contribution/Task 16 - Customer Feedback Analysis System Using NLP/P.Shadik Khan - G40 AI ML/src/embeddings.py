import os
import sys

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from preprocessing import clean_text


def calculate_similarity(
    feedback1,
    feedback2
):

    cleaned_feedback = [
        clean_text(feedback1),
        clean_text(feedback2)
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    tfidf_matrix = vectorizer.fit_transform(
        cleaned_feedback
    )

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )

    return similarity[0][0]


if __name__ == "__main__":

    feedback1 = (
        "The application is very slow"
    )

    feedback2 = (
        "The app takes a long time to load"
    )

    similarity = calculate_similarity(
        feedback1,
        feedback2
    )

    print("=" * 60)
    print("CUSTOMER FEEDBACK SIMILARITY")
    print("=" * 60)

    print("\nFeedback 1:")
    print(feedback1)

    print("\nFeedback 2:")
    print(feedback2)

    print(
        f"\nSimilarity Score: {similarity:.4f}"
    )