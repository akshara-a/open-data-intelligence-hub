"""
Streamlit Dashboard: Species Distribution Pattern Analysis
SCAR Antarctic Biodiversity Dataset
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components

from src.data_cleaning import clean_occurrence_data, load_raw_data
from src.eda import observations_by_year, top_species, total_records, total_unique_species
from src.hotspot import create_hotspot_map, detect_hotspots, summarize_hotspots
from src.mapping import create_occurrence_map
from src.richness import calculate_species_richness
from src.richness_map import create_richness_map

st.set_page_config(
    page_title="Antarctic Species Distribution",
    page_icon="🐧",
    layout="wide",
)

DATA_PATH = Path("occurrence.csv")
CLEAN_CACHE = Path("outputs/cleaned_occurrence.csv")


@st.cache_data(show_spinner=False)
def load_and_clean_data() -> pd.DataFrame:
    if CLEAN_CACHE.exists():
        df = pd.read_csv(CLEAN_CACHE, low_memory=False)
        df["eventDate"] = pd.to_datetime(df["eventDate"], errors="coerce", utc=True)
        return df
    return clean_occurrence_data(load_raw_data(DATA_PATH))


@st.cache_data(show_spinner="Building occurrence map…")
def cached_occurrence_map_html(sample_size: int, use_cluster: bool) -> str:
    m = create_occurrence_map(
        load_and_clean_data(),
        sample_size=sample_size,
        use_cluster=use_cluster,
        with_popups=False,
    )
    return m._repr_html_()


@st.cache_data(show_spinner="Computing species richness…")
def cached_richness(lat_step: float, lon_step: float) -> pd.DataFrame:
    return calculate_species_richness(load_and_clean_data(), lat_step=lat_step, lon_step=lon_step)


@st.cache_data(show_spinner="Building richness map…")
def cached_richness_map_html(lat_step: float, lon_step: float) -> str:
    richness = cached_richness(lat_step, lon_step)
    m = create_richness_map(
        load_and_clean_data(),
        lat_step=lat_step,
        lon_step=lon_step,
        richness_df=richness,
    )
    return m._repr_html_()


@st.cache_data(show_spinner="Running DBSCAN clustering…")
def cached_hotspots(eps: float, min_samples: int) -> pd.DataFrame:
    return detect_hotspots(load_and_clean_data(), eps=eps, min_samples=min_samples)


@st.cache_data(show_spinner="Building hotspot map…")
def cached_hotspot_map_html(eps: float, min_samples: int) -> str:
    clustered = cached_hotspots(eps, min_samples)
    summary = summarize_hotspots(clustered)
    m = create_hotspot_map(clustered, summary)
    return m._repr_html_()


df = load_and_clean_data()

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Overview", "Species Map", "Richness Analysis", "Hotspot Detection"],
)

st.sidebar.markdown("---")
st.sidebar.metric("Total Records", f"{len(df):,}")
st.sidebar.metric("Unique Species", f"{df['scientificName'].nunique():,}")

# --- Overview ---
if page == "Overview":
    st.title("Species Distribution Pattern Analysis")
    st.subheader("SCAR Antarctic Biodiversity Dataset")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Records", f"{total_records(df):,}")
    col2.metric("Unique Species", f"{total_unique_species(df):,}")
    col3.metric("Kingdoms", df["kingdom"].nunique())
    col4.metric("Families", df["family"].nunique())

    st.markdown("---")

    left, right = st.columns(2)

    with left:
        st.subheader("Top 10 Species")
        top10 = top_species(df, 10).reset_index()
        top10.columns = ["Scientific Name", "Observations"]
        fig = px.bar(
            top10,
            x="Observations",
            y="Scientific Name",
            orientation="h",
            color="Observations",
            color_continuous_scale="Viridis",
        )
        fig.update_layout(showlegend=False, height=450, yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig, width="stretch")

    with right:
        st.subheader("Observations by Year")
        yearly = observations_by_year(df).reset_index()
        yearly.columns = ["Year", "Observations"]
        fig2 = px.line(
            yearly,
            x="Year",
            y="Observations",
            markers=True,
            color_discrete_sequence=["#2E86AB"],
        )
        fig2.update_layout(height=450)
        st.plotly_chart(fig2, width="stretch")

    st.subheader("Taxonomic Breakdown")
    tax_cols = st.columns(5)
    for i, (label, col_name) in enumerate(
        [("Phyla", "phylum"), ("Classes", "class"), ("Orders", "order"), ("Families", "family"), ("Genera", "genus")]
    ):
        tax_cols[i].metric(label, df[col_name].nunique())

# --- Species Map ---
elif page == "Species Map":
    st.title("Species Occurrence Map")
    st.markdown("Interactive map of Antarctic biodiversity occurrence records.")

    sample_size = st.slider("Max points to display", 500, 5000, 2000, step=250)
    use_cluster = st.checkbox("Use marker clustering", value=True)

    components.html(cached_occurrence_map_html(sample_size, use_cluster), height=600, scrolling=True)

    st.info(
        f"Showing up to **{sample_size:,}** points. Maps are cached — slider changes reload only when values change."
    )

# --- Richness Analysis ---
elif page == "Richness Analysis":
    st.title("Species Richness Analysis")
    st.markdown("Geographic grid-based species richness across Antarctica.")

    lat_step = st.slider("Latitude grid size (°)", 0.5, 3.0, 1.0, 0.5)
    lon_step = st.slider("Longitude grid size (°)", 1.0, 5.0, 2.0, 0.5)

    richness = cached_richness(lat_step, lon_step)

    col1, col2 = st.columns([2, 1])
    with col1:
        components.html(cached_richness_map_html(lat_step, lon_step), height=550, scrolling=True)

    with col2:
        st.subheader("Top Rich Grid Cells")
        top_grids = richness.head(15)[["lat_bin", "lon_bin", "species_count"]]
        top_grids.columns = ["Lat", "Lon", "Species"]
        st.dataframe(top_grids, width="stretch", hide_index=True)

        st.metric("Grid Cells", len(richness))
        st.metric("Max Richness", int(richness["species_count"].max()))
        st.metric("Mean Richness", f"{richness['species_count'].mean():.1f}")

    pivot = richness.pivot_table(
        index="lat_bin", columns="lon_bin", values="species_count", aggfunc="first"
    ).sort_index(ascending=False)
    fig = px.imshow(
        pivot,
        labels={"x": "Longitude (°)", "y": "Latitude (°)", "color": "Species"},
        color_continuous_scale="YlOrRd",
        aspect="auto",
    )
    fig.update_layout(title="Species Richness Heatmap", height=400)
    st.plotly_chart(fig, width="stretch")

# --- Hotspot Detection ---
elif page == "Hotspot Detection":
    st.title("Biodiversity Hotspot Detection")
    st.markdown("DBSCAN clustering to identify spatial biodiversity hotspots.")

    eps = st.slider("DBSCAN eps (degrees, ~0.8° ≈ 50–90 km)", 0.3, 2.0, 0.8, 0.1)
    min_samples = st.slider("DBSCAN min_samples", 5, 50, 12, 1)

    clustered = cached_hotspots(eps, min_samples)
    hotspot_summary = summarize_hotspots(clustered)

    col1, col2, col3 = st.columns(3)
    n_clusters = clustered["cluster"].nunique() - (1 if (clustered["cluster"] == -1).any() else 0)
    col1.metric("Clusters Found", n_clusters)
    col2.metric("Noise Points", int((clustered["cluster"] == -1).sum()))
    col3.metric("Top Hotspot Species", int(hotspot_summary["n_species"].max()) if not hotspot_summary.empty else 0)

    components.html(cached_hotspot_map_html(eps, min_samples), height=550, scrolling=True)

    if not hotspot_summary.empty:
        st.subheader("Hotspot Cluster Summary")
        display = hotspot_summary.copy()
        display["centroid_lat"] = display["centroid_lat"].round(3)
        display["centroid_lon"] = display["centroid_lon"].round(3)
        display.columns = ["Cluster", "Records", "Centroid Lat", "Centroid Lon", "Species"]
        st.dataframe(display, width="stretch", hide_index=True)
    else:
        st.warning("No clusters detected. Try lowering eps or min_samples.")
