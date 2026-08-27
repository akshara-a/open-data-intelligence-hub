# Apache Arrow Assignment Using Python

## Objective

Learn how to create, inspect, filter, convert, and save tabular data using **Apache Arrow and Python**.

## Technologies Used

* Python
* Pandas
* Apache Arrow (PyArrow)

## Installation

Install the required libraries using:

```bash
pip install pyarrow pandas
```

## Dataset

The assignment uses employee data with the following columns:

| Employee ID | Name  | Department | Salary | City      |
| ----------: | ----- | ---------- | -----: | --------- |
|           1 | Aisha | IT         |  60000 | Delhi     |
|           2 | Rahul | HR         |  50000 | Mumbai    |
|           3 | Priya | Finance    |  70000 | Chennai   |
|           4 | Arjun | IT         |  65000 | Bangalore |
|           5 | Sneha | Marketing  |  55000 | Hyderabad |

## Assignment Tasks

### 1. Create Employee Data

Employee records are created using a Pandas DataFrame.

### 2. Convert Pandas DataFrame to Arrow Table

The Pandas DataFrame is converted into an Apache Arrow Table using PyArrow.

### 3. Inspect Arrow Data

The Arrow table schema and contents are inspected to understand the structure and data types.

### 4. Filter Employee Records

Employee records are filtered based on conditions such as salary and department.

### 5. Convert Arrow Table Back to Pandas

The Arrow Table is converted back into a Pandas DataFrame.

### 6. Save Data Using Apache Arrow

The employee data is saved in an Arrow-compatible file format for later use.

## Project Structure

```text
Apache-Arrow-Assignment/
│
├── apache_arrow_assignment.py
├── employees.arrow
└── README.md
```

## How to Run

Clone the repository and navigate to the project directory:

```bash
cd Apache-Arrow-Assignment
```

Run the Python script:

```bash
python apache_arrow_assignment.py
```

The program will create and process the employee data using Pandas and Apache Arrow.

## Key Learning Outcomes

Through this assignment, the following concepts were practiced:

* Creating tabular data with Pandas
* Understanding Apache Arrow Tables
* Inspecting Arrow schemas
* Filtering tabular data
* Converting between Pandas and Arrow
* Saving and working with Arrow data
* Using PyArrow with Python

## Conclusion

This assignment demonstrates the basic use of **Apache Arrow with Python** for efficient tabular data processing and conversion between Pandas and Arrow formats.
