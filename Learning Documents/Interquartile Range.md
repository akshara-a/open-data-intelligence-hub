# Interquartile Range (IQR) in AI/ML

## 1. What is Interquartile Range?

**Interquartile Range**, commonly called **IQR**, is a statistical measure that shows the spread of the middle 50% of the data.

In simple words:

> IQR tells us how spread out the central part of the data is.

It is mainly used in **Exploratory Data Analysis (EDA)** to understand data distribution and detect **outliers**.

---

## 2. Why is IQR Important in AI/ML?

In AI/ML, data quality is very important. If the dataset contains extreme values, also called **outliers**, they can affect model performance.

IQR helps us to:

- Understand the spread of data
- Detect outliers
- Clean noisy datasets
- Make better preprocessing decisions
- Improve machine learning model reliability

Example:

If you are building a model to predict customer salary and one salary value is extremely high, the model may learn incorrectly. IQR can help identify such unusual values.

---

## 3. Quartiles

To understand IQR, first understand **quartiles**.

Quartiles divide sorted data into four equal parts.

| Quartile | Meaning |
|---|---|
| Q1 | First quartile, 25th percentile |
| Q2 | Second quartile, 50th percentile, also called median |
| Q3 | Third quartile, 75th percentile |

---

## 4. Formula for IQR

```text
IQR = Q3 - Q1
```

Where:

- **Q1** = 25th percentile
- **Q3** = 75th percentile

So, IQR measures the distance between Q1 and Q3.

---

## 5. Simple Example

Consider this dataset:

```text
10, 12, 14, 15, 18, 20, 22, 25, 30
```

The values are already sorted.

### Step 1: Find the Median

The middle value is:

```text
18
```

So:

```text
Q2 = 18
```

### Step 2: Find Q1

Lower half:

```text
10, 12, 14, 15
```

Median of lower half:

```text
Q1 = (12 + 14) / 2 = 13
```

### Step 3: Find Q3

Upper half:

```text
20, 22, 25, 30
```

Median of upper half:

```text
Q3 = (22 + 25) / 2 = 23.5
```

### Step 4: Calculate IQR

```text
IQR = Q3 - Q1
IQR = 23.5 - 13
IQR = 10.5
```

So, the Interquartile Range is:

```text
10.5
```

---

## 6. Outlier Detection Using IQR

IQR is commonly used to find outliers.

The standard rule is:

```text
Lower Bound = Q1 - 1.5 × IQR
Upper Bound = Q3 + 1.5 × IQR
```

Any value below the lower bound or above the upper bound is considered an **outlier**.

---

## 7. Outlier Detection Example

Dataset:

```text
10, 12, 14, 15, 18, 20, 22, 25, 30, 100
```

Here, `100` looks unusually large.

Assume:

```text
Q1 = 14
Q3 = 25
```

### Step 1: Calculate IQR

```text
IQR = Q3 - Q1
IQR = 25 - 14
IQR = 11
```

### Step 2: Calculate Lower Bound

```text
Lower Bound = Q1 - 1.5 × IQR
Lower Bound = 14 - 1.5 × 11
Lower Bound = 14 - 16.5
Lower Bound = -2.5
```

### Step 3: Calculate Upper Bound

```text
Upper Bound = Q3 + 1.5 × IQR
Upper Bound = 25 + 1.5 × 11
Upper Bound = 25 + 16.5
Upper Bound = 41.5
```

### Step 4: Identify Outliers

Valid range:

```text
-2.5 to 41.5
```

Value `100` is greater than `41.5`.

So:

```text
100 is an outlier
```

---

## 8. Why Use IQR Instead of Range?

### Range

```text
Range = Maximum Value - Minimum Value
```

Range uses only the smallest and largest values.

Problem:

If there is one extreme value, the range becomes very large.

### IQR

IQR focuses only on the middle 50% of the data.

So, it is less affected by extreme values.

| Measure | Sensitive to Outliers? | Explanation |
|---|---|---|
| Range | Yes | Uses minimum and maximum values |
| IQR | No / Less | Uses Q1 and Q3 only |

---

## 9. IQR in Exploratory Data Analysis

In EDA, IQR is used to understand numerical columns.

For example, in a customer churn dataset, IQR can be used on:

- Age
- Monthly charges
- Total charges
- Tenure
- Number of support tickets
- Usage hours

EDA questions using IQR:

- Are there customers with unusually high bills?
- Are there customers with very low or very high usage?
- Are some values unrealistic?
- Do churned customers have a wider spread in monthly charges?
- Are there outliers that need treatment before model training?

---

## 10. IQR and Box Plot

A **box plot** is a visualization that uses quartiles and IQR.

A box plot shows:

- Minimum value
- Q1
- Median
- Q3
- Maximum value
- Outliers

### Box Plot Structure

```text
Minimum ---- Q1 ===== Median ===== Q3 ---- Maximum
```

The box part represents the IQR.

```text
IQR = Q3 - Q1
```

Outliers are usually shown as separate points outside the whiskers.

---

## 11. IQR Method in Machine Learning Workflow

IQR is usually applied during the data preprocessing stage.

### Typical Workflow

```text
Raw Data
   ↓
Data Cleaning
   ↓
EDA
   ↓
Outlier Detection using IQR
   ↓
Outlier Treatment
   ↓
Feature Engineering
   ↓
Model Training
   ↓
Model Evaluation
```

---

## 12. How to Handle Outliers Found by IQR

After detecting outliers, do not blindly delete them. First understand why they exist.

Common ways to handle outliers:

| Method | Meaning | When to Use |
|---|---|---|
| Remove outliers | Delete extreme values | When values are clearly wrong |
| Cap values | Replace extreme values with boundary values | When you want to reduce extreme impact |
| Transform data | Apply log or scaling | When data is heavily skewed |
| Keep outliers | Leave them unchanged | When outliers represent real business cases |

---

## 13. Example: Customer Churn Dataset

Suppose you have a subscription business dataset.

Column:

```text
MonthlyCharges
```

Values:

```text
200, 220, 250, 270, 300, 320, 350, 400, 450, 5000
```

Here, `5000` looks suspicious.

Using IQR, we may find that `5000` is an outlier.

Possible reasons:

- Data entry mistake
- Enterprise customer with high billing
- Currency mismatch
- System error
- Genuine premium customer

Business decision:

- If it is a data error, fix or remove it.
- If it is a real customer, keep it or treat it separately.

---

## 14. Python Example

```python
import pandas as pd

data = {
    "MonthlyCharges": [200, 220, 250, 270, 300, 320, 350, 400, 450, 5000]
}

df = pd.DataFrame(data)

Q1 = df["MonthlyCharges"].quantile(0.25)
Q3 = df["MonthlyCharges"].quantile(0.75)

IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = df[
    (df["MonthlyCharges"] < lower_bound) |
    (df["MonthlyCharges"] > upper_bound)
]

print("Q1:", Q1)
print("Q3:", Q3)
print("IQR:", IQR)
print("Lower Bound:", lower_bound)
print("Upper Bound:", upper_bound)
print("Outliers:")
print(outliers)
```

---

## 15. Output Explanation

If the output shows:

```text
Outliers:
   MonthlyCharges
9            5000
```

It means the value `5000` is outside the acceptable IQR range.

So, it is detected as an outlier.

---

## 16. IQR for Multiple Columns

In real ML projects, you may want to check outliers for multiple numerical columns.

```python
numeric_columns = ["Age", "MonthlyCharges", "TotalCharges", "Tenure"]

for column in numeric_columns:
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outlier_count = df[
        (df[column] < lower_bound) |
        (df[column] > upper_bound)
    ].shape[0]

    print(column, "outliers:", outlier_count)
```

---

## 17. IQR with Box Plot in Python

```python
import matplotlib.pyplot as plt

plt.boxplot(df["MonthlyCharges"])
plt.title("Box Plot of Monthly Charges")
plt.ylabel("Monthly Charges")
plt.show()
```

Box plots make outliers easy to visually detect.

---

## 18. Advantages of IQR

- Easy to understand
- Easy to calculate
- Useful for outlier detection
- Less affected by extreme values
- Works well for skewed data
- Very useful in EDA

---

## 19. Limitations of IQR

- It only works well for numerical data
- It does not explain why an outlier exists
- It may mark valid rare business cases as outliers
- It may not work well for every distribution
- It should not be used blindly without domain knowledge

---

## 20. IQR vs Standard Deviation

| Feature | IQR | Standard Deviation |
|---|---|---|
| Based on | Q1 and Q3 | Mean |
| Affected by outliers | Less affected | Highly affected |
| Best for | Skewed data | Normally distributed data |
| Used in | Outlier detection, EDA | Spread measurement, statistical analysis |

---

## 21. Common Interview Explanation

You can explain IQR like this:

> Interquartile Range is the difference between the third quartile and first quartile. It measures the spread of the middle 50% of the data. In machine learning, IQR is commonly used during EDA to detect outliers. Values below Q1 - 1.5 × IQR or above Q3 + 1.5 × IQR are considered outliers.

---

## 22. Beginner-Friendly Summary

- IQR means **Interquartile Range**
- It measures the spread of the middle 50% of data
- Formula:

```text
IQR = Q3 - Q1
```

- It is useful for outlier detection
- Outlier rule:

```text
Lower Bound = Q1 - 1.5 × IQR
Upper Bound = Q3 + 1.5 × IQR
```

- Values outside this range are considered outliers
- IQR is very useful in AI/ML preprocessing and EDA

---

## 23. Mini Practice Task

Use this dataset:

```text
5, 7, 8, 9, 10, 12, 14, 15, 100
```

Find:

1. Q1
2. Q3
3. IQR
4. Lower Bound
5. Upper Bound
6. Outlier values

Expected observation:

```text
100 is likely an outlier
```

---

## 24. Key Takeaway

IQR is one of the simplest and most powerful methods for detecting outliers in AI/ML datasets.

It helps data scientists clean data, understand distributions, and build better machine learning models.
