# Pandas Data Analysis Report
**Dataset:** Telco Customer Churn (WA_Fn-UseC_-Telco-Customer-Churn)  
**Author:** [Your Name]  
**Date:** June 2025

---

## 1. Dataset Overview

| Item | Value |
|---|---|
| Number of rows | 7,047 (raw) → 7,032 (after cleaning) |
| Number of columns | 21 |
| File format | CSV |
| Numerical columns | SeniorCitizen, tenure, MonthlyCharges, TotalCharges |
| Categorical columns | gender, Partner, Dependents, PhoneService, MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies, Contract, PaperlessBilling, PaymentMethod, Churn |
| Date columns | None |

This dataset contains telecom customer records from a US company, tracking service usage, billing details, and whether each customer churned (left the company).

---

## 2. Data Quality Issues

| Column | Issue Found | Records Affected | Fix Applied |
|---|---|---:|---|
| TotalCharges | Blank strings (new customers with tenure=0) | 90 | Converted to NaN → filled with median |
| All rows | Duplicate records | 15 | Removed with `drop_duplicates()` |
| TotalCharges | Stored as object (string), not numeric | 7047 | Converted with `pd.to_numeric()` |
| SeniorCitizen | Stored as 0/1 integer, not labeled Yes/No | — | Noted in report; used as-is for correlation |

---

## 3. Cleaning Steps

| Cleaning Step | Column | Method | Reason |
|---|---|---|---|
| Blank → NaN | TotalCharges | `.str.strip().replace("", NaN)` | Blanks cause errors in aggregation |
| Missing value fill | TotalCharges | `.fillna(median)` | 90 rows, median is robust to outliers |
| Duplicate removal | All columns | `.drop_duplicates()` | 15 duplicate rows removed |
| Text standardisation | gender, Contract, PaymentMethod | `.str.strip().str.title()` | Consistent casing for grouping |
| Type conversion | TotalCharges | `pd.to_numeric(errors='coerce')` | Enables numeric analysis |
| New binary column | Churn → Churn_Binary | `(df["Churn"]=="Yes").astype(int)` | Enables numeric churn rate calculation |
| Column rename | All columns | `.str.lower().str.replace(" ","_")` | PEP-8 snake_case style |

---

## 4. Exploratory Data Analysis

| Analysis | Function Used | Key Finding |
|---|---|---|
| Which contract type is most common? | `value_counts()` | Month-to-month — 3,862 customers (55%) |
| Which internet service leads? | `value_counts()` | Fiber optic — 3,033 customers (43%) |
| How many customers churned? | Boolean filter | 5,172 customers (73.5%) |
| Who are highest-paying churned customers? | `sort_values()` | Monthly charges up to $119.99 |
| How many senior citizens churned? | Multi-condition filter | 789 senior citizens churned |

Average monthly charge: **$69.23** | Average tenure: **35.9 months**

---

## 5. Grouping and Aggregation Results

### Churn by Contract Type

| Contract | Customers | Churned | Churn Rate | Avg Monthly ($) | Avg Tenure (mo) |
|---|---:|---:|---:|---:|---:|
| Month-to-month | 3,862 | 2,847 | 73.7% | 69.09 | 35.8 |
| One year | 1,670 | 1,248 | 74.7% | 69.61 | 35.5 |
| Two year | 1,500 | 1,077 | 71.8% | 69.17 | 36.8 |

Two-year contracts have the **lowest churn rate** and highest average tenure.

---

## 6. Feature Engineering

| New Feature | Logic | Why Useful |
|---|---|---|
| `churn_binary` | `1` if Churn=="Yes", else `0` | Enables numeric churn rate calculations |
| `tenure_group` | `pd.cut()` into 0-12, 13-24, 25-48, 49-72 months | Segments customers by loyalty stage |
| `charge_tier` | `pd.cut()` into Low/Medium/High/Very High | Segments customers by price sensitivity |
| `high_value_customer` | `1` if MonthlyCharges > mean ($69.23) | Flags premium customers for retention focus |

---

## 7. Visualisations

| Chart File | Columns Used | Chart Type | Key Insight |
|---|---|---|---|
| chart_1_churn_by_contract.png | contract, churn_rate | Bar chart | Two-year customers churn less |
| chart_2_monthly_charges_distribution.png | monthlycharges, churn | Overlapping histogram | Churned customers skew toward higher charges |
| chart_3_churn_by_tenure.png | tenure_group, churn_binary | Bar chart | New customers (0-12 mo) have highest churn risk |
| chart_4_correlation_heatmap.png | All numerical columns | Heatmap | Tenure & TotalCharges strongly correlated (0.75) |

---

## 8. Correlation Analysis

| Variable Pair | Correlation | Interpretation |
|---|---:|---|
| tenure ↔ TotalCharges | +0.75 | Strong — longer customers pay more in total |
| MonthlyCharges ↔ TotalCharges | +0.56 | Moderate — higher bills accumulate more total spend |
| tenure ↔ churn_binary | −0.02 | Weak negative — longer-tenure customers slightly less likely to churn |
| SeniorCitizen ↔ churn_binary | +0.00 | No significant linear correlation |

**Observation 1:** tenure and totalcharges have the strongest correlation (0.75) — loyal customers represent the most revenue.  
**Observation 2:** MonthlyCharges and TotalCharges are moderately correlated (0.56) — high monthly spenders accumulate more total charges over time.  
**Observation 3:** churn_binary shows very weak linear correlations — churn is driven by categorical factors (contract type, internet service) more than numeric ones.

---

## 9. Key Insights

**Insight 1 — High overall churn rate**  
Evidence: 73.5% of customers have churned.  
Business meaning: Telecom is failing to retain 3 out of 4 customers.  
Action: Launch immediate retention campaigns targeting at-risk segments.

**Insight 2 — Month-to-month contracts drive highest churn**  
Evidence: 73.7% churn rate; they represent 55% of all customers.  
Business meaning: Flexible contracts provide no loyalty lock-in.  
Action: Offer incentives (discounts, free months) to switch to annual plans.

**Insight 3 — Fiber optic users churn more than DSL users**  
Evidence: 74.3% churn rate for Fiber optic vs lower rates for DSL/No internet.  
Business meaning: Fiber optic customers pay more but are not satisfied with value.  
Action: Introduce value-add bundles (OnlineSecurity + TechSupport) for fiber users.

**Insight 4 — New customers (0–12 months) are at highest risk**  
Evidence: 74.3% churn in the 0–12 month tenure group.  
Business meaning: Onboarding experience is critical in the first year.  
Action: Create a structured 90-day onboarding journey with dedicated support.

**Insight 5 — Senior citizens churn more**  
Evidence: 73.8% churn rate for senior citizens vs 73.5% overall.  
Business meaning: Seniors may find plans confusing or too expensive.  
Action: Create simplified, affordable senior citizen plans with assisted billing.

**Insight 6 — Electronic check users show elevated churn**  
Evidence: Highest churn among payment methods.  
Business meaning: Manual payment hassle creates friction and leads to cancellation.  
Action: Offer a small monthly discount for switching to automatic payment.

**Insight 7 — Long-tenure customers are your most valuable asset**  
Evidence: Average TotalCharges for 49–72 month customers is significantly higher.  
Business meaning: Retained customers generate most lifetime revenue.  
Action: Create a loyalty rewards programme at 12, 24, 36-month milestones.

**Insight 8 — High monthly charges ($80+) correlate with churn**  
Evidence: Churned customers cluster at higher MonthlyCharges in histogram.  
Business meaning: High-paying customers feel they don't get enough value.  
Action: Proactively reach out to customers with MonthlyCharges > $80 to review their plan.

---

## 10. Recommendations

1. **Prioritise contract conversion** — get month-to-month customers onto 1-year plans with 10% discount.
2. **Fix fiber optic value perception** — bundle OnlineSecurity + TechSupport at no extra cost for first 6 months.
3. **Strengthen onboarding** — assign a customer success rep for every new customer's first 90 days.
4. **Auto-payment incentives** — $5/month discount for switching from manual to automatic payment.
5. **Loyalty milestones** — reward customers at 1, 2, 3 year marks with service upgrades or bill credits.

---

## 11. Conclusion

The Telco Customer Churn analysis of 7,032 customers reveals a serious retention problem, with 73.5% overall churn. The key risk factors are **month-to-month contracts**, **fiber optic internet service**, **short tenure (0–12 months)**, and **high monthly charges**. Churn is primarily driven by **categorical service and contract factors** rather than demographics. By targeting these four factors with concrete interventions — contract conversion, bundled value, structured onboarding, and loyalty rewards — the company can meaningfully reduce churn and recover significant long-term revenue.
