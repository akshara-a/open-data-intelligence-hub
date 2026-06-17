# Exploratory Data Analysis (EDA) and EDA Methods in AI/ML

## 1. What is EDA?

**EDA stands for Exploratory Data Analysis.**

It is the process of understanding, checking, summarizing, and visualizing data before building a Machine Learning model.

In simple words:

> EDA means exploring your dataset to understand what is inside it, what problems it has, and what useful patterns can be found.

Before training an AI/ML model, we should not directly give raw data to the model. Real-world data usually has missing values, wrong values, duplicates, outliers, inconsistent formats, and hidden patterns. EDA helps us find these issues and understand the data better.

---

## 2. Why is EDA Important in AI/ML?

EDA is important because a Machine Learning model learns from data. If the data is poor, the model will also perform poorly.

This is often explained using the phrase:

> Garbage in, garbage out.

If we give bad-quality data to a model, the output will also be unreliable.

### EDA helps us to:

- Understand the dataset properly
- Find missing values
- Find duplicate records
- Detect wrong or impossible values
- Identify outliers
- Understand relationships between columns
- Understand the target variable
- Select useful features
- Remove irrelevant features
- Decide preprocessing steps
- Improve model accuracy
- Avoid misleading conclusions

---

## 3. EDA in the AI/ML Workflow

EDA usually comes after data collection and before model building.

### Typical AI/ML workflow:

1. Define the problem
2. Collect data
3. Perform EDA
4. Clean the data
5. Engineer features
6. Split data into training and testing sets
7. Train the model
8. Evaluate the model
9. Improve the model
10. Deploy the model

EDA is one of the most important steps because it helps us understand what needs to be fixed or improved before training the model.

---

## 4. Example Dataset Scenario

Let us imagine we are working on a Machine Learning problem:

> Predict whether a customer will cancel a subscription or continue using the service.

This is called a **customer churn prediction problem**.

The dataset may contain columns like:

| Column Name | Meaning |
|---|---|
| CustomerId | Unique customer identifier |
| Age | Customer age |
| Gender | Customer gender |
| SubscriptionType | Basic, Standard, Premium |
| MonthlyCharges | Monthly subscription amount |
| TotalCharges | Total amount paid so far |
| TenureMonths | Number of months customer stayed |
| SupportCalls | Number of customer support calls |
| PaymentMethod | Credit card, UPI, bank transfer, etc. |
| Churn | Whether the customer left or not |

Here, `Churn` is the target column.

EDA helps us answer questions like:

- Are customers with high monthly charges more likely to churn?
- Do customers with many support calls leave more often?
- Are new customers more likely to churn than long-term customers?
- Are there missing values in TotalCharges?
- Are there duplicate customers?
- Are there incorrect ages like 0, -5, or 200?

---

# 5. Types of EDA

EDA can be divided into different types based on how many variables we analyze at a time.

## 5.1 Univariate Analysis

**Univariate analysis** means analyzing one column at a time.

Example:

- Analyzing only `Age`
- Analyzing only `MonthlyCharges`
- Analyzing only `Churn`

### Purpose:

To understand the distribution, range, and quality of a single column.

### Questions answered:

- What is the average age?
- What is the minimum and maximum monthly charge?
- How many customers churned?
- Are there missing values in this column?
- Are there unusual values?

### Common methods:

- Count values
- Mean
- Median
- Mode
- Minimum
- Maximum
- Standard deviation
- Histogram
- Box plot
- Bar chart

---

## 5.2 Bivariate Analysis

**Bivariate analysis** means analyzing two columns together.

Example:

- `MonthlyCharges` vs `Churn`
- `TenureMonths` vs `Churn`
- `Age` vs `MonthlyCharges`

### Purpose:

To understand the relationship between two variables.

### Questions answered:

- Do customers with higher monthly charges churn more?
- Does age affect total spending?
- Does tenure affect churn?
- Are two columns strongly related?

### Common methods:

- Scatter plot
- Box plot grouped by category
- Bar chart comparison
- Correlation
- Cross-tabulation
- Group by summary

---

## 5.3 Multivariate Analysis

**Multivariate analysis** means analyzing more than two columns together.

Example:

- `MonthlyCharges`, `TenureMonths`, and `Churn`
- `Age`, `SubscriptionType`, `SupportCalls`, and `Churn`

### Purpose:

To understand complex relationships between multiple features.

### Questions answered:

- Do premium customers with high support calls churn more?
- Does churn depend on both tenure and payment method?
- Which combination of features affects the target most?

### Common methods:

- Pair plot
- Heatmap
- Grouped bar chart
- Pivot table
- Correlation matrix
- Feature interaction analysis

---

# 6. Important EDA Methods in AI/ML

## Method 1: Understanding the Dataset Structure

The first step in EDA is understanding the basic structure of the dataset.

### Check:

- Number of rows
- Number of columns
- Column names
- Data types
- First few records
- Last few records
- Basic summary

### Why this matters:

This helps us quickly understand what kind of data we have.

### Example questions:

- How many customers are there?
- How many features are available?
- Which columns are numerical?
- Which columns are categorical?
- Is the target column present?

### Python example:

```python
import pandas as pd

# Load dataset
df = pd.read_csv("customer_churn.csv")

# Display first 5 rows
print(df.head())

# Display number of rows and columns
print(df.shape)

# Display column names and data types
print(df.info())

# Display summary statistics
print(df.describe())
```

---

## Method 2: Checking Data Types

Every column has a data type.

Common data types are:

| Data Type | Example |
|---|---|
| Integer | Age, Number of purchases |
| Float | MonthlyCharges, Salary |
| String/Object | Name, City, Gender |
| Boolean | True/False |
| DateTime | SignupDate, TransactionDate |

### Why this matters:

Machine Learning models need data in the correct format. Wrong data types can cause errors or poor model performance.

### Example issue:

`TotalCharges` may look like a number but may be stored as text because of blank spaces or invalid values.

### Python example:

```python
# Check data types
print(df.dtypes)

# Convert column to numeric if needed
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
```

---

## Method 3: Checking Missing Values

Missing values are empty or unavailable values in the dataset.

Examples:

- Age is missing
- TotalCharges is blank
- Gender is unknown
- PaymentMethod is not recorded

### Why missing values are a problem:

Many ML algorithms cannot handle missing values directly. Missing data can also hide important patterns.

### Common ways to handle missing values:

| Method | Meaning |
|---|---|
| Remove rows | Delete records with missing values |
| Remove columns | Delete columns with too many missing values |
| Fill with mean | Use average value for numerical columns |
| Fill with median | Use middle value for numerical columns |
| Fill with mode | Use most frequent value for categorical columns |
| Fill with "Unknown" | Useful for categorical columns |

### Python example:

```python
# Count missing values in each column
print(df.isnull().sum())

# Percentage of missing values
missing_percentage = df.isnull().mean() * 100
print(missing_percentage)

# Fill missing Age with median
df["Age"] = df["Age"].fillna(df["Age"].median())

# Fill missing PaymentMethod with Unknown
df["PaymentMethod"] = df["PaymentMethod"].fillna("Unknown")
```

---

## Method 4: Checking Duplicate Records

Duplicate records are repeated rows in the dataset.

### Why duplicates are a problem:

Duplicates can make the model biased. For example, if one customer appears multiple times, the model may give too much importance to that customer.

### Python example:

```python
# Count duplicate rows
print(df.duplicated().sum())

# Remove duplicate rows
df = df.drop_duplicates()
```

---

## Method 5: Summary Statistics

Summary statistics help us understand numerical columns.

### Common statistics:

| Statistic | Meaning |
|---|---|
| Count | Number of non-empty values |
| Mean | Average value |
| Median | Middle value |
| Mode | Most common value |
| Minimum | Smallest value |
| Maximum | Largest value |
| Standard deviation | How spread out the values are |
| Percentiles | Values below which a percentage of data falls |

### Why this matters:

Summary statistics help us detect unusual or incorrect values.

### Example:

If the minimum age is `-10`, that is clearly wrong.

If the maximum age is `250`, that is probably incorrect.

### Python example:

```python
# Summary of numerical columns
print(df.describe())

# Summary of categorical columns
print(df.describe(include="object"))
```

---

## Method 6: Analyzing Categorical Variables

Categorical variables contain categories or labels.

Examples:

- Gender
- City
- SubscriptionType
- PaymentMethod

### Common checks:

- Unique values
- Number of unique categories
- Frequency of each category
- Spelling inconsistencies
- Rare categories

### Example issue:

The same category may be written in different ways:

- Male
- male
- M
- MALE

These should be cleaned and standardized.

### Python example:

```python
# Count unique values
print(df["SubscriptionType"].nunique())

# Display unique values
print(df["SubscriptionType"].unique())

# Frequency count
print(df["SubscriptionType"].value_counts())
```

---

## Method 7: Analyzing Numerical Variables

Numerical variables contain numbers.

Examples:

- Age
- Salary
- MonthlyCharges
- TotalCharges
- TenureMonths

### Common checks:

- Minimum value
- Maximum value
- Average value
- Distribution shape
- Outliers
- Negative values where not allowed
- Zero values where suspicious

### Python example:

```python
# Check numerical column distribution
print(df["MonthlyCharges"].describe())

# Check invalid values
print(df[df["Age"] < 0])
```

---

## Method 8: Data Visualization

Data visualization means using charts to understand data visually.

Charts make patterns easier to understand than raw tables.

### Common EDA visualizations:

| Chart | Used For |
|---|---|
| Histogram | Distribution of numerical data |
| Box plot | Outlier detection |
| Bar chart | Category comparison |
| Pie chart | Simple percentage distribution |
| Scatter plot | Relationship between two numerical variables |
| Line chart | Trend over time |
| Heatmap | Correlation between many variables |
| Pair plot | Relationship among multiple numerical columns |

---

## Method 9: Histogram

A histogram shows the distribution of a numerical column.

### Use it to understand:

- Is the data normally distributed?
- Is the data skewed?
- Are values concentrated in one range?
- Are there unusual gaps?

### Example:

A histogram of `Age` shows whether most customers are young, middle-aged, or older.

### Python example:

```python
import matplotlib.pyplot as plt

plt.hist(df["Age"], bins=20)
plt.xlabel("Age")
plt.ylabel("Number of Customers")
plt.title("Age Distribution")
plt.show()
```

---

## Method 10: Box Plot

A box plot is useful for detecting outliers.

### Outlier meaning:

An outlier is a value that is very different from most other values.

Example:

If most monthly charges are between 200 and 2000, but one value is 100000, that value may be an outlier.

### Python example:

```python
plt.boxplot(df["MonthlyCharges"])
plt.title("Monthly Charges Box Plot")
plt.show()
```

---

## Method 11: Bar Chart

A bar chart is used for categorical data.

### Example:

We can use a bar chart to show the number of customers in each subscription type.

### Python example:

```python
df["SubscriptionType"].value_counts().plot(kind="bar")
plt.xlabel("Subscription Type")
plt.ylabel("Number of Customers")
plt.title("Customers by Subscription Type")
plt.show()
```

---

## Method 12: Scatter Plot

A scatter plot shows the relationship between two numerical variables.

### Example:

We can compare `TenureMonths` and `TotalCharges`.

Usually, customers with longer tenure may have higher total charges.

### Python example:

```python
plt.scatter(df["TenureMonths"], df["TotalCharges"])
plt.xlabel("Tenure Months")
plt.ylabel("Total Charges")
plt.title("Tenure vs Total Charges")
plt.show()
```

---

## Method 13: Correlation Analysis

Correlation measures how strongly two numerical variables are related.

### Correlation values:

| Correlation Value | Meaning |
|---|---|
| +1 | Perfect positive relationship |
| 0 | No linear relationship |
| -1 | Perfect negative relationship |

### Example:

If `TenureMonths` and `TotalCharges` have high positive correlation, it means customers who stay longer usually pay more overall.

### Important note:

Correlation does not always mean causation.

For example, two variables may move together, but one may not directly cause the other.

### Python example:

```python
# Correlation matrix
corr = df.corr(numeric_only=True)
print(corr)
```

Using heatmap:

```python
import seaborn as sns

sns.heatmap(corr, annot=True)
plt.title("Correlation Heatmap")
plt.show()
```

---

## Method 14: Target Variable Analysis

The target variable is the column we want to predict.

Examples:

| Problem Type | Target Variable Example |
|---|---|
| Churn prediction | Churn |
| House price prediction | Price |
| Spam detection | Spam or Not Spam |
| Loan approval | Approved or Rejected |
| Disease prediction | Disease Present or Not |

### Why target analysis is important:

We need to understand the output column before building the model.

### For classification problems:

Check how many records belong to each class.

Example:

```python
print(df["Churn"].value_counts())
print(df["Churn"].value_counts(normalize=True) * 100)
```

### Class imbalance:

If one class has too many records and another class has very few, it is called class imbalance.

Example:

| Churn | Count |
|---|---:|
| No | 9500 |
| Yes | 500 |

This means only 5% customers churned. A model may become biased toward predicting `No` all the time.

---

## Method 15: Outlier Detection

Outliers are values that are far away from normal values.

### Examples:

- Age = 200
- Salary = 999999999
- MonthlyCharges = -500
- TenureMonths = 10000

### Common ways to detect outliers:

- Box plot
- IQR method
- Z-score method
- Domain knowledge

---

## Method 16: IQR Method for Outliers

IQR stands for **Interquartile Range**.

```text
IQR = Q3 - Q1
```

Where:

- Q1 = 25th percentile
- Q3 = 75th percentile

### Outlier rule:

```text
Lower Bound = Q1 - 1.5 * IQR
Upper Bound = Q3 + 1.5 * IQR
```

Values below the lower bound or above the upper bound are considered outliers.

### Python example:

```python
Q1 = df["MonthlyCharges"].quantile(0.25)
Q3 = df["MonthlyCharges"].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = df[(df["MonthlyCharges"] < lower_bound) | (df["MonthlyCharges"] > upper_bound)]
print(outliers)
```

---

## Method 17: Skewness Analysis

Skewness tells us whether data is balanced or tilted to one side.

### Types of skewness:

| Type | Meaning |
|---|---|
| No skew | Data is balanced |
| Right skew | Long tail on the right side |
| Left skew | Long tail on the left side |

### Why this matters:

Some ML models perform better when numerical data is more normally distributed.

### Python example:

```python
print(df["MonthlyCharges"].skew())
```

If the value is highly positive or negative, the column may be skewed.

---

## Method 18: Feature Relationship Analysis

Feature relationship analysis means checking how input columns relate to each other and to the target.

### Example questions:

- Does `SupportCalls` affect `Churn`?
- Does `SubscriptionType` affect `MonthlyCharges`?
- Does `TenureMonths` affect `TotalCharges`?

### Python example:

```python
# Average monthly charges by churn status
print(df.groupby("Churn")["MonthlyCharges"].mean())

# Average support calls by churn status
print(df.groupby("Churn")["SupportCalls"].mean())
```

---

## Method 19: GroupBy Analysis

GroupBy analysis summarizes data based on categories.

### Example:

Find average monthly charges for each subscription type.

```python
print(df.groupby("SubscriptionType")["MonthlyCharges"].mean())
```

Find churn rate by payment method.

```python
churn_by_payment = df.groupby("PaymentMethod")["Churn"].value_counts(normalize=True)
print(churn_by_payment)
```

### Why this matters:

It helps find business insights.

Example insight:

> Customers using monthly payment plans have a higher churn rate than customers using annual plans.

---

## Method 20: Cross-Tabulation

Cross-tabulation compares two categorical variables.

### Example:

Compare `SubscriptionType` and `Churn`.

```python
pd.crosstab(df["SubscriptionType"], df["Churn"])
```

With percentages:

```python
pd.crosstab(df["SubscriptionType"], df["Churn"], normalize="index") * 100
```

### Why this matters:

It helps us understand category-wise behavior.

---

## Method 21: Date and Time Analysis

Many datasets contain date columns.

Examples:

- SignupDate
- LastLoginDate
- PurchaseDate
- RenewalDate

### Useful date-based features:

- Year
- Month
- Day
- Day of week
- Weekend or weekday
- Customer age in days
- Time since last activity

### Python example:

```python
# Convert to datetime
df["SignupDate"] = pd.to_datetime(df["SignupDate"])

# Extract month and year
df["SignupMonth"] = df["SignupDate"].dt.month
df["SignupYear"] = df["SignupDate"].dt.year
```

---

## Method 22: Data Quality Checks

Data quality checks help us detect wrong, inconsistent, or impossible values.

### Examples of bad data:

| Column | Bad Value | Reason |
|---|---|---|
| Age | -5 | Age cannot be negative |
| Age | 200 | Very unlikely |
| MonthlyCharges | -100 | Charges cannot be negative |
| Gender | M, Male, male | Inconsistent formatting |
| SignupDate | Future date | May be invalid |
| Email | missing @ symbol | Invalid email |

### Data quality checklist:

- Are there missing values?
- Are there duplicates?
- Are data types correct?
- Are values within valid range?
- Are categories consistent?
- Are date values valid?
- Are numerical values realistic?

---

## Method 23: Feature Importance Exploration

Before using advanced feature importance methods, EDA helps us guess which features may be important.

### Example:

For churn prediction, useful features may be:

- TenureMonths
- MonthlyCharges
- SupportCalls
- PaymentMethod
- SubscriptionType

### Why this matters:

Feature importance helps us understand which columns may influence prediction.

---

## Method 24: Detecting Data Leakage

Data leakage happens when the model uses information that would not be available at prediction time.

### Example:

Suppose we want to predict customer churn before the customer leaves.

A column like `CancellationDate` should not be used because it directly tells us that the customer already cancelled.

### Why this is dangerous:

The model may perform very well during training but fail in real life.

### EDA questions for leakage:

- Does any column directly reveal the target?
- Was this information available before prediction time?
- Are there future values included in training data?

---

## Method 25: Checking Class Imbalance

Class imbalance happens when one target class has many more records than another.

### Example:

| Churn | Percentage |
|---|---:|
| No | 90% |
| Yes | 10% |

### Why it matters:

The model may learn to always predict the majority class.

### Python example:

```python
print(df["Churn"].value_counts(normalize=True) * 100)
```

### Ways to handle imbalance:

- Use better evaluation metrics like precision, recall, F1-score
- Oversampling minority class
- Undersampling majority class
- SMOTE
- Class weights

---

# 7. EDA Methods Based on Data Type

## 7.1 EDA for Numerical Data

Numerical data contains numbers.

### Examples:

- Age
- Salary
- Price
- Tenure
- MonthlyCharges

### Methods:

- Mean
- Median
- Minimum
- Maximum
- Standard deviation
- Histogram
- Box plot
- Scatter plot
- Correlation
- Outlier detection
- Skewness check

---

## 7.2 EDA for Categorical Data

Categorical data contains labels or groups.

### Examples:

- Gender
- City
- Department
- SubscriptionType
- PaymentMethod

### Methods:

- Unique value count
- Frequency count
- Bar chart
- Pie chart
- Cross-tabulation
- Category standardization
- Rare category detection

---

## 7.3 EDA for Date/Time Data

Date/time data contains time-based information.

### Examples:

- SignupDate
- PurchaseDate
- LastLoginDate

### Methods:

- Convert to datetime
- Extract year, month, day
- Analyze trends over time
- Check seasonality
- Calculate duration
- Detect future dates or invalid dates

---

## 7.4 EDA for Text Data

Text data contains written language.

### Examples:

- Reviews
- Comments
- Feedback
- Support tickets

### Methods:

- Text length analysis
- Word count
- Most common words
- Missing text check
- Duplicate text check
- Sentiment analysis
- Stopword analysis
- Word cloud

---

# 8. Common EDA Visualizations and When to Use Them

| Visualization | Best Used For | Example |
|---|---|---|
| Histogram | Numerical distribution | Age distribution |
| Box plot | Outlier detection | Salary outliers |
| Bar chart | Category counts | Customers by plan type |
| Pie chart | Simple proportions | Churn percentage |
| Scatter plot | Relationship between two numbers | Age vs income |
| Line chart | Time-based trend | Monthly sales trend |
| Heatmap | Correlation matrix | Feature relationships |
| Pair plot | Multiple numerical relationships | All numeric features |
| Count plot | Category frequency | Payment method count |
| Violin plot | Distribution by category | Charges by churn |

---

# 9. EDA Checklist for AI/ML Projects

Use this checklist before building a model.

## Basic Understanding

- [ ] What is the problem statement?
- [ ] What is the target variable?
- [ ] How many rows are there?
- [ ] How many columns are there?
- [ ] What does each column mean?
- [ ] Are column names clear?

## Data Structure

- [ ] Are data types correct?
- [ ] Are numerical columns stored as numbers?
- [ ] Are date columns stored as datetime?
- [ ] Are categorical columns clean and consistent?

## Missing Values

- [ ] Which columns have missing values?
- [ ] What percentage of values are missing?
- [ ] Should missing values be removed or filled?
- [ ] Is missingness itself meaningful?

## Duplicates

- [ ] Are there duplicate rows?
- [ ] Are duplicate IDs present?
- [ ] Should duplicates be removed?

## Numerical Data

- [ ] What are the min and max values?
- [ ] Are there impossible values?
- [ ] Are there outliers?
- [ ] Is the data skewed?
- [ ] Should transformation be applied?

## Categorical Data

- [ ] How many unique categories are there?
- [ ] Are there spelling inconsistencies?
- [ ] Are there rare categories?
- [ ] Should categories be grouped?

## Target Variable

- [ ] Is the target column clean?
- [ ] Is there class imbalance?
- [ ] Are target labels correct?
- [ ] Is there data leakage?

## Relationships

- [ ] Which features are related to the target?
- [ ] Which numerical columns are correlated?
- [ ] Are there redundant features?
- [ ] Are there useful feature interactions?

## Final EDA Output

- [ ] Key data quality issues listed
- [ ] Important charts created
- [ ] Business insights written
- [ ] Preprocessing plan prepared
- [ ] Feature engineering ideas identified

---

# 10. EDA Report Template

You can use this structure for writing an EDA report.

## 10.1 Project Title

Example:

**Exploratory Data Analysis for Customer Churn Prediction**

## 10.2 Problem Statement

Explain the problem in simple words.

Example:

The goal of this project is to understand customer behavior and identify patterns that may help predict whether a customer will churn.

## 10.3 Dataset Overview

Mention:

- Number of rows
- Number of columns
- Source of data
- Target variable
- Important features

## 10.4 Data Dictionary

| Column | Description | Data Type |
|---|---|---|
| CustomerId | Unique customer ID | Text |
| Age | Customer age | Number |
| MonthlyCharges | Monthly bill amount | Number |
| Churn | Whether customer left | Category |

## 10.5 Missing Value Analysis

Mention:

- Columns with missing values
- Percentage of missing values
- How you handled them

## 10.6 Duplicate Analysis

Mention:

- Number of duplicate records
- Whether duplicates were removed

## 10.7 Numerical Analysis

Mention:

- Summary statistics
- Outliers
- Distribution
- Skewness

## 10.8 Categorical Analysis

Mention:

- Unique categories
- Frequency counts
- Rare categories
- Inconsistent values

## 10.9 Target Variable Analysis

Mention:

- Target distribution
- Class imbalance
- Target-related insights

## 10.10 Relationship Analysis

Mention:

- Important correlations
- Feature-target relationships
- Business patterns

## 10.11 Key Insights

Example:

- Customers with shorter tenure have higher churn.
- Customers with more support calls are more likely to churn.
- Premium plan customers have higher monthly charges.
- Some columns have missing values and need cleaning.

## 10.12 Preprocessing Recommendations

Example:

- Fill missing values in Age using median.
- Convert TotalCharges to numeric.
- Encode categorical variables.
- Scale numerical features.
- Remove duplicate rows.
- Handle outliers in MonthlyCharges.

## 10.13 Conclusion

Summarize what was learned from the data and what should be done before model building.

---

# 11. Sample EDA Code Template

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load dataset
df = pd.read_csv("data.csv")

# 2. Basic information
print(df.head())
print(df.shape)
print(df.info())
print(df.describe())

# 3. Missing values
print(df.isnull().sum())
print(df.isnull().mean() * 100)

# 4. Duplicate values
print(df.duplicated().sum())
df = df.drop_duplicates()

# 5. Categorical columns
categorical_cols = df.select_dtypes(include="object").columns
for col in categorical_cols:
    print(col)
    print(df[col].value_counts())
    print("-" * 50)

# 6. Numerical columns
numerical_cols = df.select_dtypes(include=["int64", "float64"]).columns
for col in numerical_cols:
    print(col)
    print(df[col].describe())
    print("-" * 50)

# 7. Histogram for numerical columns
for col in numerical_cols:
    plt.figure()
    plt.hist(df[col].dropna(), bins=20)
    plt.title(f"Distribution of {col}")
    plt.xlabel(col)
    plt.ylabel("Frequency")
    plt.show()

# 8. Box plot for outlier detection
for col in numerical_cols:
    plt.figure()
    plt.boxplot(df[col].dropna())
    plt.title(f"Box Plot of {col}")
    plt.show()

# 9. Correlation heatmap
corr = df.corr(numeric_only=True)
sns.heatmap(corr, annot=True)
plt.title("Correlation Heatmap")
plt.show()
```

---

# 12. Beginner-Friendly Example: Customer Churn EDA

## Step 1: Load the data

```python
import pandas as pd

df = pd.read_csv("customer_churn.csv")
```

## Step 2: View the first few rows

```python
print(df.head())
```

This helps us see how the data looks.

## Step 3: Check size of dataset

```python
print(df.shape)
```

Example output:

```text
(7043, 21)
```

This means the dataset has 7043 rows and 21 columns.

## Step 4: Check missing values

```python
print(df.isnull().sum())
```

If any column has missing values, we need to decide how to handle them.

## Step 5: Check churn count

```python
print(df["Churn"].value_counts())
```

This tells us how many customers churned and how many stayed.

## Step 6: Compare churn with monthly charges

```python
print(df.groupby("Churn")["MonthlyCharges"].mean())
```

This helps us understand whether churned customers paid more or less on average.

## Step 7: Compare churn with tenure

```python
print(df.groupby("Churn")["TenureMonths"].mean())
```

This helps us understand whether new customers or old customers churn more.

---

# 13. Difference Between EDA and Data Cleaning

| EDA | Data Cleaning |
|---|---|
| Understands the data | Fixes the data |
| Finds problems | Solves problems |
| Uses charts and statistics | Uses transformations and corrections |
| Example: Find missing values | Example: Fill missing values |
| Example: Detect outliers | Example: Cap or remove outliers |

EDA and data cleaning are closely connected. Usually, we perform EDA, find issues, clean the data, and then perform EDA again to confirm the data is better.

---

# 14. Difference Between EDA and Feature Engineering

| EDA | Feature Engineering |
|---|---|
| Explores existing data | Creates new useful features |
| Finds patterns | Uses patterns to improve model input |
| Example: Tenure affects churn | Create `IsNewCustomer` feature |
| Example: SignupDate has seasonality | Extract SignupMonth |

EDA helps us decide what features to create.

---

# 15. Common Mistakes Beginners Make in EDA

## Mistake 1: Directly training the model without understanding data

This can lead to poor model performance.

## Mistake 2: Ignoring missing values

Missing values can cause model errors.

## Mistake 3: Ignoring outliers

Outliers can strongly affect some models.

## Mistake 4: Not checking data types

Wrong data types can cause incorrect analysis.

## Mistake 5: Not analyzing the target variable

The target variable is the most important column in supervised learning.

## Mistake 6: Using too many charts without insights

Charts are useful only when we explain what they mean.

## Mistake 7: Confusing correlation with causation

Just because two columns are related does not mean one causes the other.

---

# 16. How EDA Helps Model Building

EDA helps us decide:

| EDA Finding | ML Decision |
|---|---|
| Missing values found | Apply imputation |
| Categorical columns found | Apply encoding |
| Numerical columns have different scales | Apply scaling |
| Outliers found | Remove, cap, or transform |
| Target imbalance found | Use class weights or resampling |
| Strongly correlated features found | Remove redundant features |
| Date columns found | Extract date features |
| Text columns found | Apply NLP preprocessing |

---

# 17. EDA Methods Summary Table

| Method | Purpose | Example |
|---|---|---|
| Dataset overview | Understand shape and columns | `df.shape`, `df.info()` |
| Missing value check | Find empty values | `df.isnull().sum()` |
| Duplicate check | Find repeated rows | `df.duplicated().sum()` |
| Data type check | Ensure correct formats | `df.dtypes` |
| Summary statistics | Understand numeric columns | `df.describe()` |
| Value counts | Understand categories | `df['Gender'].value_counts()` |
| Histogram | See distribution | Age distribution |
| Box plot | Detect outliers | Salary outliers |
| Bar chart | Compare categories | Plan type count |
| Scatter plot | Compare two numbers | Age vs income |
| Correlation | Find numerical relationship | Tenure vs total charges |
| Heatmap | Visualize correlation matrix | Feature correlation |
| GroupBy | Compare groups | Average salary by department |
| Cross-tab | Compare categories | Plan type vs churn |
| Target analysis | Understand output variable | Churn Yes/No count |
| Data leakage check | Avoid unrealistic features | Remove cancellation date |

---

# 18. Simple EDA Workflow for Any Dataset

Use this order for most AI/ML projects:

1. Load the dataset
2. Check rows and columns
3. Understand column meanings
4. Check data types
5. Check missing values
6. Check duplicates
7. Analyze numerical columns
8. Analyze categorical columns
9. Analyze target variable
10. Visualize important columns
11. Check outliers
12. Check correlations
13. Compare features with target
14. Write key insights
15. Decide preprocessing steps

---

# 19. Mini Project Idea: EDA for Customer Churn

## Objective

Perform EDA on a customer churn dataset and identify patterns that may explain why customers leave.

## Dataset Columns

- CustomerId
- Age
- Gender
- SubscriptionType
- MonthlyCharges
- TotalCharges
- TenureMonths
- SupportCalls
- PaymentMethod
- Churn

## Tasks

### Task 1: Dataset Overview

- Load the dataset
- Display first 10 rows
- Display number of rows and columns
- Display column names
- Display data types

### Task 2: Missing Value Analysis

- Find missing values
- Calculate missing percentage
- Decide how to handle missing values

### Task 3: Duplicate Analysis

- Count duplicate rows
- Remove duplicates if needed

### Task 4: Numerical Analysis

Analyze:

- Age
- MonthlyCharges
- TotalCharges
- TenureMonths
- SupportCalls

For each column, find:

- Mean
- Median
- Minimum
- Maximum
- Standard deviation
- Outliers

### Task 5: Categorical Analysis

Analyze:

- Gender
- SubscriptionType
- PaymentMethod
- Churn

For each column, find:

- Unique values
- Frequency count
- Percentage distribution

### Task 6: Visualization

Create:

- Histogram of Age
- Histogram of MonthlyCharges
- Bar chart of SubscriptionType
- Bar chart of Churn
- Box plot of MonthlyCharges
- Scatter plot of TenureMonths vs TotalCharges
- Correlation heatmap

### Task 7: Target Analysis

Analyze the `Churn` column.

Find:

- Number of churned customers
- Number of non-churned customers
- Churn percentage
- Whether class imbalance exists

### Task 8: Business Insights

Write at least 5 insights.

Example:

1. Customers with shorter tenure are more likely to churn.
2. Customers with higher support calls have higher churn.
3. Monthly charges may be higher for churned customers.
4. Some payment methods may have higher churn.
5. Premium customers may behave differently from basic plan customers.

### Task 9: Preprocessing Plan

Write what should be done before model training.

Example:

- Fill missing values
- Remove duplicate rows
- Convert categorical columns using encoding
- Scale numerical columns
- Handle outliers
- Split data into train and test sets

---

# 20. Final Notes

EDA is not just about creating charts. It is about understanding the data deeply.

A good EDA should answer:

- What data do we have?
- Is the data clean?
- What problems exist in the data?
- What patterns are visible?
- Which features may be useful?
- What preprocessing is required?
- What business insights can we generate?

In AI/ML, EDA is the foundation of a successful model. A model trained after good EDA is usually more reliable, explainable, and useful.

