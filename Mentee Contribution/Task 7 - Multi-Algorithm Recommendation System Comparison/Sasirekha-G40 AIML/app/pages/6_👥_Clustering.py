import streamlit as st
import joblib

st.title("👥 Customer Segmentation")

try:

    model = joblib.load(
        r"C:\Users\ELCOT\Desktop\Sasirekha-G40 AIML 7\models\kmeans_model.pkl"
    )

    st.success("K-Means Model Loaded")

except:

    st.error("Model not found")

st.write("""

Algorithm Used

✔ K-Means Clustering

Purpose

Customer Segmentation

""")

st.info(
    "Cluster prediction interface will be added later."
)