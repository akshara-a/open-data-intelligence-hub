# Customer Churn Exploratory Data Analysis

## Project Overview
This project performs an Exploratory Data Analysis (EDA) on the 
Telco Customer Churn dataset to identify key patterns and factors 
that contribute to customer churn. The analysis helps businesses 
understand why customers leave and provides actionable recommendations 
to reduce churn.

---

## Dataset Details
| Detail | Information |
|---|---|
| Dataset Name | Telco Customer Churn |
| Source | Kaggle|
| Total Rows | 7043 |
| Total Columns | 21 |
| Target Column | Churn (Yes = churned, No = stayed) |

---

## Tools and Libraries Used
| Tool/Library | Purpose |
|---|---|
| Python | Programming Language |
| Polars | Data Loading and Manipulation |
| Matplotlib | Data Visualization |
| Seaborn | Statistical Visualizations |
| Google Colab | Development Environment |

---



## Questions Answered
| No. | Question | Answer |
|---|---|---|
| 1 | What percentage of customers churned? | 26.6% |
| 2 | Which customer group has highest churn? | Month-to-month contract customers |
| 3 | Which numerical features relate to churn? | Tenure (-0.35), MonthlyCharges (0.19) |
| 4 | Which categorical features relate to churn? | Contract type, Internet service |
| 5 | Are there missing values? | Yes, TotalCharges had 11 — dropped |
| 6 | Are there outliers? | No outliers found using IQR method |
| 7 | Top 3 factors affecting churn? | Contract type, Tenure, Monthly Charges |
| 8 | Recommendations to reduce churn? | See Business Recommendations above |

---

## Conclusion
This EDA revealed that contract type, tenure and monthly charges 
are the top factors affecting churn. Month-to-month contract 
customers and fiber optic users are the most at risk groups. 
By implementing targeted retention strategies the company can 
significantly reduce its churn rate and improve customer satisfaction.

---

## Author
**Lahari Prasanna Desetty**
