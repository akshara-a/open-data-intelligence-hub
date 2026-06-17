import os
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(
    page_title="Earthquake Trend Analytics",
    page_icon="🌋",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def generate_and_load_data():
    filename = "usgs_earthquake_trends_dataset.csv"
    if not os.path.exists(filename):
        np.random.seed(42)
        num_records = 2000
        
        start_date = pd.to_datetime("1970-01-01")
        end_date = pd.to_datetime("2025-12-31")
        total_days = (end_date - start_date).days
        
        random_days = np.random.randint(0, total_days, num_records)
        latitudes = np.random.uniform(-60, 80, num_records)
        longitudes = np.random.uniform(-180, 180, num_records)
        
        magnitudes = np.random.exponential(scale=1.1, size=num_records) + 2.0
        magnitudes = np.clip(magnitudes, 2.0, 9.5)
        magnitudes[0] = 9.2
        
        depths = np.random.uniform(0, 700, num_records)
        
        places = np.random.choice([
            "Pacific Ring of Fire", "Mid-Atlantic Ridge", "Alpide Belt", 
            "San Andreas Fault", "Japan Trench", "Hindukush Region"
        ], num_records)
        
        df_raw = pd.DataFrame({
            "latitude": latitudes,
            "longitude": longitudes,
            "mag": magnitudes,
            "depth": depths,
            "place": places
        })
        
        df_raw["time"] = start_date + pd.to_timedelta(random_days, unit="D")
        df_raw.to_csv(filename, index=False)
    
    df = pd.read_csv(filename)
    df["time"] = pd.to_datetime(df["time"])
    df["year"] = df["time"].dt.year
    df["month"] = df["time"].dt.month
    return df

df = generate_and_load_data()

st.sidebar.header("🕹️ Control Panel")
st.sidebar.markdown("Use the filters below to slice the historical seismic records dynamically.")

min_year, max_year = int(df["year"].min()), int(df["year"].max())
year_range = st.sidebar.slider(
    "Select Year Range", 
    min_year, max_year, (min_year, max_year),
    help="Filters the data based on the chronological year of occurrence."
)

min_mag, max_mag = float(df["mag"].min()), float(df["mag"].max())
mag_range = st.sidebar.slider(
    "Select Magnitude Range (Mw)", 
    min_mag, max_mag, (min_mag, max_mag),
    help="Seismic energy scale. Every +1 increase represents roughly 32 times more energy release!"
)

filtered_df = df[
    (df["year"] >= year_range[0]) & (df["year"] <= year_range[1]) &
    (df["mag"] >= mag_range[0]) & (df["mag"] <= mag_range[1])
]

st.title("🌋 Earthquake Trend Analytics Dashboard")
st.markdown("### Analyzing Long-Term Global Seismic Trends (1970–2025)")

with st.container(border=True):
    col1, col2, col3, col4 = st.columns(4)
    if not filtered_df.empty:
        col1.metric(label="Total Recorded Events", value=f"{len(filtered_df)}")
        col2.metric(label="Max Magnitude", value=f"{filtered_df['mag'].max():.1f} Mw")
        col3.metric(label="Average Magnitude", value=f"{filtered_df['mag'].mean():.2f} Mw")
        col4.metric(label="Average Depth", value=f"{filtered_df['depth'].mean():.1f} km")
    else:
        col1.metric(label="Total Recorded Events", value="0")
        col2.metric(label="Max Magnitude", value="N/A")
        col3.metric(label="Average Magnitude", value="N/A")
        col4.metric(label="Average Depth", value="N/A")

if not filtered_df.empty:
    max_selected_mag = filtered_df["mag"].max()
    if max_selected_mag >= 7.0:
        st.error(f"⚠️ **High-Risk Seismic Alert:** The active filters include major catastrophic earthquakes (Max: {max_selected_mag:.1f} Mw). Events above 7.0 cause serious damage to infrastructure and require specialized engineering codes.")
    elif 5.0 <= max_selected_mag < 7.0:
        st.warning(f"⚠️ **Moderate Activity Alert:** The active filters contain moderate-to-strong events (Max: {max_selected_mag:.1f} Mw). These are capable of shaking buildings and causing minor localized damage.")
    else:
        st.success("✅ **Stable Seismic Window:** The current view contains only minor, micro-seismic events. No major risks or significant infrastructural hazards detected.")

tab1, tab2, tab3 = st.tabs([
    "📊 Temporal & Regional Trends", 
    "📈 Geological Distributions", 
    "🗺️ Interactive Geospatial Mapping"
])

with tab1:
    st.subheader("Seismic Event Counts Over Time Continuum")
    if not filtered_df.empty:
        yearly_counts = filtered_df.groupby("year").size().reset_index(name="Event Count")
        fig1 = px.line(yearly_counts, x='year', y='Event Count', markers=True, title="Annual Seismic Activity Rates")
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.warning("No trend timeline available for current query filters.")

with tab2:
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("Magnitude vs. Hypocentral Depth Correlation")
        if not filtered_df.empty:
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.scatterplot(data=filtered_df, x='mag', y='depth', alpha=0.4, color='#84cc16', edgecolor='none', ax=ax)
            ax.set_xlabel("Magnitude (M)")
            ax.set_ylabel("Hypocentral Depth (km)")
            ax.invert_yaxis()
            st.pyplot(fig)
        else:
            st.warning("Insufficient metrics available.")
            
    with col_right:
        st.subheader("Pairwise Variable Correlation Matrix")
        if not filtered_df.empty:
            fig, ax = plt.subplots(figsize=(8, 4))
            features = ['mag', 'depth', 'latitude', 'longitude', 'year', 'month']
            sns.heatmap(filtered_df[features].corr(), annot=True, cmap='coolwarm', fmt=".4f", linewidths=0.5, square=True, ax=ax)
            st.pyplot(fig)
        else:
            st.warning("Insufficient matrix data fields.")

with tab3:
    st.subheader("Geospatial Distribution of Filtered Seismic Events")
    if not filtered_df.empty:
        map_data = filtered_df[['latitude', 'longitude', 'mag', 'depth', 'place']].dropna()
        
        fig_map = px.density_map(
            map_data,
            lat="latitude",
            lon="longitude",
            z="mag",
            radius=10,
            zoom=1,
            color_continuous_scale="Viridis",
            hover_name="place",
            hover_data={"mag": True, "depth": True, "latitude": False, "longitude": False},
            title="Global Seismic Density Heatmap"
        )
        
        fig_map.update_layout(
            margin={"r":0,"t":40,"l":0,"b":0},
            map_style="open-street-map"
        )
        
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.warning("No geospatial coordinate tracks match your current parameter configurations.")

        st.markdown("---")
        if not filtered_df.empty:
            st.dataframe(
                filtered_df[['time', 'place', 'mag', 'depth', 'latitude', 'longitude']]
                .sort_values('time', ascending=False)
                .head(100), 
                use_container_width=True
            )