# Model Comparison Report

## Project
Machine Learning Analysis on E-commerce Customer Behavior Dataset

---

# Models Used

| Model | Task | Target Variable |
|-------|------|-----------------|
| Linear Regression | Regression | Average Rating |
| Logistic Regression | Classification | Discount Applied |
| K-Means Clustering | Customer Segmentation | No Target Variable |

---

# Model 1: Linear Regression

## Purpose

Predict the customer's **Average Rating** based on purchasing behavior and customer information.

### Input Features

- Customer ID
- Gender
- Age
- City
- Membership Type
- Total Spend
- Items Purchased
- Discount Applied
- Days Since Last Purchase
- Satisfaction Level

### Target

Average Rating

### Evaluation Metrics

- Mean Absolute Error (MAE)
- Mean Squared Error (MSE)
- Root Mean Squared Error (RMSE)
- R² Score

### Advantages

- Simple and easy to interpret.
- Suitable for continuous numerical prediction.
- Fast training time.

### Limitations

- Assumes a linear relationship between features and the target.
- Sensitive to outliers.

---

# Model 2: Logistic Regression

## Purpose

Predict whether a customer received a discount.

### Input Features

- Customer ID
- Gender
- Age
- City
- Membership Type
- Total Spend
- Items Purchased
- Average Rating
- Days Since Last Purchase
- Satisfaction Level

### Target

Discount Applied

### Evaluation Metrics

- Accuracy
- Confusion Matrix
- Classification Report

### Hyperparameter Tuning

GridSearchCV was used to determine the best model parameters.

Parameters Tested

- C = 0.01, 0.1, 1, 10, 100
- Solver = liblinear, lbfgs

### Advantages

- Performs well for binary classification.
- Produces probability estimates.
- Easy to interpret.

### Limitations

- Works best when classes are reasonably separable.
- Performance decreases for complex nonlinear relationships.

---

# Model 3: K-Means Clustering

## Purpose

Group customers with similar purchasing behavior into clusters.

### Number of Clusters

3

### Features Used

- Customer ID
- Gender
- Age
- City
- Membership Type
- Total Spend
- Items Purchased
- Days Since Last Purchase
- Satisfaction Level

### Evaluation Metric

- Silhouette Score

### Advantages

- Simple and efficient.
- Useful for customer segmentation.
- Supports targeted marketing strategies.

### Limitations

- Requires specifying the number of clusters.
- Sensitive to feature scaling.
- Can be affected by outliers.

---

# Performance Comparison

| Model | Learning Type | Evaluation |
|-------|---------------|------------|
| Linear Regression | Supervised | MAE, MSE, RMSE, R² Score |
| Logistic Regression | Supervised | Accuracy, Confusion Matrix, Classification Report |
| K-Means | Unsupervised | Silhouette Score |

---

# Best Use Cases

### Linear Regression

Best suited for predicting customer ratings and other continuous numerical values.

### Logistic Regression

Best suited for predicting whether discounts should be applied to customers.

### K-Means Clustering

Best suited for grouping customers into meaningful segments for marketing and customer relationship management.

---

# Overall Comparison

| Criteria | Linear Regression | Logistic Regression | K-Means |
|----------|-------------------|---------------------|----------|
| Problem Type | Regression | Classification | Clustering |
| Target Variable | Average Rating | Discount Applied | None |
| Supervised Learning | Yes | Yes | No |
| Easy to Interpret | Yes | Yes | Moderate |
| Hyperparameter Tuning | No | Yes | No |
| Business Value | Rating Prediction | Discount Prediction | Customer Segmentation |

---

# Final Decision

The three models complement each other:

- Linear Regression estimates customer satisfaction through Average Rating.
- Logistic Regression predicts whether a customer is likely to receive a discount.
- K-Means Clustering segments customers into groups with similar characteristics.

Together, these models provide valuable insights that can support pricing strategies, personalized marketing campaigns, customer retention, and overall business decision-making.