import os
import sys
import joblib
import streamlit as st

from sklearn.feature_extraction.text import TfidfVectorizer

sys.path.append(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "src"
    )
)

from preprocessing import clean_text


MODEL_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "models"
)


@st.cache_resource
def load_models():
    sentiment_model = joblib.load(
        os.path.join(MODEL_PATH, "sentiment_model.pkl")
    )

    category_model = joblib.load(
        os.path.join(MODEL_PATH, "category_model.pkl")
    )

    return sentiment_model, category_model


def extract_keywords(text, top_n=5):
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    tfidf_matrix = vectorizer.fit_transform([text])

    feature_names = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.toarray()[0]

    keyword_scores = list(
        zip(feature_names, scores)
    )

    keyword_scores.sort(
        key=lambda item: item[1],
        reverse=True
    )

    return [
        word for word, score in keyword_scores[:top_n]
    ]


st.set_page_config(
    page_title="Customer Feedback NLP",
    page_icon="💬",
    layout="centered"
)

st.title("💬 Customer Feedback Analysis System")
st.write(
    "Enter customer feedback to analyze sentiment, "
    "category, and important keywords."
)

feedback = st.text_area(
    "Enter customer feedback:",
    placeholder=(
        "Example: The payment failed and the app is very slow"
    )
)

if st.button("Analyze Feedback"):

    if not feedback.strip():
        st.warning("Please enter some feedback.")

    else:
        sentiment_model, category_model = load_models()

        cleaned_feedback = clean_text(feedback)

        sentiment = sentiment_model.predict(
            [cleaned_feedback]
        )[0]

        category = category_model.predict(
            [cleaned_feedback]
        )[0]

        keywords = extract_keywords(cleaned_feedback)

        st.subheader("Analysis Results")

        st.write("**Cleaned Text:**", cleaned_feedback)
        st.write("**Sentiment:**", sentiment)
        st.write("**Category:**", category)

        st.write("**Important Keywords:**")
        st.write(", ".join(keywords))