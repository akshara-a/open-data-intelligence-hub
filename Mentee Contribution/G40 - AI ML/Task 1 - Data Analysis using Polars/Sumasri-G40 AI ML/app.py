import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Biodiversity Hotspot Detection",
    page_icon="🌿",
    layout="wide"
)

st.title("🌿 Biodiversity Hotspot Detection")
st.write("Upload biodiversity occurrence data and identify hotspot regions.")

# -----------------------------
# FILE UPLOAD
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # -----------------------------
    # COLUMN CHECK
    # -----------------------------
    required_columns = ["latitude", "longitude"]

    missing_cols = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_cols:
        st.error(
            f"Missing required columns: {missing_cols}"
        )
        st.stop()

    # -----------------------------
    # BASIC STATS
    # -----------------------------
    st.subheader("Dataset Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Records",
            len(df)
        )

    with col2:
        st.metric(
            "Unique Locations",
            len(
                df[
                    ["latitude", "longitude"]
                ].drop_duplicates()
            )
        )

    # -----------------------------
    # MAP CENTER
    # -----------------------------
    center_lat = df["latitude"].mean()
    center_lon = df["longitude"].mean()

    # -----------------------------
    # HEATMAP
    # -----------------------------
    st.subheader("Hotspot Heatmap")

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=5
    )

    heat_data = df[
        ["latitude", "longitude"]
    ].values.tolist()

    HeatMap(
        heat_data,
        radius=15
    ).add_to(m)

    st_folium(
        m,
        width=1000,
        height=600
    )

    # -----------------------------
    # HOTSPOT TABLE
    # -----------------------------
    st.subheader("Potential Hotspots")

    hotspot_df = (
        df.groupby(
            ["latitude", "longitude"]
        )
        .size()
        .reset_index(name="species_count")
        .sort_values(
            "species_count",
            ascending=False
        )
    )

    st.dataframe(
        hotspot_df.head(20),
        use_container_width=True
    )

    # -----------------------------
    # DOWNLOAD
    # -----------------------------
    csv = hotspot_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Hotspot Results",
        data=csv,
        file_name="hotspot_results.csv",
        mime="text/csv"
    )

    st.success(
        "Biodiversity hotspot analysis completed successfully."
    )

else:
    st.info(
        "Please upload a biodiversity CSV file to begin analysis."
    )