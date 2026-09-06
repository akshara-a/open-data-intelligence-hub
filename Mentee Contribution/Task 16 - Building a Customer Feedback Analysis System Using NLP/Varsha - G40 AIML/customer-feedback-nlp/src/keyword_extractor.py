import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer


# Words that are usually not useful as keywords
CUSTOM_STOP_WORDS = {
    "very", "really", "just", "did", "does", "doesnt",
    "dont", "the", "and", "is", "was", "are", "am",
    "to", "of", "a", "an", "for", "with", "this",
    "that", "it", "my", "i", "we", "they", "you",
    "has", "have", "had", "been", "be", "in", "on",
    "at", "but", "so", "not", "after", "few", "new"
}


def clean_text(text):

    text = str(text).lower()

    text = re.sub(
        r"http\S+|www\S+|https\S+",
        "",
        text
    )

    text = re.sub(
        r"[^a-zA-Z\s]",
        "",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    return text


def extract_keywords(text, top_n=5):

    cleaned = clean_text(text)

    if not cleaned:
        return []

    vectorizer = TfidfVectorizer(
        stop_words=list(CUSTOM_STOP_WORDS),
        ngram_range=(1, 2),
        token_pattern=r"(?u)\b[a-zA-Z]{3,}\b"
    )

    try:
        matrix = vectorizer.fit_transform([cleaned])
    except ValueError:
        return cleaned.split()[:top_n]

    feature_names = vectorizer.get_feature_names_out()
    scores = matrix.toarray()[0]

    ranked_indices = scores.argsort()[::-1]

    keywords = []

    for index in ranked_indices:

        keyword = feature_names[index]

        # Avoid phrases containing unnecessary words
        words = keyword.split()

        if any(word in CUSTOM_STOP_WORDS for word in words):
            continue

        if keyword not in keywords:
            keywords.append(keyword)

        if len(keywords) >= top_n:
            break

    return keywords


# ============================================================
# TEST KEYWORD EXTRACTION
# ============================================================

test_feedback = [

    "Payment failed and customer support did not respond",

    "The product quality is very poor and delivery was late",

    "The application is very slow and keeps freezing",

    "I love the new dashboard and excellent design",

    "I am very disappointed with the product quality"
]


print("=" * 70)
print("IMPROVED KEYWORD EXTRACTION")
print("=" * 70)


for feedback in test_feedback:

    keywords = extract_keywords(
        feedback,
        top_n=5
    )

    print("\nFeedback:")
    print(feedback)

    print("\nImportant Keywords/Phrases:")
    print(", ".join(keywords))


# ============================================================
# APPLY TO DATASET
# ============================================================

df = pd.read_csv(
    "data/processed_feedback.csv"
)

df["keywords"] = df["review_text"].apply(
    lambda text: ", ".join(
        extract_keywords(text)
    )
)


print("\n" + "=" * 70)
print("DATASET KEYWORD EXTRACTION")
print("=" * 70)


print(
    df[
        ["review_text", "sentiment", "keywords"]
    ].head(20).to_string(index=False)
)


# Save result

df.to_csv(
    "data/feedback_with_keywords.csv",
    index=False
)


print("\n" + "=" * 70)
print("KEYWORD EXTRACTION COMPLETED")
print("=" * 70)

print("\nSaved file:")
print("data/feedback_with_keywords.csv")