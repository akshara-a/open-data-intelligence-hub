"""Text preprocessing utilities for customer feedback analysis.

This module performs the main NLP cleaning steps:
- lowercase conversion
- whitespace cleanup
- punctuation removal
- tokenization
- stop-word removal while keeping negations important for sentiment
- optional lemmatization
"""

from __future__ import annotations

import re
from typing import List

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Ensure required NLTK resources are available.
# In newer NLTK versions, punkt_tab is also required before tokenization.
for resource in ["punkt", "punkt_tab", "stopwords", "wordnet", "omw-1.4"]:
    try:
        nltk.data.find(resource)
    except LookupError:
        nltk.download(resource, quiet=True)

NEGATION_WORDS = {
    "not", "no", "never", "cannot", "can't", "won't", "isn't", "aren't",
    "don't", "doesn't", "didn't", "wasn't", "weren't", "hardly", "nothing",
    "none"
}


def clean_text(text: str) -> str:
    """Convert text to lowercase and remove unnecessary punctuation and extra spaces."""
    if text is None:
        return ""

    text = str(text).lower()
    text = text.replace("’", "'")
    text = re.sub(r"http\S+|www\.\S+", " ", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize_text(text: str) -> List[str]:
    """Split text into individual words (tokens)."""
    cleaned = clean_text(text)
    if not cleaned:
        return []
    return word_tokenize(cleaned)


def remove_stopwords(tokens: List[str], keep_negations: bool = True) -> List[str]:
    """Remove common stop words while preserving sentiment-important negations."""
    stop_words = set(stopwords.words("english"))
    if keep_negations:
        stop_words = {word for word in stop_words if word not in NEGATION_WORDS}

    filtered_tokens = []
    for token in tokens:
        if token and token not in stop_words:
            filtered_tokens.append(token)
    return filtered_tokens


def lemmatize_tokens(tokens: List[str]) -> List[str]:
    """Normalize words to their base form using lemmatization."""
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(token) for token in tokens]


def preprocess_text(text: str, lemmatize: bool = True, remove_stopwords_flag: bool = True) -> str:
    """Apply the full preprocessing pipeline to a feedback string.

    Parameters:
        text: raw customer feedback
        lemmatize: whether to apply lemmatization
        remove_stopwords_flag: whether stop words should be removed

    Returns:
        cleaned and normalized text string
    """
    cleaned = clean_text(text)
    tokens = tokenize_text(cleaned)

    if remove_stopwords_flag:
        tokens = remove_stopwords(tokens, keep_negations=True)

    if lemmatize:
        tokens = lemmatize_tokens(tokens)

    return " ".join(tokens)


def preprocess_dataframe(df):
    """Apply preprocessing to a pandas DataFrame column named 'feedback'."""
    if "feedback" not in df.columns:
        raise ValueError("The DataFrame must contain a 'feedback' column.")

    df = df.copy()
    df["feedback_clean"] = df["feedback"].apply(preprocess_text)
    return df
