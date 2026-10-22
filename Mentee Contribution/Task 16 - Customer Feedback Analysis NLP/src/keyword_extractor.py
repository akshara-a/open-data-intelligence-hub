import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer

from preprocessing import preprocess_feedback_dataframe


def extract_keywords(text, top_n=5):
    """
    Extract the most important keywords from one feedback text.
    """

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    tfidf_matrix = vectorizer.fit_transform([text])

    feature_names = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.toarray()[0]

    keyword_scores = list(
        zip(feature_names, scores)
    )

    keyword_scores = sorted(
        keyword_scores,
        key=lambda item: item[1],
        reverse=True
    )

    keywords = [
        word for word, score in keyword_scores[:top_n]
    ]

    return keywords


if __name__ == "__main__":
    sample_text = (
        "The application is very slow and payment failed"
    )

    keywords = extract_keywords(sample_text)

    print("Important Keywords:")
    print(keywords)
    