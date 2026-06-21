# 🌍 Social Progress Analytics Engine

A professional-grade interactive analytics dashboard built with Streamlit that explores social progress, well-being, and country performance using World Happiness Report data.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![Plotly](https://img.shields.io/badge/Plotly-5.15+-purple.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📋 Overview

The Social Progress Analytics Engine provides comprehensive analysis of global happiness and well-being data from the World Happiness Report (2011–2025). It enables users to:

- **Explore Rankings**: View and compare country rankings by life evaluation scores
- **Compare Countries**: Side-by-side analysis of multiple countries across all metrics
- **Analyze Factors**: Understand how GDP, social support, health, freedom, generosity, and corruption contribute to happiness
- **Track Trends**: Visualize temporal changes in scores, ranks, and factor contributions
- **Deep Dive**: Generate detailed country profiles with historical analysis and narrative insights
- **Export Data**: Download filtered datasets and summary reports

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download the repository**:
   ```bash
   cd social-progress-analytics
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

5. Open your browser at `http://localhost:8501`

## 📁 Project Structure

```
social-progress-analytics/
├── README.md
├── .gitignore
├── requirements.txt
├── app.py
├── fix_keys.py
├── data/
│   └── WHR26_Data_Figure_2.1.xlsx
├── pages/
│   ├── 1_Home.py
│   ├── 2_Country_Rankings.py
│   ├── 3_Country_Comparison.py
│   ├── 4_Factor_Analysis.py
│   ├── 5_Time_Trends.py
│   ├── 6_Country_Profile.py
│   └── 7_Data_Table.py
├── utils/
│   ├── __init__.py
│   ├── charts.py
│   ├── config.py
│   └── data_loader.py
├── notebook/
│   └── Social_Progress_Analysis.ipynb
├── screenshots/
│   ├── home.png
│   ├── country_rankings.png
│   ├── country_comparison.png
│   ├── factor_analysis.png
│   ├── time_trends.png
│   ├── country_profile.png
│   └── data_table.png
└── docs/
    └── Project_Report.pdf
```

## 📊 Dashboard Pages

| Page | Description |
|------|-------------|
| **Home** | Overview with KPI cards, top countries, and navigation |
| **Country Rankings** | Interactive ranking explorer with bar charts and confidence intervals |
| **Country Comparison** | Multi-country comparison with radar charts and trend lines |
| **Factor Analysis** | Correlation analysis, factor importance, and distribution views |
| **Time Trends** | Year-over-year changes, top movers, and global trends |
| **Country Profile** | Deep-dive single country analysis with narrative insights |
| **Data Table** | Filterable, sortable, downloadable data browser |

## 🗂 Dataset

The application uses the **World Happiness Report 2026** dataset (`WHR26_Data_Figure_2.1.xlsx`) containing:

- **2,116 records** across **14 years** (2011–2025)
- **Metrics**: Life evaluation (Cantril ladder), confidence intervals, and 7 explanatory factors
- **Coverage**: 140+ countries ranked annually

### Key Columns

| Column | Description |
|--------|-------------|
| Life Evaluation | 3-year average Cantril ladder score (0-10) |
| Log GDP per capita | Economic contribution to happiness |
| Social support | Social network contribution |
| Healthy life expectancy | Health contribution |
| Freedom to make life choices | Freedom contribution |
| Generosity | Generosity contribution |
| Perceptions of corruption | Anti-corruption contribution |
| Dystopia + residual | Baseline + unexplained variance |

## ☁️ Deployment (Streamlit Cloud)

1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Set the main file path to `app.py`
5. Click **Deploy**

The app uses relative paths and is fully compatible with Streamlit Cloud.

## 🛠 Configuration

Key configuration options are in `utils/config.py`:

- **Color palette**: Customizable dark theme colors
- **Chart styling**: Plotly template and defaults
- **Factor mappings**: Short names to full column names
- **CSS theming**: Custom glassmorphism and gradient styles

## 📝 Assumptions

- The dataset follows the World Happiness Report format
- Missing values in factor columns are handled gracefully (filtered out for relevant analyses)
- Life evaluation column is auto-detected by searching for 'life evaluation' in column names
- Years without data (e.g., 2013) are handled seamlessly

## 📄 License

This project is for academic and portfolio use. The World Happiness Report data is publicly available.

---

Built with ❤️ using Streamlit, Plotly, and pandas.
