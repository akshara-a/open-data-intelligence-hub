#  Developer Career Intelligence Warehouse
 A Data Analytics and Business Intelligence project built from the Stack Overflow Developer Survey (2020–2025)

## 🌐 Live Dashboard
https://developer-career-intelligence-warehouse.streamlit.app/

## 📌 Project Overview

This project analyzes **424,980 developer responses** across 6 years to generate career intelligence, salary insights, and technology trends for HR professionals, recruiters, and students.

The project ingests raw Stack Overflow survey data, cleans and standardizes it using **Polars**, stores it as an optimized **Parquet warehouse**, and presents insights through an interactive **Streamlit dashboard** powered by **Plotly**.

## 🎯 Project Goals

- Analyze developer salaries across roles, countries, and education levels
- Track technology adoption trends from 2020 to 2025
- Build a mini HR analytics platform from survey responses

---

## 📊 Key Findings

| Metric | Finding |
|---|---|
| Most Used Language | JavaScript (66.3% in 2025) |
| Fastest Growing Language | TypeScript (+18.4% since 2020) |
| Top Database | PostgreSQL overtook MySQL in 2023 |
| Global Median Salary | $64,630 |
| Highest Paying Country | United States ($135,000) |
| Most Common Role | Full-stack Developer (145,063 responses) |
| Remote Work | 32.4% of developers work remotely |
| Most Common Education | Bachelor's Degree |
| Highest Paid Role | Engineering Manager ($103,408) |
| Countries Covered | 196 |


## 🗂️ Project Structure

```
developer-career-intelligence/
│
├── app.py                          ← Streamlit main entry point
│
├── pages/
│   ├── 1_Overview.py               ← KPI cards and summary charts
│   ├── 2_Salary_Analysis.py        ← Salary by role, country, education
│   ├── 3_Technology_Trends.py      ← Language, database, framework trends
│   └── 4_HR_Analytics.py           ← Geography, employment, developer profiles
│
├── data/
│   └── master_survey.parquet       ← Cleaned warehouse dataset (424,980 rows)
│
├── .streamlit/
│   └── config.toml                 ← Streamlit configuration
│
├── requirements.txt                ← Python dependencies
└── README.md                       ← Project documentation
```
---

## 🛠️ Technology Stack

| Layer | Tool | Purpose |
|---|---|---|
| Data Processing | Polars | Fast DataFrame operations |
| Visualization | Plotly | Interactive charts |
| Dashboard | Streamlit | Web application |
| File Format | Parquet | Optimized data storage |
| Language | Python 3.12 | Core language |
| Deployment | Streamlit Cloud | Free cloud hosting |
| Version Control | GitHub | Code repository |

---

## 📦 Data Source

| Detail | Info |
|---|---|
| Source | Stack Overflow Developer Survey |
| Official URL | https://survey.stackoverflow.co/ |
| Years Covered | 2020, 2021, 2022, 2023, 2024, 2025 |
| Total Responses | 424,980 |
| Countries | 196 |
| Raw Data Size | 709 MB |
| Warehouse Size | 8.65 MB |


## 🏗️ Data Pipeline Architecture

```
Raw CSV Files (709 MB — 6 years)
        ↓
Data Ingestion (Polars)
        ↓
Column Standardization
(unified names across years)
        ↓
Data Cleaning
(nulls, outliers, name fixes)
        ↓
Master Parquet Warehouse
(8.65 MB — 424,980 rows)
        ↓
Analytics Layer
(aggregations, KPIs)
        ↓
Streamlit Dashboard
(Plotly interactive charts)
```


---

## 🚀 Run Locally

**Step 1 — Clone the repository**
```bash
git clone https://github.com/lahari-prasanna/developer-career-intelligence.git
cd developer-career-intelligence
```

**Step 2 — Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 3 — Run the dashboard**
```bash
streamlit run app.py
```
