# Apache Parquet Task

## Project Overview

This project demonstrates the use of **Apache Parquet**, a columnar storage file format designed for efficient data storage and faster analytical processing. The project compares the performance of **CSV** and **Apache Parquet** formats using the **Mall Customers Dataset**.

The project includes:

- Loading a CSV dataset
- Exploratory Data Analysis (EDA)
- Data Cleaning
- Converting CSV to Apache Parquet
- Comparing file sizes
- Comparing read performance
- Comparing write performance
- Visualizing the results
- Drawing observations and conclusions

---

# Project Structure

```
Apache-Parquet-Task/
│
├── data/
│   └── Mall_Customers.csv
│
├── output/
│   ├── Mall_Customers_Clean.csv
│   ├── Mall_Customers.parquet
│   ├── Mall_Customers_Write.csv
│   └── Mall_Customers_Write.parquet
│
├── images/
│   ├── file_size_comparison.png
│   ├── read_time_comparison.png
│   └── write_time_comparison.png
│
├── parquet_demo.py
├── requirements.txt
└── README.md
```

---

# Dataset

**Dataset Name:** Mall Customers Dataset

The dataset contains customer information including:

- CustomerID
- Gender
- Age
- Annual Income
- Spending Score

Number of Records: **200**

Number of Columns: **5**

---

# Technologies Used

- Python 3.x
- Pandas
- PyArrow
- Fastparquet
- Matplotlib

---

# Python Libraries

Install the required libraries using:

```bash
pip install pandas pyarrow fastparquet matplotlib
```

---

# Project Workflow

## Step 1

Create a Python virtual environment.

## Step 2

Install required libraries.

## Step 3

Download the Mall Customers dataset.

## Step 4

Load the dataset using Pandas.

## Step 5

Perform Exploratory Data Analysis (EDA).

## Step 6

Clean the dataset.

## Step 7

Convert the cleaned CSV file into Apache Parquet format.

## Step 8

Read the Parquet file and verify the data.

## Step 9

Compare CSV and Parquet file sizes.

## Step 10

Compare CSV and Parquet read performance.

## Step 11

Compare CSV and Parquet write performance.

## Step 12

Generate visualization charts.

## Step 13

Write observations and conclusions.

---

# Results

The project compares the following:

- CSV File Size
- Parquet File Size
- CSV Read Time
- Parquet Read Time
- CSV Write Time
- Parquet Write Time

Three comparison charts are generated:

- File Size Comparison
- Read Time Comparison
- Write Time Comparison

---

# Sample Output

Example:

```
CSV File Size       : 3.89 KB

Parquet File Size   : 5.68 KB

CSV Read Time       : 0.017663 seconds

Parquet Read Time   : 0.016203 seconds

CSV Write Time      : 0.003719 seconds

Parquet Write Time  : 0.013857 seconds
```

> **Note:** Because the Mall Customers dataset contains only **200 records**, the Parquet file may be larger than the CSV file due to metadata overhead. Apache Parquet is most beneficial for large datasets.

---

# Advantages of Apache Parquet

- Efficient columnar storage
- Better compression for large datasets
- Faster read performance
- Reduced storage requirements
- Optimized for analytics
- Supports Hadoop, Spark, Hive and cloud data platforms

---

# Conclusion

Apache Parquet is a powerful columnar storage format that improves analytical query performance and storage efficiency for large datasets.

In this project, the Mall Customers dataset was converted from CSV to Parquet, and both formats were compared in terms of file size and read/write performance. Since the dataset is very small, CSV performed better in some cases. However, Apache Parquet becomes significantly more efficient when working with large-scale data.

---

# Author

**Name:** Varsha C

Apache Parquet Task