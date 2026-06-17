# Global Happiness Analytics Platform - Project Guidelines

## Project Overview

The Global Happiness Analytics Platform is a data analytics and machine learning project developed using the World Happiness Report dataset. The project provides insights into global happiness trends, country-wise comparisons, factor analysis, and happiness score prediction through an interactive Streamlit dashboard.

---

## Objective

The primary objective of this project is to:

* Analyze global happiness indicators.
* Identify factors influencing happiness.
* Compare countries based on happiness scores.
* Visualize trends and patterns using interactive charts.
* Predict happiness scores using Machine Learning.

---

## Dataset Information

### Dataset Source

World Happiness Report Data Portal

https://data.worldhappiness.report/map

### Dataset Used

WHR26_Data_Figure_2.1.xlsx

### Important Features

* Year
* Rank
* Country name
* Life evaluation (3-year average)
* Explained by: Log GDP per capita
* Explained by: Social support
* Explained by: Healthy life expectancy
* Explained by: Freedom to make life choices
* Explained by: Generosity
* Explained by: Perceptions of corruption
* Dystopia + residual

---

## Project Structure

```text
Global-Happiness-Analytics/
│
├── app.py
├── README.md
├── GUIDELINES.md
├── requirements.txt
│
├── data/
│   └── WHR26_Data_Figure_2.1.xlsx
│
├── models/
│   └── happiness_model.pkl
│
├── notebooks/
│   └── EDA.ipynb
│
└── src/
    └── model.py
```

---

## Exploratory Data Analysis (EDA)

The EDA phase includes:

1. Dataset loading
2. Dataset inspection
3. Missing value analysis
4. Statistical summary
5. Top 10 happiest countries
6. Bottom 10 happiest countries
7. Distribution analysis
8. Correlation analysis
9. Feature relationship analysis
10. Happiness trend visualization

---

## Machine Learning Pipeline

### Problem Type

Regression

### Target Variable

Life evaluation (3-year average)

### Input Features

* Explained by: Log GDP per capita
* Explained by: Social support
* Explained by: Healthy life expectancy
* Explained by: Freedom to make life choices
* Explained by: Generosity
* Explained by: Perceptions of corruption
* Dystopia + residual

### Model Used

Random Forest Regressor

### Data Split

* Training Data: 80%
* Testing Data: 20%

### Evaluation Metrics

* Mean Absolute Error (MAE)
* Root Mean Squared Error (RMSE)
* R² Score

### Final Performance

* MAE: 0.168
* RMSE: 0.222
* R² Score: 0.950

---

## Dashboard Features

### Dashboard Analytics

Displays:

* Total Countries
* Average Happiness Score
* Happiest Country
* Least Happy Country

### Country Comparison

Allows users to compare:

* Happiness Score
* GDP Contribution
* Social Support
* Life Expectancy
* Freedom
* Generosity
* Corruption

### Trend Analysis

Provides:

* Global Happiness Trends
* Top Performing Countries
* Lowest Performing Countries

### Happiness Prediction

Users can provide:

* GDP Contribution
* Social Support
* Life Expectancy
* Freedom
* Generosity
* Corruption
* Dystopia + Residual

The model predicts the expected happiness score.

---

## Happiness Score Interpretation

| Score Range | Interpretation        |
| ----------- | --------------------- |
| 0 – 3       | Very Low Happiness    |
| 3 – 5       | Low Happiness         |
| 5 – 6       | Moderate Happiness    |
| 6 – 7       | High Happiness        |
| 7 – 8       | Very High Happiness   |
| Above 8     | Exceptional Happiness |

---

## Technologies Used

### Programming Language

* Python

### Libraries

* Pandas
* NumPy
* Matplotlib
* Seaborn
* Plotly
* Scikit-Learn
* Joblib
* OpenPyXL
* Streamlit

### Development Tools

* VS Code
* Git
* GitHub
* Streamlit Cloud

---

## Deployment

The application is deployed using Streamlit Community Cloud.

Deployment URL:

https://global-happiness-analytics-kkwudzcjizeg7vao4xnrxc.streamlit.app/

---

## Future Enhancements

* Advanced forecasting models
* Regional happiness analytics
* AI-generated insights
* Automated report generation
* Downloadable dashboards

---

## Conclusion

The Global Happiness Analytics Platform successfully combines data analytics, visualization, and machine learning to provide meaningful insights into global happiness trends. The project demonstrates practical applications of data science concepts including EDA, predictive modeling, and dashboard development.
