"""
Text Preprocessing Module for Customer Feedback Analysis
Includes:
- Text Cleaning & Normalization
- Tokenization
- Negation-Preserving Stopword Filtering
- Stemming & Lemmatization with Comparative Utilities
"""

import re
from typing import List, Tuple, Dict, Optional

# Sentiment-critical negation and contrast words to preserve when removing stopwords
NEGATION_WORDS = {
    "not", "no", "never", "none", "neither", "nor", "hardly", "scarcely",
    "barely", "doesn't", "don't", "didn't", "wasn't", "weren't", "haven't",
    "hasn't", "hadn't", "won't", "wouldn't", "can't", "couldn't", "shouldn't",
    "isn't", "aren't", "ain't", "without", "against", "but", "however"
}

# Standard English stopwords
BASE_STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "as", "at", "be", "because", "been", "before", "being", "below",
    "between", "both", "by", "could", "did", "do", "does", "doing", "down", "during",
    "each", "few", "for", "from", "further", "had", "has", "have", "having", "he",
    "her", "here", "hers", "herself", "him", "himself", "his", "how", "i", "if",
    "in", "into", "is", "it", "its", "itself", "just", "me", "more", "most", "my",
    "myself", "of", "off", "on", "once", "only", "or", "other", "our", "ours",
    "ourselves", "out", "over", "own", "s", "same", "she", "should", "so", "some",
    "such", "t", "than", "that", "the", "their", "theirs", "them", "themselves",
    "then", "there", "these", "they", "this", "those", "through", "to", "too",
    "under", "until", "up", "very", "was", "we", "were", "what", "when", "where",
    "which", "while", "who", "whom", "why", "will", "with", "you", "your", "yours",
    "yourself", "yourselves"
}

# Curated morphological lemmatization lookup dictionary for domain vocabulary
LEMMA_LOOKUP = {
    "better": "good",
    "best": "good",
    "worse": "bad",
    "worst": "bad",
    "running": "run",
    "runs": "run",
    "ran": "run",
    "payments": "payment",
    "paid": "pay",
    "paying": "pay",
    "crashes": "crash",
    "crashed": "crash",
    "crashing": "crash",
    "complaining": "complain",
    "complained": "complain",
    "complaints": "complaint",
    "failed": "fail",
    "failing": "fail",
    "fails": "fail",
    "slowest": "slow",
    "slower": "slow",
    "faster": "fast",
    "fastest": "fast",
    "screens": "screen",
    "buttons": "button",
    "features": "feature",
    "bugs": "bug",
    "issues": "issue",
    "tickets": "ticket",
    "transactions": "transaction",
    "updates": "update",
    "updated": "update",
    "updating": "update",
    "errors": "error",
    "logging": "log",
    "logged": "log",
    "services": "service",
    "solved": "solve",
    "solving": "solve",
    "resolving": "resolve",
    "resolved": "resolve",
    "studies": "study",
    "studied": "study",
    "connected": "connect",
    "connecting": "connect",
    "connections": "connect"
}


def clean_text(text: str, keep_punctuation_sentiment: bool = False) -> str:
    """
    Cleans raw customer feedback text.
    - Converts to lowercase
    - Normalizes URLs, emails, and phone numbers
    - Normalizes repeated punctuation (e.g. '!!!!' -> '!')
    - Strips noisy special characters while preserving contraction apostrophes and hyphens
    - Normalizes whitespace
    """
    if not isinstance(text, str):
        return ""

    # Convert to lowercase
    text = text.lower().strip()

    # Normalize URLs
    text = re.sub(r"https?://\S+|www\.\S+", " url ", text)

    # Normalize emails
    text = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", " email ", text)

    # Compress repeated punctuation (e.g. 'sooo slow!!!!!' -> 'sooo slow !')
    text = re.sub(r"!+", " !", text)
    text = re.sub(r"\?+", " ?", text)

    # Compress repeated characters (e.g. 'soooo' -> 'soo')
    text = re.sub(r"(.)\1{2,}", r"\1\1", text)

    if not keep_punctuation_sentiment:
        # Keep alphanumeric, apostrophes, and spaces
        text = re.sub(r"[^a-z0-9\s']", " ", text)

    # Collapse multiple whitespaces
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize(text: str) -> List[str]:
    """
    Tokenizes text into a list of word tokens.
    Uses regex boundary matching for fast execution without external dependencies.
    """
    cleaned = clean_text(text, keep_punctuation_sentiment=False)
    # Split on words and keep apostrophes intact (e.g., "doesn't", "user's")
    tokens = re.findall(r"\b[a-z0-9]+(?:'[a-z]+)?\b", cleaned)
    return tokens


def remove_stopwords(tokens: List[str], preserve_negations: bool = True) -> List[str]:
    """
    Filters stopwords while optionally preserving sentiment-critical negation tokens.
    Crucial for sentiment analysis so 'not good' doesn't become 'good'.
    """
    if preserve_negations:
        active_stopwords = BASE_STOPWORDS - NEGATION_WORDS
    else:
        active_stopwords = BASE_STOPWORDS

    return [t for t in tokens if t not in active_stopwords and len(t) > 1]


def stem_words(tokens: List[str]) -> List[str]:
    """
    Applies suffix stemming (reducing words to morphological roots).
    e.g. 'playing' -> 'play', 'crashes' -> 'crash', 'studies' -> 'studi'
    """
    stemmed = []
    for t in tokens:
        if t.endswith("ing") and len(t) > 5:
            stemmed.append(t[:-3])
        elif t.endswith("ies") and len(t) > 4:
            stemmed.append(t[:-3] + "i")  # e.g., studies -> studi
        elif t.endswith("ed") and len(t) > 4:
            stemmed.append(t[:-2])
        elif t.endswith("ly") and len(t) > 4:
            stemmed.append(t[:-2])
        elif t.endswith("es") and len(t) > 4:
            stemmed.append(t[:-2])
        elif t.endswith("s") and len(t) > 3 and not t.endswith("ss"):
            stemmed.append(t[:-1])
        else:
            stemmed.append(t)
    return stemmed


def lemmatize_words(tokens: List[str]) -> List[str]:
    """
    Applies Lemmatization to convert words into their grammatical dictionary base form.
    e.g. 'better' -> 'good', 'studies' -> 'study', 'complaining' -> 'complain'
    """
    lemmas = []
    for t in tokens:
        if t in LEMMA_LOOKUP:
            lemmas.append(LEMMA_LOOKUP[t])
        elif t.endswith("ies") and len(t) > 4:
            lemmas.append(t[:-3] + "y")  # e.g., studies -> study
        elif t.endswith("ing") and len(t) > 5:
            lemmas.append(t[:-3])
        elif t.endswith("ed") and len(t) > 4:
            lemmas.append(t[:-2])
        elif t.endswith("s") and len(t) > 3 and not t.endswith("ss"):
            lemmas.append(t[:-1])
        else:
            lemmas.append(t)
    return lemmas


def preprocess_feedback(text: str,
                        lemmatize: bool = True,
                        preserve_negations: bool = True) -> str:
    """
    Full text preprocessing pipeline for downstream TF-IDF and classification.
    Returns cleaned, filtered, and lemmatized text joined as a string.
    """
    tokens = tokenize(text)
    filtered = remove_stopwords(tokens, preserve_negations=preserve_negations)
    if lemmatize:
        processed_tokens = lemmatize_words(filtered)
    else:
        processed_tokens = filtered
    return " ".join(processed_tokens)


def compare_stem_vs_lemma(sample_words: Optional[List[str]] = None) -> List[Dict[str, str]]:
    """
    Educational helper comparing Stemming vs Lemmatization on words.
    Useful for interactive inspection in UI and notebooks.
    """
    if sample_words is None:
        sample_words = [
            "complaining", "payments", "better", "crashes",
            "failing", "studies", "connected", "resolution"
        ]

    stems = stem_words(sample_words)
    lemmas = lemmatize_words(sample_words)

    results = []
    for word, stem, lemma in zip(sample_words, stems, lemmas):
        results.append({
            "original": word,
            "stemmed": stem,
            "lemmatized": lemma,
            "is_different": stem != lemma
        })
    return results
