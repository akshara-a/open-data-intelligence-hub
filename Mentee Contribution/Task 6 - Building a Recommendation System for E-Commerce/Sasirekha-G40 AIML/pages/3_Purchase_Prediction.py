import streamlit as st
import joblib
import numpy as np

model=joblib.load("models/logistic_regression_model.pkl")

scaler=joblib.load("models/classification_scaler.pkl")

st.title("🛒 Purchase Prediction")

browse=st.number_input("Browsing Time",0.0)

cart=st.selectbox("Cart Addition",[0,1])

previous=st.number_input("Previous Purchases",0)

rating=st.slider("Rating",1,5)

price=st.number_input("Price",500,5000)

discount=st.selectbox("Discount",[0,1])

spending=st.number_input("Total Spending",0)

if st.button("Predict"):

    sample=np.array([[

        browse,

        cart,

        previous,

        rating,

        price,

        discount,

        spending

    ]])

    sample=scaler.transform(sample)

    prediction=model.predict(sample)

    probability=model.predict_proba(sample)

    if prediction[0]==1:

        st.success("Customer is likely to Purchase")

    else:

        st.error("Customer is unlikely to Purchase")

    st.metric(
    "Purchase Probability",

    f"{round(probability[0][1]*100,2)} %"
    )

    st.write("Purchase Probability")

    st.write(round(probability[0][1]*100,2),"%")

st.markdown("---")

st.caption(

"© 2026 Ecommerce Recommendation System | Built with Streamlit"

)