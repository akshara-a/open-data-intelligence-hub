import json
from pathlib import Path
import pandas as pd
import streamlit as st

from src.model import load_model, predict

ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "models" / "sentiment_pipeline.joblib"
METRICS_PATH = ROOT / "reports" / "metrics.json"
ERRORS_PATH = ROOT / "reports" / "error_analysis.csv"

st.set_page_config(
    page_title="Sentiment Intelligence",
    page_icon="💬",
    layout="wide",
)

@st.cache_resource
def get_model():
    return load_model(MODEL_PATH)

@st.cache_data
def get_metrics():
    return json.loads(METRICS_PATH.read_text(encoding="utf-8"))

st.title("💬 Sentiment Intelligence")
st.caption("Production-style multi-class sentiment analysis using TF-IDF + Logistic Regression")

metrics = get_metrics()
m1, m2, m3, m4 = st.columns(4)
m1.metric("Test Accuracy", f"{metrics['accuracy']:.1%}")
m2.metric("Macro F1", f"{metrics['macro_f1']:.3f}")
m3.metric("Test Samples", f"{metrics['test_rows']:,}")
m4.metric("Classes", len(metrics["classes"]))

st.divider()

tab1, tab2, tab3 = st.tabs(["🔮 Predict", "📊 Model Evaluation", "🔎 Error Analysis"])

with tab1:
    st.subheader("Analyze a message")
    text = st.text_area(
        "Enter a tweet, review, or short message",
        placeholder="Example: I absolutely loved this movie!",
        height=140,
    )
    if st.button("Analyze Sentiment", type="primary", use_container_width=True):
        if not text.strip():
            st.warning("Please enter some text first.")
        else:
            result = predict(get_model(), text)
            sentiment = result["sentiment"]
            st.success(f"Predicted sentiment: **{sentiment.upper()}**")
            if "confidence" in result:
                st.progress(result["confidence"], text=f"Model confidence: {result['confidence']:.1%}")
                st.json(result["probabilities"])

with tab2:
    st.subheader("Evaluation snapshot")
    report = metrics["classification_report"]
    table = pd.DataFrame(report).T
    st.dataframe(table.round(3), use_container_width=True)

    figure = ROOT / "reports" / "figures" / "confusion_matrix.png"
    if figure.exists():
        st.image(str(figure), caption="Confusion matrix")

    distribution = ROOT / "reports" / "figures" / "sentiment_distribution.png"
    if distribution.exists():
        st.image(str(distribution), caption="Training dataset class distribution")

with tab3:
    st.subheader("Incorrect predictions")
    st.write(
        "The table below is generated from the held-out test set. "
        "Use it to inspect common model failure patterns such as negation, "
        "mixed sentiment, sarcasm, and context-dependent language."
    )
    if ERRORS_PATH.exists():
        errors = pd.read_csv(ERRORS_PATH)
        st.metric("Incorrect test predictions", f"{len(errors):,}")
        st.dataframe(errors.head(100), use_container_width=True)
    else:
        st.info("Run the training script to generate error analysis.")

st.sidebar.header("About")
st.sidebar.write(
    "Dataset: supplied Tweets.csv\n\n"
    "Pipeline: text cleaning → TF-IDF (1–2 grams) → Logistic Regression\n\n"
    "Classes: positive, neutral, negative"
)
