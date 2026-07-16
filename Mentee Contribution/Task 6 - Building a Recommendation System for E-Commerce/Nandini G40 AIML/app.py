
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os
from sklearn.metrics import confusion_matrix
st.set_page_config(
    page_title="E-Commerce dashboard",
    page_icon="🛒" 
)
DATA_PATH = "dataset/e-commerce-data.csv"
MODEL_PATH = "Models"
@st.cache_data
def load_data():
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    return None
df = load_data()
def load_model(filename):
    path = os.path.join(
        MODEL_PATH,
        filename
    )
    if os.path.exists(path):
        return joblib.load(path)
    return None
regression_model = load_model(
    "regression_model.pkl"
)
rating_scaler = load_model(
    "rating_scaler.pkl"
)
logistic_model = load_model(
    "logistic_model.pkl"
)
purchase_scaler = load_model(
    "purchase_scaler.pkl"
)
kmeans_model = load_model(
    "kmeans_model.pkl"
)
cluster_scaler = load_model(
    "cluster_scaler.pkl"
)
st.title(
    "🛒 E-Commerce Recommendation System"
)
st.sidebar.title(
    "Navigation"
)
page = st.sidebar.radio(
    "Go To",
    [
        "Home",
        "Dataset & EDA",
        "Rating Prediction",
        "Purchase Prediction",
        "Customer Segmentation",
    ]

)
if page == "Home":
    st.header(
        "Introduction"
    )
    st.write(
        """
        This project aims to build an intelligent e-commerce
        recommendation system using Machine Learning.

        The system analyzes customer behaviour,
        product ratings, purchase history and spending patterns
        to provide personalized recommendations.
        """
    )
    st.header(
        "Business Scenario"
    )
    st.write(
        """
        An e-commerce company wants to improve product
        recommendations and understand customer behaviour.
        Machine Learning helps the business:
        • Predict customer ratings
        • Predict purchase likelihood
        • Segment customers
        • Improve marketing strategies
        """
    )
    st.header(
        "Objectives"
    )
    st.write(
        """
        ✔ Regression - Predict product ratings
        ✔ Classification - Predict purchase probability 
       ✔ Clustering - Create customer segments
        ✔ Hyperparameter optimization
        ✔ Model evaluation using suitable metrics
        """
    )
elif page == "Dataset & EDA":
    st.header(
        "📊 Dataset Overview"
    )
    if df is not None:
        st.success(
            "Dataset Loaded Successfully"
        )
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                "Total Rows",
                df.shape[0]
            )
        with col2:
            st.metric(
                "Total Columns",
                df.shape[1]
            )
        st.subheader(
            "Dataset Preview"
        )
        st.dataframe(
            df.head()
        )
        st.subheader(
            "Dataset Description"
        )
        st.write(
            df.describe()
        )
        st.subheader(
            "Missing Values"
        )
        missing = pd.DataFrame(
            {
                "Column": df.columns,
                "Missing Values": df.isnull().sum()
            }
        )
        st.dataframe(
            missing
        )
        st.subheader(
            "Most Purchased Product Categories"
        )
        fig, ax = plt.subplots(
            figsize=(8,5)
        )
        df["Category"].value_counts().plot(

            kind="bar",
            ax=ax
        )
        ax.set_xlabel(
            "Category"
        )
        ax.set_ylabel(
            "Count"
        )
        st.pyplot(
            fig
        )
        st.subheader(
            "Average Rating by Category"
        )
        fig, ax = plt.subplots(
            figsize=(8,5)
        )
        df.groupby(
            "Category"
        )["Rating"].mean().plot(
            kind="bar",
            ax=ax
        )
        ax.set_ylabel(
            "Average Rating"
        )
        st.pyplot(
            fig
        )
        st.subheader(
            "Browsing Time vs Purchase Status"
        )
        fig, ax = plt.subplots(
            figsize=(8,5)
        )
        df.groupby(
            "Purchase_Status"
        )["Browsing_Time"].mean().plot(

            kind="bar",
            ax=ax
        )
        ax.set_xlabel(
            "Purchase Status"
        )
        ax.set_ylabel(
            "Average Browsing Time"
        )
        st.pyplot(
            fig
        )
        st.subheader(
            "Customer Spending Distribution"
        )
        fig, ax = plt.subplots(
            figsize=(8,5)
        )
        ax.hist(
            df["Total_Spending"],
            bins=20
        )
        ax.set_xlabel(
            "Total Spending"
        )
        ax.set_ylabel(
            "Frequency"
        )
        st.pyplot(
            fig
        )
        st.subheader(
            "Purchase Rate by Discount Usage"
        )
        fig, ax = plt.subplots(
            figsize=(8,5)
        )
        df.groupby(
            "Discount_Applied"
        )["Purchase_Status"].mean().plot(
            kind="bar",
            ax=ax
        )
        ax.set_ylabel(
            "Purchase Rate"
        )
        st.pyplot(
            fig
        )
        st.subheader(
            "Correlation Heatmap"
        )
        fig, ax = plt.subplots(
            figsize=(10,7)
        )
        sns.heatmap(
            df.corr(numeric_only=True),
            annot=True,
            cmap="coolwarm",
            ax=ax
        )
        st.pyplot(
            fig
        )
    else:
        st.error(
            "Dataset not found. Check dataset folder."
        )


elif page == "Rating Prediction":
    st.header(
        "⭐ Regression - Rating Prediction"
    )
    st.write(
        """
        Linear Regression predicts the rating a customer
        may give to a product.
        """
    )
    col1, col2 = st.columns(2)
    with col1:
        price = st.number_input(
            "Price",
            min_value=0.0
        )
        browsing_time = st.number_input(
            "Browsing Time",
            min_value=0.0
        )
        previous_purchase = st.number_input(
            "Previous Purchases",
            min_value=0
        )
    with col2:
        discount = st.number_input(
            "Discount Applied",
            min_value=0
        )
        age = st.number_input(
            "Age",
            min_value=1
        )
        total_spending = st.number_input(
            "Total Spending",
            min_value=0.0
        )
    if st.button(
        "Predict Rating"
    ):
        if regression_model is not None and rating_scaler is not None:
            input_data = np.array(
                [[
                price,
                browsing_time,
                previous_purchase,
                discount,
                age,
                total_spending
                ]]

            )
            scaled_data = rating_scaler.transform(
                input_data
            )
            prediction = regression_model.predict(
                scaled_data
            )
            st.success(

                f"Predicted Rating: {prediction[0]:.2f} / 5"

            )
            st.info(
                """
                Regression Evaluation:
                MAE : 0.503
                RMSE : 0.589
                R² Score : 0.228
                """
            )

        else:
            st.error(
                "Regression model not found."
            )

elif page == "Purchase Prediction":
    st.header(
        "🛍 Classification - Purchase Likelihood Prediction"
    )
    st.write(
        """
        Logistic Regression predicts whether a customer
        is likely to purchase a product.
        """
    )
    col1, col2 = st.columns(2)
    with col1:
        browsing_time = st.number_input(
            "Browsing Time",
            min_value=0.0
        )       

        cart_addition = st.number_input(
            "Cart Addition",
            min_value=0
        )
        previous_purchase = st.number_input(
            "Previous Purchases",
            min_value=0
        )

        rating = st.number_input(
            "Rating",
            min_value=0.0,
            max_value=5.0
        )
    with col2:
        price = st.number_input(
            "Price",
            min_value=0.0
        )
        discount = st.number_input(
            "Discount Applied",
            min_value=0
        )
        total_spending = st.number_input(
            "Total Spending",
            min_value=0.0
        )
    if st.button(
        "Predict Purchase"
    ):
        if logistic_model is not None and purchase_scaler is not None:

            input_data = np.array(
                [[
                browsing_time,
                cart_addition,
                previous_purchase,
                rating,
                price,
                discount,
                total_spending
                ]]
            )
            scaled_input = purchase_scaler.transform(
                input_data
            )
            prediction = logistic_model.predict(
                scaled_input
            )
            probability = (
                logistic_model
                .predict_proba(scaled_input)[0][1]
                * 100
            )
            if prediction[0] == 1:
                st.success(
                    "Customer is likely to purchase ✅"
                )
            else:
                st.warning(
                    "Customer is unlikely to purchase ❌"
                )
            st.write(
                f"Purchase Probability: {probability:.2f}%"
            )
            st.info(
                """
                Classification Evaluation:
                Accuracy : 82.4%
                Precision : 85.8%
                Recall : 91.6%
                F1 Score : 88.6%
                ROC-AUC : 73.3%
               """
            )
            st.subheader(
                "Confusion Matrix"
            )
            X_cm = df[[
                "Browsing_Time",
                "Cart_Addition",
                "Previous_Purchases",
                "Rating",
                "Price",
                "Discount_Applied",
                "Total_Spending"
            ]]
            y_cm = df[
                "Purchase_Status"
            ]
            X_cm_scaled = purchase_scaler.transform(
                X_cm
            )
            y_cm_pred = logistic_model.predict(
                X_cm_scaled
            )
            cm = confusion_matrix(
                y_cm,
                y_cm_pred
            )
            fig, ax = plt.subplots(
                figsize=(5,4)
            )
            sns.heatmap(
                cm,
                annot=True,
                fmt="d",
                cmap="Blues",
                ax=ax
            )
            ax.set_xlabel(
                "Predicted"
            )
            ax.set_ylabel(
                "Actual"
            )
            ax.set_title(
                "Logistic Regression Confusion Matrix"
            )
            st.pyplot(
                fig
            )
        else:
            st.error(
                "Logistic model not found."
            )
elif page == "Customer Segmentation":
    st.header(
        "👥 Customer Segmentation - K-Means Clustering"
    )
    st.write(
      """
        K-Means clustering groups customers based on
        shopping behaviour.
        Customer Segments:
        • Frequent Buyers
        • Browsers with Low Purchases
        • Discount Sensitive Customers
        • High Value Customers
        """
    )
    col1, col2 = st.columns(2)
    with col1:
        browsing_time = st.number_input(
            "Browsing Time",
            min_value=0.0
        )
        previous_purchase = st.number_input(
            "Previous Purchases",
            min_value=0
        )
        rating = st.number_input(
            "Average Rating",
            min_value=0.0,
            max_value=5.0
        )
    with col2:
        total_spending = st.number_input(
            "Total Spending",
            min_value=0.0
        )
        cart_addition = st.number_input(
            "Cart Addition Count",
            min_value=0
        )
        discount_usage = st.number_input(
            "Discount Usage",
            min_value=0
        )
    if st.button(
        "Find Customer Segment"
    ):
        if kmeans_model is not None and cluster_scaler is not None:
            input_data = np.array(
                [[
                browsing_time,
                previous_purchase,
                rating,
                total_spending,
                cart_addition,
                discount_usage
                ]]
            )
            scaled_input = cluster_scaler.transform(
                input_data
            )
            cluster = kmeans_model.predict(
                scaled_input
            )[0]
            segment = {
                0:"Frequent Buyers",
                1:"Browsers with Low Purchases",
                2:"Discount Sensitive Customers",
                3:"High Value Customers"
            }
            st.success(
                f"Customer Segment: {segment.get(cluster)}"
            )
            st.info(
                """
                Clustering Evaluation:
                Number of Clusters: 4
                Inertia: 68997.48
                Silhouette Score: 0.2007"""
            )
        else:
            st.error(
                "K-Means model not found."
            )