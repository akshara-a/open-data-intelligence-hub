"""Streamlit web interface for the E-Commerce Recommendation System."""

import subprocess
import sys
from pathlib import Path

# Re-launch via Streamlit when run as `python app.py`
if __name__ == "__main__":
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx

        if get_script_run_ctx() is None:
            sys.exit(
                subprocess.call(
                    [sys.executable, "-m", "streamlit", "run", str(Path(__file__).resolve()), *sys.argv[1:]]
                )
            )
    except ImportError:
        print("Install streamlit: pip install streamlit")
        sys.exit(1)

import pandas as pd
import streamlit as st

from model_service import (
    CATEGORIES,
    CLUSTER_LABELS,
    load_engine,
    predict_purchase,
    predict_rating,
    predict_segment_from_behavior,
    get_customer_segment,
    train_and_save_models,
)

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "outputs"

st.set_page_config(
    page_title="ShopML Platform",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Safe, isolated CSS only for custom HTML components
st.markdown("""
<style>
    /* Gradient Texts */
    .text-gradient {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline-block;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }

    /* Isolated Metric Cards */
    .custom-card {
        background-color: rgba(59, 130, 246, 0.05);
        border: 1px solid rgba(59, 130, 246, 0.2);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .custom-card-title {
        color: #64748b;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    
    .custom-card-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #3b82f6;
        line-height: 1;
    }

    /* Prediction Result Boxes */
    .result-box-success {
        background-color: rgba(16, 185, 129, 0.1);
        border-left: 5px solid #10b981;
        padding: 1.5rem;
        border-radius: 8px;
        margin-top: 1rem;
    }
    
    .result-box-danger {
        background-color: rgba(244, 63, 94, 0.1);
        border-left: 5px solid #f43f5e;
        padding: 1.5rem;
        border-radius: 8px;
        margin-top: 1rem;
    }
    
    .result-box-info {
        background-color: rgba(59, 130, 246, 0.1);
        border-left: 5px solid #3b82f6;
        padding: 1.5rem;
        border-radius: 8px;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_engine():
    return load_engine()


def render_metric(title, value):
    return f"""
    <div class="custom-card">
        <div class="custom-card-title">{title}</div>
        <div class="custom-card-value">{value}</div>
    </div>
    """


def page_dashboard(engine):
    st.markdown("<h1 class='text-gradient'>Dashboard</h1>", unsafe_allow_html=True)
    st.write("Real-time analytics and system overview")
    st.divider()

    results = engine.results
    reg_score = results.get("regression", {}).get("Gradient Boosting Regressor", {}).get("R2", 0)
    clf_score = results.get("classification", {}).get("Logistic Regression (Tuned)", {}).get("F1", 0)

    # Use native columns
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(render_metric("Total Records", f"{len(engine.raw_data):,}"), unsafe_allow_html=True)
    with col2:
        st.markdown(render_metric("Customers", f"{engine.customer_segments['User_ID'].nunique():,}"), unsafe_allow_html=True)
    with col3:
        st.markdown(render_metric("Regression R²", f"{reg_score:.3f}"), unsafe_allow_html=True)
    with col4:
        st.markdown(render_metric("Classification F1", f"{clf_score:.3f}"), unsafe_allow_html=True)
        
    st.divider()
    
    left, right = st.columns(2)
    
    with left:
        st.subheader("📋 Dataset Preview")
        st.dataframe(engine.raw_data.head(10), use_container_width=True, hide_index=True)
    
    with right:
        st.subheader("🏆 Best Performing Models")
        best_models = pd.DataFrame({
            "Task": ["Regression", "Classification", "Clustering"],
            "Algorithm": ["Gradient Boosting", "Tuned Logistic Regression", "K-Means (k=6)"],
            "Score": ["0.374 (R²)", "0.873 (F1)", "0.172 (Silhouette)"]
        })
        st.dataframe(best_models, use_container_width=True, hide_index=True)
    
    if (OUTPUT_DIR / "eda_overview.png").exists():
        st.subheader("Data Overview")
        st.image(str(OUTPUT_DIR / "eda_overview.png"), use_container_width=True)


def get_form_inputs(prefix):
    """Reusable native Streamlit form inputs"""
    col1, col2 = st.columns(2)
    with col1:
        cat = st.selectbox("Product Category", CATEGORIES, key=f"{prefix}_cat")
        price = st.number_input("Price ($)", min_value=1.0, max_value=1000.0, value=150.0, key=f"{prefix}_price")
        views = st.number_input("Number of Views", min_value=1, max_value=100, value=15, key=f"{prefix}_views")
    with col2:
        time = st.number_input("Time Spent (s)", min_value=1.0, max_value=600.0, value=120.0, key=f"{prefix}_time")
        cart_str = st.selectbox("Cart Status", ["Not in Cart", "In Cart"], key=f"{prefix}_cart")
        prev = st.number_input("Previous Purchases", min_value=0, max_value=50, value=2, key=f"{prefix}_prev")
        
    return {
        "product_category": cat,
        "price": price,
        "number_of_views": views,
        "cart_status": 1 if cart_str == "In Cart" else 0,
        "time_spent": time,
        "previous_purchases": prev
    }


def page_rating_predictor(engine):
    st.markdown("<h1 class='text-gradient'>⭐ Rating Predictor</h1>", unsafe_allow_html=True)
    st.write("Predict how customers will rate your products using native components.")
    st.divider()
    
    inputs = get_form_inputs("rating")
    
    _, btn_col, _ = st.columns([1, 1, 1])
    with btn_col:
        predict = st.button("Predict Rating", use_container_width=True, type="primary")
        
    if predict:
        with st.spinner("Analyzing..."):
            predicted = predict_rating(engine, inputs)
            stars = "★" * int(round(predicted)) + "☆" * (5 - int(round(predicted)))
            
            st.markdown(f"""
            <div class="result-box-info" style="text-align: center;">
                <h4 style="color: #3b82f6;">Predicted Rating</h4>
                <div style="font-size: 4rem; font-weight: 800; color: #3b82f6; line-height: 1;">{predicted:.1f}</div>
                <div style="font-size: 2rem; color: #f59e0b; margin-bottom: 1rem;">{stars}</div>
                <p style="color: #64748b;">Based on product features and customer engagement metrics.</p>
            </div>
            """, unsafe_allow_html=True)


def page_purchase_predictor(engine):
    st.markdown("<h1 class='text-gradient'>🎯 Purchase Predictor</h1>", unsafe_allow_html=True)
    st.write("Evaluate the likelihood of a purchase conversion.")
    st.divider()
    
    inputs = get_form_inputs("purchase")
    
    # Native slider
    rating = st.slider("Product Rating", 1.0, 5.0, 4.0, 0.1, key="purchase_rating")
    inputs["rating"] = rating
    
    _, btn_col, _ = st.columns([1, 1, 1])
    with btn_col:
        predict = st.button("Predict Purchase", use_container_width=True, type="primary")
        
    if predict:
        with st.spinner("Calculating..."):
            pred, prob = predict_purchase(engine, inputs)
            is_buyer = pred == 1
            
            if is_buyer:
                st.markdown(f"""
                <div class="result-box-success" style="text-align: center;">
                    <h4 style="color: #10b981;">Likely to Purchase</h4>
                    <div style="font-size: 4rem; font-weight: 800; color: #10b981; line-height: 1;">{prob*100:.0f}%</div>
                    <p style="color: #64748b;">High probability of conversion. Target with offers.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="result-box-danger" style="text-align: center;">
                    <h4 style="color: #f43f5e;">Unlikely to Purchase</h4>
                    <div style="font-size: 4rem; font-weight: 800; color: #f43f5e; line-height: 1;">{prob*100:.0f}%</div>
                    <p style="color: #64748b;">Low probability of conversion.</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.progress(prob)


def page_customer_segments(engine):
    st.markdown("<h1 class='text-gradient'>👥 Customer Segments</h1>", unsafe_allow_html=True)
    st.write("Analyze clustering profiles and lookup behaviors.")
    st.divider()
    
    tab1, tab2, tab3 = st.tabs(["Search User", "Predict from Behavior", "Segment Profiles"])
    
    with tab1:
        st.subheader("Lookup by ID")
        user_id = st.number_input("Enter User ID", min_value=1, max_value=500, value=45)
        if st.button("Search User Profile", type="primary"):
            info = get_customer_segment(engine, user_id)
            if info:
                st.markdown(f"""
                <div class="result-box-info">
                    <h4 style="color: #3b82f6;">{info['label']}</h4>
                    <p style="color: #64748b;">{info['description']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Total Spent", f"${info['total_spent']:.0f}")
                c2.metric("Purchases", int(info['num_purchases']))
                c3.metric("Avg Rating", f"{info['avg_rating']:.1f}")
                c4.metric("Products Viewed", int(info['products_viewed']))
            else:
                st.error("User not found.")

    with tab2:
        st.subheader("Predict Segment from Behavior")
        
        b1, b2, b3 = st.columns(3)
        with b1:
            pv = st.number_input("Products Viewed", 1, 500, 200, key="b_pv")
            ar = st.number_input("Average Rating", 1.0, 5.0, 4.5, key="b_ar")
        with b2:
            np_ = st.number_input("Number of Purchases", 0, 30, 5, key="b_np")
            at = st.number_input("Avg Time Spent (s)", 1.0, 300.0, 140.0, key="b_at")
        with b3:
            ts = st.number_input("Total Spent ($)", 0.0, 5000.0, 1200.0, key="b_ts")
            ca = st.number_input("Cart Additions", 0, 20, 4, key="b_ca")

        if st.button("🔮 Predict Segment", key="btn_seg", use_container_width=True, type="primary"):
            result = predict_segment_from_behavior(engine, {
                "products_viewed": pv, "num_purchases": np_, "avg_rating": ar,
                "avg_time_spent": at, "total_spent": ts, "cart_additions": ca,
            })
            st.markdown(f"""
            <div class="result-box-info">
                <h4 style="color: #3b82f6;">{result['label']}</h4>
                <p style="color: #64748b;">{result['description']}</p>
            </div>
            """, unsafe_allow_html=True)

    with tab3:
        st.subheader("All Profiles")
        for cid, (label, desc) in CLUSTER_LABELS.items():
            st.markdown(f"""
            <div class="result-box-info" style="margin-top: 0.5rem; padding: 1rem;">
                <h4 style="color: #3b82f6; margin: 0; margin-bottom: 0.25rem;">{label}</h4>
                <p style="margin: 0; color: #64748b;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)


def page_model_comparison(engine):
    st.markdown("<h1 class='text-gradient'>📋 Model Comparison</h1>", unsafe_allow_html=True)
    st.write("Comprehensive evaluation across machine learning algorithms.")
    st.divider()
    
    results = engine.results

    st.subheader("📊 Regression Models — Predict Product Rating")
    reg_df = pd.DataFrame(results.get("regression", {})).T
    reg_df.index.name = "Algorithm"
    st.dataframe(
        reg_df.style.highlight_max(axis=0, subset=["R2"]).highlight_min(axis=0, subset=["MAE", "RMSE"]),
        use_container_width=True,
    )

    st.divider()
    st.subheader("🎯 Classification Models — Predict Purchase")
    clf_df = pd.DataFrame(results.get("classification", {})).T
    clf_df.index.name = "Algorithm"
    st.dataframe(clf_df.style.highlight_max(axis=0), use_container_width=True)

    if (OUTPUT_DIR / "confusion_matrix.png").exists():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(str(OUTPUT_DIR / "confusion_matrix.png"), caption="Confusion Matrix — Tuned Logistic Regression", use_container_width=True)

    st.divider()
    st.subheader("🔀 Clustering Models — Customer Segmentation")
    clust_df = pd.DataFrame(results.get("clustering", {})).T
    clust_df.index.name = "Algorithm"
    st.dataframe(clust_df, use_container_width=True)

    st.divider()
    st.subheader("💡 Business Recommendations")
    
    rec_df = pd.DataFrame({
        "Business Goal": [
            "Product Ranking",
            "Customer Targeting",
            "Audience Segmentation"
        ],
        "Recommended Model": [
            "Gradient Boosting Regressor",
            "Tuned Logistic Regression",
            "K-Means Clustering (k=6)"
        ],
        "Why": [
            "Lowest MAE, highest R² — most accurate predictions",
            "Best F1 & recall (92.6%) — identifies buyers effectively",
            "Actionable, distinct customer profiles for targeted marketing"
        ]
    })
    st.dataframe(rec_df, use_container_width=True, hide_index=True)


def main():
    engine = get_engine()
    
    # Sidebar
    with st.sidebar:
        st.markdown("<h2 class='text-gradient' style='font-size: 2rem;'>✨ ShopML</h2>", unsafe_allow_html=True)
        st.write("Machine Learning System")
        st.divider()
        
        page = st.radio(
            "Navigation",
            ["Dashboard", "Rating Predictor", "Purchase Predictor", "Customer Segments", "Model Comparison"],
            label_visibility="collapsed"
        )
        
        st.divider()
        st.subheader("🔧 Model Management")
        sc1, sc2 = st.columns(2)
        
        with sc1:
            if st.button("🔄 Retrain", use_container_width=True):
                with st.spinner("Training..."):
                    train_and_save_models()
                    st.cache_resource.clear()
                    st.success("Models retrained successfully!")
                    st.rerun()
                    
        with sc2:
            if st.button("🔗 Reset Cache", use_container_width=True):
                st.cache_resource.clear()
                st.success("✅ Cache cleared!")
                st.rerun()
                
        st.divider()
        st.subheader("📊 System Info")
        sc3, sc4 = st.columns(2)
        with sc3:
            st.metric("Records", f"{len(engine.raw_data):,}")
        with sc4:
            st.metric("Customers", f"{engine.customer_segments['User_ID'].nunique():,}")
        
        st.caption("🚀 Machine Learning System v2.0")
    
    if page == "Dashboard":
        page_dashboard(engine)
    elif page == "Rating Predictor":
        page_rating_predictor(engine)
    elif page == "Purchase Predictor":
        page_purchase_predictor(engine)
    elif page == "Customer Segments":
        page_customer_segments(engine)
    elif page == "Model Comparison":
        page_model_comparison(engine)


if __name__ == "__main__":
    main()
