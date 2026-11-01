# Fraud Detection using Machine Learning

## Objective

To identify fraudulent credit card transactions using machine learning classification models.

## Dataset

The project uses the Credit Card Fraud Detection dataset.

## Data Preprocessing

- Checked missing values
- Removed duplicate records
- Scaled numerical features
- Split the dataset into training and testing sets

## Exploratory Data Analysis

Performed:

- Class Distribution
- Amount Distribution
- Correlation Heatmap

## Machine Learning Models

### Logistic Regression

Evaluated using Accuracy, Precision, Recall, F1 Score, and ROC-AUC.

### Decision Tree

Compared against Logistic Regression.

### Random Forest

Selected as the best-performing model for fraud detection.

## Hyperparameter Tuning

GridSearchCV was used to optimize:

- Decision Tree
- Random Forest

## Feature Importance

Analyzed the most influential features used by the Random Forest model.

## Conclusion

The project successfully developed and compared multiple machine learning models for fraud detection. Random Forest provided the strongest performance and can help financial institutions identify potentially fraudulent transactions more effectively.