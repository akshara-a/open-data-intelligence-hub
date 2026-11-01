# Task 6 - E-Commerce Recommendation System

## Project Overview

This project implements an **E-Commerce Recommendation System** using Machine Learning techniques. It analyzes customer behavior, predicts product ratings, predicts purchase decisions, and segments customers based on their shopping behavior.

## Dataset

* `ecommerce_dataset.csv`

## Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Scikit-learn
* Joblib
* Jupyter Notebook

## Machine Learning Models

### 1. Linear Regression

Predicts customer product ratings.

**Evaluation Metrics:**

* MAE
* RMSE
* R² Score

### 2. Ridge Regression

Predicts customer ratings using regularization and improves model generalization.

**Evaluation Metrics:**

* MAE
* MSE
* RMSE
* R² Score

### 3. Logistic Regression

Predicts whether a customer will purchase a product.

**Evaluation Metrics:**

* Accuracy
* Precision
* Recall
* F1 Score
* ROC-AUC

### 4. K-Means Clustering

Segments customers based on their shopping and purchasing behavior.

**Evaluation Metrics:**

* Elbow Method
* Inertia
* Silhouette Score

## Hyperparameter Tuning

Hyperparameter optimization was performed using **GridSearchCV** for:

* Ridge Regression
* Logistic Regression
* K-Means Clustering

## Project Structure

```text
Task 6 Recommendation-System-Ecommerce

│
├── data
│   └── ecommerce_dataset.csv
│
├── images
├── models
├── run_pipeline.py
├── README.md
└── requirements.txt
```

## Results

* Completed data preprocessing
* Performed exploratory data analysis
* Built Regression models
* Built Classification model
* Performed Customer Segmentation
* Applied Hyperparameter Tuning
* Evaluated model performance
* Generated charts and saved trained models

## Business Applications

* Personalized product recommendations
* Purchase prediction
* Customer segmentation
* Targeted promotions
* Customer behavior analysis

## Author

**P. Harshitha**

**SURE Trust G40 AI/ML**
