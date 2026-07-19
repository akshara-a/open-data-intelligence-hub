import streamlit as st
import pandas as pd

st.set_page_config(
page_title="Urbanization Analytics Engine",
page_icon="🏙️",
layout="wide"
)

st.title("🏙️ Urbanization Analytics Engine")

st.write("World Bank Urbanization Dataset Analysis")

# Load Dataset

df = pd.read_csv("data/urbanization_data.csv")

# Show Information

st.header("Dataset Preview")
st.dataframe(df.head(10))

st.header("Column Names")
st.write(list(df.columns))

st.header("Dataset Shape")
st.write(f"Rows: {df.shape[0]}")
st.write(f"Columns: {df.shape[1]}")

st.header("Data Types")
st.write(df.dtypes)

st.header("Summary Statistics")
st.write(df.describe(include="all"))
