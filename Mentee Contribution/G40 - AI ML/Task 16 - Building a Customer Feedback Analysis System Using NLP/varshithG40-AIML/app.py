"""
Streamlit Web Application: Customer Feedback Analysis System Using NLP
Features:
- Live Interactive Feedback Analyzer (Sentiment, Multi-labels, Keywords, Similar Feedback)
- Step-by-Step NLP Inspector (Preprocessing, Tokenization, Lemmatization, TF-IDF vectors)
- Batch Feedback Analyzer with Visual Analytics & CSV Export
- Classical NLP vs Modern Transformer (DistilBERT) Comparison
- Model Evaluation & Performance Dashboard
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

from src.pipeline import CustomerFeedbackAnalyzer
from src.preprocessing import (
    clean_text, tokenize, remove_stopwords, stem_words, lemmatize_words, compare_stem_vs_lemma
)
from src.transformer_model import compare_tfidf_vs_transformer, TransformerSentimentAnalyzer

# Page configuration
st.set_page_config(
    page_title="Customer Feedback NLP Studio",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for rich modern aesthetics
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .main-header {
        background: linear-gradient(135deg, #1E1B4B 0%, #312E81 50%, #4338CA 100%);
        padding: 2.2rem 2rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(49, 46, 129, 0.3);
    }

    .main-header h1 {
        margin: 0;
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.02em;
    }

    .main-header p {
        margin: 0.6rem 0 0 0;
        opacity: 0.85;
        font-size: 1.05rem;
    }

    .stat-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(8px);
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 0.5rem;
        margin-top: 0.8rem;
    }

    .sentiment-positive {
        background: linear-gradient(135deg, #059669 0%, #10B981 100%);
        color: white;
        padding: 0.8rem 1.4rem;
        border-radius: 12px;
        text-align: center;
        font-weight: 700;
        font-size: 1.3rem;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25);
    }

    .sentiment-negative {
        background: linear-gradient(135deg, #DC2626 0%, #EF4444 100%);
        color: white;
        padding: 0.8rem 1.4rem;
        border-radius: 12px;
        text-align: center;
        font-weight: 700;
        font-size: 1.3rem;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.25);
    }

    .sentiment-neutral {
        background: linear-gradient(135deg, #475569 0%, #64748B 100%);
        color: white;
        padding: 0.8rem 1.4rem;
        border-radius: 12px;
        text-align: center;
        font-weight: 700;
        font-size: 1.3rem;
        box-shadow: 0 4px 12px rgba(100, 116, 139, 0.25);
    }

    .category-chip {
        display: inline-block;
        background: #EEF2FF;
        color: #4338CA;
        border: 1px solid #C7D2FE;
        padding: 0.35rem 0.9rem;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.9rem;
        margin: 0.25rem;
    }

    .keyword-chip {
        display: inline-block;
        background: #FEF3C7;
        color: #B45309;
        border: 1px solid #FDE68A;
        padding: 0.35rem 0.85rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.88rem;
        margin: 0.25rem;
    }

    .card-box {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 1.4rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03);
    }

    .similar-item {
        background: #F8FAFC;
        border-left: 4px solid #4F46E5;
        padding: 0.85rem 1.1rem;
        border-radius: 0 10px 10px 0;
        margin-bottom: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_analyzer():
    analyzer = CustomerFeedbackAnalyzer(
        models_dir="models",
        data_path="data/feedback.csv"
    )
    analyzer.load_or_train()
    return analyzer


analyzer = get_analyzer()

# Header Banner
st.markdown("""
<div class="main-header">
    <h1>💬 Customer Feedback Analysis System</h1>
    <p>Comprehensive Natural Language Processing Studio &bull; Classical TF-IDF &bull; Multi-Label Classification &bull; Semantic Similarity &bull; Transformers</p>
    <div>
        <span class="stat-badge">📊 80+ Feedback Samples</span>
        <span class="stat-badge">🎯 8 Category Classes</span>
        <span class="stat-badge">⚡ TF-IDF & N-Grams</span>
        <span class="stat-badge">🤖 DistilBERT Comparison</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Main Navigation Tabs
tab_live, tab_nlp, tab_batch, tab_compare, tab_eval = st.tabs([
    "🔍 Live Feedback Analyzer",
    "🔬 Step-by-Step NLP Inspector",
    "📊 Batch Feedback Analytics",
    "🤖 Classical NLP vs Transformer",
    "📈 Model Evaluation & Performance"
])

# -------------------------------------------------------------
# TAB 1: LIVE FEEDBACK ANALYZER
# -------------------------------------------------------------
with tab_live:
    st.subheader("Interactive Customer Feedback Analyzer")
    st.caption("Type custom feedback or select one of the classic scenarios below to analyze in real-time.")

    # Preset feedback buttons
    preset_cols = st.columns(5)
    default_text = "The application is very slow and payment keeps failing."

    if "feedback_input" not in st.session_state:
        st.session_state.feedback_input = default_text

    if preset_cols[0].button("⚡ App Slow & Payment Fails"):
        st.session_state.feedback_input = "The application is very slow and payment keeps failing."
    if preset_cols[1].button("🎧 Helpful Support Team"):
        st.session_state.feedback_input = "The support team solved my issue very quickly and followed up by email."
    if preset_cols[2].button("🔐 Login OTP Delay"):
        st.session_state.feedback_input = "Login OTP is not arriving on my registered mobile number."
    if preset_cols[3].button("🌙 Request Dark Mode"):
        st.session_state.feedback_input = "Can you please add dark mode support in the app settings?"
    if preset_cols[4].button("⚠️ Update Crashes & Buggy"):
        st.session_state.feedback_input = "The latest update is terrible, crashes often and looks confusing."

    user_feedback = st.text_area(
        "Enter Customer Feedback Text:",
        value=st.session_state.feedback_input,
        height=95,
        placeholder="e.g., Payment failed twice and money was deducted..."
    )

    if user_feedback.strip():
        result = analyzer.analyze(user_feedback.strip())

        col1, col2, col3 = st.columns([1, 1.2, 1.4])

        # Column 1: Sentiment
        with col1:
            st.markdown("#### Customer Sentiment")
            sent = result["sentiment"].lower()
            conf = result["sentiment_confidence"]

            if sent == "positive":
                st.markdown(f'<div class="sentiment-positive">😊 POSITIVE<br><span style="font-size:0.9rem; font-weight:normal;">{conf*100:.1f}% confidence</span></div>', unsafe_allow_html=True)
            elif sent == "negative":
                st.markdown(f'<div class="sentiment-negative">😡 NEGATIVE<br><span style="font-size:0.9rem; font-weight:normal;">{conf*100:.1f}% confidence</span></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="sentiment-neutral">😐 NEUTRAL<br><span style="font-size:0.9rem; font-weight:normal;">{conf*100:.1f}% confidence</span></div>', unsafe_allow_html=True)

            st.write("")
            # Probability breakdown bar chart
            prob_df = pd.DataFrame(list(result["sentiment_scores"].items()), columns=["Sentiment", "Probability"])
            fig_prob = px.bar(
                prob_df, x="Probability", y="Sentiment",
                orientation="h",
                color="Sentiment",
                color_discrete_map={"positive": "#10B981", "negative": "#EF4444", "neutral": "#64748B"},
                range_x=[0, 1]
            )
            fig_prob.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=180, showlegend=False)
            st.plotly_chart(fig_prob, use_container_width=True)

        # Column 2: Categories (Multi-Label)
        with col2:
            st.markdown("#### Detected Categories (Multi-Label)")
            if result["categories"]:
                chips_html = "".join([f'<span class="category-chip">🏷️ {cat.capitalize()}</span>' for cat in result["categories"]])
                st.markdown(chips_html, unsafe_allow_html=True)
            else:
                st.info("No specific category surpassed the 35% threshold.")

            st.write("")
            st.markdown("**Category Confidence Scores:**")
            cat_df = pd.DataFrame(
                list(result["category_scores"].items()),
                columns=["Category", "Score"]
            ).sort_values("Score", ascending=True)

            fig_cat = px.bar(
                cat_df, x="Score", y="Category",
                orientation="h",
                color="Score",
                color_continuous_scale="Blues",
                range_x=[0, 1]
            )
            fig_cat.add_vline(x=0.35, line_dash="dash", line_color="#EF4444", annotation_text="Threshold (35%)")
            fig_cat.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=220, coloraxis_showscale=False)
            st.plotly_chart(fig_cat, use_container_width=True)

        # Column 3: Keywords & Similar Complaints
        with col3:
            st.markdown("#### Extracted Keywords & Keyphrases")
            if result["keywords"]:
                kw_html = "".join([f'<span class="keyword-chip">🔑 {kw}</span>' for kw in result["keywords"]])
                st.markdown(kw_html, unsafe_allow_html=True)
            else:
                st.caption("No salient keywords extracted.")

            st.write("")
            st.markdown("#### Semantically Similar Historical Feedback")
            if result["similar_feedback"]:
                for item in result["similar_feedback"]:
                    st.markdown(f"""
                    <div class="similar-item">
                        <div style="display:flex; justify-content:space-between; margin-bottom: 4px;">
                            <strong>Similarity: {item['similarity_percentage']}</strong>
                            <span style="font-size:0.82rem; color:#475569;">Sentiment: {item['sentiment']} | {item['categories']}</span>
                        </div>
                        <div style="font-style:italic; color:#1E293B;">"{item['feedback']}"</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.caption("No historical feedback matched above similarity cutoff.")


# -------------------------------------------------------------
# TAB 2: STEP-BY-STEP NLP INSPECTOR
# -------------------------------------------------------------
with tab_nlp:
    st.subheader("Step-by-Step NLP Pipeline Inspection")
    st.write("Understand exactly how raw human language is converted into numerical representations and classification decisions.")

    inspect_text = st.text_input(
        "Enter text to inspect preprocessing stages:",
        value="The APP is soooo slow!!!!! And payment is not working 😡"
    )

    clean_res = clean_text(inspect_text)
    raw_tokens = tokenize(inspect_text)
    filtered_tokens_all = remove_stopwords(raw_tokens, preserve_negations=False)
    filtered_tokens_neg = remove_stopwords(raw_tokens, preserve_negations=True)
    lemmas = lemmatize_words(filtered_tokens_neg)
    stems = stem_words(filtered_tokens_neg)

    stage_cols = st.columns(4)
    with stage_cols[0]:
        st.markdown("**1. Raw Input**")
        st.code(inspect_text, language="text")
    with stage_cols[1]:
        st.markdown("**2. Text Cleaning**")
        st.caption("Lowercase, normalize URLs/emails/repeated characters.")
        st.code(clean_res, language="text")
    with stage_cols[2]:
        st.markdown("**3. Tokenization**")
        st.caption("Splits text into linguistic tokens.")
        st.json(raw_tokens)
    with stage_cols[3]:
        st.markdown("**4. Lemmatization**")
        st.caption("Converts words to dictionary base forms.")
        st.json(lemmas)

    st.markdown("---")
    col_stop, col_stem_lemma = st.columns(2)

    with col_stop:
        st.markdown("#### Critical Concept: Stopwords & Negation Inversion")
        st.info("""
        **Why we do NOT blindly remove every stopword:**
        If the word `'not'` is eliminated from *"The app is not good"*, it becomes *"The app is good"*, totally inverting customer sentiment!
        Our pipeline uses negation-preserving filtering.
        """)
        st.write("**Standard Stopword Filtering (Dangerous):**", filtered_tokens_all)
        st.write("**Negation-Preserving Filtering (Our System):**", filtered_tokens_neg)

    with col_stem_lemma:
        st.markdown("#### Stemming vs Lemmatization Comparison")
        comp_df = pd.DataFrame(compare_stem_vs_lemma([
            "complaining", "payments", "better", "crashes", "failing", "studies", "connected"
        ]))
        st.dataframe(comp_df, use_container_width=True, hide_index=True)


# -------------------------------------------------------------
# TAB 3: BATCH FEEDBACK ANALYTICS
# -------------------------------------------------------------
with tab_batch:
    st.subheader("Batch Customer Feedback Processing")
    st.caption("Upload a CSV with a 'feedback' column or analyze the historical feedback dataset.")

    uploaded_file = st.file_uploader("Upload Customer Feedback CSV", type=["csv"])

    if uploaded_file is not None:
        batch_input_df = pd.read_csv(uploaded_file)
        if "feedback" not in batch_input_df.columns:
            st.error("Uploaded CSV must contain a 'feedback' column.")
            batch_input_df = None
    else:
        batch_input_df = pd.read_csv("data/feedback.csv")
        st.caption("Showing analysis of indexed feedback dataset (80+ records):")

    if batch_input_df is not None:
        feedback_list = batch_input_df["feedback"].astype(str).tolist()

        with st.spinner("Analyzing batch feedback..."):
            enriched_df = analyzer.analyze_batch(feedback_list)

        # Overview statistics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Reviews Analyzed", len(enriched_df))
        pos_pct = (enriched_df["sentiment"] == "positive").mean() * 100
        neg_pct = (enriched_df["sentiment"] == "negative").mean() * 100
        neu_pct = (enriched_df["sentiment"] == "neutral").mean() * 100
        m2.metric("Positive Feedback", f"{pos_pct:.1f}%")
        m3.metric("Negative Feedback", f"{neg_pct:.1f}%")
        m4.metric("Neutral Feedback", f"{neu_pct:.1f}%")

        # Charts
        c_chart1, c_chart2 = st.columns(2)
        with c_chart1:
            st.markdown("##### Sentiment Distribution")
            fig_sent_pie = px.pie(
                enriched_df, names="sentiment",
                color="sentiment",
                color_discrete_map={"positive": "#10B981", "negative": "#EF4444", "neutral": "#64748B"},
                hole=0.45
            )
            fig_sent_pie.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=280)
            st.plotly_chart(fig_sent_pie, use_container_width=True)

        with c_chart2:
            st.markdown("##### Top Complaint & Feedback Categories")
            all_cats = []
            for item in enriched_df["categories"]:
                all_cats.extend([c.strip() for c in item.split(",") if c.strip()])
            cat_counts = pd.Series(all_cats).value_counts().reset_index()
            cat_counts.columns = ["Category", "Count"]

            fig_cat_bar = px.bar(
                cat_counts, x="Count", y="Category", orientation="h",
                color="Count", color_continuous_scale="Viridis"
            )
            fig_cat_bar.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=280, coloraxis_showscale=False)
            st.plotly_chart(fig_cat_bar, use_container_width=True)

        # Enriched Data Table
        st.markdown("##### Enriched Feedback Data")
        st.dataframe(enriched_df, use_container_width=True)

        # CSV Download
        csv_data = enriched_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Analyzed Feedback CSV",
            data=csv_data,
            file_name="analyzed_customer_feedback.csv",
            mime="text/csv"
        )


# -------------------------------------------------------------
# TAB 4: CLASSICAL NLP VS TRANSFORMER COMPARISON
# -------------------------------------------------------------
with tab_compare:
    st.subheader("Classical NLP (TF-IDF + Logistic Regression) vs Modern Transformer (DistilBERT)")
    st.markdown("""
    Explore how bag-of-words / TF-IDF representations compare with deep bidirectional transformer attention mechanisms on difficult linguistic structures.
    """)

    sample_tests = [
        "The app is not good, it keeps crashing.",
        "Customer support was not unhelpful, but took too long.",
        "I wouldn't say the update was bad, but performance suffered.",
        "Fast checkout and smooth experience overall.",
        "Payment is failing repeatedly."
    ]

    comp_results = compare_tfidf_vs_transformer(sample_tests, tfidf_classifier=analyzer.sentiment_model)
    comp_df = pd.DataFrame(comp_results)

    for item in comp_results:
        with st.container():
            st.markdown(f"""
            <div class="card-box">
                <div style="font-size:1.1rem; font-weight:700; margin-bottom:8px;">"{item['text']}"</div>
                <div style="display:flex; gap: 2rem; margin-bottom: 8px;">
                    <div><strong>TF-IDF Prediction:</strong> <span style="text-transform:uppercase; font-weight:700;">{item['tfidf_sentiment']}</span></div>
                    <div><strong>Transformer Prediction:</strong> <span style="text-transform:uppercase; font-weight:700; color:#4338CA;">{item['transformer_sentiment']}</span> ({item['transformer_confidence']*100:.1f}%)</div>
                </div>
                <div style="font-size:0.9rem; color:#475569; background:#F1F5F9; padding:0.6rem 0.9rem; border-radius:8px;">
                    <strong>Linguistic Architecture Insight:</strong> {item['key_difference']}
                </div>
            </div>
            """, unsafe_allow_html=True)


# -------------------------------------------------------------
# TAB 5: MODEL EVALUATION & PERFORMANCE
# -------------------------------------------------------------
with tab_eval:
    st.subheader("Model Evaluation Metrics & Diagnostics")

    df_eval = pd.read_csv("data/feedback.csv")
    texts_eval = df_eval["feedback"].astype(str).tolist()
    sentiments_eval = df_eval["sentiment"].astype(str).tolist()
    categories_eval = df_eval["categories"].astype(str).tolist()

    sent_metrics = analyzer.sentiment_model.evaluate(texts_eval, sentiments_eval)
    cat_metrics = analyzer.category_model.evaluate(texts_eval, categories_eval)

    col_m1, col_m2 = st.columns(2)

    with col_m1:
        st.markdown("#### Sentiment Classifier Performance")
        sc1, sc2, sc3 = st.columns(3)
        sc1.metric("Accuracy", f"{sent_metrics['accuracy']*100:.1f}%")
        sc2.metric("Precision", f"{sent_metrics['precision']*100:.1f}%")
        sc3.metric("F1 Score", f"{sent_metrics['f1_score']*100:.1f}%")

        st.markdown("##### Confusion Matrix")
        cm = np.array(sent_metrics["confusion_matrix"])
        classes = sent_metrics["classes"]

        fig_cm = px.imshow(
            cm,
            x=[f"Pred: {c}" for c in classes],
            y=[f"Actual: {c}" for c in classes],
            text_auto=True,
            color_continuous_scale="Blues"
        )
        fig_cm.update_layout(height=280, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_cm, use_container_width=True)

    with col_m2:
        st.markdown("#### Multi-Label Category Classifier Performance")
        cc1, cc2, cc3 = st.columns(3)
        cc1.metric("Micro F1 Score", f"{cat_metrics['micro_f1']*100:.1f}%")
        cc2.metric("Macro F1 Score", f"{cat_metrics['macro_f1']*100:.1f}%")
        cc3.metric("Hamming Loss", f"{cat_metrics['hamming_loss']:.4f}")

        st.markdown("##### Top Category Indicative Terms")
        top_kws = analyzer.category_model.get_top_category_keywords(n_top=3)
        cat_term_data = []
        for cat, term_list in top_kws.items():
            terms_joined = ", ".join([f"{t[0]} ({t[1]})" for t in term_list])
            cat_term_data.append({"Category": cat, "Top Salient N-grams (Weight)": terms_joined})
        st.dataframe(pd.DataFrame(cat_term_data), use_container_width=True, hide_index=True)
