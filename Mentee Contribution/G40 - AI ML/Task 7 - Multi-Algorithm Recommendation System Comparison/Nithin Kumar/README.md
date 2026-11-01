# Task 7 - Multi-Algorithm Recommendation System Comparison

## Student
Nithin Kumar

## Project Overview

This project builds a multi-algorithm machine learning solution for an
e-commerce recommendation system.

The project compares three different machine learning approaches:

1. Ridge Regression - Product rating prediction
2. Logistic Regression - Purchase prediction
3. K-Means Clustering - Customer segmentation

Hyperparameter optimization is performed using GridSearchCV.

## Dataset

A synthetic e-commerce dataset containing 1500 records was generated
for this project.

### Features

- UserID
- ProductID
- ProductCategory
- Price
- NumberOfViews
- CartStatus
- TimeSpent
- PreviousPurchases
- Rating
- PurchaseStatus
- TotalAmountSpent

## 1. Ridge Regression

### Goal

Predict the rating a customer may give to a product.

### Baseline Results

- MAE: 0.4047
- RMSE: 0.5002
- R2 Score: 0.6139

### Hyperparameter Tuning

GridSearchCV was used to tune the alpha parameter.

Best alpha:

10

### Tuned Results

- MAE: 0.4051
- RMSE: 0.5005
- R2 Score: 0.6134

### Business Use

Rating prediction can help an e-commerce business recommend products
that customers are more likely to enjoy.

## 2. Logistic Regression

### Goal

Predict whether a customer is likely to purchase a product.

### Baseline Results

- Accuracy: 0.8500
- Precision: 0.8672
- Recall: 0.9414
- F1 Score: 0.9028

### Hyperparameter Tuning

GridSearchCV selected:

- C: 0.1
- max_iter: 100
- solver: lbfgs

### Tuned Results

- Accuracy: 0.8533
- Precision: 0.8648
- Recall: 0.9505
- F1 Score: 0.9056

### Business Use

The model can identify customers who are more likely to purchase,
allowing businesses to provide targeted offers and personalized
recommendations.

## 3. K-Means Clustering

### Goal

Group customers based on similar shopping behaviour.

The following values of K were evaluated:

- K = 2
- K = 3
- K = 4
- K = 5
- K = 6

The best number of clusters based on Silhouette Score was:

K = 2

### Final Results

- Inertia: 1118.3634
- Silhouette Score: 0.3116

### Customer Distribution

- Cluster 0: 154 customers
- Cluster 1: 143 customers

### Business Use

Customer segmentation can help businesses create targeted marketing
campaigns and personalized recommendation strategies.

## Model Comparison

| ML Task | Algorithm | Best Result | Business Use |
|---|---|---|---|
| Regression | Ridge Regression | RMSE = 0.5005, R2 = 0.6134 | Product rating prediction |
| Classification | Logistic Regression | Accuracy = 0.8533, F1 = 0.9056 | Purchase prediction |
| Clustering | K-Means | Silhouette = 0.3116 | Customer segmentation |

## Final Conclusion

The three machine learning approaches solve different e-commerce
business problems.

Ridge Regression provides useful product rating predictions.

Logistic Regression achieved strong purchase prediction performance,
with an accuracy of 85.33% and an F1 score of 0.9056.

K-Means successfully divided customers into two behavioural segments.

Among the supervised models, Logistic Regression produced the strongest
classification performance and can be useful for identifying likely buyers.

Together, these models can support personalized recommendations,
customer targeting, and customer segmentation.

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn

## Output Files

- `confusion_matrix.png`
- `elbow_method.png`
- `customer_segments.csv`
- `model_comparison.csv`

## How to Run

Generate the dataset:

python generate_dataset.py

Run the machine learning models:

python recommendation_system.py