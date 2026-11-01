import streamlit as st
from utils.data_loader import load_data

st.title("📊 Dataset Overview")

filtered_df = load_data()

st.sidebar.header("Filters")

category = st.sidebar.multiselect(
    "Category",
    options=sorted(filtered_df["Category"].unique()),
    default=sorted(filtered_df["Category"].unique())
)

region = st.sidebar.multiselect(
    "Region",
    options=sorted(filtered_df["Region"].unique()),
    default=sorted(filtered_df["Region"].unique())
)

membership = st.sidebar.multiselect(
    "Membership",
    options=sorted(filtered_df["Membership"].unique()),
    default=sorted(filtered_df["Membership"].unique())
)

filtered_df = filtered_df[
    (filtered_df["Category"].isin(category))
    &
    (filtered_df["Region"].isin(region))
    &
    (filtered_df["Membership"].isin(membership))
]

st.subheader("Dataset Preview")
st.dataframe(filtered_df.head(10), use_container_width=True)

st.subheader("Dataset Shape")

col1, col2 = st.columns(2)

with col1:
    st.metric("Rows", filtered_df.shape[0])

with col2:
    st.metric("Columns", filtered_df.shape[1])

st.subheader("Column Information")

st.dataframe(
    filtered_df.dtypes.astype(str).reset_index().rename(
        columns={
            "index":"Column",
            0:"Data Type"
        }
    )
)

import plotly.express as px

st.subheader("Category Distribution")

fig = px.histogram(
    filtered_df,
    x="Category",
    color="Category"
)

st.plotly_chart(
    fig,
    use_container_width=True
)