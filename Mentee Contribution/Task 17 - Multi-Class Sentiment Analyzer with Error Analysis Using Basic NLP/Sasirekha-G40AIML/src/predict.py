"""Command-line prediction utility."""
import argparse
from pathlib import Path
from .model import load_model, predict

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser(description="Predict tweet sentiment.")
    parser.add_argument("text", help="Text to classify.")
    args = parser.parse_args()
    model = load_model(ROOT / "models" / "sentiment_pipeline.joblib")
    print(predict(model, args.text))

if __name__ == "__main__":
    main()
