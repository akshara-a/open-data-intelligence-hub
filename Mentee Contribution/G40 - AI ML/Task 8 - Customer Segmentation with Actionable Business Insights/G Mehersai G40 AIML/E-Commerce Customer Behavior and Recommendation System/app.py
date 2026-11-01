from pathlib import Path

import pandas as pd
import streamlit as st


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="E-Commerce Customer Intelligence System",
    page_icon="🛒",
    layout="wide",
)


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent
DATA_PATH = PROJECT_ROOT / "data" / "Ecommerce.csv"
RESULT_PATH = PROJECT_ROOT / "outputs" / "results"


# --------------------------------------------------
# SAFE DATA LOADING
# --------------------------------------------------

@st.cache_data
def load_csv(filename, required=True):
    path = RESULT_PATH / filename

    if not path.exists():
        if required:
            st.error(f"Required project output not found: {path}")
            st.stop()
        return pd.DataFrame()

    return pd.read_csv(path)


@st.cache_data
def load_dataset():
    if not DATA_PATH.exists():
        st.error(f"Dataset not found: {DATA_PATH}")
        st.stop()

    return pd.read_csv(DATA_PATH)


# --------------------------------------------------
# LOAD FINAL PROJECT OUTPUTS
# --------------------------------------------------

df = load_dataset()
customer_segments = load_csv("customer_segments.csv")
cluster_summary = load_csv("cluster_summary.csv")
business_insights = load_csv("final_business_insights.csv")
final_recommender = load_csv("final_recommender_comparison.csv")
final_cart_models = load_csv("final_cart_conversion_comparison.csv")
final_recommendations = load_csv("final_recommendations.csv")

temporal_models = load_csv(
    "temporal_purchase_model_comparison.csv",
    required=False,
)
balancing_results = load_csv(
    "balancing_strategy_comparison.csv",
    required=False,
)


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def format_percent(value):
    if pd.isna(value):
        return "Not Available"
    return f"{float(value) * 100:.2f}%"


def format_score(value):
    if pd.isna(value):
        return "Not Available"
    return f"{float(value):.2f}"


def normalize_customer_id(value):
    try:
        number = float(value)
        if number.is_integer():
            return int(number)
    except (TypeError, ValueError):
        pass
    return value


def get_customer_recommendations(customer_id):
    customer_rows = final_recommendations[
        final_recommendations["customer_id"] == customer_id
    ].sort_values("rank")

    return customer_rows["recommended_product_id"].tolist()


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("E-Commerce Intelligence")
st.sidebar.caption(
    "Customer Behavior, Conversion, Recommendation, and Business Decision System"
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Executive Dashboard",
        "Customer Intelligence",
        "Customer Segmentation",
        "Cart Conversion",
        "Recommendation System",
        "Business Decision Engine",
    ],
)

st.sidebar.divider()

st.sidebar.info(
    "Final ML Pipeline\n\n"
    "Historical Feature Engineering\n\n"
    "K-Means Segmentation\n\n"
    "Class-Weighted Random Forest\n\n"
    "Item-Based Collaborative Filtering\n\n"
    "Business Decision Engine"
)


# ==================================================
# EXECUTIVE DASHBOARD
# ==================================================

if page == "Executive Dashboard":

    st.title("🛒 E-Commerce Customer Intelligence System")

    st.write(
        "An end-to-end machine learning and decision-support system "
        "for customer segmentation, future cart-conversion intelligence, "
        "personalized product recommendation, and business action planning."
    )

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("E-Commerce Sessions", f"{len(df):,}")
    col2.metric("Customers", f"{df['customer_id'].nunique():,}")
    col3.metric("Products", f"{df['product_id'].nunique():,}")
    col4.metric(
        "Production Recommendations",
        f"{len(final_recommendations):,}",
    )

    st.divider()

    st.subheader("Final Machine Learning Results")

    model1, model2, model3 = st.columns(3)

    with model1:
        st.markdown("### 👥 Customer Segmentation")
        st.success("K-Means Clustering")
        st.metric("Customer Profiles", f"{len(customer_segments):,}")
        st.metric("Behavioral Segments", customer_segments["cluster"].nunique())

    with model2:
        st.markdown("### 🎯 Cart Conversion")
        st.success("Class-Weighted Random Forest")
        st.metric("Future Conversion Recall", "95.34%")
        st.metric("F1 Score", "51.01%")

    with model3:
        st.markdown("### 🎁 Recommendation")
        st.success("Item-Based Collaborative Filtering")
        st.metric("Catalog Coverage@5", "97.33%")
        st.metric("Unique Products Recommended", "875")

    st.divider()

    st.subheader("Customer Segment Distribution")

    segment_counts = (
        business_insights["customer_segment"]
        .value_counts()
        .rename_axis("Customer Segment")
        .reset_index(name="Customers")
    )

    st.dataframe(
        segment_counts,
        use_container_width=True,
        hide_index=True,
    )

    st.bar_chart(
        segment_counts.set_index("Customer Segment")
    )

    st.divider()

    st.subheader("Business Priority Distribution")

    priority_counts = (
        business_insights["business_priority"]
        .value_counts()
        .rename_axis("Business Priority")
        .reset_index(name="Customers")
    )

    st.dataframe(
        priority_counts,
        use_container_width=True,
        hide_index=True,
    )

    st.bar_chart(
        priority_counts.set_index("Business Priority")
    )

    st.info(
        "The final system converts machine learning outputs into customer-level "
        "business priorities, marketing actions, discount strategies, product "
        "recommendations, risk classifications, and opportunity scores."
    )


# ==================================================
# CUSTOMER INTELLIGENCE
# ==================================================

elif page == "Customer Intelligence":

    st.title("🔎 Customer Intelligence Search")

    st.write(
        "Select a customer to view the final customer-level intelligence "
        "generated by the business decision engine."
    )

    st.divider()

    customer_ids = sorted(
        business_insights["customer_id"]
        .map(normalize_customer_id)
        .unique()
        .tolist()
    )

    selected_customer = st.selectbox(
        "Select Customer ID",
        customer_ids,
    )

    customer_row = business_insights[
        business_insights["customer_id"] == selected_customer
    ]

    if customer_row.empty:
        customer_row = business_insights[
            business_insights["customer_id"].astype(str)
            == str(selected_customer)
        ]

    if customer_row.empty:
        st.warning("Customer intelligence record not found.")
    else:
        customer = customer_row.iloc[0]

        st.subheader(f"Customer {selected_customer}")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Customer Segment",
            str(customer["customer_segment"]),
        )
        col2.metric(
            "Customer Risk",
            str(customer["customer_risk"]),
        )
        col3.metric(
            "Business Priority",
            str(customer["business_priority"]),
        )
        col4.metric(
            "Opportunity Score",
            format_score(customer["business_opportunity_score"]),
        )

        st.divider()

        col5, col6, col7 = st.columns(3)

        has_score = customer.get("has_cart_conversion_score", False)
        probability = customer.get("cart_conversion_probability")

        with col5:
            st.markdown("### 🎯 Conversion Intelligence")
            if bool(has_score) and pd.notna(probability):
                st.metric(
                    "Cart Conversion Probability",
                    format_percent(probability),
                )
                st.progress(
                    min(max(float(probability), 0.0), 1.0)
                )
            else:
                st.info(
                    "No future cart-conversion score is available for this customer."
                )

        with col6:
            st.markdown("### 📣 Marketing Action")
            st.success(str(customer["marketing_action"]))
            st.write(
                f"**Discount Strategy:** "
                f"{customer['discount_strategy']}"
            )

        with col7:
            st.markdown("### 🎁 Recommendation Strategy")
            st.success(str(customer["recommendation_strategy"]))

            recommendations = get_customer_recommendations(
                selected_customer
            )

            if recommendations:
                st.write(
                    "**Top-5 Products:** "
                    + ", ".join(map(str, recommendations))
                )
            else:
                st.write(
                    f"**Top-5 Products:** "
                    f"{customer.get('recommended_products', 'Not Available')}"
                )

        st.divider()

        st.subheader("Customer Business Decision Record")

        display_columns = [
            column
            for column in [
                "customer_id",
                "customer_segment",
                "customer_risk",
                "business_priority",
                "marketing_action",
                "discount_strategy",
                "recommendation_strategy",
                "recommended_products",
                "cart_conversion_probability",
                "business_opportunity_score",
            ]
            if column in customer_row.columns
        ]

        st.dataframe(
            customer_row[display_columns],
            use_container_width=True,
            hide_index=True,
        )


# ==================================================
# CUSTOMER SEGMENTATION
# ==================================================

elif page == "Customer Segmentation":

    st.title("👥 Customer Segmentation")

    st.write(
        "Explore customer behavior segments identified using K-Means clustering."
    )

    st.divider()

    segment_counts = (
        business_insights["customer_segment"]
        .value_counts()
        .rename_axis("Customer Segment")
        .reset_index(name="Customers")
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Segment Distribution")
        st.dataframe(
            segment_counts,
            use_container_width=True,
            hide_index=True,
        )
        st.bar_chart(
            segment_counts.set_index("Customer Segment")
        )

    with col2:
        st.subheader("Cluster Profile Summary")
        st.dataframe(
            cluster_summary,
            use_container_width=True,
            hide_index=True,
        )

    st.divider()

    customer_ids = sorted(
        customer_segments["customer_id"]
        .map(normalize_customer_id)
        .unique()
        .tolist()
    )

    selected_customer = st.selectbox(
        "Inspect Customer ID",
        customer_ids,
    )

    profile_rows = customer_segments[
        customer_segments["customer_id"] == selected_customer
    ]

    if profile_rows.empty:
        profile_rows = customer_segments[
            customer_segments["customer_id"].astype(str)
            == str(selected_customer)
        ]

    profile = profile_rows.iloc[0]

    cluster = int(profile["cluster"])

    if cluster == 0:
        st.warning("Segment: Low-Engagement Customers")
    else:
        st.success("Segment: High-Value Purchasing Customers")

    metric1, metric2, metric3, metric4 = st.columns(4)

    metric1.metric(
        "Total Sessions",
        int(profile["total_sessions"]),
    )
    metric2.metric(
        "Purchase Rate",
        format_percent(profile["purchase_rate"]),
    )
    metric3.metric(
        "Total Purchases",
        int(profile["total_purchases"]),
    )
    metric4.metric(
        "Total Revenue",
        f"{float(profile['total_revenue']):,.2f}",
    )

    metric5, metric6, metric7, metric8 = st.columns(4)

    metric5.metric(
        "Avg Pages Viewed",
        f"{float(profile['avg_pages_viewed']):.2f}",
    )
    metric6.metric(
        "Avg Time on Site",
        f"{float(profile['avg_time_on_site']):.2f} sec",
    )
    metric7.metric(
        "Cart Add Rate",
        format_percent(profile["cart_add_rate"]),
    )
    metric8.metric(
        "Cart Abandon Rate",
        format_percent(profile["cart_abandon_rate"]),
    )


# ==================================================
# CART CONVERSION
# ==================================================

elif page == "Cart Conversion":

    st.title("🎯 Future Cart Conversion Intelligence")

    st.write(
        "Review the final temporal cart-conversion model and balancing experiments."
    )

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Selected Model", "Class-Weighted RF")
    col2.metric("Recall", "95.34%")
    col3.metric("F1 Score", "51.01%")
    col4.metric("Locked Threshold", "0.41")

    st.warning(
        "The model is recall-oriented. It prioritizes identifying future cart "
        "conversions and therefore produces more false positives. Accuracy alone "
        "is not used as the primary selection metric."
    )

    st.divider()

    st.subheader("Final Cart Conversion Model Comparison")

    display_cart = final_cart_models.copy()

    numeric_columns = display_cart.select_dtypes(
        include="number"
    ).columns

    display_cart[numeric_columns] = (
        display_cart[numeric_columns].round(4)
    )

    st.dataframe(
        display_cart,
        use_container_width=True,
        hide_index=True,
    )

    chart_columns = [
        column
        for column in [
            "Balanced Accuracy",
            "Precision",
            "Recall",
            "F1 Score",
            "ROC-AUC",
            "PR-AUC",
        ]
        if column in final_cart_models.columns
    ]

    st.bar_chart(
        final_cart_models
        .set_index("Strategy")[chart_columns]
    )

    if not balancing_results.empty:
        st.divider()
        st.subheader("Balancing Strategy Experiment")

        display_balancing = balancing_results.copy()
        numeric_columns = display_balancing.select_dtypes(
            include="number"
        ).columns
        display_balancing[numeric_columns] = (
            display_balancing[numeric_columns].round(4)
        )

        st.dataframe(
            display_balancing,
            use_container_width=True,
            hide_index=True,
        )

    if not temporal_models.empty:
        st.divider()
        st.subheader("Temporal Purchase Model Experiment")
        st.dataframe(
            temporal_models.round(4),
            use_container_width=True,
            hide_index=True,
        )


# ==================================================
# RECOMMENDATION SYSTEM
# ==================================================

elif page == "Recommendation System":

    st.title("🎁 Personalized Product Recommendation")

    st.write(
        "Explore the standardized recommender evaluation and production Top-5 "
        "recommendations generated for every customer."
    )

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Selected Recommender", "Item-Based CF")
    col2.metric("Coverage@5", "97.33%")
    col3.metric("Evaluation Products", "875")
    col4.metric(
        "Production Recommendations",
        f"{len(final_recommendations):,}",
    )

    st.divider()

    st.subheader("Standardized Recommender Comparison")

    display_recommender = final_recommender.copy()

    numeric_columns = display_recommender.select_dtypes(
        include="number"
    ).columns

    display_recommender[numeric_columns] = (
        display_recommender[numeric_columns].round(6)
    )

    st.dataframe(
        display_recommender,
        use_container_width=True,
        hide_index=True,
    )

    chart_columns = [
        column
        for column in [
            "Hit Rate@5",
            "MRR@5",
            "Coverage@5",
        ]
        if column in final_recommender.columns
    ]

    st.bar_chart(
        final_recommender
        .set_index("Algorithm")[chart_columns]
    )

    st.divider()

    st.subheader("Customer Top-5 Recommendations")

    customer_ids = sorted(
        final_recommendations["customer_id"]
        .map(normalize_customer_id)
        .unique()
        .tolist()
    )

    selected_customer = st.selectbox(
        "Select Customer ID",
        customer_ids,
    )

    recommendations = final_recommendations[
        final_recommendations["customer_id"] == selected_customer
    ]

    if recommendations.empty:
        recommendations = final_recommendations[
            final_recommendations["customer_id"].astype(str)
            == str(selected_customer)
        ]

    recommendations = recommendations.sort_values("rank")

    st.dataframe(
        recommendations.rename(
            columns={
                "rank": "Rank",
                "recommended_product_id": "Recommended Product ID",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.success(
        "Production recommendation validation passed: all 8,442 customers "
        "receive exactly five unique recommendations, with no previously "
        "interacted products included."
    )

    st.caption(
        "Offline Top-5 ranking metrics remain low because the interaction "
        "dataset is sparse. The selected Item-Based CF model achieved the "
        "strongest standardized Hit Rate@5 and MRR@5 while maintaining "
        "97.33% catalog coverage."
    )


# ==================================================
# BUSINESS DECISION ENGINE
# ==================================================

elif page == "Business Decision Engine":

    st.title("💼 Business Decision Engine")

    st.write(
        "Translate customer behavior, segmentation, cart-conversion intelligence, "
        "and product recommendations into actionable business decisions."
    )

    st.divider()

    priority_counts = (
        business_insights["business_priority"]
        .value_counts()
        .rename_axis("Business Priority")
        .reset_index(name="Customers")
    )

    action_counts = (
        business_insights["marketing_action"]
        .value_counts()
        .rename_axis("Marketing Action")
        .reset_index(name="Customers")
    )

    risk_counts = (
        business_insights["customer_risk"]
        .value_counts()
        .rename_axis("Customer Risk")
        .reset_index(name="Customers")
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Business Priorities")
        st.dataframe(
            priority_counts,
            use_container_width=True,
            hide_index=True,
        )

    with col2:
        st.subheader("Marketing Actions")
        st.dataframe(
            action_counts,
            use_container_width=True,
            hide_index=True,
        )

    with col3:
        st.subheader("Customer Risk")
        st.dataframe(
            risk_counts,
            use_container_width=True,
            hide_index=True,
        )

    st.divider()

    st.subheader("Top Business Opportunities")

    top_opportunities = (
        business_insights
        .sort_values(
            "business_opportunity_score",
            ascending=False,
        )
        .head(20)
    )

    opportunity_columns = [
        column
        for column in [
            "customer_id",
            "customer_segment",
            "cart_conversion_probability",
            "customer_risk",
            "business_priority",
            "marketing_action",
            "discount_strategy",
            "recommendation_strategy",
            "recommended_products",
            "business_opportunity_score",
        ]
        if column in top_opportunities.columns
    ]

    st.dataframe(
        top_opportunities[opportunity_columns],
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    st.subheader("Opportunity Score Distribution")

    st.bar_chart(
        business_insights["business_opportunity_score"]
        .round()
        .value_counts()
        .sort_index()
    )

    st.info(
        "The opportunity score ranks customers for business attention. "
        "It is a decision-support score built from customer behavior and "
        "model outputs; it should not be interpreted as a purchase probability."
    )
