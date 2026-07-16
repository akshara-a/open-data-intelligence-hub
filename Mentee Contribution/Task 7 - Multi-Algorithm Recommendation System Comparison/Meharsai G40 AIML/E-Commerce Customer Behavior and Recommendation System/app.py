from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="E-Commerce Intelligence System",
    page_icon="🛒",
    layout="wide",
)


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent

DATA_PATH = PROJECT_ROOT / "data" / "Ecommerce.csv"

MODEL_PATH = PROJECT_ROOT / "models"

RESULT_PATH = PROJECT_ROOT / "outputs" / "results"


# --------------------------------------------------
# CONSTANTS
# --------------------------------------------------

PURCHASE_FEATURES = [
    "device_type",
    "user_type",
    "marketing_channel",
    "product_category",
    "unit_price",
    "quantity",
    "discount_percent",
    "discount_amount",
    "pages_viewed",
    "time_on_site_sec",
    "visit_day",
    "visit_month",
    "visit_weekday",
    "visit_season",
    "location",
]


# --------------------------------------------------
# DATA LOADING
# --------------------------------------------------

@st.cache_data
def load_dataset():
    """Load the e-commerce dataset."""

    return pd.read_csv(DATA_PATH)


@st.cache_data
def load_customer_segments():
    """Load customer segmentation results."""

    return pd.read_csv(
        RESULT_PATH / "customer_segments.csv"
    )


@st.cache_data
def load_cluster_summary():
    """Load cluster profile summary."""

    return pd.read_csv(
        RESULT_PATH / "cluster_summary.csv"
    )


@st.cache_data
def load_recommender_comparison():
    """Load recommendation algorithm comparison."""

    return pd.read_csv(
        RESULT_PATH / "recommender_comparison.csv"
    )


# --------------------------------------------------
# MODEL LOADING
# --------------------------------------------------

@st.cache_resource
def load_purchase_model():
    """Load trained Random Forest model."""

    return joblib.load(
        MODEL_PATH / "rf_model.pkl"
    )


@st.cache_resource
def load_interaction_matrix():
    """Load customer-product interaction matrix."""

    return joblib.load(
        MODEL_PATH / "interaction_matrix.pkl"
    )


@st.cache_resource
def load_item_similarity():
    """Load item similarity matrix."""

    return joblib.load(
        MODEL_PATH / "item_similarity.pkl"
    )


@st.cache_resource
def load_popular_products():
    """Load popular product ranking."""

    return joblib.load(
        MODEL_PATH / "popular_products.pkl"
    )


# --------------------------------------------------
# LOAD PROJECT DATA
# --------------------------------------------------

df = load_dataset()

customer_segments = load_customer_segments()

cluster_summary = load_cluster_summary()

recommender_comparison = load_recommender_comparison()


# --------------------------------------------------
# RECOMMENDATION FUNCTION
# --------------------------------------------------

def recommend_products(
    customer_id,
    interaction_matrix,
    item_similarity,
    popular_products,
    top_k=5,
):
    """Generate Item-Based CF recommendations."""

    if customer_id not in interaction_matrix.index:

        return (
            popular_products
            .head(top_k)
            .index
            .tolist()
        )

    customer_interactions = (
        interaction_matrix.loc[customer_id]
    )

    interacted_products = (
        customer_interactions[
            customer_interactions > 0
        ]
    )

    if interacted_products.empty:

        return (
            popular_products
            .head(top_k)
            .index
            .tolist()
        )

    recommendation_scores = pd.Series(
        0.0,
        index=item_similarity.index,
    )

    for (
        product_id,
        interaction_score,
    ) in interacted_products.items():

        if product_id not in item_similarity.columns:
            continue

        recommendation_scores += (
            item_similarity[product_id]
            * interaction_score
        )

    recommendation_scores = (
        recommendation_scores
        .drop(
            labels=interacted_products.index,
            errors="ignore",
        )
    )

    recommendations = (
        recommendation_scores
        .sort_values(
            ascending=False
        )
        .head(top_k)
        .index
        .tolist()
    )

    return recommendations


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title(
    "E-Commerce Intelligence"
)

st.sidebar.caption(
    "Customer Behavior and Recommendation System"
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard Overview",
        "Purchase Prediction",
        "Customer Segmentation",
        "Product Recommendation",
    ],
)

st.sidebar.divider()

st.sidebar.info(
    "Machine Learning System\n\n"
    "Random Forest\n\n"
    "K-Means Clustering\n\n"
    "Item-Based Collaborative Filtering"
)


# ==================================================
# DASHBOARD OVERVIEW
# ==================================================

if page == "Dashboard Overview":

    st.title(
        "🛒 E-Commerce Customer Intelligence System"
    )

    st.write(
        "A machine learning system for purchase prediction, "
        "customer segmentation, and personalized product "
        "recommendation."
    )

    st.divider()

    # ----------------------------------------------
    # DATASET METRICS
    # ----------------------------------------------

    st.subheader(
        "Dataset Overview"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Sessions",
        f"{len(df):,}",
    )

    col2.metric(
        "Customers",
        f"{df['customer_id'].nunique():,}",
    )

    col3.metric(
        "Products",
        f"{df['product_id'].nunique():,}",
    )

    purchase_rate = (
        df["purchased"].mean() * 100
    )

    col4.metric(
        "Purchase Rate",
        f"{purchase_rate:.2f}%",
    )

    st.divider()

    # ----------------------------------------------
    # ML MODULES
    # ----------------------------------------------

    st.subheader(
        "Machine Learning Modules"
    )

    module1, module2, module3 = st.columns(3)

    with module1:

        st.markdown(
            "### 🎯 Purchase Prediction"
        )

        st.write(
            "Predicts whether an e-commerce session "
            "is likely to result in a purchase."
        )

        st.success(
            "Random Forest Classifier"
        )

        st.metric(
            "ROC-AUC",
            "0.5611",
        )

        st.metric(
            "Purchase Recall",
            "64.11%",
        )

    with module2:

        st.markdown(
            "### 👥 Customer Segmentation"
        )

        st.write(
            "Groups customers using aggregated "
            "behavior and purchasing patterns."
        )

        st.success(
            "K-Means Clustering"
        )

        st.metric(
            "Best Number of Clusters",
            "2",
        )

        st.metric(
            "Silhouette Score",
            "0.2399",
        )

    with module3:

        st.markdown(
            "### 🎁 Product Recommendation"
        )

        st.write(
            "Generates personalized Top-5 product "
            "recommendations."
        )

        st.success(
            "Item-Based Collaborative Filtering"
        )

        st.metric(
            "Hit Rate@5",
            "0.0052",
        )

        st.metric(
            "Catalog Coverage@5",
            "96.44%",
        )

    st.divider()

    # ----------------------------------------------
    # RECOMMENDER COMPARISON
    # ----------------------------------------------

    st.subheader(
        "Recommendation Algorithm Comparison"
    )

    display_comparison = (
        recommender_comparison.copy()
    )

    metric_columns = [
        "Hit Rate@5",
        "Precision@5",
        "Recall@5",
        "MRR@5",
        "Coverage@5",
    ]

    display_comparison[
        metric_columns
    ] = display_comparison[
        metric_columns
    ].round(4)

    st.dataframe(
        display_comparison,
        use_container_width=True,
        hide_index=True,
    )

    chart_data = (
        recommender_comparison
        .set_index("Algorithm")[
            [
                "Hit Rate@5",
                "MRR@5",
                "Coverage@5",
            ]
        ]
    )

    st.bar_chart(
        chart_data
    )

    st.info(
        "Item-Based Collaborative Filtering achieved "
        "the highest Hit Rate@5 and 96.44% catalog "
        "coverage, making it the selected recommendation "
        "algorithm for this system."
    )


# ==================================================
# PURCHASE PREDICTION
# ==================================================

elif page == "Purchase Prediction":

    st.title(
        "🎯 Purchase Prediction"
    )

    st.write(
        "Estimate the probability that an e-commerce "
        "session will result in a purchase."
    )

    purchase_model = load_purchase_model()

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:

        device_type = st.selectbox(
            "Device Type",
            sorted(
                df["device_type"].unique()
            ),
        )

        user_type = st.selectbox(
            "User Type",
            sorted(
                df["user_type"].unique()
            ),
        )

        marketing_channel = st.selectbox(
            "Marketing Channel",
            sorted(
                df["marketing_channel"].unique()
            ),
        )

        product_category = st.selectbox(
            "Product Category",
            sorted(
                df["product_category"].unique()
            ),
        )

        unit_price = st.number_input(
            "Unit Price",
            min_value=float(
                df["unit_price"].min()
            ),
            max_value=float(
                df["unit_price"].max()
            ),
            value=float(
                df["unit_price"].median()
            ),
        )

    with col2:

        quantity = st.number_input(
            "Quantity",
            min_value=1,
            max_value=int(
                df["quantity"].max()
            ),
            value=1,
        )

        discount_percent = st.number_input(
            "Discount Percent",
            min_value=0,
            max_value=int(
                df["discount_percent"].max()
            ),
            value=0,
        )

        discount_amount = st.number_input(
            "Discount Amount",
            min_value=0.0,
            max_value=float(
                df["discount_amount"].max()
            ),
            value=0.0,
        )

        pages_viewed = st.number_input(
            "Pages Viewed",
            min_value=1,
            max_value=int(
                df["pages_viewed"].max()
            ),
            value=10,
        )

        time_on_site_sec = st.number_input(
            "Time on Site (Seconds)",
            min_value=int(
                df["time_on_site_sec"].min()
            ),
            max_value=int(
                df["time_on_site_sec"].max()
            ),
            value=900,
        )

    with col3:

        visit_day = st.number_input(
            "Visit Day",
            min_value=1,
            max_value=31,
            value=15,
        )

        visit_month = st.number_input(
            "Visit Month",
            min_value=1,
            max_value=12,
            value=6,
        )

        visit_weekday = st.number_input(
            "Visit Weekday",
            min_value=0,
            max_value=6,
            value=3,
        )

        visit_season = st.number_input(
            "Visit Season",
            min_value=0,
            max_value=3,
            value=1,
        )

        location = st.number_input(
            "Location Code",
            min_value=int(
                df["location"].min()
            ),
            max_value=int(
                df["location"].max()
            ),
            value=int(
                df["location"].median()
            ),
        )

    st.divider()

    if st.button(
        "Predict Purchase",
        type="primary",
        use_container_width=True,
    ):

        input_data = pd.DataFrame(
            [
                {
                    "device_type": device_type,
                    "user_type": user_type,
                    "marketing_channel": marketing_channel,
                    "product_category": product_category,
                    "unit_price": unit_price,
                    "quantity": quantity,
                    "discount_percent": discount_percent,
                    "discount_amount": discount_amount,
                    "pages_viewed": pages_viewed,
                    "time_on_site_sec": time_on_site_sec,
                    "visit_day": visit_day,
                    "visit_month": visit_month,
                    "visit_weekday": visit_weekday,
                    "visit_season": visit_season,
                    "location": location,
                }
            ],
            columns=PURCHASE_FEATURES,
        )

        prediction = (
            purchase_model.predict(
                input_data
            )[0]
        )

        prediction_probability = (
            purchase_model.predict_proba(
                input_data
            )[0][1]
        )

        st.subheader(
            "Prediction Result"
        )

        result_col1, result_col2 = st.columns(2)

        with result_col1:

            if prediction == 1:

                st.success(
                    "Likely to Purchase"
                )

            else:

                st.warning(
                    "Not Likely to Purchase"
                )

        with result_col2:

            st.metric(
                "Purchase Probability",
                f"{prediction_probability * 100:.2f}%",
            )

        st.progress(
            float(
                prediction_probability
            )
        )

        st.caption(
            "The prediction model has limited discrimination "
            "(ROC-AUC 0.5611). The probability should be "
            "interpreted as a model estimate rather than a "
            "guaranteed purchase outcome."
        )


# ==================================================
# CUSTOMER SEGMENTATION
# ==================================================

elif page == "Customer Segmentation":

    st.title(
        "👥 Customer Segmentation"
    )

    st.write(
        "Explore customer groups identified using "
        "K-Means clustering."
    )

    st.divider()

    customer_ids = sorted(
        customer_segments[
            "customer_id"
        ].unique()
    )

    selected_customer = st.selectbox(
        "Select Customer ID",
        customer_ids,
    )

    customer_profile = (
        customer_segments[
            customer_segments["customer_id"]
            == selected_customer
        ]
        .iloc[0]
    )

    customer_cluster = int(
        customer_profile["cluster"]
    )

    st.subheader(
        f"Customer {selected_customer}"
    )

    if customer_cluster == 0:

        st.warning(
            "Segment: Low-Engagement / Low-Value Customer"
        )

    else:

        st.success(
            "Segment: High-Value / Purchasing Customer"
        )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Sessions",
        int(
            customer_profile[
                "total_sessions"
            ]
        ),
    )

    col2.metric(
        "Purchase Rate",
        f"{customer_profile['purchase_rate'] * 100:.2f}%",
    )

    col3.metric(
        "Total Purchases",
        int(
            customer_profile[
                "total_purchases"
            ]
        ),
    )

    col4.metric(
        "Total Revenue",
        f"{customer_profile['total_revenue']:.2f}",
    )

    col5, col6, col7, col8 = st.columns(4)

    col5.metric(
        "Avg Pages Viewed",
        f"{customer_profile['avg_pages_viewed']:.2f}",
    )

    col6.metric(
        "Avg Time on Site",
        f"{customer_profile['avg_time_on_site']:.2f} sec",
    )

    col7.metric(
        "Cart Add Rate",
        f"{customer_profile['cart_add_rate'] * 100:.2f}%",
    )

    col8.metric(
        "Cart Abandon Rate",
        f"{customer_profile['cart_abandon_rate'] * 100:.2f}%",
    )

    st.divider()

    st.subheader(
        "Customer Segment Profile"
    )

    st.dataframe(
        cluster_summary,
        use_container_width=True,
        hide_index=True,
    )

    if customer_cluster == 0:

        st.info(
            "Suggested Business Strategy: cart recovery "
            "campaigns, targeted discounts, retargeting, "
            "and purchase conversion offers."
        )

    else:

        st.info(
            "Suggested Business Strategy: personalized "
            "recommendations, loyalty rewards, cross-selling, "
            "and customer retention campaigns."
        )


# ==================================================
# PRODUCT RECOMMENDATION
# ==================================================

elif page == "Product Recommendation":

    st.title(
        "🎁 Personalized Product Recommendation"
    )

    st.write(
        "Generate Top-5 product recommendations using "
        "Item-Based Collaborative Filtering."
    )

    st.divider()

    interaction_matrix = (
        load_interaction_matrix()
    )

    item_similarity = (
        load_item_similarity()
    )

    popular_products = (
        load_popular_products()
    )

    customer_ids = sorted(
        interaction_matrix.index.tolist()
    )

    selected_customer = st.selectbox(
        "Select Customer ID",
        customer_ids,
    )

    customer_interactions = (
        interaction_matrix.loc[
            selected_customer
        ]
    )

    interacted_products = (
        customer_interactions[
            customer_interactions > 0
        ]
        .sort_values(
            ascending=False
        )
    )

    recommendations = recommend_products(
        selected_customer,
        interaction_matrix,
        item_similarity,
        popular_products,
        top_k=5,
    )

    st.subheader(
        f"Customer {selected_customer}"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            "### Previously Interacted Products"
        )

        interaction_table = pd.DataFrame(
            {
                "Product ID": (
                    interacted_products.index
                ),
                "Interaction Score": (
                    interacted_products.values
                ),
            }
        )

        st.dataframe(
            interaction_table,
            use_container_width=True,
            hide_index=True,
        )

    with col2:

        st.markdown(
            "### Recommended Products"
        )

        recommendation_table = pd.DataFrame(
            {
                "Rank": np.arange(
                    1,
                    len(recommendations) + 1,
                ),
                "Product ID": recommendations,
            }
        )

        st.dataframe(
            recommendation_table,
            use_container_width=True,
            hide_index=True,
        )

    st.divider()

    st.success(
        "Selected Model: Item-Based Collaborative Filtering"
    )

    st.write(
        "The recommender uses cosine similarity between "
        "product interaction vectors. Products similar to "
        "the customer's previously interacted products are "
        "ranked using weighted implicit interaction scores."
    )

    st.caption(
        "The dataset contains sparse customer-product "
        "interaction history. Evaluation produced a "
        "Hit Rate@5 of 0.0052 and Catalog Coverage@5 of "
        "96.44%. These results indicate limited purchase "
        "recovery but broad catalog exposure."
    )