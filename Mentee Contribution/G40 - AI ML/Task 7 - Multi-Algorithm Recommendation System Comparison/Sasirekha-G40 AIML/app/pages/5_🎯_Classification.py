import streamlit as st
import joblib

st.title("🎯 Purchase Prediction")

try:

    model = joblib.load(
        r"C:\Users\ELCOT\Desktop\Sasirekha-G40 AIML 7\models\best_logistic_model.pkl"
    )

    st.success("Classification Model Loaded")

except:

    st.error("Model Not Found")

st.write("""

Algorithm:

✔ Logistic Regression

Target:

Purchase Status

""")

st.info(
    "Interactive prediction form will be added later."
)