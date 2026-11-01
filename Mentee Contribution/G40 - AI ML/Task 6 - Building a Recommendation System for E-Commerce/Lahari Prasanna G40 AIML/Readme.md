# E-Commerce Recommendation System

## Project Overview

This project uses machine learning techniques to analyze e-commerce customer behavior. It focuses on predicting product ratings, predicting purchase likelihood, and grouping customers based on their shopping patterns.

## Objectives

- Predict product ratings using Regression.
- Predict purchase likelihood using Classification.
- Segment customers using K-Means Clustering.
- Tune model parameters and compare performance.
- Identify useful business insights from customer behavior.

## Dataset

**File:** `Ecommerce.csv`

The dataset contains 25,000 session records and 29 columns, including customer and session IDs, product information, browsing activity, discounts, purchase status, ratings, revenue, and payment details.

## Technologies Used

- Python
- Google Colab / Jupyter Notebook
- Pandas and NumPy
- Matplotlib
- Scikit-learn

## Project Workflow

1. Load and inspect the dataset.
2. Clean and preprocess the data.
3. Perform exploratory data analysis (EDA).
4. Train and evaluate Linear Regression and Ridge Regression models.
5. Train and evaluate a Logistic Regression model.
6. Tune model hyperparameters.
7. Use K-Means to segment customers.
8. Compare model results and summarize business insights.

## Models and Results

### 1. Regression

Linear Regression and Ridge Regression were used to predict product ratings.

| Model | MAE | RMSE | R² |
|---|---:|---:|---:|
| Linear Regression | 0.9219 | 1.1415 | -0.0829 |
| Tuned Ridge Regression | 0.8970 | 1.1033 | -0.0115 |

Ridge Regression performed slightly better than Linear Regression, although the negative R² indicates that rating prediction needs further improvement.

### 2. Classification

Logistic Regression was used to predict whether a customer session would result in a purchase.

| Metric | Test Result |
|---|---:|
| Accuracy | 0.6142 |
| Precision | 0.3601 |
| Recall | 0.9234 |
| F1-score | 0.5181 |
| ROC-AUC | 0.7644 |

The classification threshold was selected using cross-validation on the training data. The final threshold was approximately 0.2691. The model identifies most actual purchases, but it also produces false positive predictions.

### 3. Customer Segmentation

K-Means Clustering was applied to customer-level features.

- Number of clusters: 3
- Initialization: `k-means++`
- Inertia: 60178.54
- Silhouette score: 0.1216

The three clusters showed different purchase rates and revenue patterns. Cluster 1 had the highest average purchase rate and revenue, while Cluster 0 had the lowest purchase rate.

## Business Insights

- High-value customers can be identified for targeted loyalty campaigns.
- Customers who add items to their carts but purchase less frequently may benefit from improved checkout experiences or targeted offers.
- Purchase prediction can help prioritize marketing campaigns, but false positives should be considered.
- Rating prediction requires further improvement before it can be relied upon for recommendations.

## How to Run

1. Download or clone the project files.
2. Place `Ecommerce.csv` in the location expected by the notebook.
3. Open `Ecommerce_Recommendation_System.ipynb` in Google Colab or Jupyter Notebook.
4. Update the dataset path if necessary.
5. Run the notebook cells in order.

## Limitations

- The regression model has a negative R² score.
- The classification model has relatively low precision at the selected threshold.
- The silhouette score indicates that the customer clusters are not strongly separated.
- Further feature engineering, model testing, and parameter tuning may improve the results.

## Conclusion

This project demonstrates the use of regression, classification, and clustering for different e-commerce business objectives. The results provide initial insights into purchase behavior and customer segments, while also highlighting areas where model performance can be improved.