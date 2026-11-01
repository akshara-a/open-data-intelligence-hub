import streamlit as st
import pandas as pd
import numpy as np

from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV

from sklearn.linear_model import Ridge, LogisticRegression
from sklearn.cluster import KMeans

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    silhouette_score
)

st.set_page_config(
    page_title="Multi-Algorithm Recommendation System",
    layout="wide"
)

st.title("🛒 Multi-Algorithm Recommendation System Comparison")
st.write("Task 7 - E-Commerce Machine Learning Project")

# -----------------------------
# Load Dataset
# -----------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("E-commerce Customer Behavior - Sheet1.csv")
    return df

df = load_data()

st.subheader("Dataset Preview")
st.dataframe(df.head())

st.write("Dataset Shape:", df.shape)

# -----------------------------
# Data Preprocessing
# -----------------------------

df = df.drop_duplicates()

encoder = LabelEncoder()

categorical_columns = [
    "Gender",
    "City",
    "Membership Type",
    "Discount Applied",
    "Satisfaction Level"
]

for col in categorical_columns:
    df[col] = encoder.fit_transform(df[col])

# ======================================================
# Ridge Regression
# ======================================================

st.header("1️⃣ Ridge Regression")

X_reg = df.drop(["Average Rating", "Customer ID"], axis=1)
y_reg = df["Average Rating"]

X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(
    X_reg,
    y_reg,
    test_size=0.2,
    random_state=42
)

scaler_reg = StandardScaler()

X_train_reg = scaler_reg.fit_transform(X_train_reg)
X_test_reg = scaler_reg.transform(X_test_reg)

ridge_grid = GridSearchCV(
    Ridge(),
    {"alpha": [0.01, 0.1, 1, 10, 100]},
    cv=5,
    scoring="r2"
)

ridge_grid.fit(X_train_reg, y_train_reg)

ridge = ridge_grid.best_estimator_

pred_reg = ridge.predict(X_test_reg)

mae = mean_absolute_error(y_test_reg, pred_reg)
rmse = np.sqrt(mean_squared_error(y_test_reg, pred_reg))
r2 = r2_score(y_test_reg, pred_reg)

col1, col2, col3 = st.columns(3)

col1.metric("MAE", round(mae,3))
col2.metric("RMSE", round(rmse,3))
col3.metric("R² Score", round(r2,3))

# ======================================================
# Logistic Regression
# ======================================================

st.header("2️⃣ Logistic Regression")

X_cls = df.drop(["Discount Applied", "Customer ID"], axis=1)
y_cls = df["Discount Applied"]

X_train_cls, X_test_cls, y_train_cls, y_test_cls = train_test_split(
    X_cls,
    y_cls,
    test_size=0.2,
    random_state=42
)

scaler_cls = StandardScaler()

X_train_cls = scaler_cls.fit_transform(X_train_cls)
X_test_cls = scaler_cls.transform(X_test_cls)

grid = GridSearchCV(
    LogisticRegression(random_state=42),
    {
        "C":[0.01,0.1,1,10],
        "solver":["liblinear","lbfgs"],
        "max_iter":[100,200,500]
    },
    cv=5,
    scoring="accuracy"
)

grid.fit(X_train_cls, y_train_cls)

log_model = grid.best_estimator_

pred_cls = log_model.predict(X_test_cls)

acc = accuracy_score(y_test_cls,pred_cls)
pre = precision_score(y_test_cls,pred_cls)
rec = recall_score(y_test_cls,pred_cls)
f1 = f1_score(y_test_cls,pred_cls)

c1,c2,c3,c4 = st.columns(4)

c1.metric("Accuracy",round(acc,3))
c2.metric("Precision",round(pre,3))
c3.metric("Recall",round(rec,3))
c4.metric("F1 Score",round(f1,3))

# ======================================================
# KMeans
# ======================================================

st.header("3️⃣ K-Means Customer Segmentation")

cluster_data = df[
    [
        "Age",
        "Total Spend",
        "Items Purchased",
        "Average Rating",
        "Days Since Last Purchase"
    ]
]

cluster_scaler = StandardScaler()

scaled_cluster = cluster_scaler.fit_transform(cluster_data)

kmeans = KMeans(
    n_clusters=3,
    random_state=42,
    n_init=10
)

clusters = kmeans.fit_predict(scaled_cluster)

df["Cluster"] = clusters

sil = silhouette_score(scaled_cluster,clusters)

st.metric("Silhouette Score",round(sil,3))

st.subheader("Cluster Distribution")

st.bar_chart(df["Cluster"].value_counts())

# ======================================================
# Interactive Prediction
# ======================================================

st.header("4️⃣ Predict Customer Rating")

gender = st.selectbox("Gender", [0, 1])

age = st.number_input("Age", 18, 80, 25)

city = st.selectbox("City", sorted(df["City"].unique()))

membership = st.selectbox("Membership Type", sorted(df["Membership Type"].unique()))

spend = st.number_input("Total Spend", 0.0, 5000.0, 500.0)

items = st.number_input("Items Purchased", 1, 50, 5)

discount = st.selectbox("Discount Applied", [0, 1])

days = st.number_input("Days Since Last Purchase", 0, 365, 20)

satisfaction = st.selectbox("Satisfaction Level", sorted(df["Satisfaction Level"].unique()))


if st.button("Predict Rating"):

    input_df = pd.DataFrame({
        "Gender":[gender],
        "Age":[age],
        "City":[city],
        "Membership Type":[membership],
        "Total Spend":[spend],
        "Items Purchased":[items],
        "Discount Applied":[discount],
        "Days Since Last Purchase":[days],
        "Satisfaction Level":[satisfaction]
    })

    input_scaled = scaler_reg.transform(input_df)

    prediction = ridge.predict(input_scaled)

    st.success(f"Predicted Average Rating : {prediction[0]:.2f}")

# ======================================================
# Comparison Table
# ======================================================

st.header("Model Comparison")

comparison = pd.DataFrame({
    "Task":[
        "Regression",
        "Classification",
        "Clustering"
    ],
    "Algorithm":[
        "Ridge Regression",
        "Logistic Regression",
        "KMeans"
    ],
    "Metric":[
        f"R² = {round(r2,3)}",
        f"Accuracy = {round(acc,3)}",
        f"Silhouette = {round(sil,3)}"
    ]
})

st.table(comparison)

st.success("Project Completed Successfully!")