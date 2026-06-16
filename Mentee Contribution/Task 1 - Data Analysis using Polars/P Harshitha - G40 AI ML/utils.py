import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    df = pd.read_csv("data/enrollment_data.csv")
    df.columns = df.columns.str.strip()
    if "enrollment_date" in df.columns:
        df["enrollment_date"] = pd.to_datetime(df["enrollment_date"])
    return df
