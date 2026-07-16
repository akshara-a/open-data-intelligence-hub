# Customer Churn Exploratory Data Analysis Report

## Student Details

**Name:** Nidhi Sandbhor

**Batch:** G40 AIML

**Project Title:** Customer Churn Exploratory Data Analysis Using Pandas

---

# 1. Introduction

Customer churn is one of the biggest challenges for subscription-based businesses. Customer churn occurs when customers discontinue using a company's services. High churn leads to reduced revenue, lower customer retention, and increased costs for acquiring new customers.

This project focuses on analyzing customer behavior using the Telco Customer Churn dataset. The goal is to clean the dataset, perform exploratory data analysis (EDA), identify factors affecting customer churn, and provide business recommendations to improve customer retention.

---

# 2. Problem Statement

A telecom company is experiencing a high customer churn rate. The company wants to understand why customers leave their services and identify the key factors contributing to churn.

The objective of this project is to analyze customer data, identify churn patterns, and provide recommendations that help reduce customer churn and improve customer satisfaction.

---

# 3. Objectives

The objectives of this project are:

* Load and inspect the customer churn dataset.
* Perform data cleaning and preprocessing.
* Identify missing values and duplicate records.
* Analyze customer behavior using EDA.
* Create meaningful visualizations.
* Generate business insights.
* Suggest feature engineering ideas.
* Recommend strategies to reduce customer churn.

---

# 4. Dataset Overview

The dataset contains customer information collected from a telecom subscription company.

It includes customer demographic information, subscription details, billing information, payment methods, internet services, customer support details, and churn status.

Important columns include:

* CustomerID
* Gender
* SeniorCitizen
* Partner
* Dependents
* Tenure
* PhoneService
* InternetService
* Contract
* PaymentMethod
* MonthlyCharges
* TotalCharges
* Churn

The target variable used in this analysis is **Churn**, where:

* Yes = Customer left the company
* No = Customer stayed with the company

---

# 5. Data Quality Issues

During the inspection of the dataset, the following issues were identified:

### Issue 1

The TotalCharges column contained blank values and was stored as text instead of numeric.

### Solution

Converted TotalCharges into numeric format and replaced missing values using the median value.

---

### Issue 2

Duplicate customer records were checked to avoid incorrect analysis.

### Solution

Duplicate rows were removed whenever found.

---

### Issue 3

Some categorical columns contained inconsistent formatting such as extra spaces or mixed letter cases.

### Solution

Text values were standardized using string cleaning methods.

---

# 6. Data Cleaning

The following preprocessing steps were performed:

* Converted TotalCharges to numeric format.
* Handled missing values.
* Removed duplicate records.
* Standardized categorical values.
* Renamed columns where necessary.
* Verified data types.

These steps improved the quality and consistency of the dataset before analysis.

---

# 7. Exploratory Data Analysis

Several exploratory analyses were performed to understand customer behavior.

### Churn Distribution

The majority of customers remained with the company, while a significant portion had churned.

### Tenure Analysis

Customers with shorter tenure were more likely to churn than long-term customers.

### Contract Analysis

Customers with month-to-month contracts showed the highest churn rate.

### Monthly Charges Analysis

Customers paying higher monthly charges were more likely to discontinue the service.

### Payment Method Analysis

Customers using electronic check payment methods had higher churn compared to customers using automatic payment methods.

### Correlation Analysis

Correlation analysis showed relationships among numerical variables such as tenure, monthly charges, and total charges.

---

# 8. Feature Engineering

To improve future machine learning models, the following new features were created:

* TenureGroup
* HighMonthlyCharge
* AutoPay

These features help represent customer behavior more effectively.

---

# 9. Key Business Insights

### Insight 1

Customers with month-to-month contracts have the highest churn rate.

### Insight 2

Customers with shorter tenure are more likely to leave.

### Insight 3

Higher monthly charges increase the probability of churn.

### Insight 4

Customers using electronic check payments show higher churn.

### Insight 5

Customers without technical support are more likely to churn.

### Insight 6

Customers without online security services have higher churn.

### Insight 7

Long-term customers are generally more loyal.

### Insight 8

Customers using additional telecom services tend to remain with the company longer.

---

# 10. Business Recommendations

Based on the analysis, the following recommendations are suggested:

* Encourage customers to switch to yearly contracts.
* Improve customer onboarding during the initial months.
* Offer personalized discounts for high-risk customers.
* Strengthen customer support services.
* Promote automatic payment methods.
* Bundle internet security services with subscription plans.
* Increase customer engagement through loyalty programs.
* Monitor high-risk customers regularly using predictive analytics.

---

# 11. Conclusion

The analysis identified contract type, tenure, monthly charges, payment method, and support services as the major factors influencing customer churn.

Customers with month-to-month contracts, low tenure, and high monthly charges are more likely to discontinue their services.

By improving customer engagement, offering long-term subscription benefits, enhancing technical support, and implementing targeted retention strategies, the company can significantly reduce churn and improve customer satisfaction.

This exploratory analysis also provides a strong foundation for future machine learning models that can accurately predict customer churn.
