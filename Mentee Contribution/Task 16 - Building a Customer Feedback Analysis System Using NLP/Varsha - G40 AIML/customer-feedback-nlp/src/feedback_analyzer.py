import joblib
import re
from sklearn.feature_extraction.text import TfidfVectorizer


# ============================================================
# 1. LOAD TRAINED MODEL
# ============================================================

model = joblib.load(
    "models/sentiment_model.pkl"
)

vectorizer = joblib.load(
    "models/tfidf_vectorizer.pkl"
)


# ============================================================
# 2. CATEGORY KEYWORDS
# ============================================================

CATEGORY_KEYWORDS = {

    "payment": [
        "payment",
        "pay",
        "paid",
        "card",
        "transaction",
        "upi",
        "billing",
        "charge"
    ],

    "delivery": [
        "delivery",
        "delivered",
        "shipping",
        "shipment",
        "courier",
        "late",
        "delay",
        "arrived"
    ],

    "quality": [
        "quality",
        "poor quality",
        "bad quality",
        "damaged",
        "broken",
        "defective"
    ],

    "performance": [
        "slow",
        "speed",
        "performance",
        "lag",
        "loading",
        "freeze",
        "freezing",
        "crash",
        "crashing"
    ],

    "support": [
        "support",
        "customer service",
        "agent",
        "help",
        "response",
        "respond",
        "contact"
    ],

    "login": [
        "login",
        "log in",
        "sign in",
        "signin",
        "password",
        "otp",
        "verification",
        "account"
    ],

    "refund": [
        "refund",
        "money back",
        "return",
        "returned",
        "reimbursement"
    ],

    "feature_request": [
        "add",
        "feature",
        "option",
        "please provide",
        "would like",
        "need a feature",
        "dark mode"
    ]
}


# ============================================================
# 3. TEXT CLEANING
# ============================================================

def clean_text(text):

    text = str(text)

    text = text.lower()

    text = re.sub(
        r"http\S+|www\S+|https\S+",
        "",
        text
    )

    text = re.sub(
        r"[^a-zA-Z\s]",
        "",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    return text


# ============================================================
# 4. SENTIMENT OVERRIDE RULES
# ============================================================

STRONG_NEGATIVE_PHRASES = [

    "payment failed",
    "payment is failing",
    "money was deducted",
    "money deducted",
    "transaction failed",
    "card payment failed",

    "want a refund",
    "need a refund",
    "request a refund",
    "refund my money",

    "very disappointed",
    "extremely disappointed",
    "terrible",
    "very poor",
    "poor quality",

    "not working",
    "stopped working",
    "keeps crashing",
    "keeps freezing",

    "cannot login",
    "cannot log in",
    "otp is not arriving",
    "otp not arriving",

    "did not respond",
    "didn't respond",

    "very slow",
    "extremely slow",
    "very late"
]


STRONG_POSITIVE_PHRASES = [

    "very happy",
    "extremely happy",
    "absolutely love",
    "really love",
    "love this product",

    "excellent",
    "amazing",
    "highly recommend",

    "very satisfied",
    "extremely satisfied",
    "satisfied with my purchase",

    "great product",
    "great experience",
    "excellent product",

    "fast delivery",
    "great quality"
]


def apply_sentiment_rules(
    text,
    ml_sentiment
):

    text = clean_text(text)

    # Check strong negative phrases first
    for phrase in STRONG_NEGATIVE_PHRASES:

        if phrase in text:

            return "negative"


    # Check strong positive phrases
    for phrase in STRONG_POSITIVE_PHRASES:

        if phrase in text:

            return "positive"


    # Otherwise use ML model prediction
    return ml_sentiment


# ============================================================
# 5. CATEGORY DETECTION
# ============================================================

def detect_categories(text):

    text = clean_text(text)

    categories = []

    for category, keywords in CATEGORY_KEYWORDS.items():

        for keyword in keywords:

            pattern = (
                r"\b" +
                re.escape(keyword) +
                r"\b"
            )

            if re.search(
                pattern,
                text
            ):

                categories.append(
                    category
                )

                break


    if not categories:

        categories.append(
            "general"
        )


    return categories


# ============================================================
# 6. KEYWORD EXTRACTION
# ============================================================

CUSTOM_STOP_WORDS = {

    "very",
    "really",
    "just",
    "did",
    "does",
    "doesnt",
    "dont",
    "the",
    "and",
    "is",
    "was",
    "are",
    "am",
    "to",
    "of",
    "a",
    "an",
    "for",
    "with",
    "this",
    "that",
    "it",
    "my",
    "i",
    "we",
    "they",
    "you",
    "has",
    "have",
    "had",
    "been",
    "be",
    "in",
    "on",
    "at",
    "but",
    "so",
    "not",
    "after",
    "few",
    "new",
    "keeps"
}


def extract_keywords(
    text,
    top_n=5
):

    cleaned = clean_text(
        text
    )

    if not cleaned:

        return []


    keyword_vectorizer = TfidfVectorizer(

        stop_words=list(
            CUSTOM_STOP_WORDS
        ),

        ngram_range=(1, 2),

        token_pattern=(
            r"(?u)\b[a-zA-Z]{3,}\b"
        )
    )


    try:

        matrix = (
            keyword_vectorizer
            .fit_transform(
                [cleaned]
            )
        )

    except ValueError:

        return cleaned.split()[
            :top_n
        ]


    feature_names = (
        keyword_vectorizer
        .get_feature_names_out()
    )

    scores = matrix.toarray()[0]

    ranked_indices = (
        scores.argsort()[::-1]
    )

    keywords = []


    for index in ranked_indices:

        keyword = feature_names[index]

        words = keyword.split()


        if any(
            word in CUSTOM_STOP_WORDS
            for word in words
        ):

            continue


        if keyword not in keywords:

            keywords.append(
                keyword
            )


        if len(keywords) >= top_n:

            break


    return keywords


# ============================================================
# 7. GENERATE OVERALL MEANING
# ============================================================

def generate_meaning(
    sentiment,
    categories
):

    if sentiment == "positive":

        if categories == ["general"]:

            return (
                "The customer has a generally "
                "positive experience."
            )

        return (
            "The customer has a positive "
            "experience related to "
            + ", ".join(categories)
            + "."
        )


    elif sentiment == "negative":

        if categories == ["general"]:

            return (
                "The customer is dissatisfied "
                "with the experience."
            )

        return (
            "The customer is dissatisfied and "
            "is experiencing an issue related "
            "to "
            + ", ".join(categories)
            + "."
        )


    else:

        if categories == ["general"]:

            return (
                "The customer has a neutral "
                "experience."
            )

        return (
            "The customer has a neutral "
            "experience related to "
            + ", ".join(categories)
            + "."
        )


# ============================================================
# 8. COMPLETE ANALYSIS
# ============================================================

def analyze_feedback(
    feedback
):

    cleaned = clean_text(
        feedback
    )


    # ML prediction
    text_tfidf = vectorizer.transform(
        [cleaned]
    )

    ml_sentiment = model.predict(
        text_tfidf
    )[0]


    probabilities = (
        model.predict_proba(
            text_tfidf
        )
    )

    ml_confidence = (
        probabilities.max()
    )


    # Apply strong phrase rules
    sentiment = apply_sentiment_rules(
        feedback,
        ml_sentiment
    )


    # Categories
    categories = detect_categories(
        feedback
    )


    # Keywords
    keywords = extract_keywords(
        feedback,
        top_n=5
    )


    # Meaning
    meaning = generate_meaning(
        sentiment,
        categories
    )


    return {

        "sentiment": sentiment,

        "confidence": ml_confidence,

        "categories": categories,

        "keywords": keywords,

        "meaning": meaning
    }


# ============================================================
# 9. FINAL TESTING
# ============================================================

if __name__ == "__main__":

    test_feedback = [

        "Payment failed and my money was deducted",

        "The delivery was very late",

        "The product quality is very poor",

        "The application is very slow and keeps freezing",

        "Customer support did not respond to my complaint",

        "I cannot login because the OTP is not arriving",

        "I want a refund for this product",

        "Please add dark mode to the application",

        "I am extremely happy with my purchase",

        "The product is okay, nothing special",

        "I am very happy with the product",

        "I absolutely love this product",

        "This product is excellent",

        "The application keeps crashing"
    ]


    print("=" * 70)

    print(
        "FINAL CUSTOMER FEEDBACK ANALYSIS SYSTEM"
    )

    print("=" * 70)


    for feedback in test_feedback:

        result = analyze_feedback(
            feedback
        )


        print("\nFeedback:")
        print(feedback)


        print("\nSentiment:")
        print(
            result["sentiment"]
        )


        print("\nConfidence:")
        print(
            f"{result['confidence']:.2%}"
        )


        print("\nComplaint Categories:")
        print(
            ", ".join(
                result["categories"]
            )
        )


        print("\nImportant Keywords:")
        print(
            ", ".join(
                result["keywords"]
            )
        )


        print("\nOverall Meaning:")
        print(
            result["meaning"]
        )


        print(
            "\n" + "-" * 70
        )


    print("\n")

    print("=" * 70)

    print(
        "FINAL ANALYSIS COMPLETED SUCCESSFULLY"
    )

    print("=" * 70)