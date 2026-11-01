import streamlit as st
import joblib
import numpy as np

model=joblib.load("models/kmeans_model.pkl")

scaler=joblib.load("models/clustering_scaler.pkl")

st.title("👥 Customer Segmentation")

browse=st.number_input("Browsing Time",0.0)

previous=st.number_input("Previous Purchases",0)

spending=st.number_input("Total Spending",0)

rating=st.slider("Rating",1,5)

price=st.number_input("Price",500,5000)

if st.button("Predict Cluster"):

    sample=np.array([[

        browse,

        previous,

        spending,

        rating,

        price

    ]])

    sample=scaler.transform(sample)

    cluster=model.predict(sample)
    
    segments={

    0:"Frequent Buyer",

    1:"Window Shopper",

    2:"Premium Customer",

    3:"Discount Lover"

    }

    st.metric(

    "Customer Segment",

    segments.get(cluster[0],"Unknown")

    )

st.markdown("---")

st.caption(

"© 2026 Ecommerce Recommendation System | Built with Streamlit"

)