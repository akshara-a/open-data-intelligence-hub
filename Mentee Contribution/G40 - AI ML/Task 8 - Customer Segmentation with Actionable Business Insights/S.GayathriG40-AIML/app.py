import streamlit as st
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="Customer Segmentation Dashboard",
    layout="wide"
)

st.title("🛒 Customer Segmentation with Actionable Business Insights")

st.markdown("---")

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

@st.cache_data
def load_data():

    try:
        data = pd.read_csv("marketing_campaign.csv", sep="\t")
    except:
        data = pd.read_csv("marketing_campaign.csv")

    return data


df = load_data()

# ---------------------------------------------------------
# DATA CLEANING
# ---------------------------------------------------------

df.drop_duplicates(inplace=True)

df["Income"] = df["Income"].fillna(df["Income"].median())

current_year = 2026

df["Age"] = current_year - df["Year_Birth"]

df["Children"] = df["Kidhome"] + df["Teenhome"]

df["TotalSpending"] = (
    df["MntWines"]
    + df["MntFruits"]
    + df["MntMeatProducts"]
    + df["MntFishProducts"]
    + df["MntSweetProducts"]
    + df["MntGoldProds"]
)

# ---------------------------------------------------------
# LABEL ENCODING
# ---------------------------------------------------------

encoder = LabelEncoder()

df["Education"] = encoder.fit_transform(df["Education"])

df["Marital_Status"] = encoder.fit_transform(df["Marital_Status"])

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(

    "Select Page",

    [

        "Dataset",

        "EDA",

        "Clustering",

        "Regression",

        "Classification",

        "Business Insights"

    ]

)

# ---------------------------------------------------------
# DATASET PAGE
# ---------------------------------------------------------

if page == "Dataset":

    st.header("Dataset Overview")

    st.write(df.head())

    st.subheader("Dataset Shape")

    st.write(df.shape)

    st.subheader("Column Names")

    st.write(df.columns.tolist())

    st.subheader("Data Types")

    st.write(df.dtypes)

    st.subheader("Missing Values")

    st.write(df.isnull().sum())

# ---------------------------------------------------------
# EDA PAGE
# ---------------------------------------------------------

elif page == "EDA":

    st.header("Exploratory Data Analysis")

    st.subheader("Statistical Summary")

    st.write(df.describe())

    st.subheader("Customer Spending Distribution")

    fig = plt.figure(figsize=(8,5))

    plt.hist(df["TotalSpending"], bins=30)

    plt.xlabel("Total Spending")

    plt.ylabel("Customers")

    plt.title("Customer Spending Distribution")

    st.pyplot(fig)

    st.subheader("Income Distribution")

    fig = plt.figure(figsize=(8,5))

    plt.hist(df["Income"], bins=30)

    plt.xlabel("Income")

    plt.ylabel("Customers")

    plt.title("Income Distribution")

    st.pyplot(fig)

    st.subheader("Age Distribution")

    fig = plt.figure(figsize=(8,5))

    plt.hist(df["Age"], bins=25)

    plt.xlabel("Age")

    plt.ylabel("Customers")

    plt.title("Customer Age Distribution")

    st.pyplot(fig)

    st.subheader("Correlation Heatmap")

    corr = df.select_dtypes(include=np.number).corr()

    fig = plt.figure(figsize=(14,10))

    plt.imshow(corr)

    plt.colorbar()

    plt.xticks(

        range(len(corr.columns)),

        corr.columns,

        rotation=90

    )

    plt.yticks(

        range(len(corr.columns)),

        corr.columns

    )

    plt.tight_layout()

    st.pyplot(fig)
    # ---------------------------------------------------------
# CLUSTERING PAGE
# ---------------------------------------------------------

elif page == "Clustering":

    st.header("Customer Segmentation using K-Means")

    cluster_features = [

        "Income",
        "Recency",
        "TotalSpending",
        "NumWebPurchases",
        "NumStorePurchases",
        "NumCatalogPurchases",
        "NumDealsPurchases",
        "NumWebVisitsMonth",
        "Children",
        "Age"

    ]

    X = df[cluster_features]

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)

    st.subheader("Scaled Feature Matrix")

    st.write(pd.DataFrame(X_scaled, columns=cluster_features).head())

    # -----------------------------------------------------
    # ELBOW METHOD
    # -----------------------------------------------------

    st.subheader("Elbow Method")

    from sklearn.cluster import KMeans

    inertia = []

    K = range(2,11)

    for k in K:

        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10
        )

        model.fit(X_scaled)

        inertia.append(model.inertia_)

    fig = plt.figure(figsize=(8,5))

    plt.plot(K, inertia, marker="o")

    plt.xlabel("Number of Clusters")

    plt.ylabel("Inertia")

    plt.title("Elbow Method")

    st.pyplot(fig)

    # -----------------------------------------------------
    # SILHOUETTE SCORE
    # -----------------------------------------------------

    st.subheader("Silhouette Score")

    from sklearn.metrics import silhouette_score

    silhouette_scores = []

    for k in range(2,11):

        model = KMeans(

            n_clusters=k,

            random_state=42,

            n_init=10

        )

        labels = model.fit_predict(X_scaled)

        silhouette_scores.append(

            silhouette_score(

                X_scaled,

                labels

            )

        )

    fig = plt.figure(figsize=(8,5))

    plt.plot(

        range(2,11),

        silhouette_scores,

        marker="o"

    )

    plt.xlabel("Clusters")

    plt.ylabel("Silhouette Score")

    plt.title("Silhouette Analysis")

    st.pyplot(fig)

    # -----------------------------------------------------
    # NUMBER OF CLUSTERS
    # -----------------------------------------------------

    st.subheader("Choose Number of Clusters")

    k = st.slider(

        "Clusters",

        min_value=2,

        max_value=8,

        value=4

    )

    model = KMeans(

        n_clusters=k,

        random_state=42,

        n_init=10

    )

    df["Cluster"] = model.fit_predict(X_scaled)

    st.success("Customer Segmentation Completed")

    st.write(df[["ID","Cluster"]].head())

    # -----------------------------------------------------
    # PCA VISUALIZATION
    # -----------------------------------------------------

    st.subheader("PCA Cluster Visualization")

    from sklearn.decomposition import PCA

    pca = PCA(n_components=2)

    pca_features = pca.fit_transform(X_scaled)

    fig = plt.figure(figsize=(8,6))

    plt.scatter(

        pca_features[:,0],

        pca_features[:,1],

        c=df["Cluster"]

    )

    plt.xlabel("Principal Component 1")

    plt.ylabel("Principal Component 2")

    plt.title("Customer Segments")

    st.pyplot(fig)

    # -----------------------------------------------------
    # CLUSTER COUNTS
    # -----------------------------------------------------

    st.subheader("Cluster-wise Customer Count")

    cluster_count = df["Cluster"].value_counts().sort_index()

    st.write(cluster_count)

    fig = plt.figure(figsize=(7,5))

    plt.bar(

        cluster_count.index.astype(str),

        cluster_count.values

    )

    plt.xlabel("Cluster")

    plt.ylabel("Customers")

    plt.title("Customer Count by Cluster")

    st.pyplot(fig)

    # -----------------------------------------------------
    # CLUSTER PROFILE
    # -----------------------------------------------------

    st.subheader("Cluster Profile")

    profile = df.groupby("Cluster")[

        [

            "Income",

            "TotalSpending",

            "Age",

            "Recency",

            "NumWebPurchases",

            "NumStorePurchases",

            "NumCatalogPurchases"

        ]

    ].mean().round(2)

    st.dataframe(profile)

    # -----------------------------------------------------
    # SEGMENT NAMES
    # -----------------------------------------------------

    st.subheader("Business Segment Names")

    segment_names = {

        0:"High Value Customers",

        1:"Regular Customers",

        2:"Potential Customers",

        3:"At Risk Customers",

        4:"Premium Customers",

        5:"Discount Lovers",

        6:"Occasional Buyers",

        7:"Inactive Customers"

    }

    df["Segment"] = df["Cluster"].map(segment_names)

    st.write(

        df[

            [

                "ID",

                "Cluster",

                "Segment"

            ]

        ].head(15)

    )

    # -----------------------------------------------------
    # REVENUE BY SEGMENT
    # -----------------------------------------------------

    st.subheader("Revenue Contribution")

    revenue = df.groupby("Segment")["TotalSpending"].sum()

    fig = plt.figure(figsize=(9,5))

    plt.bar(

        revenue.index,

        revenue.values

    )

    plt.xticks(rotation=30)

    plt.ylabel("Revenue")

    plt.title("Revenue by Customer Segment")

    st.pyplot(fig)
    # ---------------------------------------------------------
# REGRESSION PAGE
# ---------------------------------------------------------

elif page == "Regression":

    st.header("Regression Models")

    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    from sklearn.linear_model import Ridge
    from sklearn.metrics import (
        mean_absolute_error,
        mean_squared_error,
        r2_score
    )

    features = [

        "Income",
        "Age",
        "Recency",
        "Children",
        "NumWebPurchases",
        "NumCatalogPurchases",
        "NumStorePurchases",
        "NumDealsPurchases",
        "NumWebVisitsMonth"

    ]

    X = df[features]

    y = df["TotalSpending"]

    X_train, X_test, y_train, y_test = train_test_split(

        X,
        y,
        test_size=0.2,
        random_state=42

    )

    model = LinearRegression()

    model.fit(X_train, y_train)

    prediction = model.predict(X_test)

    mae = mean_absolute_error(y_test,prediction)

    rmse = np.sqrt(mean_squared_error(y_test,prediction))

    r2 = r2_score(y_test,prediction)

    st.subheader("Linear Regression")

    st.write("MAE :",round(mae,2))
    st.write("RMSE :",round(rmse,2))
    st.write("R² Score :",round(r2,3))

    ridge = Ridge(alpha=1)

    ridge.fit(X_train,y_train)

    ridge_prediction = ridge.predict(X_test)

    ridge_r2 = r2_score(y_test,ridge_prediction)

    st.subheader("Ridge Regression")

    st.write("R² Score :",round(ridge_r2,3))

    fig = plt.figure(figsize=(7,5))

    plt.scatter(y_test,prediction)

    plt.xlabel("Actual Spending")

    plt.ylabel("Predicted Spending")

    plt.title("Actual vs Predicted")

    st.pyplot(fig)

# ---------------------------------------------------------
# CLASSIFICATION PAGE
# ---------------------------------------------------------

elif page == "Classification":

    st.header("Purchase Response Prediction")

    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import GridSearchCV

    from sklearn.metrics import (

        accuracy_score,
        precision_score,
        recall_score,
        f1_score,
        confusion_matrix,
        roc_auc_score

    )

    features = [

        "Income",
        "Age",
        "Recency",
        "Children",
        "TotalSpending",
        "NumWebPurchases",
        "NumCatalogPurchases",
        "NumStorePurchases",
        "NumDealsPurchases",
        "NumWebVisitsMonth"

    ]

    X = df[features]

    y = df["Response"]

    X_train,X_test,y_train,y_test = train_test_split(

        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y

    )

    logistic = LogisticRegression(max_iter=1000)

    logistic.fit(X_train,y_train)

    prediction = logistic.predict(X_test)

    st.subheader("Logistic Regression")

    st.write("Accuracy :",round(accuracy_score(y_test,prediction),3))

    st.write("Precision :",round(precision_score(y_test,prediction),3))

    st.write("Recall :",round(recall_score(y_test,prediction),3))

    st.write("F1 Score :",round(f1_score(y_test,prediction),3))

    st.write("ROC-AUC :",round(roc_auc_score(y_test,prediction),3))

    st.subheader("GridSearchCV")

    params={

        "C":[0.01,0.1,1,10],

        "solver":["liblinear","lbfgs"]

    }

    grid = GridSearchCV(

        LogisticRegression(max_iter=1000),

        params,

        cv=5,

        scoring="accuracy"

    )

    grid.fit(X_train,y_train)

    st.write("Best Parameters")

    st.write(grid.best_params_)

    st.write("Best Accuracy")

    st.write(round(grid.best_score_,3))

    cm = confusion_matrix(y_test,prediction)

    fig = plt.figure(figsize=(5,5))

    plt.imshow(cm)

    plt.colorbar()

    plt.title("Confusion Matrix")

    plt.xticks([0,1],["No","Yes"])

    plt.yticks([0,1],["No","Yes"])

    plt.xlabel("Predicted")

    plt.ylabel("Actual")

    for i in range(cm.shape[0]):

        for j in range(cm.shape[1]):

            plt.text(j,i,cm[i,j],
                     ha="center",
                     va="center")

    st.pyplot(fig)

# ---------------------------------------------------------
# BUSINESS INSIGHTS PAGE
# ---------------------------------------------------------

elif page == "Business Insights":

    st.header("Business Insights")

    st.success("Customer segmentation completed successfully.")

    st.markdown("### Key Findings")

    st.write("• High-value customers contribute the highest revenue.")

    st.write("• Customers with recent purchases show higher engagement.")

    st.write("• Customers with low recency require retention campaigns.")

    st.write("• Customers purchasing through multiple channels are more valuable.")

    st.write("• Discount-focused customers should receive targeted promotions.")

    st.write("• Loyal customers can be rewarded with premium memberships.")

    st.write("• Personalized recommendations improve customer retention.")

    st.write("• Marketing campaigns should prioritize high-value customer segments.")

    st.markdown("---")

    st.subheader("Model Comparison")

    comparison = pd.DataFrame({

        "Model":[

            "K-Means",

            "Linear Regression",

            "Ridge Regression",

            "Logistic Regression"

        ],

        "Objective":[

            "Customer Segmentation",

            "Predict Spending",

            "Predict Spending",

            "Predict Campaign Response"

        ]

    })

    st.table(comparison)

    st.subheader("Download Customer Segments")

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(

        label="Download customer_segments.csv",

        data=csv,

        file_name="customer_segments.csv",

        mime="text/csv"

    )

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown("---")

st.caption("Customer Segmentation with Actionable Business Insights | Task 8 | Streamlit Dashboard")