# Decision Log - Task 7: Multi-Algorithm Recommendation System Comparison

## Project Title

**Multi-Algorithm Recommendation System Comparison for E-Commerce Customer Behavior Analysis**

---

# Objective

The objective of this project is to compare multiple machine learning algorithms for solving different business problems in an e-commerce environment. Instead of relying on a single model, the project evaluates regression, classification, and clustering techniques to understand their strengths and practical business applications.

---

# Dataset Selection Decision

The **E-commerce Customer Behavior Dataset** was selected because it contains customer demographic information, purchasing behavior, spending details, ratings, and discount information.

Important dataset features include:

* Customer ID
* Gender
* Age
* City
* Membership Type
* Total Spend
* Items Purchased
* Average Rating
* Discount Applied
* Days Since Last Purchase
* Satisfaction Level

This dataset provides sufficient information to perform regression, classification, and clustering tasks required for this project.

---

# Data Preprocessing Decisions

Several preprocessing steps were performed before training the machine learning models.

### Duplicate Records

Duplicate records were identified and removed to avoid bias in model training.

### Missing Values

The dataset was checked for missing values before model development. Since the dataset was clean, no additional imputation was required.

### Categorical Encoding

Machine learning algorithms require numerical input. Therefore, categorical variables such as Gender, City, Membership Type, Discount Applied, and Satisfaction Level were converted into numerical values using Label Encoding.

### Feature Scaling

StandardScaler was applied before Regression, Logistic Regression, and K-Means Clustering because these algorithms perform better when numerical features are standardized.

---

# Regression Model Decision

## Selected Algorithm

**Ridge Regression**

### Reason for Selection

Ridge Regression was selected instead of Linear Regression because it reduces overfitting through L2 regularization. It performs well when multiple numerical features contribute to the prediction.

### Prediction Target

Average Rating

### Input Features

* Gender
* Age
* City
* Membership Type
* Total Spend
* Items Purchased
* Discount Applied
* Days Since Last Purchase
* Satisfaction Level

### Evaluation Metrics

* Mean Absolute Error (MAE)
* Root Mean Squared Error (RMSE)
* R² Score

These metrics measure prediction accuracy and explain how well the model predicts customer ratings.

---

# Hyperparameter Optimization Decision

GridSearchCV was used to optimize Ridge Regression.

### Tuned Parameter

* alpha

Candidate values:

* 0.01
* 0.1
* 1
* 10
* 100

The model with the highest cross-validation performance was selected as the final regression model.

---

# Classification Model Decision

## Selected Algorithm

**Logistic Regression**

### Reason for Selection

Logistic Regression is a simple and effective algorithm for binary classification problems. It predicts whether a customer received a discount based on purchasing behavior.

### Target Variable

Discount Applied

### Input Features

* Gender
* Age
* City
* Membership Type
* Total Spend
* Items Purchased
* Average Rating
* Days Since Last Purchase
* Satisfaction Level

### Evaluation Metrics

* Accuracy
* Precision
* Recall
* F1 Score
* Confusion Matrix

These metrics evaluate the ability of the model to correctly classify customer discount status.

---

# Logistic Regression Hyperparameter Tuning

GridSearchCV was applied to improve the classification model.

Parameters explored:

* C
* Solver
* Max Iterations

The combination producing the highest cross-validation accuracy was selected.

---

# Clustering Model Decision

## Selected Algorithm

**K-Means Clustering**

### Reason for Selection

K-Means is widely used for customer segmentation because it groups customers with similar purchasing behavior.

### Features Used

* Age
* Total Spend
* Items Purchased
* Average Rating
* Days Since Last Purchase

### Evaluation

The Elbow Method was used to estimate the appropriate number of clusters.

Silhouette Score was calculated to evaluate cluster quality.

---

# Model Comparison Decision

Three machine learning algorithms were compared based on their objectives.

| Task           | Algorithm           | Purpose                      |
| -------------- | ------------------- | ---------------------------- |
| Regression     | Ridge Regression    | Predict customer ratings     |
| Classification | Logistic Regression | Predict discount application |
| Clustering     | K-Means             | Customer segmentation        |

Each algorithm solves a different business problem, making the overall recommendation system more comprehensive.

---

# Business Interpretation

The Ridge Regression model predicts customer ratings, enabling the business to recommend products that customers are more likely to appreciate.

The Logistic Regression model predicts whether discounts are likely to be applied, helping marketing teams design personalized promotional campaigns.

The K-Means clustering model segments customers into groups based on purchasing behavior. These customer segments can be used to develop targeted marketing strategies, improve customer retention, and personalize recommendations.

Combining these three approaches allows the business to make more informed decisions regarding customer engagement and recommendation strategies.

---

# Challenges Faced

* Selecting appropriate target variables from the available dataset.
* Encoding multiple categorical features.
* Choosing suitable evaluation metrics for each machine learning algorithm.
* Determining the optimal number of clusters.
* Improving model performance through hyperparameter tuning.

These challenges were addressed through preprocessing, feature scaling, and GridSearchCV.

---

# Final Decision

The selected combination of Ridge Regression, Logistic Regression, and K-Means Clustering provides a complete solution for analyzing customer behavior in an e-commerce environment.

Using multiple algorithms enables better prediction, customer segmentation, and business decision-making compared to relying on a single machine learning model.

The project successfully demonstrates how regression, classification, and clustering can work together to support intelligent recommendation systems for e-commerce platforms.
