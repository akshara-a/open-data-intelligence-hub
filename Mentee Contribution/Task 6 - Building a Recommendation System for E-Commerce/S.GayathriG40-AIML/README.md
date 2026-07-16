# Task 6 - Machine Learning Analysis on E-commerce Customer Behavior Dataset

## Project Overview

This project demonstrates the application of machine learning techniques on the **E-commerce Customer Behavior** dataset. The objective is to analyze customer purchasing behavior, predict customer ratings and discount application, and segment customers using clustering techniques.

The project includes data preprocessing, exploratory data analysis (EDA), supervised learning, unsupervised learning, model evaluation, and business interpretation.

---

## Dataset

**Dataset Name:**
E-commerce Customer Behavior - Sheet1.csv

### Features

- Customer ID
- Gender
- Age
- City
- Membership Type
- Total Spend
- Items Purchased
- Average Rating
- Discount Applied
- Days Since Last Purchase
- Satisfaction Level

---

## Objectives

The objectives of this project are to:

- Explore and understand customer behavior.
- Perform data preprocessing.
- Build a regression model.
- Build a classification model.
- Segment customers using clustering.
- Evaluate model performance.
- Provide business insights.

---

## Technologies Used

- Python
- Jupyter Notebook
- Pandas
- NumPy
- Matplotlib
- Scikit-learn

---

## Machine Learning Models

### 1. Linear Regression

**Target Variable:**

Average Rating

**Purpose:**

Predict customer ratings based on purchasing behavior.

**Evaluation Metrics**

- Mean Absolute Error (MAE)
- Mean Squared Error (MSE)
- Root Mean Squared Error (RMSE)
- R² Score

---

### 2. Logistic Regression

**Target Variable:**

Discount Applied

**Purpose:**

Predict whether a customer receives a discount.

**Evaluation Metrics**

- Accuracy
- Confusion Matrix
- Classification Report

---

### 3. GridSearchCV

GridSearchCV was used to optimize the Logistic Regression model by selecting the best hyperparameters.

---

### 4. K-Means Clustering

**Purpose**

Segment customers into different groups based on their purchasing behavior.

**Evaluation Metric**

- Silhouette Score

---

## Data Preprocessing

The following preprocessing techniques were applied:

- Missing value checking
- Label Encoding
- Feature Scaling using StandardScaler
- Train-Test Split

---

## Exploratory Data Analysis

The notebook includes:

- Dataset overview
- Dataset information
- Statistical summary
- Missing value analysis
- Histograms
- Scatter plots

---

## Project Structure

```
Task6/
│
├── Task6.ipynb
├── E-commerce Customer Behavior - Sheet1.csv
├── README.md
├── decision.long.md
└── model.comparison.md
```

---

## How to Run

1. Install Python 3.x.

2. Install required libraries:

```bash
pip install pandas numpy matplotlib scikit-learn
```

3. Place the dataset in the same folder as the notebook.

4. Open `Task6.ipynb` in Jupyter Notebook or Google Colab.

5. Run all cells sequentially.

---

## Results

The project successfully:

- Loaded and explored the dataset.
- Preprocessed customer data.
- Predicted customer ratings using Linear Regression.
- Predicted discount application using Logistic Regression.
- Improved classification using GridSearchCV.
- Segmented customers using K-Means Clustering.
- Compared model performance.
- Generated business insights for decision making.

---

## Business Insights

- Customer spending behavior influences average ratings.
- Discount prediction can support promotional strategies.
- Customer segmentation enables personalized marketing.
- Machine learning helps improve customer retention and business planning.

---

## Future Improvements

- Test additional machine learning models such as Random Forest, Decision Tree, and XGBoost.
- Perform feature selection to improve model performance.
- Add more visualizations and dashboards.
- Deploy the trained models as a web application.

---

## Author

Machine Learning Task 6

Created using Python, Scikit-learn, and Jupyter Notebook.