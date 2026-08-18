# Task 6 Report

## Objective

To develop an E-Commerce Recommendation System using Machine Learning algorithms for customer behavior analysis.

## Data Preprocessing

- Removed duplicate records
- Handled missing values
- Encoded categorical variables

## Exploratory Data Analysis

Generated visualizations for:

- Rating Distribution
- Purchase Status
- Product Category Distribution
- Revenue Distribution
- Correlation Heatmap

## Machine Learning Models

### Linear Regression

Used for predicting product ratings.

Metrics:
- MAE
- RMSE
- R² Score

### Ridge Regression

Applied regularization and compared performance with Linear Regression.

### Logistic Regression

Used to predict customer purchase decisions.

Metrics:
- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC

### K-Means Clustering

Grouped customers into clusters using purchasing behavior.

Evaluation:
- Elbow Method
- Silhouette Score

## Hyperparameter Tuning

Performed GridSearchCV for:
- Ridge Regression
- Logistic Regression

Optimized K-Means using Silhouette Score.

## Conclusion

The project successfully implemented multiple machine learning techniques for customer analytics.

The developed models can help businesses understand customer behavior, predict purchases, estimate product ratings, and segment customers for targeted marketing strategies.