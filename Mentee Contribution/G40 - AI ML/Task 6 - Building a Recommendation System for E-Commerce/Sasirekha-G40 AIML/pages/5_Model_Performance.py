import streamlit as st
import pandas as pd

st.title("📈 Model Performance")

st.subheader("Regression")

st.dataframe(pd.read_csv("reports/regression_results.csv"))

st.subheader("Classification")

st.dataframe(pd.read_csv("reports/classification_results.csv"))

st.subheader("Model Comparison")

st.dataframe(pd.read_csv("reports/model_comparison.csv"))

st.markdown("---")

st.caption(

"© 2026 Ecommerce Recommendation System | Built with Streamlit"

)