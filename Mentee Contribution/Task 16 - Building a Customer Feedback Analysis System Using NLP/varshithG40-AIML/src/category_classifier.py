"""
Multi-Label Category Classifier for Customer Feedback
Uses:
- TF-IDF N-gram Representation
- MultiLabelBinarizer for category vectorization
- OneVsRestClassifier with Logistic Regression
- Threshold-tuned multi-label prediction
- Comprehensive multi-label evaluation (Micro/Macro F1, Hamming Loss)
"""

import os
from typing import List, Dict, Any, Tuple, Optional, Union
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import (
    f1_score, precision_score, recall_score, hamming_loss, classification_report
)
import joblib

from src.preprocessing import preprocess_feedback


class MultiLabelCategoryClassifier:
    """
    Multi-label classification engine allowing feedback to belong to multiple categories
    simultaneously (e.g. 'Performance' and 'Payment').
    """

    def __init__(self,
                 ngram_range: Tuple[int, int] = (1, 2),
                 threshold: float = 0.35,
                 C: float = 2.0,
                 max_iter: int = 1000,
                 random_state: int = 42):
        self.ngram_range = ngram_range
        self.threshold = threshold
        self.C = C
        self.max_iter = max_iter
        self.random_state = random_state

        self.vectorizer = TfidfVectorizer(
            ngram_range=self.ngram_range,
            sublinear_tf=True,
            min_df=1,
            max_df=0.98,
            preprocessor=preprocess_feedback
        )
        self.classifier = OneVsRestClassifier(
            LogisticRegression(
                C=self.C,
                max_iter=self.max_iter,
                class_weight="balanced",
                random_state=self.random_state,
                solver="lbfgs"
            )
        )
        self.mlb = MultiLabelBinarizer()
        self.classes_: Optional[List[str]] = None
        self.is_fitted: bool = False

    def _parse_labels(self, label_inputs: Union[List[List[str]], List[str]]) -> List[List[str]]:
        """
        Normalizes category labels whether passed as lists of strings or comma-separated strings.
        """
        parsed = []
        for item in label_inputs:
            if isinstance(item, str):
                categories = [cat.strip().lower() for cat in item.split(",") if cat.strip()]
                parsed.append(categories if categories else ["general"])
            elif isinstance(item, (list, tuple, set)):
                categories = [str(cat).strip().lower() for cat in item if str(cat).strip()]
                parsed.append(categories if categories else ["general"])
            else:
                parsed.append(["general"])
        return parsed

    def fit(self, texts: List[str], categories_list: Union[List[List[str]], List[str]]):
        """
        Fits vectorizer, MultiLabelBinarizer, and OneVsRestClassifier.
        """
        parsed_labels = self._parse_labels(categories_list)
        y_binary = self.mlb.fit_transform(parsed_labels)
        self.classes_ = list(self.mlb.classes_)

        x_features = self.vectorizer.fit_transform(texts)
        self.classifier.fit(x_features, y_binary)
        self.is_fitted = True
        return self

    def predict_proba(self, texts: List[str]) -> List[Dict[str, float]]:
        """
        Returns class probabilities for each category for the given texts.
        """
        if not self.is_fitted:
            raise RuntimeError("Model must be trained before predicting.")

        x_features = self.vectorizer.transform(texts)
        # OneVsRestClassifier with LogisticRegression supports predict_proba
        probas = self.classifier.predict_proba(x_features)

        results = []
        for row in probas:
            scores = {
                cat_name: round(float(row[idx]), 4)
                for idx, cat_name in enumerate(self.classes_)
            }
            results.append(scores)
        return results

    def predict_proba_one(self, text: str) -> Dict[str, float]:
        """
        Returns probability dictionary for a single feedback string.
        """
        return self.predict_proba([text])[0]

    def predict(self, texts: List[str], threshold: Optional[float] = None) -> List[List[str]]:
        """
        Predicts binary active categories for each text based on decision threshold.
        If no category surpasses threshold, the single top-scoring category is assigned.
        """
        if not self.is_fitted:
            raise RuntimeError("Model must be trained before predicting.")

        th = threshold if threshold is not None else self.threshold
        all_probas = self.predict_proba(texts)

        all_predictions = []
        for score_dict in all_probas:
            assigned = [cat for cat, score in score_dict.items() if score >= th]
            # Fallback to top category if none exceed threshold
            if not assigned:
                best_cat = max(score_dict.items(), key=lambda item: item[1])[0]
                assigned = [best_cat]
            all_predictions.append(assigned)
        return all_predictions

    def predict_one(self, text: str, threshold: Optional[float] = None) -> List[str]:
        """
        Predicts categories for a single feedback text.
        """
        return self.predict([text], threshold=threshold)[0]

    def evaluate(self, texts: List[str], true_categories: Union[List[List[str]], List[str]]) -> Dict[str, Any]:
        """
        Evaluates multi-label model using Hamming Loss, Micro F1, Macro F1, and per-class reports.
        """
        parsed_true = self._parse_labels(true_categories)
        y_true = self.mlb.transform(parsed_true)

        pred_labels = self.predict(texts)
        y_pred = self.mlb.transform(pred_labels)

        micro_f1 = f1_score(y_true, y_pred, average="micro", zero_division=0)
        macro_f1 = f1_score(y_true, y_pred, average="macro", zero_division=0)
        micro_precision = precision_score(y_true, y_pred, average="micro", zero_division=0)
        micro_recall = recall_score(y_true, y_pred, average="micro", zero_division=0)
        h_loss = hamming_loss(y_true, y_pred)

        report = classification_report(
            y_true, y_pred,
            target_names=self.classes_,
            output_dict=True,
            zero_division=0
        )

        return {
            "micro_f1": round(float(micro_f1), 4),
            "macro_f1": round(float(macro_f1), 4),
            "micro_precision": round(float(micro_precision), 4),
            "micro_recall": round(float(micro_recall), 4),
            "hamming_loss": round(float(h_loss), 4),
            "per_class_report": report,
            "classes": self.classes_
        }

    def get_top_category_keywords(self, n_top: int = 6) -> Dict[str, List[Tuple[str, float]]]:
        """
        Extracts the strongest indicative vocabulary terms per category.
        """
        if not self.is_fitted:
            return {}

        feature_names = np.array(self.vectorizer.get_feature_names_out())
        category_keywords = {}

        for idx, cat_name in enumerate(self.classes_):
            estimator = self.classifier.estimators_[idx]
            coefs = estimator.coef_[0]
            top_indices = np.argsort(coefs)[::-1][:n_top]
            words = [
                (feature_names[i], round(float(coefs[i]), 3))
                for i in top_indices if coefs[i] > 0
            ]
            category_keywords[cat_name] = words

        return category_keywords

    def save(self, filepath: str):
        """
        Saves category classifier to disk.
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(self, filepath)

    @classmethod
    def load(cls, filepath: str) -> "MultiLabelCategoryClassifier":
        """
        Loads saved category classifier.
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found at {filepath}")
        return joblib.load(filepath)
