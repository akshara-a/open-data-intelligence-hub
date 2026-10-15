"""Main application for customer feedback analysis."""

from __future__ import annotations

from pathlib import Path

from src.category_model import predict_categories, train_category_model
from src.keyword_extractor import extract_keywords
from src.sentiment_model import predict_sentiment, train_sentiment_model

ROOT_DIR = Path(__file__).resolve().parent
MODELS_DIR = ROOT_DIR / "models"


def ensure_models_exist() -> None:
    """Train and save models if they are missing."""
    sentiment_path = MODELS_DIR / "sentiment_model.pkl"
    category_path = MODELS_DIR / "category_model.pkl"
    mlb_path = MODELS_DIR / "multilabel_binarizer.pkl"

    if not sentiment_path.exists() or not category_path.exists() or not mlb_path.exists():
        print("Training models for the first time...\n")
        train_sentiment_model()
        train_category_model()


def analyze_feedback(feedback: str) -> dict:
    """Return the sentiment, categories, and extracted keywords for one feedback string."""
    sentiment = predict_sentiment(feedback)
    categories = predict_categories(feedback, threshold=0.4)
    keywords = extract_keywords(feedback, top_n=5)

    return {
        "sentiment": sentiment.title(),
        "categories": [category.title().replace("_", " ") for category in categories],
        "keywords": keywords,
    }


def display_analysis(feedback: str) -> None:
    """Get sentiment, categories, and keywords and print a clean output."""
    result = analyze_feedback(feedback)

    print("\n====================================")
    print("CUSTOMER FEEDBACK ANALYSIS")
    print("====================================")
    print(f"\nFeedback:\n{feedback}\n")
    print(f"Sentiment:\n{result['sentiment']}\n")
    print("Categories:")
    if result["categories"]:
        for category in result["categories"]:
            print(f"- {category}")
    else:
        print("- None detected")

    print("\nImportant Keywords:")
    if result["keywords"]:
        for keyword in result["keywords"]:
            print(f"- {keyword}")
    else:
        print("- No keywords extracted")

    print("\n====================================\n")


def main() -> None:
    """Run the interactive customer feedback analysis app."""
    ensure_models_exist()

    print("Welcome to the Customer Feedback Analysis System")
    print("Type 'exit' at any time to quit.\n")

    while True:
        user_input = input("Enter customer feedback:\n")

        if user_input.strip().lower() in {"", "exit", "quit"}:
            print("Goodbye!")
            break

        try:
            display_analysis(user_input)
        except Exception as exc:
            print(f"An error occurred while analyzing feedback: {exc}")


if __name__ == "__main__":
    main()
