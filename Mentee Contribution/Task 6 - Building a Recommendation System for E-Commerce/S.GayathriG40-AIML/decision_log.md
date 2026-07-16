# Task 6 – Decision Log

## Project Title
Machine Learning Analysis on E-commerce Customer Behavior Dataset

---

# Dataset Selection

Dataset Used:
- E-commerce Customer Behavior - Sheet1.csv

Reason:
This dataset contains customer demographic information, purchasing behavior, ratings, discounts, and satisfaction levels, making it suitable for regression, classification, and clustering tasks.

---

# Data Loading

The dataset was loaded using the Pandas library.

```python
df = pd.read_csv("E-commerce Customer Behavior - Sheet1.csv")
```

---

# Exploratory Data Analysis (EDA)

The following analyses were performed:

- Dataset shape
- Dataset information
- Statistical summary
- Missing value detection
- Histograms
- Scatter plot

Purpose:
To understand the structure of the dataset before building machine learning models.

---

# Data Preprocessing

The preprocessing steps included:

- Label Encoding for categorical columns
- Feature Scaling using StandardScaler
- Train-Test Split

Reason:
Machine learning algorithms require numerical input and scaled features for better performance.

---

# Label Encoding

Categorical columns such as:

- Gender
- City
- Membership Type
- Discount Applied
- Satisfaction Level

were converted into numeric values using LabelEncoder.

Reason:
Regression, Logistic Regression, and K-Means cannot directly process text values.

---

# Feature Scaling

StandardScaler was applied to numerical features.

Reason:
Scaling ensures that all features contribute equally to the learning process and prevents features with larger values from dominating.

---

# Regression Model

Algorithm Used:
Linear Regression

Target Variable:
Average Rating

Reason for Selection:
Average Rating is a continuous numerical value, making Linear Regression an appropriate choice.

Evaluation Metrics:

- Mean Absolute Error (MAE)
- Mean Squared Error (MSE)
- Root Mean Squared Error (RMSE)
- R² Score

---

# Classification Model

Algorithm Used:
Logistic Regression

Target Variable:
Discount Applied

Reason for Selection:
Discount Applied is a categorical variable.

Evaluation Metrics:

- Accuracy
- Confusion Matrix
- Classification Report

---

# Hyperparameter Tuning

Method Used:
GridSearchCV

Purpose:
To identify the best hyperparameters for Logistic Regression and improve classification performance.

Parameters Tested:

- C values
- Solver types

---

# Clustering

Algorithm Used:
K-Means Clustering

Number of Clusters:
3

Reason:
To segment customers based on purchasing behavior.

Evaluation Metric:

- Silhouette Score

---

# Customer Segmentation

Customers were divided into three clusters.

Purpose:

- Identify high-value customers
- Improve targeted marketing
- Increase customer retention
- Support business decision making

---

# Model Comparison

Models Compared:

1. Linear Regression
2. Logistic Regression

Comparison Metrics:

- R² Score
- Accuracy

Purpose:
To evaluate the performance of different machine learning models.

---

# Business Interpretation

The analysis provides useful insights for business decision-making.

Key findings include:

- Customer spending influences average ratings.
- Discount prediction helps improve marketing strategies.
- Customer segmentation enables personalized offers.
- Machine learning assists in identifying purchasing patterns.

---

# Conclusion

The project successfully completed all required machine learning tasks.

Completed Tasks:

- Data Loading
- Exploratory Data Analysis
- Data Preprocessing
- Label Encoding
- Feature Scaling
- Linear Regression
- Logistic Regression
- GridSearchCV
- K-Means Clustering
- Model Evaluation
- Customer Segmentation
- Business Interpretation

The developed models provide meaningful insights into customer behavior and can support business decisions related to marketing, customer retention, and sales optimization.