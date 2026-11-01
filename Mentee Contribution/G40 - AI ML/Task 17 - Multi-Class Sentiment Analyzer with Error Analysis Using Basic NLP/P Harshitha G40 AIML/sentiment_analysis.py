import pandas as pd
# pyrefly: ignore [missing-import]
import numpy as np
import re
import os
# pyrefly: ignore [missing-import]
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay


# -----------------------------------
# 1. Load Dataset
# -----------------------------------

df = pd.read_csv("sentiment_data.csv")


# -----------------------------------
# 2. Check Dataset
# -----------------------------------

print(df.head())

print(df.shape)

print(df.isnull().sum())

print(df["sentiment"].value_counts())


# -----------------------------------
# 3. Remove Missing Values
# -----------------------------------

df = df.dropna()


# -----------------------------------
# 4. Text Cleaning
# -----------------------------------

def clean_text(text):

    text = text.lower()

    text = re.sub(r"http\S+", "", text)

    text = re.sub(r"[^a-z\s]", "", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


df["clean_text"] = df["text"].apply(clean_text)


# -----------------------------------
# 5. Input and Target
# -----------------------------------

X = df["clean_text"]

y = df["sentiment"]


# -----------------------------------
# 6. Train-Test Split
# -----------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# -----------------------------------
# 7. TF-IDF
# -----------------------------------

tfidf = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2)
)

X_train_tfidf = tfidf.fit_transform(X_train)

X_test_tfidf = tfidf.transform(X_test)


# -----------------------------------
# 8. Model Training
# -----------------------------------

model = LogisticRegression(
    max_iter=1000
)

model.fit(
    X_train_tfidf,
    y_train
)


# -----------------------------------
# 9. Prediction
# -----------------------------------

y_pred = model.predict(
    X_test_tfidf
)


# -----------------------------------
# 10. Accuracy
# -----------------------------------

accuracy = accuracy_score(
    y_test,
    y_pred
)

print(
    "Accuracy:",
    accuracy
)


# -----------------------------------
# 11. Classification Report
# -----------------------------------

os.makedirs("results", exist_ok=True)

report = classification_report(
    y_test,
    y_pred
)
print(report)

with open("results/classification_report.txt", "w") as f:
    f.write(report)


# -----------------------------------
# 12. Confusion Matrix
# -----------------------------------

cm = confusion_matrix(
    y_test,
    y_pred
)

display = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=model.classes_
)

display.plot()

plt.title(
    "Confusion Matrix"
)

plt.savefig("results/confusion_matrix.png")
plt.show()


# -----------------------------------
# 13. Error Analysis
# -----------------------------------

results = pd.DataFrame({
    "text": X_test.values,
    "actual": y_test.values,
    "predicted": y_pred
})

errors = results[
    results["actual"]
    != results["predicted"]
]

errors.to_csv("results/error_analysis.csv", index=False)

print("\nIncorrect Predictions:")

print(
    errors.head(20)
)


# -----------------------------------
# 14. Error Counts
# -----------------------------------

print(
    errors.groupby(
        ["actual", "predicted"]
    ).size()
)


# -----------------------------------
# 15. Prediction Function
# -----------------------------------

def predict_sentiment(sentence):

    sentence = clean_text(sentence)

    sentence_tfidf = tfidf.transform(
        [sentence]
    )

    prediction = model.predict(
        sentence_tfidf
    )

    return prediction[0]


# -----------------------------------
# 16. Test New Sentences
# -----------------------------------

print(
    predict_sentiment(
        "I really loved this movie"
    )
)

print(
    predict_sentiment(
        "The movie was okay"
    )
)

print(
    predict_sentiment(
        "This was a terrible movie"
    )
)