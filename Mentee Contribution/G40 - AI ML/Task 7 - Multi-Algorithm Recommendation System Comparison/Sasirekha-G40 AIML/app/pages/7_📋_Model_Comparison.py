import streamlit as st
import pandas as pd

st.title("📋 Model Comparison")

try:

    summary = pd.read_csv(
        r"C:\Users\ELCOT\Desktop\Sasirekha-G40 AIML 7\outputs\model_summary.csv"
    )

    st.dataframe(summary)

except:

    st.warning("Summary file not found.")