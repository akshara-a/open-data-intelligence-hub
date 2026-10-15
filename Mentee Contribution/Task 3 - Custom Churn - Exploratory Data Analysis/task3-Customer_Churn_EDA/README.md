# Customer Churn Exploratory Data Analysis

## 📌 Project Overview

This project performs **Exploratory Data Analysis (EDA)** on a Telco
Customer Churn dataset. The objective is to understand customer churn
patterns, identify customer groups associated with higher churn, analyze
numerical and categorical features, and provide business recommendations
for improving customer retention.

## 👩‍🎓 Student Details

-   **Student Name:** Aiesha Shaik
-   **Department:** Computer Science and Engineering
-   **Project:** Customer Churn Exploratory Data Analysis

## 📊 Dataset

The project uses a **Telco Customer Churn** dataset containing customer
demographic, service, contract, billing, and churn information.

### Main Features

-   `customerID` -- Unique customer identifier
-   `gender` -- Customer gender
-   `SeniorCitizen` -- Senior citizen indicator
-   `Partner` -- Partner status
-   `Dependents` -- Dependents status
-   `tenure` -- Number of months the customer has stayed
-   `PhoneService` -- Phone service subscription
-   `MultipleLines` -- Multiple line subscription
-   `InternetService` -- Internet service type
-   `OnlineSecurity` -- Online security subscription
-   `OnlineBackup` -- Online backup subscription
-   `DeviceProtection` -- Device protection subscription
-   `TechSupport` -- Technical support subscription
-   `StreamingTV` -- Streaming TV subscription
-   `StreamingMovies` -- Streaming movies subscription
-   `Contract` -- Contract type
-   `PaperlessBilling` -- Paperless billing status
-   `PaymentMethod` -- Payment method
-   `MonthlyCharges` -- Monthly customer charges
-   `TotalCharges` -- Total customer charges
-   `Churn` -- Target variable indicating whether the customer churned

## 🎯 Objectives

The main objectives of this analysis are:

1.  Understand the structure and characteristics of the dataset.
2.  Identify and handle missing values and duplicate records.
3.  Correct inappropriate data types.
4.  Analyze customer churn distribution.
5.  Compare numerical features between churned and non-churned
    customers.
6.  Analyze categorical features with respect to churn.
7.  Identify potential outliers.
8.  Study relationships between numerical variables.
9.  Identify important churn patterns.
10. Provide business recommendations to reduce customer churn.

## 🧹 Data Cleaning

The following data-cleaning tasks were performed:

-   Checked for missing values.
-   Handled missing numerical values using median imputation.
-   Handled missing categorical values using mode imputation.
-   Converted `TotalCharges` to a numerical data type.
-   Checked for duplicate records.
-   Removed duplicate records.
-   Removed the customer identifier when it was not useful for analysis.
-   Checked numerical variables for potential outliers.

## 📈 Exploratory Data Analysis

The notebook includes:

### Univariate Analysis

Analysis of individual variables such as:

-   Customer tenure
-   Monthly charges
-   Total charges
-   Churn distribution

### Bivariate Analysis

Comparison of important features with churn, including:

-   Contract vs Churn
-   Internet Service vs Churn
-   Payment Method vs Churn
-   Tenure vs Churn
-   Monthly Charges vs Churn

### Numerical Analysis

Statistical summaries include:

-   Mean
-   Median
-   Minimum
-   Maximum
-   Standard deviation

### Correlation Analysis

A correlation heatmap is used to understand relationships between
numerical variables.

### Outlier Analysis

Boxplots are used to identify potential unusual values in numerical
features.

## 📊 Visualizations

The analysis contains more than the required eight visualizations,
including:

1.  Churn Count Plot
2.  Churn Percentage Pie Chart
3.  Tenure Histogram
4.  Monthly Charges Histogram
5.  Monthly Charges Boxplot
6.  Contract vs Churn Chart
7.  Internet Service vs Churn Chart
8.  Payment Method vs Churn Chart
9.  Tenure vs Churn Visualization
10. Monthly Charges vs Churn Visualization
11. Correlation Heatmap
12. Tenure vs Total Charges Scatter Plot

Each visualization is accompanied by an observation explaining the
important pattern.

## 🔍 Key Findings

The EDA focuses on identifying:

-   Overall customer churn percentage.
-   Customer groups with higher churn.
-   Differences in tenure between churned and non-churned customers.
-   Differences in monthly and total charges.
-   Churn patterns across contract types.
-   Churn patterns across internet service types.
-   Churn patterns across payment methods.
-   Potential outliers and numerical relationships.

The identified relationships represent **associations observed during
EDA and should not be interpreted as proof of causation**.

## 💡 Business Recommendations

Based on the analysis, possible customer-retention strategies include:

1.  Encourage month-to-month customers to choose longer-term contracts
    through discounts and loyalty benefits.
2.  Provide stronger onboarding and support for newer customers.
3.  Review pricing plans for customers with higher monthly charges.
4.  Investigate services associated with higher churn and improve
    service quality.
5.  Simplify billing and payment processes.
6.  Use customer segmentation to identify high-risk customers.
7.  Develop targeted retention campaigns for customers showing higher
    churn risk.

## 🛠️ Technologies Used

-   Python
-   Pandas
-   NumPy
-   Matplotlib
-   Seaborn
-   Jupyter Notebook
-   ReportLab

## 📁 Project Structure

``` text
CUSTOMER_CHURN_EDA_AIESHA/
│
├── Customer_Churn_EDA_Aiesha.ipynb
├── Customer_Churn_EDA_Report_Aiesha.pdf
├── Customer_Churn_Dataset_Aiesha.csv
└── Cleaned_Customer_Churn_Dataset_Aiesha.csv
```

## ▶️ How to Run

### 1. Install required libraries

``` bash
pip install pandas numpy matplotlib seaborn jupyter reportlab
```

### 2. Open Jupyter Notebook

``` bash
jupyter notebook
```

### 3. Open

``` text
Customer_Churn_EDA_Aiesha.ipynb
```

### 4. Run all notebook cells

Use **Run All** in Jupyter Notebook or VS Code.

## 📄 Assignment Deliverables

The project includes:

-   Jupyter Notebook containing the complete EDA.
-   PDF report containing the analysis, findings, recommendations, and
    conclusion.
-   Original dataset used for analysis.
-   Cleaned dataset.

## 📌 Conclusion

This project demonstrates how Exploratory Data Analysis can be used to
understand customer churn. By examining customer demographics, services,
contracts, tenure, charges, and payment methods, organizations can
identify groups associated with higher churn and develop targeted
customer-retention strategies.

------------------------------------------------------------------------

**Customer Churn EDA \| Aiesha Shaik**
