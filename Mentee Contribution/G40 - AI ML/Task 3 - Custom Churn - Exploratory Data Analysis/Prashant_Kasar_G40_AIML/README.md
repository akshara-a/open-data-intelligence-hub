# 🏦 Bank Customer Churn Prediction - Exploratory Data Analysis (EDA)

---

## 📌 Project Overview

This project performs Exploratory Data Analysis (EDA) on a Bank Customer Churn dataset to identify key factors that influence customer churn behavior. The objective is to analyze customer patterns and provide actionable insights that can help improve customer retention strategies.

---

## 🎯 Problem Statement

Banks face significant losses when customers leave their services. Understanding the reasons behind customer churn is essential to improve retention. This project analyzes customer data to identify churn patterns.

---

## 📂 Dataset Description

The dataset contains 10,000 customer records with the following attributes:

| Column | Description |
|------|--------|
| customer_id | Unique customer identifier |
| credit_score | Customer credit score |
| country | Country of customer |
| gender | Gender of customer |
| age | Age of customer |
| tenure | Number of years with bank |
| balance | Account balance |
| products_number | Number of bank products used |
| credit_card | Whether customer has credit card |
| active_member | Whether customer is active |
| estimated_salary | Estimated salary |
| churn | Target variable (1 = churn, 0 = not churn) |

---

## 🧹 Data Preprocessing

- Removed duplicate records
- Verified no missing values
- Converted categorical variables where needed
- Ensured correct data types

---

## 📊 Exploratory Data Analysis

Performed detailed analysis on:

### ✔ Univariate Analysis
- Customer churn distribution
- Age distribution
- Balance distribution

### ✔ Bivariate Analysis
- Gender vs Churn
- Country vs Churn
- Credit Score vs Churn
- Active Membership vs Churn

### ✔ Correlation Analysis
- Relationship between numerical features and churn

---

## 📈 Key Insights

- Customers with low balance are more likely to churn
- Age significantly impacts churn behavior
- Inactive members show higher churn rates
- Credit score influences customer retention
- Geography plays an important role in churn patterns

---

## 💡 Business Recommendations

- Improve engagement for inactive customers
- Provide offers for low-balance users
- Introduce loyalty programs for long-term customers
- Monitor high-risk customers using predictive models
- Regional strategies for customer retention

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Jupyter Notebook

---

## 📁 Project Structure
Bank_Customer_Churn_Project/
│
├── Bank_Customer_Churn.csv
├── Cleaned_Bank_Customer_Churn.csv
├── Bank_Churn_EDA.ipynb
├── Bank_Churn_Report.pdf
└── README.md


---

## 🚀 How to Run This Project

```bash
git clone <your-repo-url>
cd <repo-folder>
jupyter notebook

Open:
Bank_Churn_EDA.ipynb