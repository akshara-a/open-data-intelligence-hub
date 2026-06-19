import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")   # non-interactive backend — prevents memory leaks
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

# ─── Page Setup ───────────────────────────
st.set_page_config(
    page_title="Wildfire Risk Intelligence Engine",
    page_icon="🔥",
    layout="wide"
)

st.title("🔥 Wildfire Risk Intelligence Engine")
st.markdown("**Dataset:** NASA VIIRS SNPP Fire Archive | **Stack:** Pandas · NumPy · Matplotlib")
st.markdown("---")


# ─── Load Data (optimised) ────────────────
# Uses dtype map so Pandas never wastes memory upcasting columns.
# chunksize + concat is avoided here because @st.cache_data already
# ensures this runs only once per unique file path.
DTYPE_MAP = {
    "latitude":    "float32",
    "longitude":   "float32",
    "brightness":  "float32",
    "bright_t31":  "float32",
    "frp":         "float32",
    "confidence":  "category",
    "daynight":    "category",
    "satellite":   "category",
    "instrument":  "category",
    "version":     "category",
    "type":        "int8",
    "scan":        "float32",
    "track":       "float32",
}

@st.cache_data(show_spinner="Loading fire data…")
def load_data(path: str) -> pd.DataFrame:
    # First pass: read just the header to know which columns actually exist,
    # then build a dtype map that only references present columns.
    # This prevents errors on CSV exports that omit optional VIIRS columns.
    header = pd.read_csv(path, nrows=0).columns.tolist()
    safe_dtype = {k: v for k, v in DTYPE_MAP.items() if k in header}

    df = pd.read_csv(path, dtype=safe_dtype)

    # infer_datetime_format was removed in Pandas 2.2 — parse manually instead
    df["acq_date"] = pd.to_datetime(df["acq_date"], format="%Y-%m-%d", errors="coerce")
    return df


# ─── Locate default CSV ───────────────────
import gdown

DEFAULT_CSV = "fire_archive_SV-C2_761163.csv"
DRIVE_URL = "https://drive.google.com/uc?id=1_rsKmmUJdjglEHi_Tk8c_Z7zuVC065bD"

if not os.path.exists(DEFAULT_CSV):
    with st.spinner("Downloading fire data from Google Drive..."):
        gdown.download(DRIVE_URL, DEFAULT_CSV, quiet=False)

df = load_data(DEFAULT_CSV)
st.info(f"Loaded: `{DEFAULT_CSV}` — **{len(df):,}** fire detections")


# ─── Sidebar Filters ──────────────────────
st.sidebar.header("🔧 Filters")

conf_map  = {"n": "Nominal", "l": "Low", "h": "High"}
conf_opts = sorted(df["confidence"].dropna().unique().tolist())

selected_conf = st.sidebar.multiselect(
    "Confidence Level",
    options=conf_opts,
    default=conf_opts,
    format_func=lambda x: conf_map.get(str(x), str(x)),
)

dn_opts = df["daynight"].dropna().unique().tolist()
selected_dn = st.sidebar.multiselect(
    "Day / Night",
    options=dn_opts,
    default=dn_opts,
    format_func=lambda x: "☀️ Day" if x == "D" else "🌙 Night",
)

min_frp = float(df["frp"].min())
max_frp = float(df["frp"].max())
frp_range = st.sidebar.slider(
    "Fire Radiative Power (FRP) Range (MW)",
    min_value=min_frp,
    max_value=min(500.0, max_frp),
    value=(min_frp, min(500.0, max_frp)),
)

# ─── Apply filters (no .copy() — saves memory) ────
mask = (
    df["confidence"].isin(selected_conf) &
    df["daynight"].isin(selected_dn) &
    df["frp"].between(frp_range[0], frp_range[1])
)
filtered = df[mask]

if filtered.empty:
    st.warning("No data matches the current filters. Please adjust your selections.")
    st.stop()


# ─── Metric Cards ─────────────────────────
st.subheader("📊 Dataset Overview")
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Detections",   f"{len(filtered):,}")
c2.metric("Date Range",         f"{df['acq_date'].dt.year.min()} – {df['acq_date'].dt.year.max()}")
c3.metric("Avg Brightness (K)", f"{filtered['brightness'].mean():.1f}")
c4.metric("Avg FRP (MW)",       f"{filtered['frp'].mean():.2f}")
c5.metric("Max FRP (MW)",       f"{filtered['frp'].max():.1f}")
st.markdown("---")


# ─── Helper: close figure safely ──────────
def close(fig):
    plt.close(fig)


# ─── Charts Row 1 ─────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("📅 Fire Detections Over Time")
    monthly = (
        filtered.set_index("acq_date")
        .resample("ME" if pd.__version__ >= "2.2" else "M")
        .size()
        .reset_index()
    )
    monthly.columns = ["month", "count"]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(monthly["month"], monthly["count"], color="orangered", width=20)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    plt.xticks(rotation=45, ha="right")
    ax.set_ylabel("Number of Detections")
    ax.set_title("Monthly Fire Detection Count")
    plt.tight_layout()
    st.pyplot(fig)
    close(fig)

with col2:
    st.subheader("🌡️ Brightness Temperature Distribution")
    fig, ax = plt.subplots(figsize=(8, 5))
    mean_b = float(filtered["brightness"].mean())
    ax.hist(filtered["brightness"], bins=60, color="firebrick", edgecolor="white", alpha=0.85)
    ax.axvline(mean_b, color="gold", linestyle="--", linewidth=2,
               label=f"Mean: {mean_b:.1f} K")
    ax.set_xlabel("Brightness Temperature (K)")
    ax.set_ylabel("Frequency")
    ax.set_title("Brightness Temperature Distribution")
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)
    close(fig)

st.markdown("---")


# ─── Charts Row 2 ─────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("☀️🌙 Day vs Night Fire Detections")
    dn_counts = filtered["daynight"].value_counts()
    labels = ["☀️ Day" if x == "D" else "🌙 Night" for x in dn_counts.index]
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.pie(dn_counts.values, labels=labels, autopct="%1.1f%%",
           colors=["#FFB347", "#4169E1"], startangle=90, pctdistance=0.75)
    ax.set_title("Day vs Night Detections")
    plt.tight_layout()
    st.pyplot(fig)
    close(fig)

with col2:
    st.subheader("📶 Confidence Level Breakdown")
    conf_counts = filtered["confidence"].map(conf_map).value_counts()
    clr_map = {"High": "#2ecc71", "Nominal": "#f39c12", "Low": "#e74c3c"}
    bar_colors = [clr_map.get(c, "steelblue") for c in conf_counts.index]
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.bar(conf_counts.index, conf_counts.values, color=bar_colors, edgecolor="white")
    ax.set_ylabel("Count")
    ax.set_title("Fire Detection Confidence Levels")
    for i, v in enumerate(conf_counts.values):
        ax.text(i, v + max(conf_counts.values) * 0.01, f"{v:,}", ha="center", fontsize=9)
    plt.tight_layout()
    st.pyplot(fig)
    close(fig)

st.markdown("---")


# ─── Charts Row 3 ─────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("⚡ Fire Radiative Power (FRP) Distribution")
    fig, ax = plt.subplots(figsize=(8, 5))
    frp_clipped = filtered.loc[filtered["frp"] <= 100, "frp"]
    ax.hist(frp_clipped, bins=60, color="darkorange", edgecolor="white", alpha=0.85)
    ax.set_xlabel("FRP (MW) — clipped at 100 MW for clarity")
    ax.set_ylabel("Frequency")
    ax.set_title("Fire Radiative Power Distribution")
    plt.tight_layout()
    st.pyplot(fig)
    close(fig)

with col2:
    st.subheader("🗺️ Geographic Spread (Lat vs Lon)")
    # Cap scatter at 5 000 points — beyond that the dots overlap anyway
    MAX_SCATTER = 5_000
    sample = (
        filtered.sample(MAX_SCATTER, random_state=42)
        if len(filtered) > MAX_SCATTER else filtered
    )
    fig, ax = plt.subplots(figsize=(8, 5))
    sc = ax.scatter(
        sample["longitude"], sample["latitude"],
        c=sample["brightness"], cmap="hot", s=2, alpha=0.5,
        rasterized=True,   # rasterise the scatter layer → smaller SVG in memory
    )
    plt.colorbar(sc, ax=ax, label="Brightness (K)")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title(f"Fire Hotspot Map — {len(sample):,} sampled points (colored by Brightness)")
    plt.tight_layout()
    st.pyplot(fig)
    close(fig)

st.markdown("---")


# ─── Top Hotspot Regions ──────────────────
st.subheader("🏆 Top Hotspot Grid Cells (Binned by 1° Grid)")
top_cells = (
    filtered
    .assign(lat_bin=filtered["latitude"].round(0),
            lon_bin=filtered["longitude"].round(0))
    .groupby(["lat_bin", "lon_bin"], observed=True)
    .agg(Detections=("frp", "count"),
         avg_frp=("frp", "mean"),
         max_frp=("frp", "max"))
    .reset_index()
    .sort_values("Detections", ascending=False)
    .head(20)
    .reset_index(drop=True)
)
top_cells.index += 1
top_cells.columns = ["Lat (°)", "Lon (°)", "Detections", "Avg FRP (MW)", "Max FRP (MW)"]
top_cells["Avg FRP (MW)"] = top_cells["Avg FRP (MW)"].round(2)
top_cells["Max FRP (MW)"] = top_cells["Max FRP (MW)"].round(2)
st.dataframe(top_cells, use_container_width=True)

st.markdown("---")


# ─── Raw Data Preview ─────────────────────
with st.expander("🔍 Raw Data Preview"):
    n = st.slider("Rows to preview", 10, 200, 50)
    st.dataframe(filtered.head(n), use_container_width=True)

st.markdown("---")


# ─── Download (lazy — only serialises on button click) ────────────────
st.subheader("⬇️ Download Filtered Data")

@st.cache_data(show_spinner=False)
def to_csv_bytes(index_hash: int) -> bytes:
    """Cache the CSV bytes so repeated renders don't re-serialise the df."""
    return filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download filtered_fire_data.csv",
    # Pass a hash of the filter state so cache invalidates when filters change
    data=to_csv_bytes(hash((tuple(selected_conf), tuple(selected_dn), frp_range))),
    file_name="filtered_fire_data.csv",
    mime="text/csv",
)

st.markdown("---")
st.markdown("**Project:** Wildfire Risk Intelligence Engine | **Dataset:** NASA VIIRS SNPP | **Stack:** Pandas · NumPy · Matplotlib")
