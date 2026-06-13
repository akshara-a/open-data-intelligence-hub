import streamlit as st
import polars as pl
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

st.set_page_config(page_title="Seismic Risk Engine", page_icon="🌋", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    background-color: #1e0a2e !important;
    color: #f5e6ff !important;
    font-family: 'Poppins', sans-serif !important;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem !important; }

h1, h2, h3, h4 { color: #ff85a1 !important; }

.card {
    background: #2d0f42;
    border: 1px solid #ff85a1;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    text-align: center;
}
.card-label {
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #d48faa;
    margin-bottom: 0.3rem;
}
.card-value {
    font-size: 2rem;
    font-weight: 600;
    color: #ff85a1;
}
.card-unit { font-size: 0.8rem; color: #d48faa; }

[data-testid="stSidebar"] {
    background-color: #160720 !important;
    border-right: 1px solid #ff85a1 !important;
}

div[data-testid="stExpander"] {
    background: #2d0f42 !important;
    border: 1px solid #ff85a1 !important;
    border-radius: 12px !important;
}

hr { border-color: #4a1a5e !important; }

.stDownloadButton > button {
    background-color: #ff85a1 !important;
    color: #1e0a2e !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 0.5rem 1.5rem !important;
}
.stDownloadButton > button:hover {
    background-color: #ff4d79 !important;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pl.read_csv("earthquake.csv", infer_schema_length=10000, ignore_errors=True)
    df = df.drop_nulls(subset=["latitude", "longitude", "mag"])
    df = df.filter(pl.col("mag") > 0)
    return df

df = load_data()

st.markdown("## 🌋 Seismic Risk Engine")
st.markdown("<p style='color:#d48faa; margin-top:-1rem;'>Identifying earthquake-prone regions from historical seismic data</p>", unsafe_allow_html=True)
st.markdown("---")

with st.expander("📋 About This Project", expanded=True):
    col_a, col_b = st.columns(2, gap="large")
    with col_a:
        st.markdown("""
        #### 🎯 Purpose
        The Seismic Risk Engine analyzes historical earthquake data
        and identifies which regions of the world are most vulnerable
        to seismic activity. By combining earthquake frequency and
        magnitude, the engine computes a **risk score** for each zone.

        #### 📌 Objectives
        - Identify earthquake-prone regions using historical USGS data
        - Calculate a seismic risk score based on frequency and magnitude
        - Visualize high-risk zones on an interactive global heatmap
        - Provide actionable insights from the seismic dataset
        - Allow filtering by magnitude and depth for deeper analysis
        """)
    with col_b:
        st.markdown("""
        #### 🗃️ Data Source
        - **Provider:** United States Geological Survey (USGS)
        - **Format:** CSV with 22 columns
        - **Records:** 1,369 earthquake events
        - **Time Range:** May 2023 — June 2026
        - **Min Magnitude:** 5.5 Mw (significant earthquakes only)
        - **Key Fields:** Latitude, Longitude, Magnitude, Depth, Place, Time

        #### 🔬 Analysis Method
        - Data processed using **Polars** DataFrame engine
        - Coordinates rounded to 1° grid for regional grouping
        - Risk Score = **Frequency × Average Magnitude** per region
        - Heatmap rendered using **Folium** with pink gradient
        - Charts built with **Matplotlib**
        """)

st.markdown("---")

with st.sidebar:
    st.markdown("### ⚙️ Filters")
    mag_min = float(df["mag"].min())
    mag_max = float(df["mag"].max())
    min_mag, max_mag = st.slider("Magnitude Range", mag_min, mag_max, (5.5, mag_max))
    depth_max = st.slider("Max Depth (km)", 0, int(df["depth"].max()), int(df["depth"].max()))
    map_style = st.selectbox("Map Style", ["CartoDB dark_matter", "CartoDB positron", "OpenStreetMap"])

df_filtered = df.filter(
    (pl.col("mag") >= min_mag) &
    (pl.col("mag") <= max_mag) &
    (pl.col("depth") <= depth_max)
)

df_risk = df_filtered.with_columns([
    pl.col("latitude").round(1).alias("lat_bin"),
    pl.col("longitude").round(1).alias("lon_bin")
])

risk = df_risk.group_by(["lat_bin", "lon_bin"]).agg([
    pl.len().alias("frequency"),
    pl.col("mag").mean().alias("avg_mag")
])

risk = risk.with_columns(
    (pl.col("frequency") * pl.col("avg_mag")).alias("risk_score")
)

total = len(df_filtered)
avg_mag_val = round(float(df_filtered["mag"].mean()), 2)
max_mag_val = round(float(df_filtered["mag"].max()), 2)
avg_dep = round(float(df_filtered["depth"].mean()), 1)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="card"><div class="card-label">Total Events</div><div class="card-value">{total:,}</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="card"><div class="card-label">Avg Magnitude</div><div class="card-value">{avg_mag_val}<span class="card-unit"> Mw</span></div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="card"><div class="card-label">Max Magnitude</div><div class="card-value">{max_mag_val}<span class="card-unit"> Mw</span></div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="card"><div class="card-label">Avg Depth</div><div class="card-value">{avg_dep}<span class="card-unit"> km</span></div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 🗺️ Seismic Risk Heatmap")

m = folium.Map(location=[20, 0], zoom_start=2, tiles=map_style)
heat_data = list(zip(
    risk["lat_bin"].to_list(),
    risk["lon_bin"].to_list(),
    risk["risk_score"].to_list()
))
HeatMap(heat_data, radius=15, blur=10,
    gradient={0.3: '#ffb6c1', 0.6: '#ff69b4', 0.8: '#ff1493', 1.0: '#c2185b'}
).add_to(m)
st_folium(m, width=None, height=480, returned_objects=[])

st.markdown("<br>", unsafe_allow_html=True)
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("### 📊 Magnitude Distribution")
    fig, ax = plt.subplots(figsize=(6, 3.5))
    fig.patch.set_facecolor("#2d0f42")
    ax.set_facecolor("#1e0a2e")
    ax.hist(df_filtered["mag"].to_list(), bins=25, color="#ff85a1", edgecolor="#1e0a2e", alpha=0.85)
    ax.set_xlabel("Magnitude", color="#d48faa", fontsize=9)
    ax.set_ylabel("Count", color="#d48faa", fontsize=9)
    ax.tick_params(colors="#d48faa", labelsize=8)
    for spine in ax.spines.values():
        spine.set_edgecolor("#4a1a5e")
    fig.tight_layout()
    st.pyplot(fig)

with col2:
    st.markdown("### 🏆 Top 10 High-Risk Regions")
    top_risk = risk.sort("risk_score", descending=True).head(10).to_pandas()
    top_risk["Region"] = top_risk["lat_bin"].astype(str) + "°,  " + top_risk["lon_bin"].astype(str) + "°"
    top_risk = top_risk[["Region", "frequency", "avg_mag", "risk_score"]].rename(columns={
        "frequency": "Events",
        "avg_mag": "Avg Mag",
        "risk_score": "Risk Score"
    })
    top_risk["Risk Score"] = top_risk["Risk Score"].round(1)
    top_risk["Avg Mag"] = top_risk["Avg Mag"].round(2)
    st.dataframe(top_risk, use_container_width=True, hide_index=True)

with st.expander("🔍 View Raw Data"):
    st.dataframe(df_filtered.to_pandas(), use_container_width=True, height=300)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 💡 Insights")

top1 = risk.sort("risk_score", descending=True).head(1)
top1_region = f"{top1['lat_bin'][0]}°, {top1['lon_bin'][0]}°"
top1_score = round(float(top1['risk_score'][0]), 1)
top1_freq = int(top1['frequency'][0])

high_risk_count = len(risk.filter(pl.col("risk_score") > risk["risk_score"].mean()))
deep_quakes = len(df_filtered.filter(pl.col("depth") > 300))
shallow_quakes = len(df_filtered.filter(pl.col("depth") <= 70))
major_quakes = len(df_filtered.filter(pl.col("mag") >= 7.0))

st.markdown(f"""
<ul style="line-height: 2.2; font-size: 0.95rem; color: #f5e6ff;">
    <li>🔺 <b>Highest risk region</b> is at <b>{top1_region}</b> with a risk score of <b>{top1_score}</b></li>
    <li>📍 <b>{top1_freq} earthquakes</b> recorded in the highest risk zone</li>
    <li>⚠️ <b>{high_risk_count} regions</b> are above average risk level</li>
    <li>🌊 <b>{shallow_quakes} shallow earthquakes</b> (depth ≤ 70 km) — most dangerous to surface</li>
    <li>🪨 <b>{deep_quakes} deep earthquakes</b> (depth > 300 km) recorded</li>
    <li>💥 <b>{major_quakes} major earthquakes</b> with magnitude ≥ 7.0 in this dataset</li>
    <li>📈 Total of <b>{total:,} seismic events</b> analyzed after applying filters</li>
</ul>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 💾 Download Dataset")
csv_data = df_filtered.to_pandas().to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Download Filtered CSV",
    data=csv_data,
    file_name="filtered_earthquake_data.csv",
    mime="text/csv"
)