"""
Sentence Embeddings & Semantic Similarity Module
Computes numerical vector representations of customer feedback and finds
semantically similar complaints/reviews using Cosine Similarity.
"""

from typing import List, Dict, Any, Optional
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.preprocessing import preprocess_feedback


class FeedbackSimilarityEngine:
    """
    Finds historical feedback with similar meaning using vector space embeddings
    and Cosine Similarity.
    """

    def __init__(self, ngram_range: tuple = (1, 2)):
        self.ngram_range = ngram_range
        self.vectorizer = TfidfVectorizer(
            ngram_range=self.ngram_range,
            sublinear_tf=True,
            min_df=1,
            preprocessor=preprocess_feedback
        )
        self.corpus_df: Optional[pd.DataFrame] = None
        self.corpus_vectors: Optional[np.ndarray] = None
        self.is_indexed: bool = False

    def index_corpus(self, df: pd.DataFrame, text_col: str = "feedback"):
        """
        Indexes the historical customer feedback dataset.
        """
        self.corpus_df = df.copy().reset_index(drop=True)
        texts = self.corpus_df[text_col].astype(str).tolist()
        self.corpus_vectors = self.vectorizer.fit_transform(texts)
        self.is_indexed = True
        return self

    def find_similar(self,
                     query_text: str,
                     top_k: int = 3,
                     min_similarity: float = 0.15) -> List[Dict[str, Any]]:
        """
        Searches the indexed corpus for top_k most similar feedback items.
        Returns matched text, similarity score, sentiment, and categories.
        """
        if not self.is_indexed or self.corpus_vectors is None:
            raise RuntimeError("Corpus must be indexed before querying similarity.")

        query_vec = self.vectorizer.transform([query_text])
        similarities = cosine_similarity(query_vec, self.corpus_vectors)[0]

        top_indices = np.argsort(similarities)[::-1]

        results = []
        for idx in top_indices:
            score = float(similarities[idx])
            if score < min_similarity:
                break

            row = self.corpus_df.iloc[idx]
            match_data = {
                "feedback": row["feedback"],
                "similarity_score": round(score, 4),
                "similarity_percentage": f"{round(score * 100, 1)}%",
                "sentiment": row.get("sentiment", "unknown"),
                "categories": row.get("categories", "general")
            }
            results.append(match_data)
            if len(results) >= top_k:
                break

        return results

    def compute_pairwise_similarity(self, text_a: str, text_b: str) -> float:
        """
        Computes cosine similarity between two individual text strings.
        Useful for comparing:
        'Payment failed during checkout' vs 'Unable to complete my card transaction'
        """
        vecs = self.vectorizer.transform([text_a, text_b])
        score = float(cosine_similarity(vecs[0:1], vecs[1:2])[0][0])
        return round(score, 4)
