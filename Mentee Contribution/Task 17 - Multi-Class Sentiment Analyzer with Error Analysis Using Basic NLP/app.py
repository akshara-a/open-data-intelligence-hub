import os
import re
import joblib
import streamlit as st


# -----------------------------
# Project paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "sentiment_model.pkl",
)

VECTORIZER_PATH = os.path.join(
    BASE_DIR,
    "models",
    "tfidf_vectorizer.pkl",
)


# -----------------------------
# Text cleaning function
# -----------------------------
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# -----------------------------
# Load model and vectorizer
# -----------------------------
@st.cache_resource
def load_model():
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    return model, vectorizer


model, vectorizer = load_model()


# -----------------------------
# Streamlit page
# -----------------------------
st.set_page_config(
    page_title="Multi-Class Sentiment Analyzer",
    page_icon="💬",
    layout="centered",
)

st.title("💬 Multi-Class Sentiment Analyzer")
st.write(
    "Enter a sentence to predict whether its sentiment is "
    "positive, neutral, or negative."
)

user_text = st.text_area(
    "Enter your text:",
    placeholder="Example: I really enjoyed this service",
)

if st.button("Analyze Sentiment"):
    if user_text.strip():
        cleaned_text = clean_text(user_text)
        features = vectorizer.transform([cleaned_text])
        prediction = model.predict(features)[0]

        st.subheader("Prediction")

        if prediction == "positive":
            st.success("Positive Sentiment 😊")
        elif prediction == "negative":
            st.error("Negative Sentiment 😞")
        else:
            st.info("Neutral Sentiment 😐")
    else:
        st.warning("Please enter some text.")