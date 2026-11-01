#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import numpy as np
df=pd.read_csv("Ecommerce.csv")


# In[4]:


# Display first 5 rows
print("First 5 Rows")
print(df.head())


# In[8]:


# Shape
print("\nDataset Shape:")
print(df.shape)

# Column names
print("\nColumn Names:")
print(df.columns)

# Missing values
print("\nMissing Values:")
print(df.isnull().sum())


# In[11]:


# Duplicate rows
print("\nDuplicate Rows:")
print(df.duplicated().sum())

# Data types
print("\nData Types:")
print(df.dtypes)

# Statistical summary
print("\nStatistical Summary:")
print(df.describe(include='all'))


# In[12]:


# STEP 2 : DATA PREPROCESSING

from sklearn.preprocessing import LabelEncoder

# Remove duplicate rows
df = df.drop_duplicates()

# Handle missing values
df = df.dropna()

print("\nShape after cleaning:")
print(df.shape)

# Encode categorical columns
le = LabelEncoder()

for col in df.select_dtypes(include="object").columns:
    df[col] = le.fit_transform(df[col])

print("\nEncoded Dataset:")
print(df.head())

# Check missing values again
print("\nMissing Values:")
print(df.isnull().sum())


# In[14]:


# STEP 3 : RIDGE REGRESSION
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

# Target

# Features
X = df.drop(columns=["rating"])
y = df["rating"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train Ridge Regression
ridge = Ridge(alpha=1.0)
ridge.fit(X_train, y_train)

# Prediction
y_pred = ridge.predict(X_test)

# Evaluation
print("\n RIDGE REGRESSION ")
print("MAE :", mean_absolute_error(y_test, y_pred))
print("RMSE :", np.sqrt(mean_squared_error(y_test, y_pred)))
print("R2 Score :", r2_score(y_test, y_pred))


# In[15]:


from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

X = df.drop(columns=["purchased"])
y = df["purchased"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LogisticRegression(max_iter=1000)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("\nLOGISTIC REGRESSION")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))
print("Recall:", recall_score(y_test, y_pred))
print("F1 Score:", f1_score(y_test, y_pred))


# In[16]:


from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

features = [
    "pages_viewed",
    "quantity",
    "rating",
    "time_on_site_sec",
    "revenue",
    "added_to_cart"
]

X = df[features]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

kmeans = KMeans(n_clusters=4, random_state=42)

clusters = kmeans.fit_predict(X_scaled)

df["Cluster"] = clusters

print("\nCLUSTERING")
print(df[["customer_id", "Cluster"]].head())

print("Inertia:", kmeans.inertia_)
print("Silhouette Score:", silhouette_score(X_scaled, clusters))


# In[17]:


from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import Ridge

# Use the same X_train and y_train from the Ridge Regression section
params = {
    "alpha": [0.01, 0.1, 1, 10, 100]
}

grid = GridSearchCV(
    Ridge(),
    param_grid=params,
    cv=5,
    scoring="r2"
)

grid.fit(X_train, y_train)

print("\n===== HYPERPARAMETER TUNING =====")
print("Best Parameters:", grid.best_params_)
print("Best R2 Score:", grid.best_score_)


# In[18]:


import joblib

joblib.dump(grid.best_estimator_, "task7_model.pkl")

print("\nModel saved successfully!")


# In[19]:


print("\n MODEL COMPARISON ")
print("Regression  : Ridge Regression")
print("Classification : Logistic Regression")
print("Clustering : K-Means")

print("\nBusiness Use")
print("- Ridge Regression : Predict customer ratings")
print("- Logistic Regression : Predict purchase likelihood")
print("- K-Means : Segment customers for targeted marketing")


# In[ ]:




