"""
Automated Test Suite for Customer Feedback Analysis System
Tests:
- Text Preprocessing & Negation Preservation
- Sentiment Classification
- Multi-label Category Classification
- Keyword & Keyphrase Extraction
- Semantic Similarity Engine
- Full End-to-End Pipeline
"""

import pytest
import pandas as pd
from src.preprocessing import (
    clean_text, tokenize, remove_stopwords, stem_words, lemmatize_words, compare_stem_vs_lemma
)
from src.sentiment import SentimentClassifier
from src.category_classifier import MultiLabelCategoryClassifier
from src.keyword_extractor import KeywordExtractor
from src.embeddings import FeedbackSimilarityEngine
from src.pipeline import CustomerFeedbackAnalyzer


class TestPreprocessing:

    def test_clean_text_basic(self):
        raw = "   APP is SOOO slow!!!!! https://example.com 😡  "
        cleaned = clean_text(raw)
        assert "app is soo slow" in cleaned
        assert "http" not in cleaned
        assert "!" not in cleaned

    def test_tokenize(self):
        text = "Payment didn't go through."
        tokens = tokenize(text)
        assert "payment" in tokens
        assert "didn't" in tokens
        assert "through" in tokens

    def test_negation_preservation(self):
        tokens = ["this", "app", "is", "not", "good"]
        # When preserve_negations=True, 'not' must be kept
        filtered = remove_stopwords(tokens, preserve_negations=True)
        assert "not" in filtered
        assert "good" in filtered
        assert "is" not in filtered

    def test_stemming_vs_lemmatization(self):
        comparison = compare_stem_vs_lemma(["better", "crashes", "studies"])
        assert len(comparison) == 3
        # In WordNet/morphology, 'better' lemmatizes to 'good'
        better_res = next(item for item in comparison if item["original"] == "better")
        assert better_res["lemmatized"] == "good"


class TestSentimentClassifier:

    @pytest.fixture
    def sample_data(self):
        texts = [
            "I love this application, it is amazing",
            "Payment keeps failing and money was deducted",
            "The app is okay, does basic things",
            "Super fast performance and sleek interface",
            "Terrible bug, app crashes every time I open it"
        ]
        labels = ["positive", "negative", "neutral", "positive", "negative"]
        return texts, labels

    def test_fit_and_predict(self, sample_data):
        texts, labels = sample_data
        clf = SentimentClassifier(ngram_range=(1, 2))
        clf.fit(texts, labels)

        assert clf.is_fitted
        pred = clf.predict_one("Love the app, wonderful work!")
        assert pred == "positive"

        pred_neg = clf.predict_one("Payment failed and money deducted")
        assert pred_neg == "negative"

    def test_predict_proba(self, sample_data):
        texts, labels = sample_data
        clf = SentimentClassifier(ngram_range=(1, 2))
        clf.fit(texts, labels)

        probs = clf.predict_proba_one("Payment keeps failing")
        assert "negative" in probs
        assert "positive" in probs
        assert "neutral" in probs
        # Sum of probabilities should be ~ 1.0
        assert 0.99 <= sum(probs.values()) <= 1.01


class TestCategoryClassifier:

    @pytest.fixture
    def multi_label_data(self):
        texts = [
            "Payment keeps failing during checkout",
            "The app is very slow and lagging",
            "App is slow and payment keeps failing",
            "Customer support resolved my issue quickly",
            "Login OTP not arriving"
        ]
        categories = [
            ["payment"],
            ["performance"],
            ["payment", "performance"],
            ["support"],
            ["login"]
        ]
        return texts, categories

    def test_multi_label_prediction(self, multi_label_data):
        texts, categories = multi_label_data
        clf = MultiLabelCategoryClassifier(threshold=0.30)
        clf.fit(texts, categories)

        # Multi-label test
        multi_pred = clf.predict_one("The app is slow and payment keeps failing")
        assert "payment" in multi_pred or "performance" in multi_pred
        scores = clf.predict_proba_one("The app is slow and payment keeps failing")
        assert scores["payment"] > 0.3
        assert scores["performance"] > 0.3


class TestKeywordExtractor:

    def test_extract_keywords(self):
        corpus = [
            "Payment gateway timed out during credit card checkout",
            "The customer support team helped solve my account issue",
            "Fingerprint login is completely broken"
        ]
        extractor = KeywordExtractor(ngram_range=(1, 2), max_keywords=3, corpus=corpus)
        keywords = extractor.extract_keywords_list("Payment gateway timed out during credit card checkout")
        assert len(keywords) > 0
        assert any("payment" in kw or "gateway" in kw or "checkout" in kw for kw in keywords)


class TestSimilarityEngine:

    def test_similarity_search(self):
        df = pd.DataFrame({
            "feedback": [
                "Payment failed during checkout with debit card",
                "App lags and is terribly slow",
                "Customer support was very helpful"
            ],
            "sentiment": ["negative", "negative", "positive"],
            "categories": ["payment", "performance", "support"]
        })
        engine = FeedbackSimilarityEngine()
        engine.index_corpus(df)

        results = engine.find_similar("Payment keeps failing on checkout", top_k=1)
        assert len(results) == 1
        assert "Payment failed" in results[0]["feedback"]
        assert results[0]["similarity_score"] > 0.25


class TestEndToEndPipeline:

    def test_pipeline_analysis(self):
        analyzer = CustomerFeedbackAnalyzer(data_path="data/feedback.csv")
        analyzer.load_or_train()

        result = analyzer.analyze("The application is very slow and payment keeps failing.")
        assert "sentiment" in result
        assert result["sentiment"] == "negative"
        assert "categories" in result
        assert isinstance(result["categories"], list)
        assert "payment" in result["categories"]
        assert "performance" in result["categories"]
        assert "keywords" in result
        assert len(result["keywords"]) > 0
        assert "similar_feedback" in result
