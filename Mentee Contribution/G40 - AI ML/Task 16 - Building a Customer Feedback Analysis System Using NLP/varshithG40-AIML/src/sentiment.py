"""
Sentiment Analysis Module using TF-IDF and Logistic Regression
Includes:
- Training Pipeline with N-grams (Unigrams + Bigrams)
- Sentiment Probability Scoring (Positive, Negative, Neutral)
- Evaluation Metrics (Accuracy, Precision, Recall, F1, Confusion Matrix)
- Model Persistence (Save / Load)
- Model Interpretability (Top informative N-grams per sentiment class)
"""

import os
from typing import List, Dict, Any, Tuple, Optional
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report, confusion_matrix
import joblib

from src.preprocessing import preprocess_feedback


class SentimentClassifier:
    """
    Classical NLP Sentiment Classifier based on TF-IDF + Logistic Regression.
    """

    def __init__(self,
                 ngram_range: Tuple[int, int] = (1, 2),
                 C: float = 1.5,
                 max_iter: int = 1000,
                 random_state: int = 42):
        self.ngram_range = ngram_range
        self.C = C
        self.max_iter = max_iter
        self.random_state = random_state

        self.pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(
                ngram_range=self.ngram_range,
                sublinear_tf=True,
                min_df=1,
                max_df=0.98,
                preprocessor=preprocess_feedback
            )),
            ("clf", LogisticRegression(
                C=self.C,
                max_iter=self.max_iter,
                class_weight="balanced",
                random_state=self.random_state,
                solver="lbfgs"
            ))
        ])
        self.classes_: Optional[List[str]] = None
        self.is_fitted: bool = False

    def fit(self, texts: List[str], labels: List[str]):
        """
        Trains the sentiment classifier on feedback texts and sentiment labels.
        """
        self.pipeline.fit(texts, labels)
        self.classes_ = list(self.pipeline.named_steps["clf"].classes_)
        self.is_fitted = True
        return self

    def predict(self, texts: List[str]) -> List[str]:
        """
        Predicts sentiment labels for a list of texts.
        """
        if not self.is_fitted:
            raise RuntimeError("Model must be trained before predicting.")
        return list(self.pipeline.predict(texts))

    def predict_one(self, text: str) -> str:
        """
        Predicts sentiment for a single text.
        """
        return self.predict([text])[0]

    def predict_proba(self, texts: List[str]) -> List[Dict[str, float]]:
        """
        Returns prediction probabilities for each class across given texts.
        """
        if not self.is_fitted:
            raise RuntimeError("Model must be trained before predicting.")

        probas = self.pipeline.predict_proba(texts)
        results = []
        for prob_row in probas:
            class_dict = {
                cls_name: round(float(prob_row[idx]), 4)
                for idx, cls_name in enumerate(self.classes_)
            }
            results.append(class_dict)
        return results

    def predict_proba_one(self, text: str) -> Dict[str, float]:
        """
        Returns probabilities for a single text.
        """
        return self.predict_proba([text])[0]

    def evaluate(self, texts: List[str], labels: List[str]) -> Dict[str, Any]:
        """
        Computes comprehensive evaluation metrics on test dataset.
        """
        predictions = self.predict(texts)
        acc = accuracy_score(labels, predictions)
        prec, rec, f1, _ = precision_recall_fscore_support(
            labels, predictions, average="weighted", zero_division=0
        )
        report = classification_report(labels, predictions, output_dict=True, zero_division=0)
        cm = confusion_matrix(labels, predictions, labels=self.classes_)

        return {
            "accuracy": round(float(acc), 4),
            "precision": round(float(prec), 4),
            "recall": round(float(rec), 4),
            "f1_score": round(float(f1), 4),
            "classification_report": report,
            "confusion_matrix": cm.tolist(),
            "classes": self.classes_
        }

    def get_top_features(self, n_top: int = 8) -> Dict[str, List[Tuple[str, float]]]:
        """
        Returns the top most influential TF-IDF n-grams for each sentiment class.
        Provides model explainability.
        """
        if not self.is_fitted:
            return {}

        vectorizer = self.pipeline.named_steps["tfidf"]
        classifier = self.pipeline.named_steps["clf"]
        feature_names = np.array(vectorizer.get_feature_names_out())

        top_features = {}
        for class_idx, class_label in enumerate(classifier.classes_):
            coefficients = classifier.coef_[class_idx]
            top_indices = np.argsort(coefficients)[::-1][:n_top]
            top_words = [
                (feature_names[idx], round(float(coefficients[idx]), 3))
                for idx in top_indices
            ]
            top_features[class_label] = top_words

        return top_features

    def save(self, filepath: str):
        """
        Saves the trained pipeline to disk.
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(self, filepath)

    @classmethod
    def load(cls, filepath: str) -> "SentimentClassifier":
        """
        Loads a saved pipeline from disk.
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found at {filepath}")
        return joblib.load(filepath)
