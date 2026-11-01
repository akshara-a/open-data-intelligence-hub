import streamlit as st
from datetime import datetime

from utils.data_loader import *
from utils.charts import *

# --------------------------------------------------
# Load CSS
# --------------------------------------------------
def load_css():
    try:
        with open("assets/style.css") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )
    except FileNotFoundError:
        pass


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Customer Churn Analytics Hub",
    page_icon="📊",
    layout="wide"
)

load_css()

# --------------------------------------------------
# Load Dataset
# --------------------------------------------------
df = load_data()

# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------
st.sidebar.title("📊 Customer Analytics Hub")

st.sidebar.markdown("---")

st.sidebar.header("🔍 Filters")

gender = st.sidebar.selectbox(
    "Gender",
    ["All"] + sorted(df["Gender"].drop_nulls().unique().to_list())
)

city = st.sidebar.selectbox(
    "City Tier",
    ["All"] + [str(x) for x in sorted(df["CityTier"].unique().to_list())]
)

payment = st.sidebar.selectbox(
    "Payment Mode",
    ["All"] + sorted(
        df["PreferredPaymentMode"]
        .drop_nulls()
        .unique()
        .to_list()
    )
)

filtered_df = df

if gender != "All":
    filtered_df = filtered_df.filter(
        filtered_df["Gender"] == gender
    )

if city != "All":
    filtered_df = filtered_df.filter(
        filtered_df["CityTier"] == int(city)
    )

if payment != "All":
    filtered_df = filtered_df.filter(
        filtered_df["PreferredPaymentMode"] == payment
    )

# --------------------------------------------------
# Navigation
# --------------------------------------------------
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "📌 Navigation",
    [
        "Dashboard",
        "Dataset Overview",
        "Statistics",
        "Visualizations",
        "Business Insights"
    ]
)

st.sidebar.markdown("---")

st.sidebar.success("Powered by Polars + Streamlit")

st.sidebar.markdown(
"""
### 📖 About

Customer Churn Analytics Dashboard

Built using

- Streamlit
- Polars
- Plotly
- Pandas
"""
)

# ==================================================
# DASHBOARD
# ==================================================
if page == "Dashboard":

    st.title("📊 Customer Churn Analytics Hub")

    current_time = datetime.now()

    st.caption(
        f"📅 Report Generated : {current_time.strftime('%d-%m-%Y %I:%M %p')}"
    )

    st.success("Dashboard Loaded Successfully")

    st.info(
"""
Interactive Business Intelligence Dashboard
built using Polars + Streamlit + Plotly.
"""
    )

    st.progress(100)

    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "👥 Total Customers",
        total_customers(filtered_df)
    )

    c2.metric(
        "❌ Churn Customers",
        churn_customers(filtered_df)
    )

    c3.metric(
        "✅ Retained Customers",
        retained_customers(filtered_df)
    )

    c4.metric(
        "📈 Churn Rate",
        f"{churn_rate(filtered_df)}%"
    )

    st.divider()

    c5, c6, c7 = st.columns(3)

    c5.metric(
        "😊 Avg Satisfaction",
        average_satisfaction(filtered_df)
    )

    c6.metric(
        "💰 Avg Cashback",
        average_cashback(filtered_df)
    )

    c7.metric(
        "🛒 Avg Orders",
        average_orders(filtered_df)
    )

    st.divider()

    st.subheader("Current Filters")

    st.info(
f"""
Gender : **{gender}**

City Tier : **{city}**

Payment Mode : **{payment}**
"""
    )

    st.subheader("Dataset Summary")

    st.json({
        "Rows": filtered_df.height,
        "Columns": filtered_df.width,
        "Churn Rate": f"{churn_rate(filtered_df)}%",
        "Average Cashback": average_cashback(filtered_df)
    })

# ==================================================
# DATASET OVERVIEW
# ==================================================
elif page == "Dataset Overview":

    st.title("📂 Dataset Overview")

    st.success(
        f"Dataset contains **{filtered_df.height} rows** and **{filtered_df.width} columns**."
    )

    st.subheader("📋 Dataset Health")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Rows",
        filtered_df.height
    )

    col2.metric(
        "Columns",
        filtered_df.width
    )

    missing = (
        filtered_df
        .null_count()
        .sum_horizontal()
        .item()
    )

    col3.metric(
        "Missing Values",
        missing
    )

    st.divider()

    st.subheader("🚨 Missing Value Analysis")

    missing_df = (
        filtered_df
        .null_count()
        .transpose(
            include_header=True,
            header_name="Column",
            column_names=["Missing Values"]
        )
    )

    st.dataframe(
        missing_df.to_pandas(),
        width="stretch"
    )

    st.divider()

    st.subheader("🔍 Search Customer")

    search_id = st.text_input("Enter Customer ID")

    if search_id:

        result = filtered_df.filter(
            filtered_df["CustomerID"].cast(str) == search_id
        )

        st.dataframe(
            result.to_pandas(),
            width="stretch"
        )

    else:

        st.dataframe(
            filtered_df.head(10).to_pandas(),
            width="stretch"
        )

    csv = (
        filtered_df
        .to_pandas()
        .to_csv(index=False)
        .encode("utf-8")
    )

    st.download_button(
        "📥 Download Filtered Dataset",
        csv,
        "filtered_dataset.csv",
        "text/csv"
    )

    st.divider()

    st.subheader("Column Names")

    st.write(filtered_df.columns)

    with st.expander("📄 View Complete Dataset"):

        st.dataframe(
            filtered_df.to_pandas(),
            width="stretch"
        )

# ==================================================
# STATISTICS
# ==================================================
elif page == "Statistics":

    st.title("📊 Statistical Summary")

    st.info(
        "Summary statistics generated using Polars."
    )

    st.dataframe(
        filtered_df.describe().to_pandas(),
        width="stretch"
    )

# ==================================================
# VISUALIZATIONS
# ==================================================
elif page == "Visualizations":

    st.title("📉 Interactive Visualizations")

    st.caption(
        "Business insights generated from the E-Commerce dataset."
    )

    st.plotly_chart(
        churn_chart(filtered_df),
        width="stretch"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            gender_chart(filtered_df),
            width="stretch"
        )

    with col2:
        st.plotly_chart(
            payment_chart(filtered_df),
            width="stretch"
        )

    col3, col4 = st.columns(2)

    with col3:
        st.plotly_chart(
            city_chart(filtered_df),
            width="stretch"
        )

    with col4:
        st.plotly_chart(
            satisfaction_chart(filtered_df),
            width="stretch"
        )

    st.plotly_chart(
        cashback_chart(filtered_df),
        width="stretch"
    )

# ==================================================
# BUSINESS INSIGHTS
# ==================================================
elif page == "Business Insights":

    st.title("💡 Business Recommendations")

    st.success(
"""
✅ Encourage long-term subscriptions to reduce churn.
"""
    )

    st.info(
"""
ℹ Improve customer satisfaction through better support services.
"""
    )

    st.warning(
"""
⚠ Offer cashback and loyalty rewards to frequent customers.
"""
    )

    st.error(
"""
🚨 Monitor customers with complaints and fewer recent orders.
"""
    )

# ==================================================
# FOOTER
# ==================================================
st.markdown("---")

st.markdown(
"""
<div style='text-align:center;'>

Developed using ❤️ Streamlit • Polars • Plotly

<b>Customer Churn Analytics Hub</b>

</div>
""",
unsafe_allow_html=True
)