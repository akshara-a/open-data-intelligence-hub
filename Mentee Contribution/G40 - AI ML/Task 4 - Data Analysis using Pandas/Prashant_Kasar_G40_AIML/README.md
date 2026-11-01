📘 Task 4 – Data Analysis using Pandas (Telco Customer Churn EDA)
📌 Project Title

Telco Customer Churn Analysis using Exploratory Data Analysis (EDA)

👨‍💻 Author

Prashant Kasar – G40 AIML

📖 Project Overview

This project focuses on performing Exploratory Data Analysis (EDA) on a real-world telecom customer dataset to understand customer churn behavior.

Customer churn refers to customers who stop using a company's services. Identifying churn patterns helps businesses improve retention strategies and reduce revenue loss.

The analysis is performed using Python, Pandas, Matplotlib, and Seaborn.

🎯 Objective
Analyze customer demographics and service usage patterns
Identify key factors influencing customer churn
Perform data cleaning and preprocessing
Visualize important trends and insights
Generate business recommendations to reduce churn

📂 Dataset Information
Dataset Name: Telco Customer Churn Dataset
Records: 7043 customers
Features: 21 columns
Target Variable: Churn

🔑 Key Features
customerID
gender
tenure
InternetService
Contract
MonthlyCharges
TotalCharges


🧹 Data Preprocessing

The following cleaning steps were performed:

Converted TotalCharges to numeric format
Handled missing values using median imputation
Checked and verified data types
Ensured dataset consistency
📊 Exploratory Data Analysis (EDA)

The following analyses were performed:

📌 1. Univariate Analysis
Churn distribution
Tenure distribution
Monthly charges distribution

📌 2. Bivariate Analysis
Gender vs Churn
Contract vs Churn
Internet Service vs Churn

📌 3. Correlation Analysis
Relationship between numerical features
Heatmap visualization for feature correlation

📈 Key Insights
Customers with month-to-month contracts are more likely to churn
Low tenure customers have higher churn probability
Higher monthly charges increase churn risk
Internet service type impacts churn behavior
Gender has minimal impact on churn

💡 Business Recommendations
Encourage long-term contracts (1 or 2 years)
Provide discounts for high monthly charge customers
Focus retention strategies on new customers (0–12 months tenure)
Improve service quality for high-churn segments
Use predictive modeling for early churn detection

📊 Visualizations
The following charts are generated and stored in /charts folder:

Churn distribution plot
Tenure histogram
Monthly charges distribution
Contract vs Churn
Internet service vs Churn
Correlation heatmap

📁 Project Structure

Prashant_Kasar_G40_AIML/
│
├── data/
│   └── Telco-Customer-Churn.csv
│
├── notebooks/
│   └── Task4_Telco_Churn_EDA.ipynb
│
├── charts/
│   ├── churn_distribution.png
│   ├── tenure_distribution.png
│   ├── monthly_charges.png
│   ├── contract_vs_churn.png
│   └── correlation_heatmap.png
│
├── outputs/
│   ├── cleaned_telco_churn.csv
│   └── analysis_report.md
│
└── README.md


⚙️ Technologies Used
Python 3.x
Pandas
NumPy
Matplotlib
Seaborn


🚀 How to Run the Project
# Clone repository
git clone https://github.com/your-username/open-data-intelligence-hub.git

# Navigate to project
cd open-data-intelligence-hub

# Open notebook
jupyter notebook


📌 Outcome
This project successfully identifies the key drivers of customer churn and provides actionable business insights to improve customer retention strategies.

🏁 Conclusion
EDA reveals that contract type, tenure, and monthly charges are the strongest indicators of churn. Businesses can significantly reduce churn by focusing on customer retention strategies targeting high-risk segments.