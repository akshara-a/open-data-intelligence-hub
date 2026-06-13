# 🌊 Marine Climate Intelligence Platform

A beginner-friendly Streamlit application for exploring, analysing, and reporting
on global marine climate data — built as **Project #30** using NOAA Ocean Data.

---

## 📁 Project Structure

```
marine_climate_platform/
├── app.py                  ← Main entry point
├── requirements.txt        ← Python dependencies
├── data/
│   ├── marine_climate_data.csv     ← Sample dataset (1 500 records)
│   └── generate_sample_data.py     ← Script to regenerate data
├── pages/
│   ├── dashboard.py        ← KPI cards, temperature & sea-level charts
│   ├── data_explorer.py    ← CSV upload, filtering, interactive charts
│   ├── ai_insights.py      ← AI-powered analysis via Claude API
│   ├── risk_analysis.py    ← Risk gauges, radar, regional breakdown
│   └── reports.py          ← Downloadable HTML & CSV reports
├── utils/
│   ├── helpers.py          ← Shared data-loading & chart helpers
│   └── styles.py           ← Global CSS & Plotly theme
└── assets/                 ← (place custom images here if needed)
```

---

## 🚀 Local Setup

### 1. Clone / download the project
```bash
cd marine_climate_platform
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate        # Mac / Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run app.py
```

Open your browser at **http://localhost:8501**

---

## 🤖 AI Insights – API Key Setup

The **AI Climate Insights** page calls the Anthropic Claude API.

### Local development
Create a `.streamlit/secrets.toml` file:
```toml
# .streamlit/secrets.toml
ANTHROPIC_API_KEY = "sk-ant-..."
```

Or set the environment variable:
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

> The current implementation sends API requests without an explicit key
> (the Anthropic SDK picks it up from `ANTHROPIC_API_KEY` in the environment).
> If deploying to Streamlit Cloud, add the key in the **Secrets** panel (see below).

---

## ☁️ Deployment — Streamlit Community Cloud

### Step 1 — Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit – Marine Climate Platform"
git remote add origin https://github.com/YOUR_USERNAME/marine-climate-platform.git
git push -u origin main
```

### Step 2 — Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io) and log in with GitHub.
2. Click **"New app"**.
3. Select your repository, branch (`main`), and set **Main file path** to `app.py`.
4. Click **"Deploy"**.

### Step 3 — Add Secrets (for AI Insights)
1. In your deployed app's dashboard, click the **⋮ menu → Settings → Secrets**.
2. Add:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-..."
   ```
3. Save. The app will automatically restart with the key available.

---

## 📊 Sample Dataset

The bundled `data/marine_climate_data.csv` contains **1 500 synthetic-but-realistic** records:

| Column | Description |
|--------|-------------|
| Date | Monthly records 2000–2024 |
| Region | 5 ocean regions |
| Sea_Surface_Temperature_C | °C |
| Sea_Level_Rise_mm | mm above 2000 baseline |
| Ocean_pH | 8.05–8.20 range |
| Coral_Bleaching_Risk | 0–100 index |
| Salinity_PSU | Practical Salinity Units |
| Dissolved_Oxygen_mgL | mg/L |
| Wave_Height_m | metres |
| Marine_Heat_Wave_Days | count per month |

Regenerate with:
```bash
cd data && python generate_sample_data.py
```

---

## 🌐 Real Data Sources

| Dataset | URL |
|---------|-----|
| NOAA Ocean Data | https://www.ncei.noaa.gov/ |
| Copernicus Marine | https://marine.copernicus.eu/ |
| ARGO Float Data | https://argo.ucsd.edu/ |
| NOAA ERDDAP | https://coastwatch.pfeg.noaa.gov/erddap/ |

---

## 🧰 Tech Stack

| Tool | Purpose |
|------|---------|
| Streamlit | Web app framework |
| Plotly | Interactive charts |
| Pandas | Data manipulation |
| NumPy | Numerical operations |
| Claude API | AI-powered climate insights |

---

## 📄 License
For educational and research use. Data generated synthetically for demonstration.
