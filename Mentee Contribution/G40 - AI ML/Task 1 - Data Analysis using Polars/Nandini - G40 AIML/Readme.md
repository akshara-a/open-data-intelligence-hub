# 🌋 Seismic Risk Engine — Data Analysis using Polars

**Nandini:** G40 AI ML
**Task:** Task 1 — Data Analysis using Polars

---

## 📌 Project Overview

The **Seismic Risk Engine** is an interactive data analysis web application that processes historical earthquake data to identify the most seismically vulnerable regions across the globe.

It combines earthquake **frequency** and **average magnitude** to compute a **risk score** per geographic zone, and visualizes results on an interactive heatmap.

---

## 🎯 Objectives

- Identify earthquake-prone regions using historical USGS seismic data
- Calculate a seismic risk score based on frequency × average magnitude
- Visualize high-risk zones on an interactive global heatmap
- Allow dynamic filtering by magnitude and depth
- Provide auto-generated insights from the dataset

---

## 🗃️ Dataset

| Field | Details |
|---|---|
| **Source** | United States Geological Survey (USGS) |
| **File** | `earthquake.csv` |
| **Records** | 1,369 earthquake events |
| **Time Range** | May 2023 — June 2026 |
| **Min Magnitude** | 5.5 Mw (significant earthquakes only) |
| **Key Columns** | `latitude`, `longitude`, `mag`, `depth`, `place`, `time` |

---

## 🔬 Analysis Method

- Data loaded and processed using **Polars** DataFrame engine
- Coordinates rounded to a **1° grid** for regional grouping
- **Risk Score = Frequency × Average Magnitude** per region
- Heatmap rendered using **Folium** with a custom pink gradient
- Charts built with **Matplotlib**

---

## 🖥️ App Features

| Feature | Description |
|---|---|
| 📊 Magnitude Distribution | Histogram of earthquake magnitudes |
| 🗺️ Seismic Risk Heatmap | Interactive global heatmap of risk zones |
| 🏆 Top 10 High-Risk Regions | Table ranked by risk score |
| 💡 Auto Insights | Dynamic text insights from filtered data |
| ⚙️ Sidebar Filters | Filter by magnitude range, max depth, map style |
| 💾 Download | Export filtered dataset as CSV |

---

## 📁 Files

```
📂 Your Folder - G40 AI ML/
├── app.py               # Main Streamlit application
├── earthquake.csv       # USGS earthquake dataset
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

---

## ▶️ How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the app
```bash
streamlit run app.py
```

### 3. Open in browser
```
https://seismicriskanalysis.streamlit.app/
```

---

## 🛠️ Tech Stack

| Library | Purpose |
|---|---|
| `polars` | Fast DataFrame processing |
| `streamlit` | Web app framework |
| `folium` | Interactive map rendering |
| `streamlit-folium` | Embed Folium maps in Streamlit |
| `matplotlib` | Charts and plots |
| `pandas` | Data export compatibility |

---

## 📊 Sample Insights

- Regions along the **Pacific Ring of Fire** consistently show the highest risk scores
- The majority of events are **shallow earthquakes** (depth ≤ 70 km), which are most dangerous to the surface
- **Major earthquakes** (Magnitude ≥ 7.0) represent a small but critical subset of the dataset
