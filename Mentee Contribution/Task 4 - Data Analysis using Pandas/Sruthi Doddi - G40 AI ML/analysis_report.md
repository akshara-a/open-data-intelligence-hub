# HR Analytics Data Analysis Report

## 1. Dataset Overview
- **Dataset:** HR Analytics (Kaggle)
- **Original Rows:** 1,480
- **Cleaned Rows:** 1,473
- **Columns:** 38
- **Key Focus:** Employee Attrition, Income, Department Performance
- **File Format:** CSV

## 2. Data Quality Issues

| Column | Issue Found | Number of Records | Suggested Fix |
|--------|------------|-------------------|---------------|
| YearsWithCurrManager | Missing values | 57 | Filled with median |
| BusinessTravel | Inconsistent values | Multiple | Standardized values |
| Multiple columns | Duplicate records | 7 | Removed duplicates |

## 3. Cleaning Steps

| Cleaning Step | Column Used | Method Applied | Reason |
|---|---|---|---|
| Missing value handling | YearsWithCurrManager | Filled with median | To handle incomplete records |
| Duplicate removal | All columns | Drop duplicates | To avoid redundant data |
| Text standardization | BusinessTravel | Replaced inconsistent values | For data consistency |
| Column renaming | All columns | Lowercase with underscores | For code standardization |

## 4. Exploratory Data Analysis

### Key Statistics
- **Average Age:** 36.9 years
- **Average Monthly Income:** $6,503
- **Average Years at Company:** 7.0 years
- **Overall Attrition Rate:** 16.1%
- **Most Common Department:** Research & Development (963 employees)
- **Most Common Education Field:** Life Sciences (606 employees)

### Department Distribution
- Research & Development: 963 (65.4%)
- Sales: 447 (30.3%)
- Human Resources: 63 (4.3%)

## 5. Grouping and Aggregation Results

| Department | Employee Count | Avg Income | Avg Age | Attrition Rate | Avg Tenure | Overtime % |
|------------|---------------|------------|---------|----------------|------------|------------|
| Human Resources | 63 | $6,654 | 37.8 | 19.05% | 7.24 | 26.98% |
| Research & Development | 963 | $6,281 | 37.0 | 13.81% | 6.86 | 28.14% |
| Sales | 447 | $6,950 | 36.5 | 20.58% | 7.28 | 28.64% |

## 6. Feature Engineering

| New Feature | Logic Used | Why It Is Useful |
|-------------|------------|------------------|
| income_category | Low (<$5k), Medium ($5k-$10k), High (>$10k) | To segment employees by income level |
| tenure_category | New (<2yrs), Intermediate (2-5yrs), Experienced (5-10yrs), Veteran (>10yrs) | To understand employee lifecycle |
| age_category | 18-25, 26-35, 36-45, 46-55, 55+ | To analyze age-based patterns |
| engagement_score | Composite of job involvement, job satisfaction, and attrition | To measure overall engagement |

## 7. Visualizations

| Chart Title | Columns Used | Chart Type | Insight |
|-------------|--------------|------------|----------|
| Attrition Rate by Department | Department, Attrition | Bar Chart | Sales has highest attrition (20.6%), R&D has lowest (13.8%) |
| Monthly Income Distribution | Monthly Income | Histogram | Most employees earn between $3,000-$8,000, with skew towards lower income |
| Attrition Rate by Overtime Status | Overtime, Attrition | Bar Chart | Employees working overtime have 30.5% attrition vs 10.4% for non-overtime |

## 8. Correlation Analysis

### Observations:

**Observation 1:**
- **Total Working Years and Monthly Income** have a strong positive correlation (0.77)
- **Business Meaning:** More experienced employees earn significantly higher incomes
- **Recommended Action:** Consider creating clear career progression paths

**Observation 2:**
- **Age and Monthly Income** have a moderate positive correlation (0.50)
- **Business Meaning:** Older employees tend to have higher income due to experience
- **Recommended Action:** Ensure age diversity in teams and fair compensation

**Observation 3:**
- **Years at Company and Monthly Income** have a moderate positive correlation (0.51)
- **Business Meaning:** Loyalty/tenure at the same company correlates with higher pay
- **Recommended Action:** Recognize and reward long-tenured employees

**Observation 4:**
- **Number of Companies Worked** has weak correlation with income (0.15)
- **Business Meaning:** Job hopping doesn't significantly impact income in this dataset
- **Recommended Action:** Focus on internal development rather than external hiring

## 9. Key Insights

### Insight 1: Sales Department Has Highest Attrition
**Evidence:** Sales department has 20.58% attrition rate vs company average of 16.1%
**Business Meaning:** Sales team faces significant retention challenges
**Recommended action:** Implement retention bonuses, career growth opportunities, and regular check-ins for Sales employees

### Insight 2: Overtime is a Major Attrition Driver
**Evidence:** 30.5% of employees working overtime leave vs only 10.4% who don't
**Business Meaning:** Work-life balance is critical for retention
**Recommended action:** Monitor overtime, implement flexible work options, and hire additional staff if needed

### Insight 3: Experience Drives Higher Income
**Evidence:** Strong correlation (0.77) between total working years and monthly income
**Business Meaning:** Companies value experience and reward it through compensation
**Recommended action:** Create structured career paths and provide learning opportunities

### Insight 4: Most Employees Are Low Income Bracket
**Evidence:** 751 employees (51%) earn less than $5,000 per month
**Business Meaning:** Majority of workforce is in entry to mid-level positions
**Recommended action:** Review compensation structure for lower-paid positions

### Insight 5: R&D Department is Most Stable
**Evidence:** R&D has lowest attrition rate at 13.81% and highest number of employees
**Business Meaning:** R&D provides stable careers with good retention
**Recommended action:** Study R&D practices and apply to other departments

### Insight 6: Income and Age Grow Together
**Evidence:** Moderate positive correlation (0.50) between age and income
**Business Meaning:** Career progression happens with age
**Recommended action:** Provide accelerated growth tracks for young employees

### Insight 7: Job Satisfaction Doesn't Strongly Correlate with Income
**Evidence:** Weak negative correlation (-0.01) between income and job satisfaction
**Business Meaning:** Money alone doesn't ensure job satisfaction
**Recommended action:** Focus on recognition, work culture, and meaningful work alongside compensation

### Insight 8: Employees with 5-10 Years Experience Are Most Common
**Evidence:** 526 employees (36%) are in "Experienced" tenure category (5-10 years)
**Business Meaning:** Retention improves after the first 5 years
**Recommended action:** Focus retention efforts on employees with <5 years experience

## 10. Recommendations

1. **Prioritize Sales Retention:** Address high attrition in Sales through bonuses, career development, and improved work conditions
2. **Manage Overtime:** Implement policies to limit overtime and monitor stressed employees
3. **Review Compensation:** Conduct salary benchmarking for lower-income employees
4. **Create Career Paths:** Develop clear progression paths to retain experienced employees
5. **Learn from R&D:** Study and replicate R&D department's retention strategies across other departments
6. **Improve Onboarding:** Strengthen onboarding for new employees to reduce early attrition
7. **Work-Life Balance Initiatives:** Introduce flexible working hours and mental health support
8. **Engagement Surveys:** Regularly measure and act on employee engagement scores

## 11. Conclusion

The HR Analytics analysis reveals that **overtime** and **department** significantly impact employee attrition. The Sales department faces the highest turnover (20.6%), while overtime employees are 3x more likely to leave than non-overtime employees. 

**Income** is strongly tied to experience and tenure, but not necessarily to job satisfaction, indicating that compensation alone is not a retention solution. 

**Key recommendations** include improving Sales retention, managing overtime, creating clear career paths, and learning from the stable R&D department. These data-driven actions can help reduce overall attrition from 16.1% to a more sustainable level.

---
**Report Generated:** June 18, 2026  
**Analyst:** [Your Name]  
**Dataset Source:** Kaggle HR Analytics Dataset