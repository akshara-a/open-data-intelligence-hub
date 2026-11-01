# Customer Churn Exploratory Data Analysis

## Overview

This project performs Exploratory Data Analysis (EDA) on the Telco Customer Churn dataset to understand customer behavior and identify the factors contributing to customer churn. The analysis includes data cleaning, statistical summaries, univariate analysis, bivariate analysis, correlation analysis, outlier detection, and visualizations.

The primary objective is to discover key patterns that influence customer attrition and provide business recommendations to improve customer retention.

---

## Dataset Information

- **Dataset Name:** Telco Customer Churn Dataset
- **Source:** Kaggle
- **Rows:** 7043
- **Columns:** 21
- **Target Variable:** Churn

### Numerical Features

- SeniorCitizen
- tenure
- MonthlyCharges
- TotalCharges

### Categorical Features

- gender
- Partner
- Dependents
- PhoneService
- InternetService
- Contract
- PaymentMethod
- Churn and other service-related attributes

---

## Project Structure

```text
Customer_Churn_EDA_Keerthana_Reddy/
│
├── Customer_Churn_EDA_Keerthana_Reddy.ipynb
├── Customer_Churn_EDA_Report_Keerthana_Reddy.pdf
├── Customer_Churn_Dataset_Keerthana_Reddy.csv
├── Cleaned_Customer_Churn_Dataset_Keerthana_Reddy.csv
└── README.md
```

---

## Data Cleaning

The following preprocessing steps were performed:

- Handled missing values in the `TotalCharges` column.
- Removed duplicate records.
- Corrected data types.
- Removed unnecessary columns such as `customerID`.
- Fixed formatting inconsistencies.
- Performed outlier detection using boxplots and the IQR method.

---

## Exploratory Data Analysis

### Univariate Analysis

- Distribution of individual variables.
- Statistical summaries of numerical features.

### Bivariate Analysis

- Relationship between important variables and customer churn.

### Numerical Analysis

- Mean
- Median
- Minimum
- Maximum
- Standard Deviation

### Categorical Analysis

- Value counts
- Category-wise churn comparisons

### Correlation Analysis

- Relationships among numerical variables.

### Outlier Analysis

- Detection of unusual observations using boxplots and IQR.

---

## Visualizations

The project includes the following visualizations:

1. Churn Count Plot
2. Churn Percentage Pie Chart
3. Histogram of Tenure
4. Boxplot of Monthly Charges
5. Gender Distribution Bar Chart
6. Contract Type vs Churn Countplot
7. Correlation Heatmap
8. Scatter Plot of Monthly Charges vs Total Charges

---

## Key Findings

- Approximately 26–27% of customers have churned.
- Customers with month-to-month contracts exhibit the highest churn rate.
- Customers with shorter tenure are more likely to leave.
- Higher monthly charges are associated with increased churn.
- Fiber optic customers show relatively higher churn.
- Contract type, tenure, and monthly charges are the most influential factors affecting customer churn.

---

## Business Recommendations

- Encourage customers to switch to long-term contracts.
- Introduce loyalty and retention programs.
- Offer customized pricing plans to customers with high monthly charges.
- Improve the quality of fiber optic services.
- Strengthen customer support and engagement.
- Identify high-risk customers and implement proactive retention strategies.

---

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Jupyter Notebook

---

## Conclusion

This project demonstrates how Exploratory Data Analysis can be used to understand customer behavior and identify the factors influencing customer churn. The insights obtained from the analysis can help organizations develop effective retention strategies, improve customer satisfaction, and achieve long-term business growth.

---

## Author

**Gundreddy Keerthana Reddy**
