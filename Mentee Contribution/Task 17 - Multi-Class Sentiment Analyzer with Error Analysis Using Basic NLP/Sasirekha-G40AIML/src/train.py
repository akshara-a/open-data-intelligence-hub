"""Train the production sentiment pipeline from the supplied Tweets.csv dataset."""
from pathlib import Path
import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from .model import build_pipeline, save_model

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw" / "Tweets.csv"
MODEL = ROOT / "models" / "sentiment_pipeline.joblib"
REPORT = ROOT / "reports" / "metrics.json"
ERRORS = ROOT / "reports" / "error_analysis.csv"

def main():
    df = pd.read_csv(DATA)
    required = {"text", "sentiment"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df = df.dropna(subset=["text", "sentiment"]).copy()
    df["text"] = df["text"].astype(str)
    df["sentiment"] = df["sentiment"].astype(str).str.lower().str.strip()

    X_train, X_test, y_train, y_test = train_test_split(
        df["text"], df["sentiment"],
        test_size=0.20, random_state=42, stratify=df["sentiment"]
    )

    model = build_pipeline()
    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    report = classification_report(y_test, pred, output_dict=True)
    cm = confusion_matrix(y_test, pred, labels=model.classes_)

    results = pd.DataFrame({
        "text": X_test.values,
        "actual": y_test.values,
        "predicted": pred,
    })
    errors = results[results["actual"] != results["predicted"]].copy()
    errors["error_type"] = errors.apply(
        lambda r: f"{r['actual']} -> {r['predicted']}", axis=1
    )
    ERRORS.parent.mkdir(parents=True, exist_ok=True)
    errors.to_csv(ERRORS, index=False)

    metrics = {
        "dataset_rows_after_cleaning": int(len(df)),
        "train_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
        "classes": list(model.classes_),
        "accuracy": float(accuracy_score(y_test, pred)),
        "macro_f1": float(report["macro avg"]["f1-score"]),
        "weighted_f1": float(report["weighted avg"]["f1-score"]),
        "classification_report": report,
        "confusion_matrix": cm.tolist(),
    }
    REPORT.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    save_model(model, MODEL)

    print(f"Saved model: {MODEL}")
    print(f"Accuracy: {metrics['accuracy']:.4f}")
    print(f"Macro F1: {metrics['macro_f1']:.4f}")
    print(f"Errors: {len(errors)}")

if __name__ == "__main__":
    main()
