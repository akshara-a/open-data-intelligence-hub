import os
import sys
import joblib

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from preprocessing import clean_text


MODEL_PATH = "models"


def load_models():
    sentiment_model = joblib.load(
        os.path.join(MODEL_PATH, "sentiment_model.pkl")
    )

    category_model = joblib.load(
        os.path.join(MODEL_PATH, "category_model.pkl")
    )

    return sentiment_model, category_model


def predict_feedback(feedback):
    sentiment_model, category_model = load_models()

    cleaned_feedback = clean_text(feedback)

    sentiment = sentiment_model.predict(
        [cleaned_feedback]
    )[0]

    category = category_model.predict(
        [cleaned_feedback]
    )[0]

    return {
        "feedback": feedback,
        "cleaned_text": cleaned_feedback,
        "sentiment": sentiment,
        "category": category
    }


if __name__ == "__main__":
    sample_feedback = (
        "The application is very slow and payment failed"
    )

    result = predict_feedback(sample_feedback)

    print("\nCustomer Feedback Analysis")
    print("-------------------------")

    for key, value in result.items():
        print(f"{key}: {value}")