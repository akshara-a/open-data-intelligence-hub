"""Model construction and inference helpers."""
from pathlib import Path
import joblib
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from .text_utils import clean_text

def build_pipeline() -> Pipeline:
    return Pipeline([
        ("tfidf", TfidfVectorizer(
            preprocessor=clean_text,
            token_pattern=r"(?u)\b\w+\b",
            ngram_range=(1, 2),
            min_df=2,
            max_features=50000,
            sublinear_tf=True,
        )),
        ("classifier", LogisticRegression(
            C=2.0,
            max_iter=1000,
            random_state=42,
        )),
    ])

def save_model(model, path: str | Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)

def load_model(path: str | Path):
    return joblib.load(path)

def predict(model, text: str) -> dict:
    label = model.predict([text])[0]
    result = {"sentiment": str(label)}
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba([text])[0]
        classes = model.classes_
        result["confidence"] = float(probs.max())
        result["probabilities"] = {
            str(c): float(p) for c, p in zip(classes, probs)
        }
    return result
