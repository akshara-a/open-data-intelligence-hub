# DuckDB Task

## Project Overview

This project demonstrates the use of **DuckDB**, an in-process analytical database designed for fast SQL querying on structured data. The project uses the **Mall Customers Dataset** to perform data loading, cleaning, SQL-based analysis, exporting results, performance comparison, and data visualization.

---

# Project Objectives

- Load a CSV dataset
- Perform Exploratory Data Analysis (EDA)
- Clean the dataset
- Create a DuckDB database
- Import data into DuckDB
- Execute SQL queries
- Perform advanced SQL analysis
- Export query results to CSV and Parquet
- Compare query performance between Pandas and DuckDB
- Generate data visualizations
- Summarize observations and conclusions

---

# Dataset

**Dataset Name:** Mall Customers Dataset

The dataset contains customer information including:

- CustomerID
- Gender
- Age
- Annual Income
- Spending Score

**Number of Records:** 200

**Number of Columns:** 5

---

# Technologies Used

- Python 3.x
- DuckDB
- Pandas
- Matplotlib
- PyArrow
- NumPy

---

# Required Libraries

Install the required libraries using:

```bash
pip install -r requirements.txt
```

or

```bash
pip install duckdb pandas matplotlib pyarrow numpy
```

---

# Project Structure

```
DuckDB-Task/
│
├── data/
│   └── Mall_Customers.csv
│
├── output/
│   ├── Mall_Customers_Clean.csv
│   ├── mall_customers.duckdb
│   ├── query_results.csv
│   └── query_results.parquet
│
├── images/
│   ├── gender_distribution.png
│   ├── age_distribution.png
│   ├── income_distribution.png
│   ├── spending_distribution.png
│   └── average_income_by_gender.png
│
├── duckdb_demo.py
├── requirements.txt
└── README.md
```

---

# Project Workflow

### Step 1
Create the project and virtual environment.

### Step 2
Install the required Python libraries.

### Step 3
Download and place the dataset in the `data` folder.

### Step 4
Load the dataset using Pandas.

### Step 5
Perform Exploratory Data Analysis (EDA).

### Step 6
Clean the dataset and save the cleaned CSV.

### Step 7
Create a DuckDB database.

### Step 8
Import the cleaned dataset into DuckDB.

### Step 9
Execute SQL queries.

### Step 10
Perform advanced SQL queries.

### Step 11
Export query results to CSV and Parquet.

### Step 12
Compare query performance between Pandas and DuckDB.

### Step 13
Generate data visualizations.

### Step 14
Summarize observations and conclusions.

### Step 15
Close the DuckDB database connection.

---

# SQL Operations Performed

The following SQL operations were executed:

- COUNT()
- AVG()
- MAX()
- MIN()
- WHERE
- ORDER BY
- GROUP BY
- LIMIT

Example queries include:

- Total number of customers
- Average age
- Average annual income
- Maximum and minimum spending score
- Customers older than 30
- Female customers
- Top spending customers
- Average spending score by gender
- Highest annual income
- Customers with annual income greater than 70

---

# Generated Output Files

## Output Folder

- Mall_Customers_Clean.csv
- mall_customers.duckdb
- query_results.csv
- query_results.parquet

## Images Folder

- gender_distribution.png
- age_distribution.png
- income_distribution.png
- spending_distribution.png
- average_income_by_gender.png

---

# Project Results

The project successfully:

- Loaded customer data into DuckDB.
- Executed SQL queries on the dataset.
- Exported query results to CSV and Parquet.
- Compared query execution time using Pandas and DuckDB.
- Generated visualizations for customer analysis.

---

# Advantages of DuckDB

- Lightweight analytical database
- Fast SQL query execution
- No separate database server required
- Works directly with CSV, Parquet, and Pandas DataFrames
- Excellent for data science and analytics
- Easy Python integration
- Efficient for large datasets

---

# Conclusion

DuckDB is a powerful embedded analytical database that enables fast SQL querying without requiring a dedicated database server.

In this project, customer data was loaded, cleaned, analyzed, queried using SQL, exported into multiple formats, and visualized. The comparison between Pandas and DuckDB demonstrates how DuckDB provides an efficient solution for analytical workloads, especially when working with larger datasets.

---

# Author

**Name:** Varsha C

**Task:** DuckDB Project

**Organization:** Open Data Intelligence Hub