# 🌍 Economic Development Analytics

A data analytics project built on **World Bank WDI data** that analyses economic development across 9 countries from 2000–2024 using only Python, NumPy, Polars, and Matplotlib.

---

## 📁 Project Structure

```
Economic_Development_Analytics/
│
├── WDI_data.csv                                            # World Bank WDI raw data (your download)
├── Economic_Development_Analytics_Polars_Notebook.ipynb    # Main notebook (Polars only)
├── dashboard.py                                            # Streamlit interactive dashboard
├── economic_dashboard.png                                  # Auto-saved summary dashboard image
└── GUIDE_ME.md
```

---

## 📊 Dataset

**Source:** [World Bank DataBank — World Development Indicators](https://databank.worldbank.org/source/world-development-indicators)

**Countries (9):**

| Country | Code | Income Group |
|---|---|---|
| India | IND | Lower-Middle |
| China | CHN | Upper-Middle |
| United States | USA | High |
| Brazil | BRA | Upper-Middle |
| Nigeria | NGA | Lower-Middle |
| Germany | DEU | High |
| Bangladesh | BGD | Lower-Middle |
| Ethiopia | ETH | Low |
| World (aggregate) | WLD | — |

**Indicators (12):**

| Indicator | Code | Theme |
|---|---|---|
| GDP (current US$) | NY.GDP.MKTP.CD | Economy |
| GDP growth (annual %) | NY.GDP.MKTP.KD.ZG | Economy |
| GDP per capita (current US$) | NY.GDP.PCAP.CD | Economy |
| Inflation, consumer prices (annual %) | FP.CPI.TOTL.ZG | Economy |
| Poverty headcount at $3.00/day (2021 PPP) | SI.POV.DDAY | Poverty |
| Gini index | SI.POV.GINI | Poverty |
| Population, total | SP.POP.TOTL | Demographics |
| Life expectancy at birth (years) | SP.DYN.LE00.IN | Human Development |
| School enrollment, primary (% gross) | SE.PRM.ENRR | Human Development |
| Unemployment (% of labor force) | SL.UEM.TOTL.ZS | Labor |
| Exports of goods & services (% of GDP) | NE.EXP.GNFS.ZS | Trade |
| Access to electricity (% of population) | EG.ELC.ACCS.ZS | Infrastructure |

---

## 🛠 Tech Stack

```
Python 3.13
Polars   — all data loading, cleaning, filtering, joining, aggregation
NumPy    — statistical computations (correlation, z-score, normalization, rolling avg)
Matplotlib — all visualizations
Streamlit  — interactive dashboard (dashboard.py only)
```



## 🚀 Getting Started

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Download the data

1. Go to [databank.worldbank.org](https://databank.worldbank.org/source/world-development-indicators)
2. Select **World Development Indicators**
3. Pick the 9 countries and 12 indicators listed above
4. Set time range: **2000 → 2024**
5. Download as **CSV** → extract the zip → rename the data file to `WDI_data.csv`
6. Place `WDI_data.csv` in the same folder as the notebook

### 3. Run the notebook

```bash
jupyter notebook Economic_Development_Analytics_Polars_Notebook.ipynb
```

Run cells top to bottom — each cell depends on the one above it.

### 4. Run the Streamlit dashboard

```bash
streamlit run dashboard.py
```

Then open `http://localhost:8501` and upload `WDI_data.csv` from the sidebar.

---


## 📈 Analyses & Key Findings

**GDP Growth Trends**
China and Ethiopia led all countries in average growth. COVID-19 (2020) caused a simultaneous contraction across all 8 countries — the only globally synchronized event in the dataset.

**Poverty vs GDP per Capita**
Pearson r ≈ −0.70 — strong negative correlation confirming higher income = lower poverty. Regression computed from scratch using NumPy (no sklearn).

**HDI Proxy Score**
Composite of Life Expectancy + School Enrollment + log(GDP per Capita), normalized to [0–1]. USA and Germany ranked highest; Ethiopia lowest but with the steepest upward trend.

**Inflation Outlier Detection**
Z-score flagged economic shocks (|z| > 2). Ethiopia 2008 (44.36%) was the most extreme — over 5 standard deviations above the global mean.

**Polars Benchmark**
LazyFrame consistently outperformed Eager API through query plan optimization (predicate pushdown, projection pushdown, constant folding).


## 📚 References

1. World Bank Group. (2024). *World Development Indicators*. [databank.worldbank.org](https://databank.worldbank.org)
