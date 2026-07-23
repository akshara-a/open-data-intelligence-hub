import streamlit as st
import pandas as pd
import joblib

# Load saved model and preprocessor
model = joblib.load("models/best_rf.pkl")
preprocessor = joblib.load("models/preprocessor.pkl")

st.title("🛒 Online Purchase Prediction")

st.write(
    "Enter customer browsing information to predict whether the customer is likely to make a purchase."
)

st.header("Customer Information")

Administrative = st.number_input("Administrative Pages", min_value=0, value=3)

Administrative_Duration = st.number_input(
    "Administrative Duration", min_value=0.0, value=50.0
)

Informational = st.number_input("Informational Pages", min_value=0, value=0)

Informational_Duration = st.number_input(
    "Informational Duration", min_value=0.0, value=0.0
)

ProductRelated = st.number_input("Product Related Pages", min_value=0, value=20)

ProductRelated_Duration = st.number_input(
    "Product Related Duration", min_value=0.0, value=500.0
)

BounceRates = st.number_input(
    "Bounce Rate",
    min_value=0.0,
    max_value=1.0,
    value=0.02,
)

ExitRates = st.number_input(
    "Exit Rate",
    min_value=0.0,
    max_value=1.0,
    value=0.05,
)

PageValues = st.number_input(
    "Page Value",
    min_value=0.0,
    value=0.0,
)

SpecialDay = st.slider(
    "Special Day",
    0.0,
    1.0,
    0.0
)

Month = st.selectbox(
    "Month",
    ["Feb", "Mar", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
)

OperatingSystems = st.selectbox(
    "Operating System",
    [1,2,3,4,5,6,7,8]
)

Browser = st.selectbox(
    "Browser",
    [1,2,3,4,5,6,7,8,9,10,11,12,13]
)

Region = st.selectbox(
    "Region",
    [1,2,3,4,5,6,7,8,9]
)

TrafficType = st.selectbox(
    "Traffic Type",
    list(range(1,21))
)

VisitorType = st.selectbox(
    "Visitor Type",
    ["Returning_Visitor","New_Visitor","Other"]
)

Weekend = st.checkbox("Weekend Visit")

TotalBrowsingTime = (
    Administrative_Duration
    + Informational_Duration
    + ProductRelated_Duration
)

TotalPagesVisited = (
    Administrative
    + Informational
    + ProductRelated
)

AvgProductPageTime = (
    ProductRelated_Duration /
    (ProductRelated + 1)
)

ExitBounceRatio = (
    ExitRates /
    (BounceRates + 0.0001)
)

ValuePerProduct = (
    PageValues /
    (ProductRelated + 1)
)

ReturningVisitor = (
    1 if VisitorType == "Returning_Visitor" else 0
)

HolidaySeason = (
    1 if Month in ["Nov","Dec"] else 0
)

input_data = pd.DataFrame({
    "Administrative":[Administrative],
    "Administrative_Duration":[Administrative_Duration],
    "Informational":[Informational],
    "Informational_Duration":[Informational_Duration],
    "ProductRelated":[ProductRelated],
    "ProductRelated_Duration":[ProductRelated_Duration],
    "BounceRates":[BounceRates],
    "ExitRates":[ExitRates],
    "PageValues":[PageValues],
    "SpecialDay":[SpecialDay],
    "Month":[Month],
    "OperatingSystems":[OperatingSystems],
    "Browser":[Browser],
    "Region":[Region],
    "TrafficType":[TrafficType],
    "VisitorType":[VisitorType],
    "Weekend":[Weekend],

    "TotalBrowsingTime":[TotalBrowsingTime],
    "TotalPagesVisited":[TotalPagesVisited],
    "AvgProductPageTime":[AvgProductPageTime],
    "ExitBounceRatio":[ExitBounceRatio],
    "ValuePerProduct":[ValuePerProduct],
    "ReturningVisitor":[ReturningVisitor],
    "HolidaySeason":[HolidaySeason]
})

if st.button("Predict"):

    processed = preprocessor.transform(input_data)

    prediction = model.predict(processed)[0]
    probability = model.predict_proba(processed)[0][1]

    if prediction:
        st.success("✅ Customer is likely to make a purchase.")
    else:
        st.error("❌ Customer is unlikely to make a purchase.")

    st.write(f"Purchase Probability: **{probability:.2%}**")