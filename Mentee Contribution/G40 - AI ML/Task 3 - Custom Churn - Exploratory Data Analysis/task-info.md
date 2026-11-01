# Customer Churn EDA Assignment Guidelines

## Assignment Title

**Customer Churn Exploratory Data Analysis**

---

## Dataset Instruction

Students can use **any customer churn dataset** of their choice.

Suggested dataset types:

| Dataset Type             | Example                                      |
| ------------------------ | -------------------------------------------- |
| Telecom churn dataset    | Customer subscription and service usage data |
| Banking churn dataset    | Customer account and exit data               |
| SaaS churn dataset       | Subscription-based product usage data        |
| E-commerce churn dataset | Customer purchase and retention data         |

Students may download datasets from:

* Kaggle
* UCI Machine Learning Repository
* GitHub public datasets
* Any open-source dataset platform

---

# Assignment Guidelines

## 1. Dataset Selection

Students should choose a dataset that has:

| Requirement          | Description                                                     |
| -------------------- | --------------------------------------------------------------- |
| Customer-level data  | Each row should represent one customer                          |
| Churn column         | Dataset should clearly show whether the customer churned or not |
| Numerical features   | Example: tenure, balance, charges, salary, usage count          |
| Categorical features | Example: gender, contract type, geography, payment method       |
| Minimum rows         | Preferably more than 500 rows                                   |

---

## 2. Dataset Understanding

Students should explain the basic details of the dataset.

| Point             | Description                          |
| ----------------- | ------------------------------------ |
| Dataset name      | Name of the dataset used             |
| Dataset source    | Kaggle, GitHub, UCI, or other source |
| Number of rows    | Total number of records              |
| Number of columns | Total number of features             |
| Target column     | Churn / Exited / Attrition column    |
| Feature types     | Numerical and categorical columns    |

---

## 3. Data Cleaning Guidelines

Students should check and handle the following data quality issues:

| Cleaning Task       | Expected Work                                             |
| ------------------- | --------------------------------------------------------- |
| Missing values      | Identify and handle null or blank values                  |
| Duplicate records   | Check and remove duplicate rows if required               |
| Wrong data types    | Convert columns to correct formats                        |
| Unnecessary columns | Remove ID columns if they are not useful for analysis     |
| Inconsistent values | Fix spelling mistakes, extra spaces, or formatting issues |
| Outliers            | Detect outliers using boxplots or IQR method              |

---

## 4. EDA Guidelines

Students should perform the following types of exploratory data analysis:

| EDA Type             | What to Analyze                                        |
| -------------------- | ------------------------------------------------------ |
| Univariate analysis  | Analyze one column at a time                           |
| Bivariate analysis   | Compare important features with churn                  |
| Numerical analysis   | Mean, median, minimum, maximum, and standard deviation |
| Categorical analysis | Value counts and churn comparison                      |
| Correlation analysis | Relationship between numerical columns                 |
| Outlier analysis     | Check unusual values in numerical columns              |

---

## 5. Required Visualizations

Students should include **at least 8 charts** in their notebook/report.

Suggested visualizations:

| Chart                      | Purpose                                          |
| -------------------------- | ------------------------------------------------ |
| Churn count plot           | Shows churned vs non-churned customers           |
| Churn percentage pie chart | Shows churn ratio                                |
| Histogram                  | Shows distribution of numerical columns          |
| Boxplot                    | Detects outliers                                 |
| Bar chart                  | Compares categorical values                      |
| Countplot with churn       | Compares category-wise churn                     |
| Correlation heatmap        | Shows numerical relationships                    |
| Scatter plot               | Shows relationship between two numerical columns |

---

## 6. Questions Students Should Answer

Students should answer the following questions in their report:

| No. | Question                                          |
| --: | ------------------------------------------------- |
|   1 | What percentage of customers churned?             |
|   2 | Which customer group has the highest churn?       |
|   3 | Which numerical features seem related to churn?   |
|   4 | Which categorical features seem related to churn? |
|   5 | Are there missing values or data quality issues?  |
|   6 | Are there outliers in the dataset?                |
|   7 | What are the top 3 factors affecting churn?       |
|   8 | What recommendations can reduce churn?            |

---

# Submission Format

Students should submit the assignment in the following format.

---

## 1. Jupyter Notebook

File name format:

```text
Customer_Churn_EDA_StudentName.ipynb
```

Notebook should include:

| Section          | Content                                         |
| ---------------- | ----------------------------------------------- |
| Title            | Customer Churn EDA                              |
| Dataset loading  | Code to load the dataset                        |
| Dataset overview | Shape, columns, and data types                  |
| Data cleaning    | Missing values, duplicates, and data type fixes |
| EDA              | Univariate and bivariate analysis               |
| Visualizations   | Minimum 8 charts                                |
| Observations     | Explanation after every chart                   |
| Final insights   | Key churn patterns                              |
| Recommendations  | Business suggestions                            |

---

## 2. EDA Report

File name format:

```text
Customer_Churn_EDA_Report_StudentName.pdf
```

Report should include:

```markdown
# Customer Churn EDA Report

## 1. Introduction
Briefly explain customer churn and why it is important.

## 2. Dataset Details
Mention dataset source, rows, columns, and target variable.

## 3. Data Cleaning Summary
Explain missing values, duplicates, data type corrections, and outlier checks.

## 4. Exploratory Data Analysis
Explain important charts and observations.

## 5. Key Findings
List the most important churn patterns.

## 6. Business Recommendations
Suggest actions to reduce churn.

## 7. Conclusion
Summarize the overall analysis.
```

---

## 3. Dataset File

Students should submit the dataset used.

Accepted formats:

```text
.csv
.xlsx
.json
```

File name format:

```text
Customer_Churn_Dataset_StudentName.csv
```

---

## 4. Optional Cleaned Dataset

If students clean and save a new version of the dataset, they can submit it as:

```text
Cleaned_Customer_Churn_Dataset_StudentName.csv
```

---

# Final Submission Folder Structure

```text
Customer_Churn_EDA_StudentName/
│
├── Customer_Churn_EDA_StudentName.ipynb
├── Customer_Churn_EDA_Report_StudentName.pdf
├── Customer_Churn_Dataset_StudentName.csv
└── Cleaned_Customer_Churn_Dataset_StudentName.csv   optional
```

---

# Evaluation Criteria

| Criteria                            |   Marks |
| ----------------------------------- | ------: |
| Dataset selection and understanding |      10 |
| Data cleaning                       |      15 |
| Univariate analysis                 |      15 |
| Bivariate analysis with churn       |      20 |
| Visualizations                      |      15 |
| Statistical summary                 |      10 |
| Business insights                   |      10 |
| Report formatting and clarity       |       5 |
| **Total**                           | **100** |

---

# Important Notes for Students

| Do                                   | Don’t                                      |
| ------------------------------------ | ------------------------------------------ |
| Use any suitable churn dataset       | Don’t use a dataset without a churn column |
| Explain every chart clearly          | Don’t paste graphs without observations    |
| Clean the data before analysis       | Don’t ignore missing values                |
| Compare features with churn          | Don’t only describe columns separately     |
| Write business insights              | Don’t submit only code                     |
| Submit notebook, report, and dataset | Don’t submit incomplete files              |
