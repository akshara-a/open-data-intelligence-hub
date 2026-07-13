# Building a Recommendation System for E-Commerce

## Project Overview

This project implements multiple machine learning algorithms to build an e-commerce recommendation system that predicts customer ratings, purchase likelihood, and segments customers for personalized recommendations and targeted marketing.

## Dataset

* **Source:** Indian E-Commerce Customer Behavior Dataset (Kaggle)
* **Size:** 25,000 rows and 29 columns
* **Key Features:** `customer_id`, `product_id`, `rating`, `purchased`, `revenue`, `cart_abandoned`

## Machine Learning Tasks

### Part A: Regression - Rating Prediction

**Algorithms Used:**

* Linear Regression
* Ridge Regression

**Target Variable:** `rating`

| Model             | MAE    | RMSE   | R² Score |
| ----------------- | ------ | ------ | -------- |
| Linear Regression | 0.2207 | 0.5447 | 0.0208   |
| Ridge Regression  | 0.2208 | 0.5447 | 0.0207   |

**Best Model:** Linear Regression

### Part B: Classification - Purchase Prediction

**Algorithm Used:** Logistic Regression

**Target Variable:** `purchased`

| Metric    | Score  |
| --------- | ------ |
| Accuracy  | 99.96% |
| Precision | 100%   |
| Recall    | 99.82% |
| F1-Score  | 99.91% |
| ROC-AUC   | 100%   |

### Part C: Clustering - Customer Segmentation

**Algorithm Used:** K-Means Clustering

**Optimal Number of Clusters:** 4

**Silhouette Score:** 0.2981

| Cluster | Count | Average Revenue | Customer Type   |
| ------- | ----: | --------------: | --------------- |
| 0       | 4,117 |          427.53 | Low-Engagement  |
| 1       | 1,272 |        4,106.83 | High-Value      |
| 2       | 2,154 |          504.69 | Cart Abandoners |
| 3       |   899 |        2,274.77 | Regular         |

## Key Findings

### Features Influencing Customer Ratings

**Positive Impact**

* discount_amount
* discount_percent
* unit_price

**Negative Impact**

* avg_spending_per_session
* user_type

### Features Influencing Purchase Decisions

**Positive Impact**

* avg_spending_per_session
* added_to_cart

**Negative Impact**

* cart_abandoned
* rating
* unit_price

## Recommendation System Workflow

1. User visits a product page.
2. Regression model predicts the expected product rating.
3. Classification model predicts the purchase probability.
4. K-Means identifies the customer's segment.
5. A combined recommendation score is calculated using:

```
Combined Score = (Predicted Rating × 0.4) + (Purchase Probability × 0.6)
```

6. Products with the highest combined scores are recommended to the customer.

## Model Comparison

| Model               | Task                  | Best Performance         | Business Value                  |
| ------------------- | --------------------- | ------------------------ | ------------------------------- |
| Linear Regression   | Rating Prediction     | MAE: 0.2207              | Recommend highly rated products |
| Logistic Regression | Purchase Prediction   | Accuracy: 99.96%         | Identify likely buyers          |
| K-Means Clustering  | Customer Segmentation | Silhouette Score: 0.2981 | Enable targeted marketing       |

## Business Recommendations

### Recommendation Strategy

* Recommend products with predicted ratings greater than 4.0.
* Prioritize products with higher discount percentages.

### Targeted Marketing

* Focus marketing campaigns on customers with purchase probabilities above 70%.
* Prioritize customers with higher average spending per session.

### Customer Segmentation

* **Cluster 0:** Win-back campaigns for low-engagement customers.
* **Cluster 1:** Loyalty rewards for high-value customers.
* **Cluster 2:** Cart recovery campaigns for cart abandoners.
* **Cluster 3:** Standard promotional campaigns for regular customers.

## Technologies Used

* Python 3.12
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Scikit-learn

  * Linear Regression
  * Ridge Regression
  * Logistic Regression
  * K-Means Clustering
  * GridSearchCV
  * StandardScaler

## Installation

```bash
pip install pandas numpy matplotlib seaborn scikit-learn kneed jupyter
```

## Results Summary

* Best Regression Model: Linear Regression (MAE: 0.2207)
* Best Classification Model: Logistic Regression (Accuracy: 99.96%)
* Optimal Number of Clusters: 4 (Silhouette Score: 0.2981)
* Most Valuable Customer Segment: Cluster 1 (High-Value Customers)

## Conclusion

This project demonstrates an end-to-end machine learning recommendation system by integrating Regression, Classification, and Clustering techniques. The combined approach enables personalized product recommendations, customer segmentation, and targeted marketing strategies that can improve customer engagement and increase sales conversion.
