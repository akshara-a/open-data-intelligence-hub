
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge, LogisticRegression
from sklearn.cluster import KMeans

st.set_page_config(
    page_title="CommerceAI Dashboard",
    page_icon="AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #F7F8FA;
    color: #111827;
}

.block-container {
    padding-top: 1.4rem;
    max-width: 1280px;
}

[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid #E5E7EB;
}

[data-testid="stSidebar"] * {
    color: #111827 !important;
}

.brand-box {
    padding: 16px 4px 18px 4px;
    border-bottom: 1px solid #E5E7EB;
    margin-bottom: 14px;
}

.brand-title {
    font-size: 23px;
    font-weight: 800;
    color: #111827;
    margin-bottom: 4px;
}

.brand-subtitle {
    font-size: 13px;
    color: #6B7280;
}

.header {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 18px;
    padding: 26px 30px;
    margin-bottom: 22px;
    box-shadow: 0 8px 20px rgba(15,23,42,0.04);
}

.header h1 {
    color: #111827 !important;
    font-size: 34px;
    font-weight: 800;
    margin: 0;
}

.header p {
    color: #6B7280;
    font-size: 15px;
    margin-top: 8px;
}

.card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 18px;
    padding: 24px;
    box-shadow: 0 8px 20px rgba(15,23,42,0.04);
    margin-bottom: 20px;
}

.kpi {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 18px;
    padding: 22px;
    min-height: 128px;
    box-shadow: 0 8px 20px rgba(15,23,42,0.04);
}

.icon-box {
    width: 42px;
    height: 42px;
    border-radius: 12px;
    background: #EFF6FF;
    color: #2563EB;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 15px;
}

.kpi-label {
    color: #6B7280;
    font-size: 13px;
    font-weight: 600;
    margin-top: 14px;
}

.kpi-value {
    color: #111827;
    font-size: 30px;
    font-weight: 800;
}

.kpi-note {
    color: #10B981;
    font-size: 12px;
    font-weight: 700;
}

.section-title {
    color: #111827;
    font-size: 24px;
    font-weight: 800;
    margin: 8px 0 18px 0;
}

.result-success {
    background: #ECFDF5;
    border: 1px solid #A7F3D0;
    color: #065F46;
    border-radius: 18px;
    padding: 28px;
    text-align: center;
    font-size: 24px;
    font-weight: 800;
    margin-top: 22px;
}

.result-danger {
    background: #FEF2F2;
    border: 1px solid #FECACA;
    color: #991B1B;
    border-radius: 18px;
    padding: 28px;
    text-align: center;
    font-size: 24px;
    font-weight: 800;
    margin-top: 22px;
}

.info-panel {
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    border-left: 5px solid #2563EB;
    border-radius: 16px;
    padding: 20px;
    color: #1E3A8A;
}

.stButton > button {
    height: 50px;
    border-radius: 12px;
    background: #111827 !important;
    color: #FFFFFF !important;
    border: 1px solid #111827 !important;
    font-weight: 700;
}

.stButton > button:hover {
    background: #2563EB !important;
    border-color: #2563EB !important;
}

label {
    color: #374151 !important;
    font-weight: 700 !important;
    font-size: 13px !important;
}

h1, h2, h3, h4 {
    color: #111827 !important;
}

.stDataFrame {
    border: 1px solid #E5E7EB;
    border-radius: 14px;
    overflow: hidden;
}
</style>
""", unsafe_allow_html=True)


def load_dataset():
    try:
        return pd.read_csv("online_shoppers_intention.csv")
    except FileNotFoundError:
        st.markdown("""
        <div class="header">
            <h1>CommerceAI Dashboard</h1>
            <p>Upload online_shoppers_intention.csv to start the live dashboard.</p>
        </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Upload online_shoppers_intention.csv",
            type=["csv"]
        )

        if uploaded_file is not None:
            return pd.read_csv(uploaded_file)

        st.stop()


df = load_dataset()

df["Purchase_Status"] = df["Revenue"].astype(int)
df["Browsing_Time"] = df["ProductRelated_Duration"]

np.random.seed(42)

df["Previous_Purchases"] = np.where(
    df["VisitorType"] == "Returning_Visitor",
    np.random.randint(5, 25, len(df)),
    np.random.randint(0, 5, len(df))
)

df["Discount_Applied"] = np.where(df["SpecialDay"] > 0, 1, 0)
df["Total_Spending"] = df["PageValues"] * np.random.uniform(20, 80, len(df))
df["Price"] = np.random.randint(20, 1000, len(df))
df["Age"] = np.random.randint(18, 60, len(df))
df["Gender"] = np.random.choice(["Male", "Female"], size=len(df))
df["User_ID"] = np.arange(1, len(df) + 1)
df["Location"] = df["Region"]

df["Product_Category"] = np.where(
    df["ProductRelated"] < 20,
    "Electronics",
    np.where(
        df["ProductRelated"] < 40,
        "Fashion",
        np.where(df["ProductRelated"] < 70, "Home & Living", "Sports")
    )
)

df["Rating"] = (
    2
    + (df["PageValues"] / df["PageValues"].max()) * 2
    + df["Purchase_Status"] * 0.8
    + df["Discount_Applied"] * 0.2
)

df["Rating"] = df["Rating"].clip(1, 5).round(1)


st.sidebar.markdown("""
<div class="brand-box">
    <div class="brand-title">CommerceAI</div>
    <div class="brand-subtitle">ML Recommendation Dashboard</div>
</div>
""", unsafe_allow_html=True)

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Rating Prediction",
        "Purchase Prediction",
        "Customer Segmentation",
        "Model Comparison"
    ]
)

st.markdown("""
<div class="header">
    <h1>E-Commerce Recommendation System</h1>
    <p>Clean machine learning dashboard for customer rating, purchase likelihood and segmentation analysis.</p>
</div>
""", unsafe_allow_html=True)


if menu == "Dashboard":

    st.markdown('<div class="section-title">Dashboard Overview</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="kpi">
            <div class="icon-box">US</div>
            <div class="kpi-label">Total Sessions</div>
            <div class="kpi-value">{len(df):,}</div>
            <div class="kpi-note">Active dataset</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="kpi">
            <div class="icon-box">CR</div>
            <div class="kpi-label">Purchase Rate</div>
            <div class="kpi-value">{df["Purchase_Status"].mean() * 100:.1f}%</div>
            <div class="kpi-note">Conversion rate</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="kpi">
            <div class="icon-box">RT</div>
            <div class="kpi-label">Average Rating</div>
            <div class="kpi-value">{df["Rating"].mean():.2f}</div>
            <div class="kpi-note">Predicted score</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="kpi">
            <div class="icon-box">SP</div>
            <div class="kpi-label">Average Spending</div>
            <div class="kpi-value">{df["Total_Spending"].mean():.0f}</div>
            <div class="kpi-note">Spending proxy</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns(2)

    with left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Purchase Distribution")
        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_facecolor("#FFFFFF")
        ax.set_facecolor("#FFFFFF")
        counts = df["Purchase_Status"].value_counts().sort_index()
        ax.bar(["No Purchase", "Purchased"], counts.values)
        ax.set_ylabel("Sessions")
        ax.spines[["top", "right"]].set_visible(False)
        st.pyplot(fig)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Product Category Distribution")
        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_facecolor("#FFFFFF")
        ax.set_facecolor("#FFFFFF")
        cat_counts = df["Product_Category"].value_counts()
        ax.bar(cat_counts.index, cat_counts.values)
        ax.set_ylabel("Count")
        ax.tick_params(axis="x", rotation=20)
        ax.spines[["top", "right"]].set_visible(False)
        st.pyplot(fig)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Dataset Preview")
    st.dataframe(df.head(10), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


elif menu == "Rating Prediction":

    st.markdown('<div class="section-title">Rating Prediction</div>', unsafe_allow_html=True)

    reg_features = [
        "Price",
        "Browsing_Time",
        "Previous_Purchases",
        "Discount_Applied",
        "Age",
        "Total_Spending"
    ]

    X = df[reg_features]
    y = df["Rating"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = Ridge(alpha=1.0)
    model.fit(X_scaled, y)

    st.markdown('<div class="card">', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        price = st.slider("Product Price", 20, 1000, 300)
        previous_purchases = st.slider("Previous Purchases", 0, 30, 4)
        age = st.slider("Customer Age", 18, 60, 24)

    with c2:
        browsing_time = st.slider("Browsing Time", 0.0, 10000.0, 500.0)
        discount = st.selectbox("Discount Applied", [0, 1], key="rating_discount")
        spending = st.slider("Total Spending", 0.0, 10000.0, 500.0)

    input_data = pd.DataFrame(
        [[price, browsing_time, previous_purchases, discount, age, spending]],
        columns=reg_features
    )

    input_scaled = scaler.transform(input_data)

    if st.button("Generate Rating Prediction", use_container_width=True):
        prediction = model.predict(input_scaled)[0]
        prediction = max(1, min(5, prediction))

        st.markdown(f"""
        <div class="result-success">
            Predicted Rating<br>{prediction:.2f} / 5
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


elif menu == "Purchase Prediction":

    st.markdown('<div class="section-title">Purchase Likelihood Prediction</div>', unsafe_allow_html=True)

    clf_features = [
        "Browsing_Time",
        "Previous_Purchases",
        "Price",
        "Discount_Applied",
        "Total_Spending",
        "ProductRelated",
        "BounceRates",
        "ExitRates",
        "PageValues"
    ]

    X = df[clf_features]
    y = df["Purchase_Status"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = LogisticRegression(max_iter=1000, class_weight="balanced")
    model.fit(X_scaled, y)

    st.markdown('<div class="card">', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        browsing_time = st.slider("Browsing Time", 0.0, 10000.0, 500.0)
        previous_purchases = st.slider("Previous Purchases", 0, 30, 4)
        product_related = st.slider("Product Pages Viewed", 0, 800, 20)
        price = st.slider("Product Price", 20, 1000, 300)

    with c2:
        discount = st.selectbox("Discount Applied", [0, 1], key="purchase_discount")
        page_values = st.slider("Page Values", 0.0, 400.0, 5.0)
        spending = st.slider("Total Spending", 0.0, 10000.0, 500.0)
        bounce_rates = st.slider("Bounce Rate", 0.0, 1.0, 0.02)
        exit_rates = st.slider("Exit Rate", 0.0, 1.0, 0.05)

    input_data = pd.DataFrame(
        [[
            browsing_time,
            previous_purchases,
            price,
            discount,
            spending,
            product_related,
            bounce_rates,
            exit_rates,
            page_values
        ]],
        columns=clf_features
    )

    input_scaled = scaler.transform(input_data)

    if st.button("Predict Purchase Probability", use_container_width=True):
        probability = model.predict_proba(input_scaled)[0][1] * 100
        prediction = 1 if probability >= 50 else 0

        st.progress(int(probability))

        if prediction == 1:
            st.markdown(f"""
            <div class="result-success">
                Likely to Purchase<br>{probability:.2f}% Probability
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-danger">
                Not Likely to Purchase<br>{probability:.2f}% Probability
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


elif menu == "Customer Segmentation":

    st.markdown('<div class="section-title">Customer Segmentation</div>', unsafe_allow_html=True)

    cluster_features = [
        "Browsing_Time",
        "Previous_Purchases",
        "Total_Spending",
        "Rating"
    ]

    X = df[cluster_features]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    kmeans.fit(X_scaled)

    st.markdown('<div class="card">', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        browsing_time = st.slider("Browsing Time", 0.0, 10000.0, 500.0)
        previous_purchases = st.slider("Previous Purchases", 0, 30, 4)

    with c2:
        spending = st.slider("Total Spending", 0.0, 10000.0, 500.0)
        rating = st.slider("Rating", 1.0, 5.0, 4.0)

    input_data = pd.DataFrame(
        [[browsing_time, previous_purchases, spending, rating]],
        columns=cluster_features
    )

    input_scaled = scaler.transform(input_data)

    segment_names = {
        0: "Frequent Buyer",
        1: "Discount Sensitive Customer",
        2: "Window Shopper",
        3: "High Value Customer"
    }

    if st.button("Identify Customer Segment", use_container_width=True):
        cluster = kmeans.predict(input_scaled)[0]
        segment = segment_names.get(cluster, "General Customer")

        st.markdown(f"""
        <div class="result-success">
            Customer Segment<br>{segment}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


elif menu == "Model Comparison":

    st.markdown('<div class="section-title">Model Comparison</div>', unsafe_allow_html=True)

    comparison = pd.DataFrame({
        "Model": [
            "Ridge Regression",
            "Logistic Regression",
            "K-Means Clustering"
        ],
        "Machine Learning Task": [
            "Rating Prediction",
            "Purchase Likelihood Prediction",
            "Customer Segmentation"
        ],
        "Business Value": [
            "Recommends products users may rate highly",
            "Identifies customers likely to purchase",
            "Creates customer groups for targeted marketing"
        ]
    })

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.dataframe(comparison, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="info-panel">
        <h3>Final Business Recommendation</h3>
        <p>
        This system helps an e-commerce business improve recommendation quality,
        predict customer buying intent, and create customer segments for personalized
        marketing. Regression supports rating prediction, classification predicts
        purchase likelihood, and clustering identifies meaningful customer groups.
        </p>
    </div>
    """, unsafe_allow_html=True)
