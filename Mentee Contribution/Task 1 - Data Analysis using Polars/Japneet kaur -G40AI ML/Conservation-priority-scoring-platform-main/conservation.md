# Conservation Priority Scoring Platform

## Overview

The Conservation Priority Scoring Platform is a data-driven web application developed using Streamlit, Polars, and Plotly. The platform analyzes species conservation records and converts conservation categories into numerical priority scores to help identify species and biological groups requiring urgent conservation attention.

The system provides interactive filtering, exploratory data analysis (EDA), risk assessment, priority ranking, and downloadable reports through a user-friendly dashboard.

**Live Application**

https://conservation-priority-scoring-platform-js6d2cgcdbgasqpww8sjny.streamlit.app/

---

## Problem Statement

Conservation datasets often contain large volumes of species information classified under different conservation categories. Interpreting these categories and identifying high-priority species can be difficult without analytical tools.

This platform addresses that challenge by:

* Converting conservation categories into priority scores.
* Categorizing species into risk levels.
* Providing visual analytics for decision-making.
* Allowing users to explore and download filtered datasets.

---

## Objectives

* Analyze species conservation data.
* Convert conservation categories into meaningful priority scores.
* Identify high-risk species and biological groups.
* Provide interactive visualizations for exploration.
* Generate downloadable conservation reports.

---

## Technology Stack

| Component            | Technology      |
| -------------------- | --------------- |
| Frontend             | Streamlit       |
| Data Processing      | Polars          |
| Visualization        | Plotly          |
| Programming Language | Python          |
| Deployment           | Streamlit Cloud |

---

## System Workflow

```text
Raw Conservation Dataset
            │
            ▼
      Data Loading
            │
            ▼
 Category Standardization
            │
            ▼
 Priority Score Assignment
            │
            ▼
 Priority Level Classification
            │
            ▼
 Interactive Filtering
            │
            ▼
 Data Analysis & Visualization
            │
            ▼
 Report Generation
```

---

## Priority Scoring Framework

| Conservation Category             | Priority Score |
| --------------------------------- | -------------- |
| Least Concern                     | 10             |
| Low Risk - Least Concern          | 15             |
| Low Risk - Near Threatened        | 25             |
| Near Threatened                   | 30             |
| Low Risk - Conservation Dependent | 35             |
| Data Deficient                    | 40             |
| Vulnerable                        | 50             |
| Endangered                        | 70             |
| Critically Endangered             | 90             |
| Extinct in Wild                   | 95             |
| Extinct                           | 100            |

---

## Priority Level Classification

| Score Range | Priority Level |
| ----------- | -------------- |
| 0 - 39      | Low            |
| 40 - 59     | Medium         |
| 60 - 79     | High           |
| 80 - 100    | Critical       |

---

## Features

### Dashboard Overview

Provides a high-level summary of:

* Total species count
* Critical priority species
* High priority species
* Medium priority species
* Low priority species

### Interactive Filters

Users can filter data by:

* Kingdom
* Conservation Category
* Priority Level

### Exploratory Data Analysis

The dashboard includes:

* Species Distribution by Conservation Category
* Priority Level Distribution
* Kingdom-wise Species Analysis
* Top Biological Classes Analysis

### Risk Analysis

Identifies conservation risk patterns through:

* Species Count vs Priority Score Analysis
* High-Risk Group Identification
* Average Priority Score Evaluation

### Priority Species Explorer

Displays species ranked by conservation priority score.

### Data Explorer

Allows users to inspect filtered datasets interactively.

### Report Download

Exports filtered results as CSV reports for further analysis.

---

## Application Architecture

```text
                 User
                   │
                   ▼
          Streamlit Interface
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
    Filters     Analytics    Reports
        │          │          │
        └──────────┼──────────┘
                   ▼
            Polars Engine
                   │
                   ▼
         Conservation Dataset
```

---

## Dataset Attributes

The dataset includes information such as:

* Taxon ID
* Kingdom
* Phylum
* Class
* Order
* Family
* Genus
* Scientific Name
* Common Name
* Population Status
* Conservation Category

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Ravneet-project/Conservation-priority-scoring-platform.git
cd Conservation-priority-scoring-platform
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

---

## Future Enhancements

* Geographic visualization using maps.
* Predictive conservation risk modeling.
* Machine Learning based species prioritization.
* Automated conservation recommendation system.
* Biodiversity trend forecasting.

---

## Author

**Ravneet Kaur**

Full Stack Developer

Technologies: Python, Streamlit, Polars, Plotly, MERN Stack, PHP CodeIgniter

---

## License

This project is developed for educational and analytical purposes.
