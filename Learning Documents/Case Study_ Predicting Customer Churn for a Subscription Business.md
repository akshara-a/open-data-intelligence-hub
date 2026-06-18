# Phase 1: ML Engineering Fundamentals

## Case Study: Predicting Customer Churn for a Subscription Business

---

## 1. Phase Overview

### Phase Name

**ML Engineering Fundamentals**

### Case Study

**Predicting Customer Churn for a Subscription Business**

### Main Goal

In this phase, students will learn how to work with real-world business data before building a machine learning model.

Students will understand how to:

* Load a dataset
* Understand the business problem
* Clean messy data
* Perform Exploratory Data Analysis, also called EDA
* Create useful visualizations
* Identify patterns related to customer churn
* Write business insights
* Suggest feature engineering ideas for future ML modeling

This phase focuses on **data understanding, data cleaning, EDA, and business insight generation**.

---

## 2. What is Customer Churn?

### Simple Explanation

Customer churn means a customer stops using a product or service.

For example, imagine a customer is paying monthly for:

* A streaming platform
* An online learning app
* A gym membership
* A SaaS product
* A mobile app subscription
* A food delivery membership

If the customer cancels the subscription or stops using the service, that customer is called a **churned customer**.

---

## 3. Why Customer Churn Matters

Customer churn is important because losing customers directly affects business revenue.

For a subscription business, customers usually pay every month or every year. If many customers leave, the company loses recurring income.

### Example

Assume a company has 10,000 customers.

If 1,000 customers leave in a month, the company loses:

* Monthly revenue
* Future revenue
* Customer trust
* Growth opportunity

It is usually cheaper to retain existing customers than to find new customers.

---

## 4. Business Problem

A subscription-based company is losing customers. The company wants to understand why customers are leaving and which customers are more likely to leave.

The main business question is:

> Why are customers churning, and what can the business do to reduce churn?

---

## 5. Learning Objectives

By the end of this phase, students should be able to:

1. Understand what customer churn means.
2. Understand why churn analysis is useful for businesses.
3. Load and inspect a dataset using Python.
4. Identify numerical and categorical columns.
5. Detect missing values.
6. Detect duplicate records.
7. Fix incorrect data types.
8. Clean inconsistent categorical values.
9. Perform univariate analysis.
10. Perform bivariate analysis.
11. Perform multivariate analysis.
12. Create meaningful visualizations.
13. Interpret EDA charts.
14. Generate business insights.
15. Suggest feature engineering ideas.
16. Prepare a beginner-friendly EDA report.

---

## 6. Suggested Dataset Columns

The dataset may contain customer-level information.

| Column Name      | Meaning                                           | Example                         |
| ---------------- | ------------------------------------------------- | ------------------------------- |
| CustomerID       | Unique ID of each customer                        | CUST001                         |
| Gender           | Gender of the customer                            | Male, Female                    |
| Age              | Age of the customer                               | 25, 42                          |
| Tenure           | Number of months customer stayed with the company | 5, 24, 60                       |
| SubscriptionPlan | Type of plan used by the customer                 | Basic, Standard, Premium        |
| ContractType     | Subscription contract type                        | Monthly, Quarterly, Yearly      |
| MonthlyCharges   | Amount paid every month                           | 499, 999                        |
| TotalCharges     | Total amount paid by the customer                 | 5000, 20000                     |
| PaymentMethod    | Customer payment method                           | Credit Card, UPI, Bank Transfer |
| UsageFrequency   | How often the customer uses the service           | Low, Medium, High               |
| SupportTickets   | Number of support tickets raised                  | 0, 2, 5                         |
| LastLoginDaysAgo | Number of days since last login                   | 2, 15, 40                       |
| Churn            | Whether the customer left or stayed               | Yes, No                         |

The most important column is:

```text
Churn
```

Usually:

```text
Churn = Yes means the customer has left.
Churn = No means the customer is still active.
```

---

# Part A: Teaching EDA Methods

---

## 7. What is EDA?

EDA stands for **Exploratory Data Analysis**.

It means exploring and understanding the dataset before building a machine learning model.

EDA helps us answer questions like:

* What data do we have?
* Is the data clean or messy?
* Are there missing values?
* Are there duplicate rows?
* Are there wrong data types?
* Which customers are leaving?
* What patterns are common among churned customers?
* Which columns may be useful for machine learning?

---

## 8. Simple Analogy for EDA

Before a doctor gives medicine, they first examine the patient.

They check:

* Symptoms
* Health history
* Test results
* Possible causes

Similarly, before building a machine learning model, we first examine the dataset.

That examination process is called **EDA**.

---

## 9. Why EDA is Important in Machine Learning

Machine learning models learn from data.

If the data is messy, incomplete, or incorrect, the model may give poor results.

EDA helps us find problems such as:

* Missing values
* Duplicate records
* Incorrect data types
* Outliers
* Invalid values
* Inconsistent category names
* Imbalanced target column
* Hidden customer behavior patterns

Without EDA, students may build a model without understanding the data. This can lead to wrong conclusions.

---

## 10. Complete EDA Flow

Students can follow this EDA flow:

1. Understand the business problem.
2. Load the dataset.
3. Check rows and columns.
4. Understand column names.
5. Check data types.
6. Identify numerical and categorical columns.
7. Check missing values.
8. Check duplicate records.
9. Clean inconsistent values.
10. Analyze the target column.
11. Perform univariate analysis.
12. Perform bivariate analysis.
13. Perform multivariate analysis.
14. Check correlation.
15. Detect outliers.
16. Generate business insights.
17. Suggest feature engineering ideas.
18. Prepare final EDA report.

---

## 11. Step 1: Understand the Business Problem

Before writing code, students should understand the business goal.

For this case study, the problem is:

> A subscription business wants to know why customers are leaving and how to reduce churn.

### Questions Students Should Ask

* What does churn mean?
* Who are the customers?
* What service is the company providing?
* Which column tells us whether the customer churned?
* What business action can be taken after analysis?

### Example

If customers with low usage are leaving, the company can send engagement emails.

If customers with many support tickets are leaving, the company can improve customer support.

If customers with high monthly charges are leaving, the company can offer discounts or flexible plans.

---

## 12. Step 2: Load the Dataset

### Code

```python
import pandas as pd

df = pd.read_csv("customer_churn.csv")
```

### View First Few Rows

```python
df.head()
```

### Explanation

`df.head()` shows the first five rows of the dataset.

It helps students quickly check:

* Whether the file loaded correctly
* What columns are available
* What kind of values are present
* Whether there are obvious issues

---

## 13. Step 3: Check Dataset Shape

### Code

```python
df.shape
```

### Example Output

```text
(5000, 13)
```

This means:

* 5000 rows
* 13 columns

### Explanation

In this dataset:

```text
One row = one customer
One column = one detail about the customer
```

---

## 14. Step 4: Check Column Names

### Code

```python
df.columns
```

### Why This is Important

Column names tell us what information is available.

Sometimes column names may have issues like:

* Extra spaces
* Special characters
* Different naming styles
* Spelling mistakes

### Example Messy Column Names

```text
Customer ID
Monthly Charges
Total-Charges
payment method
```

### Better Column Names

```text
CustomerID
MonthlyCharges
TotalCharges
PaymentMethod
```

### Optional Cleaning

```python
df.columns = df.columns.str.strip()
```

This removes extra spaces from column names.

---

## 15. Step 5: Check Data Types

### Code

```python
df.info()
```

### Explanation

`df.info()` shows:

* Column names
* Number of non-null values
* Data type of each column

### Common Data Types

| Data Type | Meaning              |
| --------- | -------------------- |
| int64     | Whole numbers        |
| float64   | Decimal numbers      |
| object    | Text or mixed values |
| bool      | True or False        |
| datetime  | Date values          |

### Example Issue

Sometimes `TotalCharges` may be stored as text instead of a number.

This may happen because the column contains blank spaces or invalid values.

### Fix Example

```python
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
```

This converts `TotalCharges` into a numeric column.

Invalid values become missing values.

---

## 16. Step 6: Identify Numerical and Categorical Columns

### Numerical Columns

Numerical columns contain numbers.

Examples:

* Age
* Tenure
* MonthlyCharges
* TotalCharges
* SupportTickets
* LastLoginDaysAgo

### Categorical Columns

Categorical columns contain groups or labels.

Examples:

* Gender
* SubscriptionPlan
* ContractType
* PaymentMethod
* Churn

### Code

```python
numerical_cols = df.select_dtypes(include=["int64", "float64"]).columns
categorical_cols = df.select_dtypes(include=["object"]).columns

print("Numerical columns:", numerical_cols)
print("Categorical columns:", categorical_cols)
```

### Teaching Point

Numerical and categorical columns are analyzed differently.

| Column Type | Common Analysis                   |
| ----------- | --------------------------------- |
| Numerical   | Mean, median, histogram, box plot |
| Categorical | Count, percentage, bar chart      |

---

## 17. Step 7: Summary Statistics

### Code

```python
df.describe()
```

### Explanation

`df.describe()` gives summary statistics for numerical columns.

It shows:

* Count
* Mean
* Standard deviation
* Minimum value
* 25th percentile
* Median
* 75th percentile
* Maximum value

### Example Interpretation

If `Tenure` has:

```text
min = 0
max = 72
mean = 30
```

This means:

* Some customers are new.
* Some customers have stayed for 72 months.
* Average customer tenure is 30 months.

### Weak Interpretation

```text
Mean tenure is 30.
```

### Better Interpretation

```text
The average customer has stayed for 30 months, which suggests many customers have a medium-term relationship with the business.
```

---

## 18. Step 8: Check Missing Values

### Code

```python
df.isnull().sum()
```

### Explanation

Missing values mean some information is not available.

### Example

| Column        | Missing Values |
| ------------- | -------------: |
| Age           |             20 |
| TotalCharges  |             15 |
| PaymentMethod |              8 |

### Why Missing Values Matter

Missing values can affect EDA and machine learning.

For example:

* If `TotalCharges` is missing, we cannot correctly analyze customer spending.
* If `PaymentMethod` is missing, we cannot properly compare churn by payment type.

### Missing Percentage

```python
missing_percentage = df.isnull().mean() * 100
missing_percentage
```

### Handling Numerical Missing Values

Use median when the column has outliers.

```python
df["TotalCharges"] = df["TotalCharges"].fillna(df["TotalCharges"].median())
```

Use mean when the values are normally distributed.

```python
df["Age"] = df["Age"].fillna(df["Age"].mean())
```

### Handling Categorical Missing Values

Use mode or `"Unknown"`.

```python
df["PaymentMethod"] = df["PaymentMethod"].fillna("Unknown")
```

### Teaching Point

Students should not blindly remove missing values.

They should ask:

* How many values are missing?
* Which column has missing values?
* Is the column important?
* Can the missing value itself have meaning?

---

## 19. Step 9: Check Duplicate Records

### Code

```python
df.duplicated().sum()
```

### Explanation

Duplicate records mean the same row is repeated.

Duplicates can create wrong analysis.

For example, if the same churned customer appears twice, churn count becomes incorrect.

### Remove Duplicates

```python
df = df.drop_duplicates()
```

### Teaching Point

Always check duplicates before EDA.

---

## 20. Step 10: Clean Categorical Values

### Code

```python
df["ContractType"].unique()
```

### Example Output

```text
['Monthly', 'monthly', 'MONTHLY', 'Yearly', 'yearly']
```

### Problem

These values mean the same thing but are written differently.

Python treats them as different categories.

This creates wrong charts and wrong analysis.

### Fix

```python
df["ContractType"] = df["ContractType"].str.strip().str.title()
```

After cleaning:

```text
Monthly
Yearly
```

### Teaching Point

Real-world business data is often messy. Students should clean inconsistent values before doing analysis.

---

## 21. Step 11: Analyze the Target Column

The target column is:

```text
Churn
```

### Code

```python
df["Churn"].value_counts()
```

### Percentage

```python
df["Churn"].value_counts(normalize=True) * 100
```

### Example Output

| Churn | Percentage |
| ----- | ---------: |
| No    |        73% |
| Yes   |        27% |

### Interpretation

This means 27% of customers have churned.

### Why This is Important

If churned customers are very few, the dataset is imbalanced.

Example:

```text
No = 95%
Yes = 5%
```

This means only 5% of customers churned.

This can affect future machine learning modeling.

### Chart

```python
import seaborn as sns
import matplotlib.pyplot as plt

sns.countplot(data=df, x="Churn")
plt.title("Churn Distribution")
plt.show()
```

---

# Part B: EDA Methods

---

## 22. Univariate Analysis

Univariate analysis means analyzing one column at a time.

### Purpose

It helps us understand the basic behavior of each column.

---

## 23. Univariate Analysis for Numerical Columns

Example column:

```text
MonthlyCharges
```

### Questions to Ask

* What is the average monthly charge?
* What is the minimum monthly charge?
* What is the maximum monthly charge?
* Are most customers paying low, medium, or high charges?
* Are there unusual values?

### Code

```python
df["MonthlyCharges"].describe()
```

### Histogram

```python
sns.histplot(data=df, x="MonthlyCharges", kde=True)
plt.title("Distribution of Monthly Charges")
plt.show()
```

### What is a Histogram?

A histogram shows how numerical values are spread.

It helps students understand whether most customers are paying:

* Low amount
* Medium amount
* High amount

### Box Plot

```python
sns.boxplot(data=df, x="MonthlyCharges")
plt.title("Box Plot of Monthly Charges")
plt.show()
```

### What is a Box Plot?

A box plot helps identify outliers.

Outliers are values that are unusually high or unusually low.

---

## 24. Univariate Analysis for Categorical Columns

Example column:

```text
ContractType
```

### Code

```python
df["ContractType"].value_counts()
```

### Percentage

```python
df["ContractType"].value_counts(normalize=True) * 100
```

### Bar Chart

```python
sns.countplot(data=df, x="ContractType")
plt.title("Customer Count by Contract Type")
plt.show()
```

### Example Interpretation

```text
Most customers are on monthly contracts. This means the business may have many short-term customers who can cancel easily.
```

---

## 25. Bivariate Analysis

Bivariate analysis means analyzing two columns together.

In churn analysis, we usually compare one feature with the churn column.

### Purpose

This helps us identify which factors may be related to churn.

---

## 26. Categorical Feature vs Churn

Example:

```text
ContractType vs Churn
```

### Question

Are monthly contract customers more likely to churn than yearly contract customers?

### Count Table

```python
pd.crosstab(df["ContractType"], df["Churn"])
```

### Percentage Table

```python
pd.crosstab(df["ContractType"], df["Churn"], normalize="index") * 100
```

### Visualization

```python
sns.countplot(data=df, x="ContractType", hue="Churn")
plt.title("Churn by Contract Type")
plt.show()
```

### Churn Rate

```python
contract_churn_rate = df.groupby("ContractType")["Churn"].apply(
    lambda x: (x == "Yes").mean() * 100
)

contract_churn_rate.sort_values(ascending=False)
```

### Example Insight

```text
Monthly contract customers have a higher churn rate than yearly contract customers. This may be because monthly customers have less commitment and can cancel easily.
```

---

## 27. Numerical Feature vs Churn

Example:

```text
Tenure vs Churn
```

### Question

Do new customers churn more than long-term customers?

### Code

```python
df.groupby("Churn")["Tenure"].mean()
```

### Box Plot

```python
sns.boxplot(data=df, x="Churn", y="Tenure")
plt.title("Tenure by Churn Status")
plt.show()
```

### Example Insight

```text
Churned customers have lower average tenure than non-churned customers. This suggests that new customers may need better onboarding and early engagement support.
```

---

## 28. Multivariate Analysis

Multivariate analysis means analyzing more than two columns together.

### Purpose

Sometimes one column alone does not explain churn clearly.

For example:

* Monthly charges alone may not explain churn.
* Contract type alone may not explain churn.
* But contract type and monthly charges together may show a stronger churn pattern.

---

## 29. Example: Contract Type, Monthly Charges, and Churn

### Question

Are monthly contract customers with high monthly charges more likely to churn?

### Code

```python
df.groupby(["ContractType", "Churn"])["MonthlyCharges"].mean()
```

### Visualization

```python
sns.barplot(data=df, x="ContractType", y="MonthlyCharges", hue="Churn")
plt.title("Average Monthly Charges by Contract Type and Churn")
plt.show()
```

### Example Insight

```text
Monthly contract customers who churn have higher average monthly charges. This may mean that short-term customers are more price-sensitive.
```

---

## 30. Example: Support Tickets, Usage Frequency, and Churn

### Question

Are customers with low usage and more support tickets more likely to churn?

### Code

```python
df.groupby("Churn")[["UsageFrequency", "SupportTickets"]].mean()
```

### Example Insight

```text
Churned customers have lower usage frequency and higher support ticket counts. This suggests that customers who face issues and do not actively use the service are at higher risk of leaving.
```

---

## 31. Correlation Analysis

Correlation shows how numerical columns are related to each other.

### Simple Explanation

Correlation tells whether two numerical values move together.

Example:

If tenure increases and total charges also increase, they may have positive correlation.

If tenure increases and churn decreases, tenure may have negative relationship with churn.

### Convert Churn to Number

```python
df["ChurnFlag"] = df["Churn"].map({"Yes": 1, "No": 0})
```

### Correlation Table

```python
df.corr(numeric_only=True)
```

### Heatmap

```python
plt.figure(figsize=(10, 6))
sns.heatmap(df.corr(numeric_only=True), annot=True)
plt.title("Correlation Heatmap")
plt.show()
```

### Important Note

Correlation does not always mean causation.

For example, if monthly charges and churn are correlated, we cannot immediately say high charges are the only reason customers leave.

We need both data analysis and business understanding.

---

## 32. Outlier Analysis

Outliers are values that are very different from normal values.

### Examples

```text
Age = 150
MonthlyCharges = 10000
Tenure = -5
SupportTickets = 999
```

These values may be:

* Data entry mistakes
* Rare but valid cases
* System errors

### Detect Outliers Using Summary Statistics

```python
df["MonthlyCharges"].describe()
```

### Detect Outliers Using Box Plot

```python
sns.boxplot(data=df, x="MonthlyCharges")
plt.title("Outlier Check for Monthly Charges")
plt.show()
```

### Questions Students Should Ask

* Is this value realistic?
* Is it a mistake?
* Should we remove it?
* Should we cap it?
* Should we keep it because it represents a real customer?

### Teaching Point

Do not remove every outlier blindly.

Some outliers may be important business cases.

---

# Part C: Feature Engineering

---

## 33. What is Feature Engineering?

Feature engineering means creating new useful columns from existing columns.

These new columns can help machine learning models understand patterns better.

### Simple Example

Instead of only using `Tenure`, we can create a new column called `TenureGroup`.

```text
0–12 months = New Customer
13–36 months = Medium-Term Customer
37+ months = Long-Term Customer
```

This makes customer behavior easier to understand.

---

## 34. Feature Engineering Ideas for Churn

| New Feature          | How to Create                              | Why It Helps                             |
| -------------------- | ------------------------------------------ | ---------------------------------------- |
| TenureGroup          | Group tenure into New, Medium, Long-term   | New customers may churn more             |
| HighMonthlyCharge    | Mark customers above median monthly charge | Expensive plans may increase churn       |
| LowUsageFlag         | Mark customers with below-average usage    | Low usage may indicate low interest      |
| FrequentSupportUser  | Mark customers with many support tickets   | More issues may increase dissatisfaction |
| InactiveCustomerFlag | Based on last login days                   | Inactive customers may churn soon        |
| TotalSpendCategory   | Group total charges                        | Spending pattern may relate to loyalty   |
| AutoPaymentFlag      | Based on payment method                    | Auto-payment customers may stay longer   |
| PremiumPlanFlag      | Based on subscription plan                 | Premium users may behave differently     |

---

## 35. Example Feature Engineering Code

### Tenure Group

```python
df["TenureGroup"] = pd.cut(
    df["Tenure"],
    bins=[0, 12, 36, 72],
    labels=["New", "Medium", "Long-term"]
)
```

### High Monthly Charge Flag

```python
df["HighMonthlyCharge"] = df["MonthlyCharges"] > df["MonthlyCharges"].median()
```

### Low Usage Flag

```python
df["LowUsageFlag"] = df["UsageFrequency"] < df["UsageFrequency"].median()
```

### Frequent Support User Flag

```python
df["FrequentSupportUser"] = df["SupportTickets"] > df["SupportTickets"].median()
```

---

# Part D: Business Insight Writing

---

## 36. Why Business Insights Matter

EDA should not end with charts.

Students should explain what the charts mean for the business.

A good insight connects data to action.

---

## 37. Weak vs Strong Insight

### Weak Observation

```text
Monthly customers have high churn.
```

### Strong Business Insight

```text
Customers on monthly contracts have a higher churn rate than customers on yearly contracts. This may be because monthly customers have less commitment and can cancel easily. The business can reduce churn by offering discounts or benefits for long-term subscriptions.
```

---

## 38. Insight Writing Format

Students should write each insight using this format:

```text
Observation:
Possible Reason:
Business Impact:
Recommendation:
```

### Example

```text
Observation:
Customers with low usage frequency have higher churn.

Possible Reason:
They may not be getting enough value from the service.

Business Impact:
The company may lose customers who are not actively engaged.

Recommendation:
Send onboarding emails, product tips, reminders, and personalized offers to low-usage customers.
```

---

# Part E: AI-Augmented EDA Activities

---

## 39. How Students Can Use AI

Students can use AI as a helper during EDA.

AI should support thinking, not replace thinking.

Students can use AI to:

* Find possible data quality issues
* Suggest visualizations
* Explain charts
* Generate feature engineering ideas
* Convert observations into business insights
* Debug errors in Python code

---

## 40. AI Prompt Examples

### Prompt 1: Data Quality Check

```text
I have a customer churn dataset with columns like tenure, monthly charges, contract type, payment method, support tickets, usage frequency, and churn. What data quality issues should I check before doing EDA?
```

### Prompt 2: Visualization Ideas

```text
Suggest beginner-friendly EDA visualizations for a customer churn dataset. The columns are tenure, monthly charges, contract type, payment method, support tickets, usage frequency, and churn.
```

### Prompt 3: Feature Engineering Ideas

```text
Suggest useful feature engineering ideas for a subscription business churn prediction problem using tenure, usage frequency, support tickets, payment method, and monthly charges.
```

### Prompt 4: Explain an Insight

```text
I found that customers with month-to-month contracts have higher churn. Explain this as a business insight in simple words.
```

### Prompt 5: Debugging Help

```text
My churn dataset has missing values in TotalCharges and inconsistent values in PaymentMethod. How should I handle these issues before EDA?
```

---

# Part F: Week-Wise Teaching Plan

---

## 41. Week 1: Business Problem and Data Understanding

### Topics to Teach

* What is churn?
* Why churn matters
* Dataset structure
* Rows and columns
* Target variable
* Numerical columns
* Categorical columns
* Basic pandas commands

### Hands-On Activities

Students should:

* Load the dataset
* Check shape
* Check columns
* Check data types
* Identify the target column
* Write a short dataset summary

### Expected Output

```text
Dataset has X rows and Y columns.
The target column is Churn.
Numerical columns are...
Categorical columns are...
```

---

## 42. Week 2: Data Cleaning

### Topics to Teach

* Missing values
* Duplicate records
* Incorrect data types
* Inconsistent categories
* Outliers
* Cleaning decisions

### Hands-On Activities

Students should:

* Find missing values
* Handle missing values
* Remove duplicates
* Fix data types
* Standardize category names
* Check outliers

### Expected Output

```text
Before cleaning:
- Total missing values:
- Duplicate rows:
- Incorrect data types:

After cleaning:
- Missing values handled
- Duplicates removed
- Data types corrected
```

---

## 43. Week 3: EDA and Visualization

### Topics to Teach

* Univariate analysis
* Bivariate analysis
* Multivariate analysis
* Correlation analysis
* Visualization selection
* Chart interpretation

### Hands-On Activities

Students should create:

* Churn distribution chart
* Contract type vs churn chart
* Tenure vs churn chart
* Monthly charges vs churn chart
* Support tickets vs churn chart
* Usage frequency vs churn chart
* Correlation heatmap

### Expected Output

Students should write observations for each chart.

Example:

```text
Customers with monthly contracts have higher churn than yearly contract customers.
```

---

## 44. Week 4: Business Insights and Mini Project Submission

### Topics to Teach

* Converting observations into insights
* Writing recommendations
* Feature engineering ideas
* Report writing
* Presentation of findings

### Hands-On Activities

Students should:

* Write final insights
* Suggest business actions
* Suggest feature engineering ideas
* Prepare final EDA report
* Submit notebook and cleaned dataset

---

# Part G: Mini Project

---

## 45. Mini Project Title

**Customer Churn Data Cleaning and EDA Report**

---

## 46. Mini Project Objective

The objective of this mini project is to help students understand how to work with real-world business data.

Students will clean a customer churn dataset, perform exploratory data analysis, identify patterns related to churn, and write business insights.

---

## 47. Problem Statement

A subscription-based business is losing customers.

The company wants to understand why customers are leaving and what actions can be taken to reduce churn.

Students need to analyze customer data and prepare a report that answers:

> What are the major factors related to customer churn?

---

## 48. Mini Project Tasks

---

## Task 1: Load the Dataset

### Student Instructions

Students should:

* Import required libraries.
* Load the CSV file.
* Display the first 5 rows.
* Check the number of rows and columns.

### Code

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("customer_churn.csv")

df.head()
df.shape
```

### Expected Explanation

```text
The dataset contains customer-level information for a subscription business. Each row represents one customer. The dataset includes customer details, subscription details, payment details, usage behavior, support information, and churn status.
```

---

## Task 2: Understand the Dataset

### Code

```python
df.info()
df.describe()
df.columns
```

### Students Should Identify

* Total rows
* Total columns
* Numerical columns
* Categorical columns
* Target column

### Expected Table

| Column Name    | Data Type | Meaning                          | Column Type |
| -------------- | --------- | -------------------------------- | ----------- |
| CustomerID     | Object    | Unique customer ID               | Identifier  |
| Tenure         | Integer   | Number of months customer stayed | Numerical   |
| ContractType   | Object    | Type of subscription contract    | Categorical |
| MonthlyCharges | Float     | Monthly payment amount           | Numerical   |
| Churn          | Object    | Whether customer left or stayed  | Target      |

---

## Task 3: Data Quality Check

### Students Should Check

* Missing values
* Duplicates
* Wrong data types
* Inconsistent values
* Outliers

### Code

```python
df.isnull().sum()
df.duplicated().sum()
df.nunique()
```

### Expected Explanation

```text
Data quality checking is important because incorrect or incomplete data can lead to wrong analysis and poor machine learning results.
```

---

## Task 4: Handle Missing Values

### Code

```python
missing_values = df.isnull().sum()
missing_values[missing_values > 0]
```

### Handling Numerical Columns

```python
df["TotalCharges"] = df["TotalCharges"].fillna(df["TotalCharges"].median())
```

### Handling Categorical Columns

```python
df["PaymentMethod"] = df["PaymentMethod"].fillna("Unknown")
```

### Expected Explanation

```text
The missing values in TotalCharges were filled using the median because numerical columns may contain outliers, and median is less affected by extreme values.
```

---

## Task 5: Remove Duplicate Records

### Code

```python
duplicate_count = df.duplicated().sum()
df = df.drop_duplicates()
```

### Expected Explanation

```text
Duplicate records were removed because they can affect customer counts and churn percentage calculations.
```

---

## Task 6: Fix Data Types

### Example

```python
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
```

### Expected Explanation

```text
TotalCharges was converted into a numeric column because it represents an amount and must be used for calculations.
```

---

## Task 7: Clean Categorical Values

### Code

```python
df["ContractType"].unique()
df["PaymentMethod"].unique()
```

### Cleaning Code

```python
df["ContractType"] = df["ContractType"].str.strip().str.title()
df["PaymentMethod"] = df["PaymentMethod"].str.strip().str.title()
```

### Expected Explanation

```text
Categorical values were standardized to avoid treating the same category as different values because of spelling or case differences.
```

---

## Task 8: Churn Distribution

### Code

```python
df["Churn"].value_counts()
df["Churn"].value_counts(normalize=True) * 100
```

### Chart

```python
sns.countplot(data=df, x="Churn")
plt.title("Churn Distribution")
plt.show()
```

### Questions to Answer

* What percentage of customers churned?
* Is the dataset balanced or imbalanced?
* Are more customers staying or leaving?

### Example Insight

```text
The churn distribution shows that most customers have not churned, but a significant portion of customers have left the business. This indicates that churn is a meaningful business problem.
```

---

## Task 9: Tenure Analysis

### Code

```python
df["Tenure"].describe()
```

### Chart

```python
sns.histplot(data=df, x="Tenure", kde=True)
plt.title("Distribution of Customer Tenure")
plt.show()
```

### Compare Tenure with Churn

```python
sns.boxplot(data=df, x="Churn", y="Tenure")
plt.title("Tenure by Churn Status")
plt.show()
```

### Questions to Answer

* Are churned customers new or long-term?
* Do customers with low tenure churn more?
* What does tenure tell us about loyalty?

### Example Insight

```text
Customers with shorter tenure appear to churn more. This suggests that the early customer experience may strongly influence retention.
```

---

## Task 10: Contract Type Analysis

### Code

```python
df["ContractType"].value_counts()
```

### Chart

```python
sns.countplot(data=df, x="ContractType", hue="Churn")
plt.title("Churn by Contract Type")
plt.show()
```

### Churn Rate

```python
contract_churn = df.groupby("ContractType")["Churn"].apply(
    lambda x: (x == "Yes").mean() * 100
)

contract_churn
```

### Questions to Answer

* Which contract type has the highest churn?
* Are monthly customers more likely to leave?
* Are yearly customers more loyal?

### Example Insight

```text
Customers with monthly contracts have a higher churn rate than yearly contract customers. This may be because monthly customers have less commitment and can cancel easily.
```

---

## Task 11: Monthly Charges Analysis

### Code

```python
df["MonthlyCharges"].describe()
```

### Chart

```python
sns.histplot(data=df, x="MonthlyCharges", kde=True)
plt.title("Distribution of Monthly Charges")
plt.show()
```

### Compare with Churn

```python
sns.boxplot(data=df, x="Churn", y="MonthlyCharges")
plt.title("Monthly Charges by Churn Status")
plt.show()
```

### Questions to Answer

* Do churned customers pay more?
* Are high-paying customers leaving?
* Is price possibly affecting churn?

### Example Insight

```text
Churned customers seem to have higher monthly charges. This may indicate that price-sensitive customers are leaving when they feel the service cost is high.
```

---

## Task 12: Payment Method Analysis

### Code

```python
df["PaymentMethod"].value_counts()
```

### Chart

```python
sns.countplot(data=df, x="PaymentMethod", hue="Churn")
plt.title("Churn by Payment Method")
plt.xticks(rotation=45)
plt.show()
```

### Questions to Answer

* Which payment method has higher churn?
* Are automatic payment users less likely to churn?
* Does payment convenience affect retention?

### Example Insight

```text
Customers using manual payment methods may have higher churn compared to customers using automatic payments. This may be because manual payment creates friction or missed payments.
```

---

## Task 13: Support Ticket Analysis

### Code

```python
df["SupportTickets"].describe()
```

### Chart

```python
sns.boxplot(data=df, x="Churn", y="SupportTickets")
plt.title("Support Tickets by Churn Status")
plt.show()
```

### Questions to Answer

* Do churned customers raise more support tickets?
* Does customer dissatisfaction appear related to churn?
* Should support experience be improved?

### Example Insight

```text
Customers who raised more support tickets have higher churn. This may indicate unresolved issues or poor customer experience.
```

---

## Task 14: Usage Frequency Analysis

### Code

```python
df["UsageFrequency"].describe()
```

### Chart

```python
sns.boxplot(data=df, x="Churn", y="UsageFrequency")
plt.title("Usage Frequency by Churn Status")
plt.show()
```

### Questions to Answer

* Are low-usage customers more likely to churn?
* Are active users more likely to stay?
* Can engagement campaigns reduce churn?

### Example Insight

```text
Customers with lower usage frequency are more likely to churn. This suggests that product engagement is an important factor in customer retention.
```

---

## Task 15: Correlation Heatmap

### Code

```python
df["ChurnFlag"] = df["Churn"].map({"Yes": 1, "No": 0})

plt.figure(figsize=(10, 6))
sns.heatmap(df.corr(numeric_only=True), annot=True)
plt.title("Correlation Heatmap")
plt.show()
```

### Questions to Answer

* Which numerical features are related to churn?
* Is tenure related to churn?
* Are monthly charges related to churn?
* Are support tickets related to churn?
* Is usage frequency related to churn?

### Example Insight

```text
The correlation heatmap helps identify numerical features that may be useful for machine learning. Features such as tenure, monthly charges, support tickets, and usage frequency may have useful relationships with churn.
```

---

# Part H: Final Report Structure

---

## 49. Final EDA Report Format

Students should submit a report with the following sections.

---

## 1. Introduction

Include:

* Business problem
* Objective of the analysis
* Why churn analysis is important

---

## 2. Dataset Overview

Include:

* Number of rows and columns
* Column descriptions
* Numerical columns
* Categorical columns
* Target column

---

## 3. Data Cleaning

Include:

* Missing values found
* How missing values were handled
* Duplicate rows found
* Data type corrections
* Category cleaning
* Outlier observations

---

## 4. Exploratory Data Analysis

Include:

* Churn distribution
* Tenure analysis
* Contract type analysis
* Monthly charges analysis
* Payment method analysis
* Support ticket analysis
* Usage frequency analysis
* Correlation analysis

---

## 5. Key Business Insights

Students should write at least 5 insights.

Each insight should follow this structure:

```text
Observation:
Possible Reason:
Business Impact:
Recommendation:
```

---

## 6. Feature Engineering Ideas

Include:

* Feature name
* How to create it
* Why it may help churn prediction

---

## 7. Conclusion

Summarize:

* Main churn patterns
* Most important risk factors
* How this EDA helps future ML modeling

---

# Part I: Sample Business Insights

---

## 50. Insight 1: Monthly Contract Customers Churn More

### Observation

Customers with monthly contracts have a higher churn rate.

### Possible Reason

Monthly customers can cancel easily because they are not locked into a long-term plan.

### Business Impact

The company may lose revenue if many monthly customers leave quickly.

### Recommendation

Offer discounts, loyalty rewards, or upgrade benefits for customers who move to quarterly or yearly plans.

---

## 51. Insight 2: Low-Tenure Customers Are at Higher Risk

### Observation

Customers with shorter tenure are more likely to churn.

### Possible Reason

New customers may not fully understand the product value yet.

### Business Impact

Poor onboarding can lead to early customer loss.

### Recommendation

Improve onboarding through welcome emails, tutorials, product demos, and early support.

---

## 52. Insight 3: High Monthly Charges May Increase Churn

### Observation

Customers with higher monthly charges show higher churn.

### Possible Reason

Some customers may feel the service is expensive compared to the value they receive.

### Business Impact

High-paying customers leaving can reduce revenue significantly.

### Recommendation

Provide personalized offers, flexible pricing, or value-based communication for high-paying customers.

---

## 53. Insight 4: More Support Tickets May Indicate Dissatisfaction

### Observation

Customers who raise more support tickets are more likely to churn.

### Possible Reason

They may be facing repeated issues or may not be satisfied with the support experience.

### Business Impact

Poor support experience can damage customer trust.

### Recommendation

Prioritize support for high-risk customers and improve issue resolution time.

---

## 54. Insight 5: Low Usage Customers Are More Likely to Leave

### Observation

Customers with low usage frequency have higher churn.

### Possible Reason

They may not be engaged with the product or may not see enough value.

### Business Impact

Inactive users are likely to cancel the service.

### Recommendation

Send engagement campaigns, product tips, reminders, and personalized recommendations.

---

# Part J: Mini Project Submission Checklist

---

## 55. Submission Items

Students must submit:

1. Cleaned dataset
2. Jupyter Notebook or Python script
3. EDA report
4. Visualizations
5. Business insights
6. Feature engineering ideas

---

## 56. Checklist

| Requirement                                   | Completed |
| --------------------------------------------- | --------- |
| Dataset loaded successfully                   |           |
| Dataset shape checked                         |           |
| Data types checked                            |           |
| Numerical and categorical columns identified  |           |
| Missing values handled                        |           |
| Duplicates removed                            |           |
| Categorical values cleaned                    |           |
| Churn distribution analyzed                   |           |
| Univariate analysis completed                 |           |
| Bivariate analysis completed                  |           |
| Multivariate analysis completed               |           |
| Correlation heatmap created                   |           |
| At least 5 business insights written          |           |
| At least 5 feature engineering ideas proposed |           |
| Final report prepared                         |           |

---

# Part K: Evaluation Rubric

---

## 57. Rubric

| Criteria                  |   Marks |
| ------------------------- | ------: |
| Problem understanding     |      10 |
| Dataset understanding     |      10 |
| Data cleaning quality     |      20 |
| EDA visualizations        |      20 |
| Quality of observations   |      10 |
| Business insights         |      15 |
| Feature engineering ideas |      10 |
| Report clarity            |       5 |
| **Total**                 | **100** |

---

# Part L: Expected Learning Outcome

---

## 58. Final Learning Outcome

After completing this mini project, students should understand that machine learning is not only about building models.

Before modeling, a good ML engineer must:

* Understand the business problem
* Understand the data
* Clean the data
* Explore the data
* Find patterns
* Explain insights clearly
* Prepare useful features

This mini project builds the foundation for the next step: creating a machine learning model to predict whether a customer will churn or not.
