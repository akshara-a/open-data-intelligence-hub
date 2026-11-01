# Pandas Assignment: Data Cleaning, EDA, and Business Insights

## Assignment Title

**Exploratory Data Analysis and Data Cleaning using Pandas**

---

## 1. Objective

The objective of this assignment is to help learners understand how to use **Pandas** for practical data analysis.

By the end of this assignment, students should be able to:

- Load datasets using Pandas.
- Inspect dataset structure.
- Identify missing values, duplicates, and invalid records.
- Clean and transform raw data.
- Perform filtering, sorting, grouping, and aggregation.
- Create meaningful visualizations.
- Generate business or analytical insights.
- Export cleaned datasets and summary reports.

---

## 2. Background

Pandas is one of the most widely used Python libraries for data analysis. It provides powerful data structures such as:

| Pandas Object | Meaning |
|---|---|
| `Series` | One-dimensional labeled data |
| `DataFrame` | Two-dimensional tabular data |

Pandas is commonly used for:

- Data cleaning
- Exploratory Data Analysis
- Data transformation
- Grouped summaries
- Time-series analysis
- Data preparation for machine learning

---

## 3. Dataset Requirement

Students may choose any one dataset from the following categories:

| Dataset Category | Example Dataset Ideas |
|---|---|
| Customer analytics | Customer churn, subscription usage, purchases |
| Sales analytics | Retail sales, store transactions, product orders |
| HR analytics | Employee attrition, salaries, attendance |
| Education analytics | Student performance, marks, attendance |
| Finance analytics | Transactions, expenses, stock prices |
| Healthcare analytics | Patient visits, appointment data, insurance claims |
| Public datasets | Kaggle, World Bank, GitHub, FIFA, weather data |

### Dataset Conditions

The dataset should ideally contain:

- At least **1,000 rows**
- At least **8 columns**
- A mix of numerical and categorical columns
- At least one column useful for grouping
- Some missing, duplicate, or messy values

Accepted formats:

- `.csv`
- `.xlsx`
- `.json`

---

## 4. Tools Required

Install the required libraries:

```bash
pip install pandas matplotlib seaborn openpyxl
```

Optional:

```bash
pip install jupyter plotly
```

Recommended environment:

- Python 3.10+
- Jupyter Notebook / VS Code / Google Colab
- Pandas
- Matplotlib or Seaborn for charts

---

## 5. Assignment Scenario

You are working as a junior data analyst. Your organization has received a raw dataset from a business team. The dataset may contain missing values, duplicate rows, inconsistent formatting, and unstructured columns.

Your task is to clean the dataset, analyze it, and prepare a small report with insights and recommendations.

---

# Part A: Data Loading and Initial Inspection

## Task A1: Load the Dataset

For CSV:

```python
import pandas as pd

df = pd.read_csv("data/dataset.csv")
df.head()
```

For Excel:

```python
df = pd.read_excel("data/dataset.xlsx")
df.head()
```

For JSON:

```python
df = pd.read_json("data/dataset.json")
df.head()
```

---

## Task A2: Inspect the Dataset

Display:

- First 10 rows
- Last 10 rows
- Number of rows and columns
- Column names
- Data types
- Basic information

Example:

```python
print(df.head(10))
print(df.tail(10))
print(df.shape)
print(df.columns)
print(df.dtypes)
print(df.info())
```

---

## Expected Output

Create a dataset overview table:

| Item | Value |
|---|---|
| Number of rows |  |
| Number of columns |  |
| File format |  |
| Numerical columns |  |
| Categorical columns |  |
| Date columns |  |

---

# Part B: Data Quality Check

## Task B1: Missing Values

Check missing values column-wise.

```python
missing_values = df.isnull().sum()
print(missing_values)
```

Calculate missing value percentage:

```python
missing_percentage = (df.isnull().sum() / len(df)) * 100
print(missing_percentage)
```

---

## Task B2: Duplicate Records

Check duplicate rows.

```python
duplicate_count = df.duplicated().sum()
print("Duplicate rows:", duplicate_count)
```

---

## Task B3: Invalid or Unusual Values

Identify at least **three possible data quality issues**.

Examples:

| Column Type | Possible Issue |
|---|---|
| Age | Negative age or age greater than 100 |
| Salary | Negative salary |
| Quantity | Zero or negative quantity |
| Date | Future date or invalid date format |
| Category | Extra spaces or inconsistent casing |
| Email | Missing `@` symbol |
| Amount | Null or negative amount |

---

## Expected Output

| Column | Issue Found | Number of Records | Suggested Fix |
|---|---|---:|---|
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

---

# Part C: Data Cleaning

## Task C1: Handle Missing Values

Choose suitable missing value treatments.

Examples:

Fill missing categorical values:

```python
df["category"] = df["category"].fillna("Unknown")
```

Fill missing numerical values with median:

```python
df["amount"] = df["amount"].fillna(df["amount"].median())
```

Drop rows if needed:

```python
df = df.dropna(subset=["customer_id"])
```

---

## Task C2: Remove Duplicates

```python
df = df.drop_duplicates()
```

---

## Task C3: Standardize Text Columns

Example:

```python
df["category"] = df["category"].str.strip().str.title()
```

---

## Task C4: Convert Data Types

Convert date column:

```python
df["date"] = pd.to_datetime(df["date"], errors="coerce")
```

Convert numeric column:

```python
df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
```

---

## Task C5: Rename Columns

Standardize column names:

```python
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)
```

---

## Expected Output

| Cleaning Step | Column Used | Method Applied | Reason |
|---|---|---|---|
| Missing value handling |  |  |  |
| Duplicate removal |  |  |  |
| Text standardization |  |  |  |
| Type conversion |  |  |  |
| Column renaming |  |  |  |

---

# Part D: Exploratory Data Analysis

## Task D1: Summary Statistics

Generate summary statistics.

```python
df.describe()
```

For categorical columns:

```python
df.describe(include="object")
```

---

## Task D2: Value Counts

Choose at least **three categorical columns** and show value counts.

```python
df["category"].value_counts()
```

---

## Task D3: Filtering

Write at least **five meaningful filters**.

Examples:

```python
high_value_records = df[df["amount"] > 1000]
```

```python
active_customers = df[df["status"] == "Active"]
```

```python
recent_records = df[df["date"] >= "2024-01-01"]
```

---

## Task D4: Sorting

Sort by an important numerical column.

```python
top_records = df.sort_values(by="amount", ascending=False).head(10)
print(top_records)
```

---

## Task D5: Column Selection

Select important columns.

```python
selected_df = df[["customer_id", "category", "amount"]]
```

---

## Expected Output

| Analysis Question | Pandas Function Used | Key Finding |
|---|---|---|
| Which category appears most often? | `value_counts()` |  |
| Which records have the highest amount? | `sort_values()` |  |
| Which records meet a condition? | filtering |  |

---

# Part E: Grouping and Aggregation

## Task E1: Single-Level Grouping

Group by one categorical column.

```python
category_summary = df.groupby("category").agg(
    record_count=("category", "count"),
    total_amount=("amount", "sum"),
    average_amount=("amount", "mean"),
    minimum_amount=("amount", "min"),
    maximum_amount=("amount", "max")
).reset_index()

print(category_summary)
```

---

## Task E2: Multi-Level Grouping

Group by two columns.

```python
region_category_summary = df.groupby(["region", "category"]).agg(
    record_count=("amount", "count"),
    total_amount=("amount", "sum"),
    average_amount=("amount", "mean")
).reset_index()

print(region_category_summary)
```

---

## Task E3: Top 10 Groups

```python
top_10_groups = category_summary.sort_values(
    by="total_amount",
    ascending=False
).head(10)

print(top_10_groups)
```

---

## Expected Output

| Group | Count | Total | Average | Rank |
|---|---:|---:|---:|---:|
|  |  |  |  |  |

---

# Part F: Feature Engineering

Create at least **three new columns**.

## Example 1: Amount Category

```python
def amount_category(value):
    if value >= 1000:
        return "High"
    elif value >= 500:
        return "Medium"
    else:
        return "Low"

df["amount_category"] = df["amount"].apply(amount_category)
```

---

## Example 2: Date-Based Features

```python
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["day_name"] = df["date"].dt.day_name()
```

---

## Example 3: Profit Margin

```python
df["profit_margin"] = df["profit"] / df["sales"]
```

---

## Example 4: Age Group

```python
df["age_group"] = pd.cut(
    df["age"],
    bins=[0, 18, 30, 45, 60, 100],
    labels=["Teen", "Young Adult", "Adult", "Middle Age", "Senior"]
)
```

---

## Expected Output

| New Feature | Logic Used | Why It Is Useful |
|---|---|---|
|  |  |  |
|  |  |  |
|  |  |  |

---

# Part G: Visualization

Create at least **three charts**.

Use Matplotlib or Seaborn.

## Chart 1: Bar Chart

```python
import matplotlib.pyplot as plt

top_categories = category_summary.sort_values(
    by="total_amount",
    ascending=False
).head(10)

plt.figure(figsize=(10, 5))
plt.bar(top_categories["category"], top_categories["total_amount"])
plt.xticks(rotation=45)
plt.title("Top Categories by Total Amount")
plt.xlabel("Category")
plt.ylabel("Total Amount")
plt.tight_layout()
plt.show()
```

---

## Chart 2: Histogram

```python
plt.figure(figsize=(8, 5))
plt.hist(df["amount"].dropna(), bins=30)
plt.title("Distribution of Amount")
plt.xlabel("Amount")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()
```

---

## Chart 3: Line Chart

```python
monthly_summary = df.groupby("month").agg(
    total_amount=("amount", "sum")
).reset_index()

plt.figure(figsize=(8, 5))
plt.plot(monthly_summary["month"], monthly_summary["total_amount"], marker="o")
plt.title("Monthly Amount Trend")
plt.xlabel("Month")
plt.ylabel("Total Amount")
plt.tight_layout()
plt.show()
```

---

## Optional Seaborn Example

```python
import seaborn as sns

plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x="category", y="amount")
plt.xticks(rotation=45)
plt.title("Amount Distribution by Category")
plt.tight_layout()
plt.show()
```

---

## Expected Output

For each chart, write:

| Chart Title | Columns Used | Chart Type | Insight |
|---|---|---|---|
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

---

# Part H: Correlation Analysis

## Task H1: Select Numerical Columns

```python
numeric_df = df.select_dtypes(include=["number"])
```

## Task H2: Correlation Matrix

```python
correlation_matrix = numeric_df.corr()
print(correlation_matrix)
```

## Task H3: Heatmap

```python
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.show()
```

## Expected Output

Write at least **three observations** from the correlation matrix.

Example:

```text
Observation 1:
Sales and profit have a strong positive correlation.

Observation 2:
Discount and profit have a weak negative correlation.

Observation 3:
Quantity and total amount show moderate correlation.
```

---

# Part I: Export Final Output

## Task I1: Save Cleaned Dataset

```python
df.to_csv("outputs/cleaned_dataset.csv", index=False)
```

## Task I2: Save Excel Output

```python
df.to_excel("outputs/cleaned_dataset.xlsx", index=False)
```

## Task I3: Save Group Summary

```python
category_summary.to_csv("outputs/category_summary.csv", index=False)
```

---

## Expected Output Files

| File Name | Purpose |
|---|---|
| `cleaned_dataset.csv` | Cleaned version of raw dataset |
| `cleaned_dataset.xlsx` | Excel version of cleaned dataset |
| `category_summary.csv` | Grouped summary output |
| `analysis_report.md` | Final written report |
| `charts/` | Folder containing saved chart images |

---

# Part J: Final Insights and Recommendations

Write at least **8 insights** from your analysis.

Each insight should follow this structure:

```text
Insight:
Evidence:
Business meaning:
Recommended action:
```

Example:

```text
Insight:
The highest sales come from the Electronics category.

Evidence:
Electronics contributed 38% of the total sales amount.

Business meaning:
The business depends heavily on Electronics for revenue.

Recommended action:
Maintain adequate stock and create targeted promotions for Electronics.
```

---

# Bonus Tasks

## Bonus 1: Pivot Table

Create a pivot table.

```python
pivot = pd.pivot_table(
    df,
    values="amount",
    index="region",
    columns="category",
    aggfunc="sum",
    fill_value=0
)

print(pivot)
```

---

## Bonus 2: Time-Series Analysis

If your dataset has a date column, analyze monthly or yearly trends.

```python
df["month_year"] = df["date"].dt.to_period("M")

monthly_trend = df.groupby("month_year").agg(
    total_amount=("amount", "sum")
).reset_index()

print(monthly_trend)
```

---

## Bonus 3: Outlier Detection using IQR

```python
Q1 = df["amount"].quantile(0.25)
Q3 = df["amount"].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = df[
    (df["amount"] < lower_bound) |
    (df["amount"] > upper_bound)
]

print(outliers)
```

---

## Bonus 4: Compare Before and After Cleaning

Create a summary table comparing:

| Metric | Before Cleaning | After Cleaning |
|---|---:|---:|
| Number of rows |  |  |
| Missing values |  |  |
| Duplicate rows |  |  |
| Invalid records |  |  |

---

# Submission Format

Students must submit a folder with this structure:

```text
pandas-assignment-submission/
│
├── data/
│   └── dataset.csv or dataset.xlsx
│
├── notebooks/
│   └── pandas_analysis.ipynb
│
├── src/
│   └── analysis.py
│
├── outputs/
│   ├── cleaned_dataset.csv
│   ├── cleaned_dataset.xlsx
│   └── category_summary.csv
│
├── charts/
│   ├── chart_1.png
│   ├── chart_2.png
│   └── chart_3.png
│
└── analysis_report.md
```

---

# Final Report Format

The `analysis_report.md` file should contain:

```markdown
# Pandas Data Analysis Report

## 1. Dataset Overview

## 2. Data Quality Issues

## 3. Cleaning Steps

## 4. Exploratory Data Analysis

## 5. Grouping and Aggregation Results

## 6. Feature Engineering

## 7. Visualizations

## 8. Correlation Analysis

## 9. Key Insights

## 10. Recommendations

## 11. Conclusion
```

---

# Evaluation Rubric

| Criteria | Marks |
|---|---:|
| Dataset loading and inspection | 10 |
| Data quality checks | 10 |
| Data cleaning | 15 |
| Exploratory data analysis | 15 |
| Grouping and aggregation | 15 |
| Feature engineering | 10 |
| Visualizations | 10 |
| Correlation analysis | 10 |
| Final insights and recommendations | 15 |
| Code readability and folder structure | 10 |
| **Total** | **120** |

---

# Mentor Review Checklist

| Checklist Item | Yes/No |
|---|---|
| Dataset is loaded successfully using Pandas |  |
| Student inspected rows, columns, and data types |  |
| Student checked missing values |  |
| Student checked duplicate records |  |
| Student cleaned the dataset properly |  |
| Student performed filtering and sorting |  |
| Student used groupby aggregation |  |
| Student created at least 3 new features |  |
| Student created at least 3 charts |  |
| Student performed correlation analysis |  |
| Student exported cleaned data and summaries |  |
| Student wrote at least 8 insights |  |
| Code is clean and reproducible |  |

---

# Common Mistakes to Avoid

- Loading a dataset but not inspecting it.
- Only using `head()` without checking data quality.
- Ignoring missing values.
- Dropping too many rows without explanation.
- Creating charts without explaining insights.
- Hardcoding file paths that do not work on another system.
- Not using `groupby`.
- Not saving cleaned outputs.
- Writing vague insights without evidence.
- Submitting notebook output without a final report.

---

# Expected Learning Outcomes

After completing this assignment, students should be able to:

- Use Pandas for real-world data analysis.
- Clean messy datasets.
- Handle missing and duplicate values.
- Perform grouping and aggregation.
- Create new analytical features.
- Visualize data.
- Interpret correlation.
- Export cleaned data and reports.
- Communicate insights clearly.

---

# Mini Project Extension

Students can extend this assignment into a mini project by building a simple dashboard using:

- Streamlit
- Pandas
- Matplotlib
- Seaborn
- Plotly

Suggested dashboard sections:

1. Dataset overview
2. Data quality summary
3. Filters
4. Top categories
5. Trend chart
6. Correlation heatmap
7. Key insights
