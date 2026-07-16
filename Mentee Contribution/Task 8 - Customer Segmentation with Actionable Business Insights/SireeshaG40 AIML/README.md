# README.md

# Task 8 - Customer Segmentation and Machine Learning Analysis

## Submitted By

**Name:** Sireesha
**Batch:** G40 AI & ML

---

## Project Overview

This project performs customer segmentation and predictive analysis using the **Customer Personality Analysis (Marketing Campaign)** dataset.

The notebook applies machine learning algorithms to identify customer groups, predict customer responses, and analyze purchasing behavior to support business decision-making.

---

## Dataset

**Dataset Name:** Marketing Campaign Dataset

**File:** `marketing_campaign.csv`

The dataset contains customer demographic information, purchasing history, campaign responses, and web activity.

---

## Objectives

* Perform Exploratory Data Analysis (EDA)
* Clean and preprocess the dataset
* Create meaningful customer features
* Segment customers using K-Means Clustering
* Evaluate the optimal number of clusters using the Elbow Method
* Measure clustering quality using the Silhouette Score
* Predict customer spending using Ridge Regression
* Predict campaign response using Logistic Regression
* Optimize the classification model using GridSearchCV
* Compare machine learning model performance
* Generate customer insights for business recommendations

---

## Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Scikit-learn
* Jupyter Notebook

---

## Machine Learning Algorithms

### Unsupervised Learning

* K-Means Clustering

### Supervised Learning

* Ridge Regression
* Logistic Regression

### Hyperparameter Optimization

* GridSearchCV

---

## Features Created

The notebook creates additional features including:

* Age
* TotalSpending
* PurchaseFrequency
* AverageOrderValue

These engineered features improve customer segmentation and predictive performance.

---

## Project Workflow

1. Import required libraries
2. Load the dataset
3. Explore and understand the data
4. Handle missing values
5. Perform feature engineering
6. Standardize numerical features
7. Apply the Elbow Method
8. Calculate Silhouette Score
9. Build K-Means clustering model
10. Visualize customer segments
11. Train Ridge Regression model
12. Train Logistic Regression model
13. Tune model using GridSearchCV
14. Evaluate model performance
15. Save results to CSV files

---

## Output Files

The notebook generates the following files:

* `customer_segments.csv`
* `cluster_profile.csv`
* `classification_predictions.csv`
* `regression_predictions.csv`
* `best_hyperparameters.csv`
* `model_comparison.csv`

---

## Evaluation Metrics

### Regression

* Mean Absolute Error (MAE)
* Root Mean Squared Error (RMSE)
* R² Score

### Classification

* Accuracy
* Precision
* Recall
* F1 Score
* ROC-AUC Score
* Confusion Matrix

---

## Business Insights

* Customers are grouped into meaningful purchasing segments.
* High-value customers can be targeted with premium campaigns.
* Low-engagement customers can receive personalized promotional offers.
* Customer segmentation improves marketing efficiency.
* Predictive models help forecast customer behavior and campaign success.

---

## Conclusion

This project demonstrates how customer analytics and machine learning techniques can be combined to understand customer behavior, improve marketing strategies, and support data-driven business decisions. The generated customer segments and predictive models provide valuable insights for targeted marketing and customer relationship management.
