import streamlit as st
import joblib
import numpy as np

model = joblib.load("models/best_regression_model.pkl")

scaler = joblib.load("models/regression_scaler.pkl")

st.title("⭐ Rating Prediction")

price = st.number_input("Price",500,5000)

browsing = st.number_input("Browsing Time",0.0)

previous = st.number_input("Previous Purchases",0)

discount = st.selectbox("Discount Applied",[0,1])

age = st.slider("Age",18,60)

category = st.number_input("Category (Encoded)",0)

spending = st.number_input("Total Spending",0)

if st.button("Predict Rating"):

    sample=np.array([[

        price,

        browsing,

        previous,

        discount,

        age,

        category,

        spending

    ]])

    sample=scaler.transform(sample)

    prediction=model.predict(sample)
    
    st.metric(
    "Predicted Rating",
    round(prediction[0],2)
    )


    st.success(f"Predicted Rating : {prediction[0]:.2f}")
    
    st.markdown("---")

    st.caption(

    "© 2026 Ecommerce Recommendation System | Built with Streamlit"

    )