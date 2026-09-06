# 🛒 Amazon E-Commerce Recommendation System

A Machine Learning based E-Commerce Recommendation System built using Python and Scikit-Learn.

---

# 📌 Project Overview

This project analyzes Amazon product data using Machine Learning techniques to:

- Analyze product data
- Predict purchase likelihood
- Segment products using clustering
- Compare model performance

---

# 🚀 Features

## 📊 Dashboard
- Total Products
- Average Rating
- Average Discount
- Product Categories

## 📈 Exploratory Data Analysis (EDA)
- Rating Distribution
- Discount Distribution
- Top Product Categories
- Correlation Heatmap
- Actual Price vs Discounted Price

## 🤖 Purchase Prediction
- Logistic Regression
- Predicts purchase likelihood using:
  - Actual Price
  - Discounted Price
  - Discount Percentage
  - Rating Count
  - Product Category

## 👥 Product Segmentation
- K-Means Clustering
- Groups products into different clusters based on product characteristics.

## ⚙ Hyperparameter Tuning
- GridSearchCV
- Finds the best parameters for Logistic Regression.

## 📉 Model Evaluation
- Accuracy
- Precision
- Recall
- F1-Score
- ROC-AUC
- Silhouette Score

---

# 🛠 Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-Learn
- Jupyter Notebook

---

# 📂 Dataset

The dataset contains Amazon product information including:

- Product Name
- Product Category
- Product Rating
- Rating Count
- Actual Price
- Discounted Price
- Discount Percentage

---

# 🤖 Machine Learning Algorithms

- Logistic Regression
- K-Means Clustering
- GridSearchCV

---

# 📊 Evaluation Metrics

### Logistic Regression
- Accuracy
- Precision
- Recall
- F1-Score
- ROC-AUC

### K-Means
- Elbow Method
- Silhouette Score

---

# ▶️ How to Run

```bash
git clone <repository-link>
```

```bash
cd Amazon-Recommendation-System
```

```bash
pip install -r requirements.txt
```

```bash
jupyter notebook
```

Open the notebook and run all cells.

---

# 📌 Conclusion

This project demonstrates how Machine Learning can be used in an e-commerce platform to predict purchase likelihood and group products into meaningful clusters. Logistic Regression helps identify products with a higher likelihood of purchase, while K-Means clustering segments products based on their characteristics, supporting better recommendation and marketing strategies.