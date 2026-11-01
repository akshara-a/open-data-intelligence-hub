# ==========================================================
# STEP 6 : LOGISTIC REGRESSION
# Purchase Prediction
# ==========================================================

import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

print("=" * 60)
print("LOGISTIC REGRESSION")
print("=" * 60)

# ----------------------------------------------------------
# Load Dataset
# ----------------------------------------------------------

df = pd.read_csv("data/processed_ecommerce.csv")

print("\nDataset Loaded Successfully")
print("Shape :", df.shape)

# ----------------------------------------------------------
# Feature Selection
# ----------------------------------------------------------

features = [

    "device_type",
    "user_type",
    "marketing_channel",
    "product_category",
    "unit_price",
    "quantity",
    "discount_percent",
    "discount_amount",
    "revenue",
    "pages_viewed",
    "time_on_site_sec",
    "added_to_cart",
    "rating",
    "payment_method",
    "visit_day",
    "visit_month",
    "visit_weekday",
    "visit_season",
    "session_duration_bucket",
    "location"

]

X = df[features]

y = df["purchased"]

print("\nFeatures Selected Successfully")
print("Number of Features :", len(features))

# ----------------------------------------------------------
# Train Test Split
# ----------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y

)

print("\nTraining Samples :", len(X_train))
print("Testing Samples :", len(X_test))

# ----------------------------------------------------------
# Grid Search
# ----------------------------------------------------------

parameters = {

    "C":[0.01,0.1,1,10],
    "solver":["liblinear"],
    "max_iter":[500]

}

model = LogisticRegression()

grid = GridSearchCV(

    model,

    parameters,

    cv=5,

    scoring="accuracy"

)

print("\nRunning Grid Search...")

grid.fit(X_train,y_train)

best_model = grid.best_estimator_

print("\nBest Parameters")
print(grid.best_params_)

# ----------------------------------------------------------
# Prediction
# ----------------------------------------------------------

predictions = best_model.predict(X_test)

# ----------------------------------------------------------
# Evaluation
# ----------------------------------------------------------

accuracy = accuracy_score(y_test,predictions)

precision = precision_score(y_test,predictions)

recall = recall_score(y_test,predictions)

f1 = f1_score(y_test,predictions)

print("\n==============================")
print("MODEL PERFORMANCE")
print("==============================")

print("Accuracy :",round(accuracy,4))
print("Precision:",round(precision,4))
print("Recall   :",round(recall,4))
print("F1 Score :",round(f1,4))

print("\nConfusion Matrix")
print(confusion_matrix(y_test,predictions))

print("\nClassification Report")
print(classification_report(y_test,predictions))

# ----------------------------------------------------------
# Save Model
# ----------------------------------------------------------

os.makedirs("models",exist_ok=True)

joblib.dump(best_model,"models/logistic_model.pkl")

print("\nModel Saved Successfully")

print("Location : models/logistic_model.pkl")

print("\nSTEP 6 COMPLETED SUCCESSFULLY")