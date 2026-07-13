# Customer Segmentation with Actionable Business Insights

## Project Overview

This project applies machine learning techniques to analyze customer purchasing behavior and group customers into meaningful segments. The objective is to help businesses better understand customer characteristics, improve marketing strategies, enhance customer retention, and maximize revenue through data-driven decision-making.

The project includes customer segmentation using K-Means clustering, regression for spending prediction, classification for campaign response prediction, hyperparameter optimization, and business-focused recommendations.

---

# Objectives

* Analyze customer purchasing behavior.
* Perform exploratory data analysis (EDA).
* Clean and preprocess customer data.
* Create meaningful customer segments using K-Means clustering.
* Predict customer spending using regression models.
* Predict customer campaign response using Logistic Regression.
* Optimize machine learning models using GridSearchCV.
* Generate actionable business insights.

---

# Dataset

**Dataset:** Marketing Campaign (Customer Personality Analysis)

The dataset contains customer demographic information, purchasing behavior, marketing campaign responses, and website activity.

### Main Features

* ID
* Year_Birth
* Education
* Marital_Status
* Income
* Kidhome
* Teenhome
* Recency
* Product spending information
* Website purchases
* Store purchases
* Catalog purchases
* Campaign responses
* Customer complaint status
* Response (Target)

Additional engineered features:

* Age
* Children
* TotalSpending

---

# Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Scikit-learn
* Streamlit

---

# Machine Learning Models

## Clustering

* K-Means Clustering

### Cluster Evaluation

* Elbow Method
* Silhouette Score

---

## Regression Models

* Linear Regression
* Ridge Regression

Evaluation Metrics:

* Mean Absolute Error (MAE)
* Mean Squared Error (MSE)
* Root Mean Squared Error (RMSE)
* R² Score

---

## Classification Model

* Logistic Regression

Evaluation Metrics:

* Accuracy
* Precision
* Recall
* F1-Score
* ROC-AUC Score
* Confusion Matrix

---

## Hyperparameter Optimization

GridSearchCV was used to optimize:

* Ridge Regression
* Logistic Regression

---

# Project Workflow

1. Data Loading
2. Data Cleaning
3. Missing Value Handling
4. Feature Engineering
5. Exploratory Data Analysis
6. Feature Encoding
7. Feature Scaling
8. Customer Segmentation
9. Cluster Profiling
10. Regression Modeling
11. Classification Modeling
12. Hyperparameter Tuning
13. Model Evaluation
14. Business Insights
15. Result Visualization

---

# Visualizations

The project includes the following visualizations:

* Customer Spending Distribution
* Income Distribution
* Age Distribution
* Correlation Heatmap
* Elbow Method
* Silhouette Score
* PCA Cluster Visualization
* Cluster-wise Customer Count
* Revenue by Customer Segment
* Actual vs Predicted Regression Plot
* Confusion Matrix

---

# Business Insights

The analysis identified multiple customer segments with different purchasing behaviors.

Key recommendations include:

* Reward high-value customers through loyalty programs.
* Re-engage inactive customers with personalized campaigns.
* Target discount-sensitive customers using promotional offers.
* Recommend premium products to high-income customers.
* Improve campaign efficiency through customer response prediction.

---

# Project Files

```text
Task8.ipynb
app.py
marketing_campaign.csv
README.md
business_insights.md
requirements.txt
customer_segments.csv
```

---

# Requirements

Install the required packages:

```bash
pip install -r requirements.txt
```

Required libraries:

* streamlit
* pandas
* numpy
* matplotlib
* scikit-learn

---

# Running the Streamlit Application

Run the following command:

```bash
streamlit run app.py
```

The application provides:

* Dataset Overview
* Exploratory Data Analysis
* Customer Segmentation
* Regression Analysis
* Classification Analysis
* Business Insights Dashboard

---

# Results

The project successfully:

* Segmented customers using K-Means clustering.
* Predicted customer spending using Linear and Ridge Regression.
* Predicted campaign response using Logistic Regression.
* Improved model performance using GridSearchCV.
* Generated actionable business recommendations for marketing and customer retention.

---

# Conclusion

This project demonstrates how machine learning techniques can be applied to customer analytics. Customer segmentation combined with predictive modeling enables organizations to personalize marketing campaigns, improve customer engagement, optimize promotional strategies, and support data-driven business decisions.
