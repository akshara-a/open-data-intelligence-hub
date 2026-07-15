import joblib
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Purchase Prediction",
    page_icon="🛒",
    layout="wide",
)

st.title("🛒 E-Commerce Purchase Prediction")
st.write(
    "Optimized Classification Model with Feature Importance Analysis"
)

DATA_PATH = "data/customer_purchase_data.csv"
MODEL_PATH = "outputs/best_purchase_model.pkl"

try:
    data = pd.read_csv(DATA_PATH)
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    st.error("Run generate_dataset.py and model.py before opening the app.")
    st.stop()

st.header("1. Dataset Overview")

column1, column2, column3 = st.columns(3)

column1.metric("Customers", data.shape[0])
column2.metric("Input Columns", data.shape[1] - 1)
column3.metric(
    "Purchase Rate",
    f"{data['Purchase'].mean() * 100:.2f}%",
)

st.dataframe(data.head(20), use_container_width=True)

st.header("2. Purchase Distribution")
st.bar_chart(data["Purchase"].value_counts())

st.header("3. Model Comparison")

model_results = pd.read_csv("outputs/model_comparison.csv")
st.dataframe(model_results, use_container_width=True)

st.header("4. Feature Importance")

feature_importance = pd.read_csv(
    "outputs/feature_importance.csv"
).head(10)

st.bar_chart(
    feature_importance.set_index("Feature")["Importance"]
)

st.header("5. Predict Customer Purchase")

column1, column2, column3 = st.columns(3)

with column1:
    age = st.number_input("Age", 18, 80, 25)
    gender = st.selectbox("Gender", ["Male", "Female"])
    device_type = st.selectbox(
        "Device Type",
        ["Mobile", "Desktop", "Tablet"],
    )
    traffic_source = st.selectbox(
        "Traffic Source",
        [
            "Search",
            "Social Media",
            "Email",
            "Direct",
            "Advertisement",
        ],
    )
    pages_viewed = st.number_input(
        "Pages Viewed",
        1,
        100,
        8,
    )

with column2:
    time_on_site = st.number_input(
        "Time on Site",
        0.0,
        120.0,
        10.0,
    )
    products_viewed = st.number_input(
        "Products Viewed",
        1,
        100,
        5,
    )
    cart_items = st.number_input(
        "Cart Items",
        0,
        30,
        2,
    )
    previous_purchases = st.number_input(
        "Previous Purchases",
        0,
        100,
        2,
    )
    average_order_value = st.number_input(
        "Average Order Value",
        0.0,
        100000.0,
        1500.0,
    )

with column3:
    discount_used = st.selectbox(
        "Discount Used",
        [0, 1],
        format_func=lambda value: "Yes" if value == 1 else "No",
    )
    email_clicked = st.selectbox(
        "Email Clicked",
        [0, 1],
        format_func=lambda value: "Yes" if value == 1 else "No",
    )
    ad_clicked = st.selectbox(
        "Advertisement Clicked",
        [0, 1],
        format_func=lambda value: "Yes" if value == 1 else "No",
    )
    days_since_last_visit = st.number_input(
        "Days Since Last Visit",
        0,
        365,
        10,
    )
    session_count = st.number_input(
        "Session Count",
        1,
        200,
        5,
    )

customer_input = pd.DataFrame(
    [
        {
            "Age": age,
            "Gender": gender,
            "DeviceType": device_type,
            "TrafficSource": traffic_source,
            "PagesViewed": pages_viewed,
            "TimeOnSite": time_on_site,
            "ProductsViewed": products_viewed,
            "CartItems": cart_items,
            "PreviousPurchases": previous_purchases,
            "AverageOrderValue": average_order_value,
            "DiscountUsed": discount_used,
            "EmailClicked": email_clicked,
            "AdClicked": ad_clicked,
            "DaysSinceLastVisit": days_since_last_visit,
            "SessionCount": session_count,
        }
    ]
)

if st.button("Predict Purchase"):
    prediction = model.predict(customer_input)[0]
    probability = model.predict_proba(customer_input)[0][1]

    st.metric(
        "Purchase Probability",
        f"{probability * 100:.2f}%",
    )

    if prediction == 1:
        st.success(
            "This customer is likely to make a purchase."
        )
    else:
        st.warning(
            "This customer is unlikely to make a purchase."
        )