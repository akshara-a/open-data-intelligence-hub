# 🔄 Reusable ML Pipeline – Customer Churn Prediction

A reusable machine learning pipeline for predicting customer churn using the **Telco Customer Churn dataset**.

The project demonstrates an end-to-end ML workflow including data loading, preprocessing, feature transformation, model training, evaluation, model persistence, and prediction on new customer data.

---

## 📌 Project Overview

Customer churn prediction helps businesses identify customers who are likely to leave their service.

This project builds a reusable **Scikit-learn Pipeline** that automatically performs:

* Data preprocessing
* Missing-value handling
* Numerical feature scaling
* Categorical feature encoding
* Random Forest classification
* Model prediction
* Churn probability estimation

The complete trained pipeline is saved as a `.pkl` file and can be reused for future predictions.

---

## 🎯 Objectives

* Build a reusable machine learning pipeline.
* Handle numerical and categorical features automatically.
* Perform missing-value imputation.
* Encode categorical variables.
* Scale numerical variables.
* Train a Random Forest classifier.
* Evaluate model performance.
* Save and reload the trained pipeline.
* Predict churn for new customers.

---

## 📊 Dataset

**Dataset:** Telco Customer Churn

The dataset contains **7,043 customer records and 21 columns**.

Important features include:

* Gender
* Senior Citizen
* Partner
* Dependents
* Tenure
* Phone Service
* Internet Service
* Online Security
* Online Backup
* Device Protection
* Tech Support
* Streaming TV
* Streaming Movies
* Contract
* Paperless Billing
* Payment Method
* Monthly Charges
* Total Charges

### Target Variable

`Churn`

* `Yes` → Customer is likely to churn
* `No` → Customer is likely to stay

---

## 🏗️ Project Structure

```text
reusable-ml-pipeline/
│
├── data/
│   └── WA_Fn-UseC_-Telco-Customer-Churn.csv
│
├── models/
│   └── churn_model.pkl
│
├── src/
│   ├── load_data.py
│   ├── preprocessing.py
│   ├── train_pipeline.py
│   ├── evaluate_pipeline.py
│   └── predict.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Machine Learning Pipeline

The project uses a Scikit-learn `Pipeline` and `ColumnTransformer`.

```text
Raw Customer Data
        ↓
Data Cleaning
        ↓
Separate Numerical & Categorical Features
        ↓
Numerical Pipeline
 ├── Median Imputation
 └── StandardScaler
        ↓
Categorical Pipeline
 ├── Most-Frequent Imputation
 └── OneHotEncoder
        ↓
ColumnTransformer
        ↓
Random Forest Classifier
        ↓
Churn Prediction
```

---

## 🤖 Model

The machine learning model used is:

**Random Forest Classifier**

Configuration:

```python
RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)
```

`class_weight="balanced"` is used to help handle the imbalance between churn and non-churn customers.

---

## 📈 Model Performance

The model was evaluated using a test set containing **1,409 customers**.

### Accuracy

```text
78.85%
```

### Classification Report

| Class            | Precision | Recall | F1-Score |
| ---------------- | --------: | -----: | -------: |
| No Churn         |      0.83 |   0.89 |     0.86 |
| Churn            |      0.63 |   0.51 |     0.56 |
| Overall Accuracy |           |        | **0.79** |

### Confusion Matrix

```text
[[922 113]
 [185 189]]
```

The model correctly identified:

* **922** non-churn customers
* **189** churn customers

---

## 🔮 Example Prediction

The saved pipeline can be used to predict a new customer's churn probability.

Example output:

```text
==============================
CUSTOMER CHURN PREDICTION
==============================

Prediction: No
Churn Probability: 41.00%

Customer is likely to STAY.
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd reusable-ml-pipeline
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

### Load the dataset

```bash
python src/load_data.py
```

### Test preprocessing

```bash
python src/preprocessing.py
```

### Train the model

```bash
python src/train_pipeline.py
```

This creates:

```text
models/churn_model.pkl
```

### Evaluate the model

```bash
python src/evaluate_pipeline.py
```

### Predict customer churn

```bash
python src/predict.py
```

---

## 💾 Saved Model

The trained pipeline is saved as:

```text
models/churn_model.pkl
```

The saved file contains the complete preprocessing and machine learning pipeline, allowing new customer data to be passed directly to the model.

---

## 🛠️ Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* Joblib
* Random Forest
* ColumnTransformer
* Pipeline
* OneHotEncoder
* StandardScaler

---

## 🔑 Key Features

### Reusable Pipeline

Preprocessing and model training are combined into a single pipeline.

### Automatic Preprocessing

The pipeline automatically handles:

* Missing numerical values
* Missing categorical values
* Numerical scaling
* Categorical encoding

### Model Persistence

The complete trained pipeline is saved using Joblib.

### New Customer Prediction

The saved model can be loaded and used to predict churn for new customers.

---

## 🔮 Future Improvements

* Hyperparameter tuning
* SMOTE for class imbalance
* XGBoost comparison
* Cross-validation
* Feature importance visualization
* SHAP explainability
* Streamlit web application
* Automated model retraining
* Model monitoring

---

## 👩‍💻 Author

**Shaik Aiesha**

B.Tech – Computer Science & Engineering

---

## ⭐ Conclusion

This project demonstrates how to build a reusable machine learning pipeline from raw customer data to production-ready prediction.

The pipeline ensures that the same preprocessing steps used during training are automatically applied during prediction, reducing preprocessing inconsistencies and making the machine learning workflow easier to reuse.
