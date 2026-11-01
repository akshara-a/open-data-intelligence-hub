# Task 4 - Data Analysis using Pandas

## 📌 Project Overview

This project demonstrates basic data analysis using Python and the Pandas library. The objective is to perform data loading, cleaning, exploratory data analysis (EDA), visualization, and insight generation on a student performance dataset.

---

## 🎯 Objective

* Load and analyze a dataset using Pandas.
* Perform data cleaning and preprocessing.
* Generate descriptive statistics.
* Create visualizations using Matplotlib.
* Extract meaningful insights from the data.

---

## 📂 Project Structure

```text
Task-4-Data-Analysis-using-Pandas/
│
├── data/
│   └── student_data.csv
│
├── notebook/
│   └── analysis.ipynb
│
├── output/
│   ├── cleaned_data.csv
│   ├── summary_statistics.csv
│   └── charts/
│       ├── gender_chart.png
│       ├── department_chart.png
│       ├── department_pie_chart.png
│       └── marks_histogram.png
│
├── src/
│   └── analysis.py
│
├── README.md
├── requirements.txt
└── insights.md
```

---

## 🛠️ Technologies Used

* Python
* Pandas
* Matplotlib
* Jupyter Notebook
* VS Code

---

## 📊 Dataset Description

The dataset contains information about student performance, including:

| Column     | Description               |
| ---------- | ------------------------- |
| Student_ID | Unique student identifier |
| Name       | Student name              |
| Gender     | Male/Female               |
| Department | Academic department       |
| Marks      | Student marks             |
| Attendance | Attendance percentage     |

---

## 🔍 Analysis Performed

The following analyses were conducted:

* Data loading and inspection
* Checking dataset dimensions and structure
* Identifying missing values
* Removing duplicate records
* Generating summary statistics
* Calculating average marks by department
* Analyzing gender distribution
* Identifying highest and lowest scorers
* Computing average attendance
* Comparing performance by gender

---

## 📈 Visualizations Generated

The project includes the following visualizations:

* Gender Distribution Bar Chart
* Department Distribution Bar Chart
* Department Percentage Pie Chart
* Marks Distribution Histogram

---

## 💡 Key Insights

* The CSE department has the highest number of students.
* Female students perform slightly better on average.
* Students with higher attendance generally achieve higher marks.
* The dataset contains minimal data quality issues.
* Average attendance among students is high.

---

## ▶️ How to Run the Project

1. Clone the repository:

```bash
git clone <repository-url>
```

2. Navigate to the project directory:

```bash
cd Task-4-Data-Analysis-using-Pandas
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Run the Python script:

```bash
python src/analysis.py
```

Or open and run:

```text
notebook/analysis.ipynb
```

---

## 📁 Output Files

After execution, the following files are generated:

* `cleaned_data.csv`
* `summary_statistics.csv`
* `gender_chart.png`
* `department_chart.png`
* `department_pie_chart.png`
* `marks_histogram.png`

---

## ✅ Conclusion

This project successfully demonstrates the use of Python Pandas for data analysis, cleaning, visualization, and insight generation. It provides a basic yet effective workflow for exploratory data analysis on structured datasets.
