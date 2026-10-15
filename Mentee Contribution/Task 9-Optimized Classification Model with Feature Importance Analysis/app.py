import streamlit as st
import numpy as np
import joblib



model = joblib.load(
    "models/heart_model.pkl"
)


scaler = joblib.load(
    "models/scaler.pkl"
)



st.title(
"Heart Disease Prediction System"
)



st.write(
"Optimized Classification Model with Feature Importance Analysis"
)



age = st.number_input(
"Age"
)


sex = st.number_input(
"Sex (0/1)"
)


cp = st.number_input(
"Chest Pain Type"
)


trestbps = st.number_input(
"Resting Blood Pressure"
)


chol = st.number_input(
"Cholesterol"
)


fbs = st.number_input(
"Fasting Blood Sugar"
)


restecg = st.number_input(
"Rest ECG"
)


thalach = st.number_input(
"Maximum Heart Rate"
)


exang = st.number_input(
"Exercise Angina"
)


oldpeak = st.number_input(
"Old Peak"
)


slope = st.number_input(
"Slope"
)


ca = st.number_input(
"Number of vessels"
)


thal = st.number_input(
"Thal"
)



if st.button("Predict"):


    data = np.array([

        age,
        sex,
        cp,
        trestbps,
        chol,
        fbs,
        restecg,
        thalach,
        exang,
        oldpeak,
        slope,
        ca,
        thal

    ]).reshape(1,-1)



    data = scaler.transform(data)



    result = model.predict(data)



    if result[0]==1:

        st.error(
        "High Risk of Heart Disease"
        )

    else:

        st.success(
        "Low Risk of Heart Disease"
        )