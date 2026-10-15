# Apache Arrow Data Processing Project


## Project Overview

This project demonstrates the usage of **Apache Arrow** for efficient
data processing and columnar data storage.

The project converts a Pandas DataFrame into an Apache Arrow Table,
stores the data in Arrow format, and compares it with CSV format
in terms of storage size and performance.


---

## Dataset Used

Dataset Name:

**Mall Customers Dataset**

Dataset contains customer information:

- Customer ID
- Gender
- Age
- Annual Income
- Spending Score


Dataset Size:

- Rows: 200
- Columns: 5


---

## Technologies Used

- Python
- Pandas
- Apache Arrow (PyArrow)
- Matplotlib
- NumPy


---

## Project Workflow


### Step 1: Environment Setup

Created Python virtual environment and installed required libraries.


### Step 2: Dataset Loading

Loaded Mall Customers CSV dataset using Pandas.


### Step 3: Exploratory Data Analysis

Performed:

- Dataset information
- Missing value checking
- Duplicate checking
- Statistical analysis


### Step 4: Data Cleaning

Performed:

- Missing value handling
- Duplicate removal
- Column name standardization


### Step 5: Apache Arrow Conversion

Converted Pandas DataFrame into Apache Arrow Table.


### Step 6: Arrow File Creation

Saved the dataset as:


### Step 7: Performance Comparison

Compared:

- CSV vs Arrow file size
- CSV vs Arrow read performance
- CSV vs Arrow write performance


### Step 8: Data Visualization

Created visualizations:

- Gender distribution
- Age distribution
- Income distribution
- Spending score distribution
- Average income by gender



---

## Project Structure

