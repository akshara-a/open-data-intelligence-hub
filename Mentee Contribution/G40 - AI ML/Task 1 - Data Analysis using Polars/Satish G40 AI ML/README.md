# Species Distribution Pattern Analysis Using SCAR Antarctic Biodiversity Dataset

A mini data science and GIS project that analyzes how species are distributed across Antarctica and identifies biodiversity hotspots using the SCAR (Scientific Committee on Antarctic Research) Antarctic Biodiversity Database.

## Dataset

**Source:** [The Biodiversity of Ice-free Antarctica Database](https://ipt.biodiversity.aq/resource?r=aas_4296_biodiversity_icefree_antarctica_db) — SCAR Antarctic Biodiversity Portal

**File:** `occurrence.csv` (~35,600 records)

| Column | Description |
|--------|-------------|
| scientificName | Full scientific name |
| decimalLatitude | Latitude (WGS84) |
| decimalLongitude | Longitude (WGS84) |
| eventDate | Observation date |
| kingdom, phylum, class, order, family, genus, species | Taxonomic hierarchy |

## Project Structure

```
species/
├── occurrence.csv          # Raw dataset
├── analyze.py              # Main analysis pipeline
├── app.py                  # Streamlit dashboard
├── requirements.txt
├── README.md
├── reports/
│   └── project_report.md   # 5–10 page project report
├── src/
│   ├── data_cleaning.py    # Data cleaning
│   ├── eda.py              # Exploratory analysis
│   ├── mapping.py          # Folium occurrence maps
│   ├── richness.py         # Grid-based richness
│   ├── richness_map.py     # Interactive richness map
│   ├── hotspot.py          # DBSCAN hotspot detection
│   └── visualizations.py   # Static charts
└── outputs/                # Generated after running analyze.py
    ├── cleaned_occurrence.csv
    ├── analysis_summary.json
    ├── figures/
    └── maps/
```

## Setup

```bash
# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Run full analysis pipeline

```bash
python analyze.py
```

This will:
1. Clean the data (deduplicate, handle missing coordinates, parse dates)
2. Run exploratory data analysis
3. Generate static visualizations (bar chart, yearly trend, richness heatmap, scatter map)
4. Create interactive Folium maps (occurrence, richness, hotspots)
5. Apply DBSCAN clustering for hotspot detection
6. Save all outputs to `outputs/`

### Launch Streamlit dashboard

```bash
streamlit run app.py
```

**Performance tips:** Run `python analyze.py` first to create `outputs/cleaned_occurrence.csv` (faster startup). Map and clustering results are cached in the dashboard — revisiting a page or reusing the same slider values is near-instant.

**Dashboard pages:**
- **Overview** — Key metrics, top species, yearly trends
- **Species Map** — Interactive occurrence map with clustering
- **Richness Analysis** — Grid-based species richness heatmap
- **Hotspot Detection** — DBSCAN clusters and biodiversity hotspots

## Methods Summary

| Task | Method |
|------|--------|
| Data cleaning | Deduplication, coordinate validation, datetime parsing |
| Distribution mapping | Folium with marker clustering |
| Species richness | Geographic grid cells (1° lat × 2° lon default) |
| Hotspot detection | DBSCAN on scaled lat/lon coordinates |
| Visualizations | Matplotlib, Seaborn, Plotly |

## Key Outputs

- `outputs/figures/top_species_bar_chart.png`
- `outputs/figures/yearly_trend_chart.png`
- `outputs/figures/richness_heatmap.png`
- `outputs/figures/occurrence_scatter_map.png`
- `outputs/maps/occurrence_map.html`
- `outputs/maps/richness_map.html`
- `outputs/maps/hotspot_map.html`

## License

Dataset: CC-BY 4.0 (SCAR Data Policy). See [SCAR Antarctic Biodiversity Portal](https://www.biodiversity.aq/) for citation requirements.

## Author

Data Science & GIS Analysis Mini Project — 2026  
BY Satish G40 AIML
