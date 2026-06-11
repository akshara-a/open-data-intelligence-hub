# 🔥 Most Active Repository Intelligence Engine

A data analysis project that identifies the most active and community-engaged 
GitHub repositories using real event data from GitHub Archive.

## 🌐 Live App
https://most-active-repository-intelligence-engine-ebs3kbhdsagthedctdc.streamlit.app

## 📌 Goal
Identify which GitHub repositories are receiving the most activity and 
community engagement by analyzing real-world GitHub event data.

## 📦 Dataset
- **Source:** [GitHub Archive](https://www.gharchive.org/)
- **File:** `2025-06-05-14.json.gz` — 1 hour of real GitHub events
- **Full Analysis:** 152,997 events across 70,880 repositories

## 🛠 Tech Stack
| Library | Purpose |
|---|---|
| Polars | Fast data loading and aggregation |
| Pandas | Data analysis and CSV export |
| NumPy | Score normalization and calculation |
| Matplotlib | Charts and visualizations |
| Streamlit | Interactive web app |

## 🧮 Scoring Formula
Each repository is scored using NumPy min-max normalization:

Score = 0.40 × Total Events
      + 0.30 × Unique Contributors
      + 0.20 × Stars (WatchEvents)
      + 0.10 × Forks

## 📊 App Features
- Dataset overview metrics
- Top-N repository leaderboard (interactive slider)
- Bar chart, pie chart, scatter plot, contributors chart
- Repository search
- Download results as CSV

## 📁 Files
| File | Description |
|---|---|
| `app.py` | Streamlit web app |
| `gharchive_small.json` | Sample dataset (5000 events) |
| `requirements.txt` | Python dependencies |
| `Most_Active_Repository_Intelligence_System.ipynb` | Full Colab analysis |

## ▶️ Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
