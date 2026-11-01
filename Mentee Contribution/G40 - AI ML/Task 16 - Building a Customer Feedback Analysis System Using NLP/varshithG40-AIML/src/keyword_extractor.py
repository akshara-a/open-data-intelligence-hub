"""
Keyword & Keyphrase Extraction Module
Uses TF-IDF and N-gram importance scoring to extract salient terms and phrases
from customer feedback text.
"""

import re
from typing import List, Tuple, Dict, Optional, Set
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from src.preprocessing import clean_text, BASE_STOPWORDS


class KeywordExtractor:
    """
    Extracts key words and phrases using TF-IDF and N-grams.
    """

    def __init__(self,
                 ngram_range: Tuple[int, int] = (1, 3),
                 max_keywords: int = 5,
                 corpus: Optional[List[str]] = None):
        self.ngram_range = ngram_range
        self.max_keywords = max_keywords
        self.vectorizer = TfidfVectorizer(
            ngram_range=self.ngram_range,
            sublinear_tf=True,
            stop_words="english",
            min_df=1
        )
        self.is_corpus_fitted = False
        if corpus is not None and len(corpus) > 0:
            self.fit_corpus(corpus)

    def fit_corpus(self, corpus: List[str]):
        """
        Fits the TF-IDF vectorizer across a corpus of feedback.
        """
        cleaned_corpus = [clean_text(doc) for doc in corpus]
        self.vectorizer.fit(cleaned_corpus)
        self.is_corpus_fitted = True
        return self

    def _filter_candidate_phrase(self, phrase: str) -> bool:
        """
        Ensures phrase doesn't start or end with stopwords or single characters.
        """
        words = phrase.split()
        if not words:
            return False
        if words[0] in BASE_STOPWORDS or words[-1] in BASE_STOPWORDS:
            return False
        if any(len(w) < 2 for w in words):
            return False
        return True

    def extract_keywords(self,
                         text: str,
                         top_n: Optional[int] = None) -> List[Tuple[str, float]]:
        """
        Extracts top keywords and keyphrases from the input text,
        ranked by TF-IDF score.
        Returns list of (phrase, score) tuples.
        """
        n = top_n if top_n is not None else self.max_keywords
        cleaned = clean_text(text)
        if not cleaned:
            return []

        # If a background corpus was fitted, transform with respect to it
        if self.is_corpus_fitted:
            tfidf_vec = self.vectorizer.transform([cleaned])
            feature_names = self.vectorizer.get_feature_names_out()
            scores = tfidf_vec.toarray()[0]
            top_indices = np.argsort(scores)[::-1]

            results = []
            seen_words: Set[str] = set()
            for idx in top_indices:
                if scores[idx] <= 0:
                    break
                phrase = feature_names[idx]
                if self._filter_candidate_phrase(phrase):
                    # Avoid pure subphrase redundancy
                    if phrase not in seen_words:
                        results.append((phrase, round(float(scores[idx]), 3)))
                        seen_words.add(phrase)
                if len(results) >= n:
                    break
            if results:
                return results

        # Single-document TF-IDF extraction fallback if corpus has no matches
        local_vec = TfidfVectorizer(
            ngram_range=self.ngram_range,
            stop_words="english",
            min_df=1
        )
        try:
            vec_matrix = local_vec.fit_transform([cleaned])
            feature_names = local_vec.get_feature_names_out()
            scores = vec_matrix.toarray()[0]
            top_indices = np.argsort(scores)[::-1]

            results = []
            for idx in top_indices:
                phrase = feature_names[idx]
                if self._filter_candidate_phrase(phrase):
                    results.append((phrase, round(float(scores[idx]), 3)))
                if len(results) >= n:
                    break
            return results
        except Exception:
            # Fallback simple non-stopword tokens
            tokens = [w for w in cleaned.split() if w not in BASE_STOPWORDS and len(w) > 2]
            return [(t, 1.0) for t in tokens[:n]]

    def extract_keywords_list(self, text: str, top_n: Optional[int] = None) -> List[str]:
        """
        Returns list of string keywords/phrases without score numbers.
        """
        tuples = self.extract_keywords(text, top_n=top_n)
        return [phrase for phrase, _ in tuples]

    def highlight_keywords_in_text(self, text: str, keywords: List[str]) -> str:
        """
        Wraps keywords in markdown bold (**keyword**) for visual inspection.
        """
        highlighted = text
        for kw in sorted(keywords, key=len, reverse=True):
            pattern = re.compile(re.escape(kw), re.IGNORECASE)
            highlighted = pattern.sub(f"**{kw}**", highlighted)
        return highlighted
