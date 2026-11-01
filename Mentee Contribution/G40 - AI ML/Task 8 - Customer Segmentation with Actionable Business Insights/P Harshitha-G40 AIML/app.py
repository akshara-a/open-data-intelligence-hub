"""
Customer Segmentation - Main Application
==========================================
Dual-mode entry point:
  1. Run the full ML pipeline end-to-end (python app.py --pipeline)
  2. Launch the Streamlit dashboard (streamlit run app.py)
"""

import os
import sys

# ── Resolve paths ────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
DATA_RAW    = os.path.join(BASE_DIR, "data", "customer_data.csv")
DATA_CLEAN  = os.path.join(BASE_DIR, "data", "cleaned_customer_data.csv")
IMAGES_DIR  = os.path.join(BASE_DIR, "images")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")

sys.path.insert(0, BASE_DIR)


# ==================================================================
#  PIPELINE MODE  (python app.py --pipeline)
# ==================================================================
def run_pipeline():
    """Execute the full end-to-end ML pipeline and generate all outputs."""
    import pandas as pd

    from src.data_preprocessing  import preprocess_pipeline
    from src.exploratory_analysis import run_eda
    from src.clustering           import run_clustering
    from src.classification       import run_classification
    from src.regression           import run_regression
    from src.hyperparameter_tuning import run_hyperparameter_tuning
    from src.business_insights    import run_business_insights

    os.makedirs(IMAGES_DIR,  exist_ok=True)
    os.makedirs(OUTPUTS_DIR, exist_ok=True)

    print("\n" + "=" * 65)
    print("  CUSTOMER SEGMENTATION - FULL PIPELINE")
    print("=" * 65)

    # Step 1: Preprocessing
    print("\n[1/6] Data Preprocessing ...")
    df_clean, df_encoded = preprocess_pipeline(DATA_RAW, DATA_CLEAN)

    # Step 2: EDA
    print("\n[2/6] Exploratory Data Analysis ...")
    run_eda(df_clean, IMAGES_DIR)

    # Step 3: Clustering
    print("\n[3/6] Clustering ...")
    df_clustered, seg_profile, seg_names, kmeans, cl_scaler = run_clustering(
        df_clean, IMAGES_DIR, OUTPUTS_DIR
    )

    # Step 4: Classification (use clustered df so Cluster is a feature)
    print("\n[4/6] Classification ...")
    run_classification(df_clustered, IMAGES_DIR, OUTPUTS_DIR)

    # Step 5: Regression
    print("\n[5/6] Regression ...")
    run_regression(df_clustered, IMAGES_DIR, OUTPUTS_DIR)

    # Step 6: Hyperparameter Tuning
    print("\n[5b/6] Hyperparameter Tuning ...")
    run_hyperparameter_tuning(df_clustered)

    # Step 7: Business Insights
    print("\n[6/6] Business Insights ...")
    run_business_insights(seg_profile, seg_names, OUTPUTS_DIR)

    print("\n" + "=" * 65)
    print("  PIPELINE COMPLETE - All outputs saved.")
    print("=" * 65)
    print(f"  Images  : {IMAGES_DIR}")
    print(f"  Outputs : {OUTPUTS_DIR}")
    print("  Launch dashboard: streamlit run app.py")
    print("=" * 65)


# ==================================================================
#  STREAMLIT DASHBOARD MODE  (streamlit run app.py)
# ==================================================================
def run_dashboard():
    import streamlit as st
    import pandas as pd
    import numpy as np
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import seaborn as sns
    from PIL import Image

    # ── Page config ──────────────────────────────────────────────
    st.set_page_config(
        page_title="Customer Segmentation Dashboard",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # ── Custom CSS ───────────────────────────────────────────────
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem; border-radius: 16px; margin-bottom: 1.5rem;
        color: white; text-align: center;
        box-shadow: 0 8px 32px rgba(102,126,234,0.35);
    }
    .main-header h1 { font-size: 2.4rem; font-weight: 700; margin: 0; }
    .main-header p  { font-size: 1.1rem; opacity: 0.9; margin-top: 0.4rem; }

    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.2rem 1.5rem; border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin-bottom: 0.5rem;
    }
    .metric-card h3 { color: #4a4a6a; font-size: 0.85rem; margin: 0; }
    .metric-card p  { color: #1a1a3e; font-size: 1.8rem; font-weight: 700; margin: 0; }

    .segment-card {
        background: white;
        border-left: 5px solid #667eea;
        padding: 1rem 1.5rem; border-radius: 0 12px 12px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.07);
        margin-bottom: 1rem;
    }
    .segment-card h4 { color: #1a1a3e; margin: 0 0 0.5rem; }
    .segment-card p  { color: #555; margin: 0; font-size: 0.9rem; }

    .stTabs [data-baseweb="tab-list"] { gap: 0.5rem; }
    .stTabs [data-baseweb="tab"] {
        background: #f0f2f6; border-radius: 8px 8px 0 0;
        padding: 0.6rem 1.4rem; font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
    }

    footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

    # ── Helpers ──────────────────────────────────────────────────
    @st.cache_data
    def load_raw():
        return pd.read_csv(DATA_RAW)

    @st.cache_data
    def load_clean():
        if os.path.exists(DATA_CLEAN):
            return pd.read_csv(DATA_CLEAN)
        return pd.read_csv(DATA_RAW)

    @st.cache_data
    def load_clustered():
        p = os.path.join(OUTPUTS_DIR, 'clustered_customers.csv')
        return pd.read_csv(p) if os.path.exists(p) else None

    @st.cache_data
    def load_segments():
        p = os.path.join(OUTPUTS_DIR, 'customer_segments.csv')
        return pd.read_csv(p, index_col=0) if os.path.exists(p) else None

    @st.cache_data
    def load_cls_pred():
        p = os.path.join(OUTPUTS_DIR, 'classification_predictions.csv')
        return pd.read_csv(p) if os.path.exists(p) else None

    @st.cache_data
    def load_reg_pred():
        p = os.path.join(OUTPUTS_DIR, 'regression_predictions.csv')
        return pd.read_csv(p) if os.path.exists(p) else None

    def img(name):
        p = os.path.join(IMAGES_DIR, name)
        return Image.open(p) if os.path.exists(p) and os.path.getsize(p) > 0 else None

    def show_img(name, caption=""):
        i = img(name)
        if i:
            st.image(i, caption=caption, use_container_width=True)
        else:
            st.info(f"📊 '{name}' not yet generated - run the pipeline first.")

    # ── Pipeline check ───────────────────────────────────────────
    pipeline_ran = os.path.exists(os.path.join(OUTPUTS_DIR, 'clustered_customers.csv'))

    # ── Sidebar ──────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("## 🔧 Controls")
        if st.button("▶ Run Full Pipeline", type="primary", use_container_width=True):
            with st.spinner("Running ML pipeline ... this may take 1-2 minutes"):
                try:
                    run_pipeline()
                    st.success("Pipeline complete! Refresh the page.")
                    st.cache_data.clear()
                    st.rerun()
                except Exception as e:
                    st.error(f"Pipeline error: {e}")

        st.markdown("---")
        st.markdown("### 📁 Files")
        st.markdown(f"**Raw data:** `customer_data.csv`")
        st.markdown(f"**Cleaned:** `cleaned_customer_data.csv`")
        st.markdown("---")
        st.markdown("### 📌 Quick Stats")
        df_raw = load_raw()
        st.metric("Total Customers", f"{len(df_raw):,}")
        st.metric("Features", df_raw.shape[1])
        st.metric("Purchase Likelihood (=1)",
                  f"{df_raw['PurchaseLikelihood'].sum():,}")
        st.markdown("---")
        st.markdown("*Customer Segmentation ML Project*")

    # ── Header ───────────────────────────────────────────────────
    st.markdown("""
    <div class="main-header">
        <h1>📊 Customer Segmentation Dashboard</h1>
        <p>E-Commerce Customer Analytics · K-Means Clustering · ML Models</p>
    </div>
    """, unsafe_allow_html=True)

    if not pipeline_ran:
        st.warning("⚠️ Pipeline outputs not found. Click **▶ Run Full Pipeline** in the sidebar to generate all results.")

    # ── Tabs ─────────────────────────────────────────────────────
    tabs = st.tabs([
        "📋 Dataset Overview",
        "🔍 EDA",
        "🗂️ Clustering",
        "🎯 Classification",
        "📈 Regression",
        "💡 Business Insights"
    ])

    # ──────────────────────────────────────────────────────────────
    # Tab 1: Dataset Overview
    # ──────────────────────────────────────────────────────────────
    with tabs[0]:
        st.markdown("## 📋 Dataset Overview")
        df = load_raw()

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("""<div class="metric-card"><h3>Total Customers</h3>
            <p>{:,}</p></div>""".format(len(df)), unsafe_allow_html=True)
        with col2:
            st.markdown("""<div class="metric-card"><h3>Features</h3>
            <p>{}</p></div>""".format(df.shape[1]), unsafe_allow_html=True)
        with col3:
            st.markdown("""<div class="metric-card"><h3>Avg Annual Income</h3>
            <p>${:,.0f}</p></div>""".format(df['AnnualIncome'].mean()), unsafe_allow_html=True)
        with col4:
            st.markdown("""<div class="metric-card"><h3>Avg Total Spending</h3>
            <p>${:,.0f}</p></div>""".format(df['TotalSpending'].mean()), unsafe_allow_html=True)

        st.markdown("### 👁️ Sample Data")
        st.dataframe(df.head(20), use_container_width=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("### 📊 Statistical Summary")
            st.dataframe(df.describe().round(2), use_container_width=True)
        with col_b:
            st.markdown("### ❓ Missing Values")
            mv = df.isnull().sum().reset_index()
            mv.columns = ['Column', 'Missing']
            st.dataframe(mv, use_container_width=True)

            st.markdown("### 🏷️ Data Types")
            dt = df.dtypes.reset_index()
            dt.columns = ['Column', 'Type']
            st.dataframe(dt, use_container_width=True)

    # ──────────────────────────────────────────────────────────────
    # Tab 2: EDA
    # ──────────────────────────────────────────────────────────────
    with tabs[1]:
        st.markdown("## 🔍 Exploratory Data Analysis")

        col1, col2 = st.columns(2)
        with col1:
            show_img('spending_distribution.png', 'Total Spending Distribution')
            show_img('boxplot_outliers.png', 'Outlier Detection - Boxplots')
        with col2:
            show_img('purchase_frequency.png', 'Purchase Frequency Distribution')
            show_img('average_spending.png', 'Average Spending by Category')

        st.markdown("### 🔗 Correlation Heatmap")
        show_img('correlation_heatmap.png', 'Feature Correlation Heatmap')

        # Interactive quick plots
        df = load_raw()
        st.markdown("### 🎨 Interactive Exploration")
        colA, colB = st.columns(2)
        with colA:
            x_feat = st.selectbox("X-axis", ['Age', 'AnnualIncome', 'PurchaseFrequency',
                                              'WebsiteVisits', 'DiscountUsage'])
        with colB:
            y_feat = st.selectbox("Y-axis", ['TotalSpending', 'AverageOrderValue',
                                              'CustomerRating', 'PurchaseFrequency'])

        fig, ax = plt.subplots(figsize=(9, 5))
        colors = {'Male': '#2196F3', 'Female': '#E91E63'}
        for gender, grp in df.groupby('Gender'):
            ax.scatter(grp[x_feat], grp[y_feat], c=colors.get(gender, 'grey'),
                       alpha=0.5, label=gender, s=40, edgecolors='w', linewidth=0.3)
        ax.set_xlabel(x_feat)
        ax.set_ylabel(y_feat)
        ax.set_title(f'{x_feat} vs {y_feat} by Gender', fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        # Category breakdown
        st.markdown("### 📦 Customer Distribution by Product Category")
        cat_counts = df['ProductCategory'].value_counts()
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        palette = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe']
        ax2.bar(cat_counts.index, cat_counts.values, color=palette)
        ax2.set_title('Customers by Product Category', fontweight='bold')
        ax2.set_ylabel('Number of Customers')
        plt.tight_layout()
        st.pyplot(fig2, use_container_width=True)
        plt.close(fig2)

    # ──────────────────────────────────────────────────────────────
    # Tab 3: Clustering
    # ──────────────────────────────────────────────────────────────
    with tabs[2]:
        st.markdown("## 🗂️ Customer Segmentation - K-Means Clustering")

        col1, col2 = st.columns(2)
        with col1:
            show_img('elbow_method.png', 'Elbow Method - Optimal K')
            show_img('customer_clusters.png', 'Customer Clusters (PCA 2D)')
        with col2:
            show_img('silhouette_scores.png', 'Silhouette Score Analysis')
            show_img('cluster_counts.png', 'Customer Count per Cluster')

        # Segment profiles table
        seg = load_segments()
        if seg is not None:
            st.markdown("### 📊 Segment Profiles")
            display_cols = [c for c in ['SegmentName', 'CustomerCount', 'TotalSpending',
                                         'PurchaseFrequency', 'DaysSinceLastPurchase',
                                         'AverageOrderValue', 'CustomerRating',
                                         'DiscountUsage', 'RevenueContribution%']
                            if c in seg.columns]
            st.dataframe(seg[display_cols].round(2), use_container_width=True)

        # Clustered data explorer
        df_clust = load_clustered()
        if df_clust is not None:
            st.markdown("### 🔎 Explore Clustered Customers")
            if 'Cluster' in df_clust.columns:
                selected_cluster = st.selectbox(
                    "Select Cluster",
                    sorted(df_clust['Cluster'].unique())
                )
                st.dataframe(
                    df_clust[df_clust['Cluster'] == selected_cluster].head(50),
                    use_container_width=True
                )

    # ──────────────────────────────────────────────────────────────
    # Tab 4: Classification
    # ──────────────────────────────────────────────────────────────
    with tabs[3]:
        st.markdown("## 🎯 Purchase Likelihood - Logistic Regression")

        col1, col2 = st.columns([1, 1])
        with col1:
            show_img('confusion_matrix.png', 'Confusion Matrix')
        with col2:
            st.markdown("### 📐 What the Model Does")
            st.info(
                "**Target:** `PurchaseLikelihood` (0 = unlikely to purchase, 1 = likely)\n\n"
                "**Algorithm:** Logistic Regression\n\n"
                "**Evaluation Metrics:** Accuracy, Precision, Recall, F1-Score, ROC-AUC\n\n"
                "**Business Use:** Identify high-potential customers to target with campaigns "
                "and avoid wasting budget on non-responders."
            )
            st.markdown("### 📊 Class Distribution")
            df_raw = load_raw()
            cls_counts = df_raw['PurchaseLikelihood'].value_counts()
            fig_cls, ax_cls = plt.subplots(figsize=(5, 3))
            ax_cls.bar(['Not Likely (0)', 'Likely (1)'], cls_counts.values,
                       color=['#f5576c', '#667eea'])
            ax_cls.set_title('Purchase Likelihood Distribution', fontweight='bold')
            plt.tight_layout()
            st.pyplot(fig_cls, use_container_width=True)
            plt.close(fig_cls)

        pred_df = load_cls_pred()
        if pred_df is not None:
            st.markdown("### 📋 Prediction Sample")
            st.dataframe(pred_df.head(30), use_container_width=True)

            # Quick metrics from predictions
            from sklearn.metrics import (accuracy_score, f1_score,
                                          precision_score, recall_score)
            y_true = pred_df['Actual']
            y_pred = pred_df['Predicted']
            mc1, mc2, mc3, mc4 = st.columns(4)
            mc1.metric("Accuracy",  f"{accuracy_score(y_true, y_pred):.3f}")
            mc2.metric("Precision", f"{precision_score(y_true, y_pred, zero_division=0):.3f}")
            mc3.metric("Recall",    f"{recall_score(y_true, y_pred, zero_division=0):.3f}")
            mc4.metric("F1-Score",  f"{f1_score(y_true, y_pred, zero_division=0):.3f}")

    # ──────────────────────────────────────────────────────────────
    # Tab 5: Regression
    # ──────────────────────────────────────────────────────────────
    with tabs[4]:
        st.markdown("## 📈 Total Spending Prediction - Regression Models")

        show_img('regression_results.png', 'Actual vs Predicted - Linear & Ridge Regression')

        reg_df = load_reg_pred()
        if reg_df is not None:
            st.markdown("### 📋 Prediction Sample")
            st.dataframe(reg_df.head(30), use_container_width=True)

            # Compute and display metrics
            from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
            y_true = reg_df['Actual_TotalSpending']
            st.markdown("### 📊 Model Comparison")
            col_lr, col_ridge = st.columns(2)
            for col_widget, pred_col, model_name in [
                (col_lr,    'LinearRegression_Predicted', 'Linear Regression'),
                (col_ridge, 'Ridge_Predicted',            'Ridge Regression')
            ]:
                if pred_col in reg_df.columns:
                    y_pred = reg_df[pred_col]
                    mae  = mean_absolute_error(y_true, y_pred)
                    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
                    r2   = r2_score(y_true, y_pred)
                    with col_widget:
                        st.markdown(f"**{model_name}**")
                        st.metric("MAE",  f"{mae:,.2f}")
                        st.metric("RMSE", f"{rmse:,.2f}")
                        st.metric("R²",   f"{r2:.4f}")
        else:
            st.info("Run the pipeline to generate regression predictions.")

        st.markdown("### ℹ️ Regression Overview")
        st.info(
            "**Target:** `TotalSpending`\n\n"
            "**Models Compared:** Linear Regression vs Ridge Regression\n\n"
            "**Evaluation:** MAE, MSE, RMSE, R² Score\n\n"
            "**Business Use:** Estimate future revenue per customer for planning "
            "marketing budgets and personalising offers."
        )

    # ──────────────────────────────────────────────────────────────
    # Tab 6: Business Insights
    # ──────────────────────────────────────────────────────────────
    with tabs[5]:
        st.markdown("## 💡 Business Insights & Recommendations")

        recs_path = os.path.join(OUTPUTS_DIR, 'business_recommendations.md')
        if os.path.exists(recs_path) and os.path.getsize(recs_path) > 0:
            with open(recs_path, 'r', encoding='utf-8') as f:
                content = f.read()
            st.markdown(content)
        else:
            st.info("Business recommendations will appear here after running the pipeline.")
            # Show preview of segment archetypes
            st.markdown("### 🏷️ Customer Segment Archetypes")
            archetypes = [
                ("👑", "High-Value Loyal Customers",
                 "High frequency, high spending, recent purchases.",
                 "Loyalty rewards, VIP membership, premium upsell."),
                ("🌱", "New and Promising Customers",
                 "Recently acquired, moderate engagement.",
                 "Onboarding offers, personalized welcome campaigns."),
                ("🏷️", "Discount-Driven Customers",
                 "Primarily purchase during promotions.",
                 "Targeted flash sales, bundle deals."),
                ("⚠️", "At-Risk Customers",
                 "Previously active, declining engagement.",
                 "Re-engagement campaigns, comeback incentives."),
                ("💤", "Low-Engagement Customers",
                 "Low frequency and spending, long intervals.",
                 "Low-cost email campaigns, entry-level products."),
            ]
            for icon, name, desc, actions in archetypes:
                st.markdown(f"""
                <div class="segment-card">
                    <h4>{icon} {name}</h4>
                    <p><strong>Profile:</strong> {desc}</p>
                    <p><strong>Strategy:</strong> {actions}</p>
                </div>
                """, unsafe_allow_html=True)


# ==================================================================
#  Entry Point
# ==================================================================
if __name__ == "__main__":
    if "--pipeline" in sys.argv or "--run-pipeline" in sys.argv:
        run_pipeline()
    else:
        # When launched directly without streamlit, still run the pipeline
        # so all outputs are generated before opening the dashboard
        print("Running pipeline to generate outputs ...")
        run_pipeline()
        print("\nDone! Now launch the dashboard with:")
        print("  streamlit run app.py")
