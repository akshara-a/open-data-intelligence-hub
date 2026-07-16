import pandas as pd
import numpy as np

# Load dataset
import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv("E-commerce Customer Behavior - Sheet1.csv")

# Basic Information

print("First 5 Rows")
print(df.head())

print("\nDataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns)

# Check Missing Values

print("\nMissing Values:")
print(df.isnull().sum())


# Remove Duplicate Rows

df = df.drop_duplicates()

print("\nShape After Removing Duplicates:")
print(df.shape)


# Data Types
print("\nData Types:")
print(df.dtypes)


# Statistical Summary

print("\nStatistical Summary:")
print(df.describe())

import matplotlib.pyplot as plt

# Total Spend Distribution

plt.figure(figsize=(6,4))
plt.hist(df["Total Spend"], bins=10)
plt.title("Distribution of Total Spend")
plt.xlabel("Total Spend")
plt.ylabel("Customers")
plt.show()

# Average Rating Distribution
plt.figure(figsize=(6,4))
plt.hist(df["Average Rating"], bins=10)
plt.title("Distribution of Average Rating")
plt.xlabel("Rating")
plt.ylabel("Count")
plt.show()

# Membership Type Count
plt.figure(figsize=(6,4))
df["Membership Type"].value_counts().plot(kind="bar")
plt.title("Membership Type")
plt.xlabel("Membership")
plt.ylabel("Customers")
plt.show()


# Gender Count
plt.figure(figsize=(5,4))
df["Gender"].value_counts().plot(kind="bar")
plt.title("Gender Distribution")
plt.show()

from sklearn.preprocessing import LabelEncoder

# Handle Missing Values

df["Satisfaction Level"] = df["Satisfaction Level"].fillna(df["Satisfaction Level"].mode()[0])

# Encode Categorical Columns

label_encoder = LabelEncoder()

df["Gender"] = label_encoder.fit_transform(df["Gender"])

df["City"] = label_encoder.fit_transform(df["City"])

df["Membership Type"] = label_encoder.fit_transform(df["Membership Type"])

df["Discount Applied"] = label_encoder.fit_transform(df["Discount Applied"])

df["Satisfaction Level"] = label_encoder.fit_transform(df["Satisfaction Level"])

print("\nEncoded Dataset")
print(df.head())
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score



# Regression


X = df[[
    "Age",
    "Total Spend",
    "Items Purchased",
    "Days Since Last Purchase"
]]

y = df["Average Rating"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

reg_model = LinearRegression()

reg_model.fit(X_train, y_train)

y_pred = reg_model.predict(X_test)

print("\nREGRESSION")

print("MAE :", mean_absolute_error(y_test, y_pred))

print("RMSE :", np.sqrt(mean_squared_error(y_test, y_pred)))

print("R2 Score :", r2_score(y_test, y_pred))
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


# Classification


X = df[[
    "Age",
    "Total Spend",
    "Items Purchased",
    "Days Since Last Purchase",
    "Gender",
    "Membership Type",
    "Discount Applied"
]]

y = df["Satisfaction Level"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# clf = LogisticRegression(max_iter=1000)

# clf.fit(X_train, y_train)
clf = LogisticRegression(
    solver="lbfgs",
    max_iter=3000,
    random_state=42
)

clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

print("\n CLASSIFICATION")

print("Accuracy :", accuracy_score(y_test, y_pred))

print("\nConfusion Matrix")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report")
print(classification_report(y_test, y_pred))
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Clustering

X_cluster = df[[
    "Age",
    "Total Spend",
    "Items Purchased",
    "Average Rating"
]]

kmeans = KMeans(
    n_clusters=3,
    random_state=42,
    n_init=10
)

clusters = kmeans.fit_predict(X_cluster)

df["Cluster"] = clusters

print("\n CLUSTERING")

print(df[["Customer ID", "Cluster"]].head())

print("Inertia :", kmeans.inertia_)

print("Silhouette Score :", silhouette_score(X_cluster, clusters))

from sklearn.model_selection import GridSearchCV

# parameters = {
#     "C": [0.1, 1, 10],
#     "solver": ["liblinear", "lbfgs"],
#     "max_iter": [500, 1000]
# }
parameters = {
    "C": [0.1, 1, 10],
    "solver": ["lbfgs"],
    "max_iter": [3000]
}

grid = GridSearchCV(
    LogisticRegression(),
    parameters,
    cv=5
)

grid.fit(X_train, y_train)

print("\nHYPERPARAMETER TUNING")

print("Best Parameters :", grid.best_params_)

print("Best Score :", grid.best_score_)
import joblib

joblib.dump(clf, "task6_logistic_model.pkl")

print("\nModel saved successfully!")
