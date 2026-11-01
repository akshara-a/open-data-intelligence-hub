# ==========================================
# Customer Classification
# Logistic Regression
# ==========================================

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
    classification_report
)

# ------------------------------------------
# Load Dataset
# ------------------------------------------

df = pd.read_csv("reports/customer_segments.csv")

print("=" * 60)
print("CUSTOMER CLASSIFICATION")
print("=" * 60)

# ------------------------------------------
# Create Target Variable
# ------------------------------------------

median_frequency = df["F"].median()

df["PurchaseLikelihood"] = (
    df["F"] >= median_frequency
).astype(int)

print("\nTarget Variable Created")

print(df["PurchaseLikelihood"].value_counts())

# ------------------------------------------
# Select Features
# ------------------------------------------

X = df[
    [
        "Income",
        "Age",
        "R",
        "M",
        "Children",
        "CampaignsAccepted",
        "WebActivity"
    ]
]

y = df["PurchaseLikelihood"]

# ------------------------------------------
# Train-Test Split
# ------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining Samples:", len(X_train))
print("Testing Samples :", len(X_test))

# ------------------------------------------
# Train Logistic Regression
# ------------------------------------------

model = LogisticRegression(max_iter=1000)

model.fit(X_train, y_train)

# ------------------------------------------
# Prediction
# ------------------------------------------

y_pred = model.predict(X_test)

y_prob = model.predict_proba(X_test)[:,1]

# ------------------------------------------
# Evaluation
# ------------------------------------------

accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(y_test, y_pred)

recall = recall_score(y_test, y_pred)

f1 = f1_score(y_test, y_pred)

roc = roc_auc_score(y_test, y_prob)

print("\nClassification Results")

print("Accuracy :", round(accuracy,3))
print("Precision:", round(precision,3))
print("Recall   :", round(recall,3))
print("F1 Score :", round(f1,3))
print("ROC-AUC  :", round(roc,3))

print("\nClassification Report")

print(classification_report(y_test,y_pred))

# ------------------------------------------
# Save Results
# ------------------------------------------

results = pd.DataFrame({

    "Metric":[
        "Accuracy",
        "Precision",
        "Recall",
        "F1 Score",
        "ROC-AUC"
    ],

    "Value":[
        accuracy,
        precision,
        recall,
        f1,
        roc
    ]

})

results.to_csv(
    "reports/classification_results.csv",
    index=False
)

# ------------------------------------------
# Confusion Matrix
# ------------------------------------------

cm = confusion_matrix(y_test,y_pred)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm
)

disp.plot(cmap="Blues")

plt.title("Confusion Matrix")

plt.show()

print("\nClassification Completed Successfully!")