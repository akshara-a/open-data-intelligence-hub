"""
End-to-End Customer Feedback Analysis Pipeline
Coordinates:
- Text Preprocessing & Tokenization
- Sentiment Analysis (Probability distribution & dominant label)
- Multi-label Category Classification (Payment, Performance, UI, Support, etc.)
- Keyword & Keyphrase Extraction
- Historical Feedback Similarity Search
- Batch Analysis with Pandas
"""

import os
from typing import Dict, Any, List, Optional
import pandas as pd

from src.preprocessing import clean_text, tokenize, remove_stopwords, lemmatize_words
from src.sentiment import SentimentClassifier
from src.category_classifier import MultiLabelCategoryClassifier
from src.keyword_extractor import KeywordExtractor
from src.embeddings import FeedbackSimilarityEngine


class CustomerFeedbackAnalyzer:
    """
    Unified NLP Pipeline for comprehensive customer feedback analysis.
    """

    def __init__(self, models_dir: str = "models", data_path: str = "data/feedback.csv"):
        self.models_dir = models_dir
        self.data_path = data_path

        self.sentiment_model: Optional[SentimentClassifier] = None
        self.category_model: Optional[MultiLabelCategoryClassifier] = None
        self.keyword_extractor: Optional[KeywordExtractor] = None
        self.similarity_engine: Optional[FeedbackSimilarityEngine] = None
        self.is_ready: bool = False

    def train_and_initialize(self, csv_path: Optional[str] = None):
        """
        Trains all models on the dataset and initializes all components.
        """
        path = csv_path or self.data_path
        if not os.path.exists(path):
            raise FileNotFoundError(f"Feedback dataset not found at {path}")

        df = pd.read_csv(path)
        texts = df["feedback"].astype(str).tolist()
        sentiments = df["sentiment"].astype(str).tolist()
        categories = df["categories"].astype(str).tolist()

        # 1. Train Sentiment Model
        self.sentiment_model = SentimentClassifier(ngram_range=(1, 2))
        self.sentiment_model.fit(texts, sentiments)

        # 2. Train Multi-Label Category Classifier
        self.category_model = MultiLabelCategoryClassifier(ngram_range=(1, 2), threshold=0.35)
        self.category_model.fit(texts, categories)

        # 3. Fit Keyword Extractor on corpus
        self.keyword_extractor = KeywordExtractor(ngram_range=(1, 3), max_keywords=5, corpus=texts)

        # 4. Index Similarity Engine
        self.similarity_engine = FeedbackSimilarityEngine(ngram_range=(1, 2))
        self.similarity_engine.index_corpus(df, text_col="feedback")

        # 5. Save models
        os.makedirs(self.models_dir, exist_ok=True)
        self.sentiment_model.save(os.path.join(self.models_dir, "sentiment_model.joblib"))
        self.category_model.save(os.path.join(self.models_dir, "category_model.joblib"))

        self.is_ready = True
        return self

    def load_or_train(self):
        """
        Loads models if already saved, or trains from scratch if not yet saved.
        """
        sentiment_path = os.path.join(self.models_dir, "sentiment_model.joblib")
        category_path = os.path.join(self.models_dir, "category_model.joblib")

        if os.path.exists(sentiment_path) and os.path.exists(category_path) and os.path.exists(self.data_path):
            try:
                self.sentiment_model = SentimentClassifier.load(sentiment_path)
                self.category_model = MultiLabelCategoryClassifier.load(category_path)

                df = pd.read_csv(self.data_path)
                texts = df["feedback"].astype(str).tolist()

                self.keyword_extractor = KeywordExtractor(ngram_range=(1, 3), max_keywords=5, corpus=texts)
                self.similarity_engine = FeedbackSimilarityEngine(ngram_range=(1, 2))
                self.similarity_engine.index_corpus(df, text_col="feedback")

                self.is_ready = True
                return self
            except Exception:
                # If loading fails, fallback to retraining
                pass

        return self.train_and_initialize()

    def analyze(self, text: str, top_k_similar: int = 3) -> Dict[str, Any]:
        """
        Analyzes a single customer feedback message.
        Produces:
        - Cleaned text & tokens
        - Sentiment prediction and probability distribution
        - Multi-label categories and scores
        - Key phrases and important words
        - Semantically similar past feedback
        """
        if not self.is_ready:
            self.load_or_train()

        # Step 1: Preprocessing inspection
        cleaned = clean_text(text)
        tokens = tokenize(text)
        lemmas = lemmatize_words(remove_stopwords(tokens, preserve_negations=True))

        # Step 2: Sentiment Analysis
        sentiment = self.sentiment_model.predict_one(text)
        sentiment_scores = self.sentiment_model.predict_proba_one(text)

        # Step 3: Multi-Label Category Classification
        categories = self.category_model.predict_one(text)
        category_scores = self.category_model.predict_proba_one(text)

        # Step 4: Keyword Extraction
        keywords_with_scores = self.keyword_extractor.extract_keywords(text, top_n=5)
        keywords_list = [kw for kw, _ in keywords_with_scores]
        highlighted_text = self.keyword_extractor.highlight_keywords_in_text(text, keywords_list)

        # Step 5: Similar Feedback Search
        similar_feedback = self.similarity_engine.find_similar(text, top_k=top_k_similar)

        return {
            "raw_text": text,
            "cleaned_text": cleaned,
            "tokens": tokens,
            "lemmatized_tokens": lemmas,
            "sentiment": sentiment,
            "sentiment_scores": sentiment_scores,
            "sentiment_confidence": sentiment_scores.get(sentiment, 0.0),
            "categories": categories,
            "category_scores": category_scores,
            "keywords": keywords_list,
            "keywords_with_scores": keywords_with_scores,
            "highlighted_text": highlighted_text,
            "similar_feedback": similar_feedback
        }

    def analyze_batch(self, texts: List[str]) -> pd.DataFrame:
        """
        Analyzes a list of feedback texts and returns an enriched Pandas DataFrame.
        """
        records = []
        for text in texts:
            result = self.analyze(text, top_k_similar=1)
            sim_text = result["similar_feedback"][0]["feedback"] if result["similar_feedback"] else ""
            sim_score = result["similar_feedback"][0]["similarity_percentage"] if result["similar_feedback"] else "0%"
            records.append({
                "feedback": text,
                "sentiment": result["sentiment"],
                "confidence": result["sentiment_confidence"],
                "categories": ", ".join(result["categories"]),
                "keywords": ", ".join(result["keywords"][:3]),
                "most_similar_past_feedback": sim_text,
                "similarity": sim_score
            })
        return pd.DataFrame(records)
