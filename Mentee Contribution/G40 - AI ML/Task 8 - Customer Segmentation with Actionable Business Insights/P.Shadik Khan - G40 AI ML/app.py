import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# --------------------------------------------------
# Page configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Customer Segmentation Dashboard",
    page_icon="📊",
    layout="wide"
)


# --------------------------------------------------
# Title
# --------------------------------------------------
st.title("📊 Customer Segmentation with Actionable Business Insights")

st.write(
    """
    This dashboard uses RFM analysis and K-Means clustering
    to group customers based on their purchasing behaviour.
    It also displays model performance and business recommendations.
    """
)


# --------------------------------------------------
# Load data
# --------------------------------------------------
@st.cache_data
def load_data():
    customer_data = pd.read_csv("reports/customer_segments.csv")
    cluster_data = pd.read_csv("reports/cluster_profile.csv")
    model_data = pd.read_csv("reports/model_comparison.csv")

    return customer_data, cluster_data, model_data


try:
    df, cluster_profile, model_comparison = load_data()

except FileNotFoundError as error:
    st.error(
        "Required report file is missing. "
        "Please run Task8.ipynb and create the files inside the reports folder."
    )
    st.code(str(error))
    st.stop()

except Exception as error:
    st.error("An error occurred while loading the project files.")
    st.code(str(error))
    st.stop()


# --------------------------------------------------
# Main metrics
# --------------------------------------------------
st.header("Project Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Customers",
        value=len(df)
    )

with col2:
    st.metric(
        label="Total Segments",
        value=df["Cluster"].nunique()
    )

with col3:
    total_revenue = df["TotalSpending"].sum()

    st.metric(
        label="Total Revenue",
        value=f"₹{total_revenue:,.0f}"
    )

with col4:
    average_spending = df["TotalSpending"].mean()

    st.metric(
        label="Average Spending",
        value=f"₹{average_spending:,.0f}"
    )


# --------------------------------------------------
# Customer dataset
# --------------------------------------------------
st.header("Customer Dataset")

st.dataframe(
    df,
    width="stretch"
)


# --------------------------------------------------
# Cluster filter
# --------------------------------------------------
st.header("Filter Customers by Cluster")

cluster_options = sorted(df["Cluster"].unique())

selected_cluster = st.selectbox(
    "Select Cluster",
    cluster_options
)

filtered_df = df[
    df["Cluster"] == selected_cluster
]

st.write(
    f"Customers available in Cluster {selected_cluster}: "
    f"{len(filtered_df)}"
)

st.dataframe(
    filtered_df,
    width="stretch"
)


# --------------------------------------------------
# Cluster-wise customer count
# --------------------------------------------------
st.header("Cluster-wise Customer Count")

cluster_counts = (
    df["Cluster"]
    .value_counts()
    .sort_index()
)

fig1, ax1 = plt.subplots(figsize=(8, 5))

ax1.bar(
    cluster_counts.index.astype(str),
    cluster_counts.values
)

ax1.set_title("Customer Count by Cluster")
ax1.set_xlabel("Cluster")
ax1.set_ylabel("Number of Customers")

for index, value in enumerate(cluster_counts.values):
    ax1.text(
        index,
        value,
        str(value),
        ha="center",
        va="bottom"
    )

st.pyplot(fig1)

plt.close(fig1)


# --------------------------------------------------
# Average spending by cluster
# --------------------------------------------------
st.header("Cluster-wise Average Spending")

cluster_average_spending = (
    df.groupby("Cluster")["TotalSpending"]
    .mean()
    .sort_index()
)

fig2, ax2 = plt.subplots(figsize=(8, 5))

ax2.bar(
    cluster_average_spending.index.astype(str),
    cluster_average_spending.values
)

ax2.set_title("Average Spending by Cluster")
ax2.set_xlabel("Cluster")
ax2.set_ylabel("Average Total Spending")

for index, value in enumerate(cluster_average_spending.values):
    ax2.text(
        index,
        value,
        f"₹{value:,.0f}",
        ha="center",
        va="bottom"
    )

st.pyplot(fig2)

plt.close(fig2)


# --------------------------------------------------
# Purchase frequency by cluster
# --------------------------------------------------
st.header("Cluster-wise Purchase Frequency")

cluster_frequency = (
    df.groupby("Cluster")["PurchaseFrequency"]
    .mean()
    .sort_index()
)

fig3, ax3 = plt.subplots(figsize=(8, 5))

ax3.bar(
    cluster_frequency.index.astype(str),
    cluster_frequency.values
)

ax3.set_title("Average Purchase Frequency by Cluster")
ax3.set_xlabel("Cluster")
ax3.set_ylabel("Average Purchase Frequency")

for index, value in enumerate(cluster_frequency.values):
    ax3.text(
        index,
        value,
        f"{value:.1f}",
        ha="center",
        va="bottom"
    )

st.pyplot(fig3)

plt.close(fig3)


# --------------------------------------------------
# Recency vs frequency scatter plot
# --------------------------------------------------
st.header("Recency vs Purchase Frequency")

fig4, ax4 = plt.subplots(figsize=(9, 6))

scatter = ax4.scatter(
    df["DaysSinceLastPurchase"],
    df["PurchaseFrequency"],
    c=df["Cluster"],
    s=80,
    alpha=0.8
)

ax4.set_title("Customer Segments")
ax4.set_xlabel("Days Since Last Purchase")
ax4.set_ylabel("Purchase Frequency")

legend = ax4.legend(
    *scatter.legend_elements(),
    title="Cluster"
)

ax4.add_artist(legend)

st.pyplot(fig4)

plt.close(fig4)


# --------------------------------------------------
# Spending vs frequency scatter plot
# --------------------------------------------------
st.header("Spending vs Purchase Frequency")

fig5, ax5 = plt.subplots(figsize=(9, 6))

scatter2 = ax5.scatter(
    df["PurchaseFrequency"],
    df["TotalSpending"],
    c=df["Cluster"],
    s=80,
    alpha=0.8
)

ax5.set_title("Spending and Purchase Frequency")
ax5.set_xlabel("Purchase Frequency")
ax5.set_ylabel("Total Spending")

legend2 = ax5.legend(
    *scatter2.legend_elements(),
    title="Cluster"
)

ax5.add_artist(legend2)

st.pyplot(fig5)

plt.close(fig5)


# --------------------------------------------------
# Cluster profile
# --------------------------------------------------
st.header("Cluster Profile")

st.dataframe(
    cluster_profile,
    width="stretch"
)


# --------------------------------------------------
# Revenue contribution
# --------------------------------------------------
st.header("Revenue Contribution by Cluster")

revenue_contribution = (
    df.groupby("Cluster")["TotalSpending"]
    .sum()
    .reset_index()
)

revenue_contribution["RevenuePercentage"] = (
    revenue_contribution["TotalSpending"]
    / revenue_contribution["TotalSpending"].sum()
    * 100
)

st.dataframe(
    revenue_contribution,
    width="stretch"
)


# --------------------------------------------------
# Model comparison
# --------------------------------------------------
st.header("Model Comparison")

st.dataframe(
    model_comparison,
    width="stretch"
)


# --------------------------------------------------
# Business recommendations
# --------------------------------------------------
st.header("Business Recommendations")

st.subheader("1. High-Value Loyal Customers")

st.write(
    """
    These customers purchase frequently, spend more money,
    and have purchased recently.
    """
)

st.markdown(
    """
    - Provide loyalty rewards.
    - Offer premium membership benefits.
    - Give early access to new products.
    - Avoid unnecessary discounts.
    """
)


st.subheader("2. New and Promising Customers")

st.write(
    """
    These customers recently joined and show good engagement,
    but their purchase frequency is still developing.
    """
)

st.markdown(
    """
    - Send personalized welcome offers.
    - Recommend popular products.
    - Encourage a second purchase.
    - Send onboarding campaigns.
    """
)


st.subheader("3. Discount-Driven Customers")

st.write(
    """
    These customers mainly purchase during promotional campaigns
    and discount periods.
    """
)

st.markdown(
    """
    - Send limited-time discounts.
    - Recommend bundled products.
    - Target them during sales campaigns.
    - Avoid unnecessary discounts outside campaign periods.
    """
)


st.subheader("4. At-Risk Customers")

st.write(
    """
    These customers previously purchased but have not purchased recently.
    """
)

st.markdown(
    """
    - Run re-engagement campaigns.
    - Offer personalized comeback incentives.
    - Request customer feedback.
    - Highlight newly launched products.
    """
)


st.subheader("5. Low-Engagement Customers")

st.write(
    """
    These customers have low spending, low purchase frequency,
    and limited activity.
    """
)

st.markdown(
    """
    - Use low-cost email campaigns.
    - Promote entry-level products.
    - Avoid expensive advertising campaigns.
    - Review whether this segment should remain a priority.
    """
)


# --------------------------------------------------
# Selected cluster details
# --------------------------------------------------
st.header("Selected Cluster Summary")

selected_cluster_data = df[
    df["Cluster"] == selected_cluster
]

summary_col1, summary_col2, summary_col3 = st.columns(3)

with summary_col1:
    st.metric(
        "Customers",
        len(selected_cluster_data)
    )

with summary_col2:
    st.metric(
        "Average Spending",
        f"₹{selected_cluster_data['TotalSpending'].mean():,.0f}"
    )

with summary_col3:
    st.metric(
        "Average Purchase Frequency",
        f"{selected_cluster_data['PurchaseFrequency'].mean():.1f}"
    )


# --------------------------------------------------
# Footer
# --------------------------------------------------
st.divider()

st.success(
    "Customer Segmentation Dashboard loaded successfully."
)