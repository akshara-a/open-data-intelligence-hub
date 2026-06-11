import streamlit as st
import pandas as pd

from utils.data_loader import load_data
from utils.analytics import athlete_summary

# Load data
df = load_data()

# Page config
st.set_page_config(page_title="Athlete Career Analytics", layout="wide")

st.title("🏃 Athlete Career Analytics Dashboard")

# Basic metrics
st.subheader("📊 Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Athletes", df["Name"].nunique())
col2.metric("Total Countries", df["region"].nunique())
col3.metric("Total Records", len(df))

st.divider()

# Athlete selection
st.subheader("🔍 Search Athlete")

athletes = sorted(df["Name"].dropna().unique())
selected_athlete = st.selectbox("Choose Athlete", athletes)

athlete_data = df[df["Name"] == selected_athlete]

st.write("### Athlete Data")
st.dataframe(athlete_data)

st.divider()

# Optional: summary function (if exists)
try:
    st.subheader("📈 Athlete Summary")
    summary = athlete_summary(df, selected_athlete)
    st.write(summary)
except Exception as e:
    st.warning("Summary function not available or has an issue.")