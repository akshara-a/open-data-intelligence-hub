# Student Performance Analysis

This mini project demonstrates student performance analysis using a sample dataset with columns:
- Student ID
- Name
- Gender
- Attendance
- Math
- Science
- English
- GPA
- Semester

## Analysis included
- Top students by GPA and total marks
- Attendance vs marks comparison
- Subject-wise average scores
- Grade distribution across the class

## Setup
1. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```

2. Confirm the data file exists:
   ```bash
   dir data\student_performance.csv
   ```

3. Run the analysis script:
   ```bash
   python analysis.py
   ```

4. Review the output in the console and the generated charts in the `output/` directory.

5. Start the Streamlit dashboard:
   ```bash
   streamlit run dashboard.py
   ```

6. Open the URL shown by Streamlit in your browser (usually `http://localhost:8501`).

7. If you need to stop the dashboard, press `Ctrl+C` in the terminal where Streamlit is running.

8. Optional: regenerate the dataset if needed:
   ```bash
   python generate_dataset.py
   ```

9. Optional: open the notebook for step-by-step EDA:
   - Launch Jupyter Notebook or JupyterLab
   - Open `eda_student_performance.ipynb`

## Using a Kaggle dataset
You can replace the sample dataset at `data/student_performance.csv` with a public Kaggle dataset. The script expects columns matching the project schema above. If you use another dataset, adjust the column names in `analysis.py` accordingly.

## Mini Project Extension: Interactive Dashboard

Build an interactive web dashboard using **Streamlit** to explore student performance data visually:

### Features
1. **Dataset Overview** - Total students, average GPA, attendance, and semester count
2. **Data Quality Summary** - Before/after cleaning metrics with data transformation details
3. **Interactive Filters** - Filter by semester, gender, and GPA range with real-time updates
4. **Top Students** - Display top 10 performers with their scores and GPA
5. **Trend Analysis** - GPA distributions, attendance by gender, and semester trends
6. **Correlation Heatmap** - Visualize relationships between attendance, marks, and GPA
7. **Key Insights** - Statistical summaries and performance patterns

### Running the Dashboard
```bash
streamlit run dashboard.py
```

The dashboard automatically:
- Loads and cleans the data on startup
- Caches cleaned data for performance
- Provides responsive charts and metrics
- Supports multi-select filtering with instant updates

### Learning Outcomes
This extension teaches:
- Web app development with Streamlit
- Interactive filtering and user input handling
- Data visualization with Plotly and Matplotlib
- Caching strategies for performance optimization
- Building professional dashboards for stakeholders

## Files
- `data/student_performance.csv` - sample student dataset with some missing, duplicate, and messy values for cleaning practice
- `analysis.py` - analysis script producing console results and plots
- `dashboard.py` - interactive Streamlit dashboard for data exploration
- `eda_student_performance.ipynb` - interactive exploratory data analysis notebook for cleaning, visualization, and reporting
- `generate_dataset.py` - script to regenerate or extend the student dataset
- `requirements.txt` - Python dependencies
