import pandas as pd
import re


# ============================================================
# COMPLAINT CATEGORY KEYWORDS
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
        "freezing"
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
    ],

    "product": [
        "product",
        "item",
        "device",
        "purchase"
    ]
}


# ============================================================
# CATEGORY DETECTION FUNCTION
# ============================================================

def detect_categories(text):

    text = str(text).lower()

    detected_categories = []

    for category, keywords in CATEGORY_KEYWORDS.items():

        for keyword in keywords:

            # Check keyword as a word/phrase
            if re.search(r"\b" + re.escape(keyword) + r"\b", text):

                detected_categories.append(category)

                # Stop checking more keywords for this category
                break

    # If no category is detected
    if not detected_categories:
        detected_categories.append("general")

    return detected_categories


# ============================================================
# LOAD PROCESSED DATASET
# ============================================================

df = pd.read_csv("data/processed_feedback.csv")

print("=" * 60)
print("COMPLAINT CATEGORY DETECTION")
print("=" * 60)


# ============================================================
# CREATE CATEGORY COLUMN
# ============================================================

df["categories"] = df["cleaned_text"].apply(detect_categories)

# Convert list to readable text
df["category"] = df["categories"].apply(
    lambda x: ", ".join(x)
)


# ============================================================
# DISPLAY EXAMPLES
# ============================================================

print("\nCategory Examples:\n")

print(
    df[
        ["review_text", "sentiment", "category"]
    ].head(20).to_string(index=False)
)


# ============================================================
# CATEGORY COUNTS
# ============================================================

print("\nCategory Counts:")

category_counts = {}

for categories in df["categories"]:

    for category in categories:

        if category not in category_counts:
            category_counts[category] = 0

        category_counts[category] += 1


for category, count in sorted(
    category_counts.items(),
    key=lambda x: x[1],
    reverse=True
):

    print(f"{category}: {count}")


# ============================================================
# SAVE DATASET
# ============================================================

df.to_csv(
    "data/feedback_with_categories.csv",
    index=False
)


print("\n" + "=" * 60)
print("CATEGORY DETECTION COMPLETED")
print("=" * 60)

print("\nSaved file:")
print("data/feedback_with_categories.csv")