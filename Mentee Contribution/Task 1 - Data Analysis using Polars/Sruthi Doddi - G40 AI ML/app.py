# app.py - PROFESSIONAL DARK THEME VERSION
import streamlit as st
import polars as pl
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Extreme Weather Intelligence",
    page_icon="🌩️",
    layout="wide"
)

# Custom CSS for clean dark theme
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #0e1117;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    /* Metric cards */
    .metric-card {
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #333333;
        text-align: center;
    }
    
    .metric-card h3 {
        color: #ffffff !important;
        margin: 0;
        font-size: 2em;
    }
    
    .metric-card p {
        color: #888888;
        margin: 5px 0 0 0;
    }
    
    /* Dataframes */
    .dataframe {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #1e1e1e;
    }
    
    /* Info boxes */
    .stAlert {
        background-color: #1e1e1e;
        border-left: 3px solid #00ff00;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #2e2e2e;
        color: white;
        border: 1px solid #444444;
        border-radius: 5px;
    }
    
    .stButton > button:hover {
        background-color: #3e3e3e;
        border-color: #666666;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #1e1e1e;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #2e2e2e;
        border-radius: 5px;
        padding: 10px 20px;
        color: white;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #3e3e3e;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #1e1e1e;
        border-radius: 5px;
    }
    
    /* Divider */
    hr {
        border-color: #333333;
    }
    
    /* Caption */
    .caption {
        color: #666666;
        text-align: center;
        padding: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("🌩️ Extreme Weather Intelligence Platform")
st.markdown("---")

# Load and process data
@st.cache_data
def load_and_process():
    with st.spinner("Loading weather data..."):
        # Load files
        df1 = pl.read_csv("01001099999.csv")
        df2 = pl.read_csv("01008099999.csv")
        df3 = pl.read_csv("01293099999.csv")
        
        # Combine
        weather = pl.concat([df1, df2, df3], how="vertical_relaxed")
        
        # Clean numeric columns
        for col in ["TEMP", "MAX", "MIN", "PRCP", "MXSPD", "WDSP", "GUST"]:
            if col in weather.columns:
                weather = weather.with_columns(
                    pl.col(col).str.strip_chars().cast(pl.Float64, strict=False).alias(col)
                )
        
        # Fix missing values
        if "PRCP" in weather.columns:
            weather = weather.with_columns(
                pl.when(pl.col("PRCP") == 99.99).then(0).otherwise(pl.col("PRCP")).alias("PRCP")
            )
        
        if "GUST" in weather.columns:
            weather = weather.with_columns(
                pl.when(pl.col("GUST") == 999.9).then(None).otherwise(pl.col("GUST")).alias("GUST")
            )
        
        # Classify events
        weather = weather.with_columns(
            pl.when(pl.col("MAX") >= 90).then(pl.lit("EXTREME_HEAT"))
              .when(pl.col("MAX") >= 80).then(pl.lit("HEATWAVE"))
              .when(pl.col("MIN") <= -10).then(pl.lit("EXTREME_COLD"))
              .when(pl.col("MIN") <= 0).then(pl.lit("COLD_WAVE"))
              .when((pl.col("PRCP") >= 1.0) & (pl.col("MXSPD") >= 40)).then(pl.lit("STORM"))
              .when(pl.col("PRCP") >= 1.0).then(pl.lit("HEAVY_RAIN"))
              .when(pl.col("MXSPD") >= 40).then(pl.lit("HIGH_WIND"))
              .otherwise(pl.lit("NORMAL"))
              .alias("EVENT_TYPE")
        )
        
        # Calculate severity
        weather = weather.with_columns(
            (
                pl.col("MAX").fill_null(0) * 0.3 +
                pl.col("PRCP").fill_null(0) * 25 +
                pl.col("MXSPD").fill_null(0) * 0.7
            ).alias("SEVERITY_SCORE")
        )
        
        return weather

weather = load_and_process()

# Get data
event_counts = weather.group_by("EVENT_TYPE").agg(pl.len()).sort("len", descending=True)
extreme_events = weather.filter(pl.col("EVENT_TYPE") != "NORMAL")
total_extreme = len(extreme_events)

# Sidebar
with st.sidebar:
    st.header("📊 Dashboard Controls")
    st.markdown("---")
    
    st.metric("Total Records", f"{len(weather):,}")
    st.metric("Extreme Events", total_extreme)
    st.metric("Weather Stations", weather['NAME'].n_unique())
    
    st.markdown("---")
    st.subheader("🔍 Filter Events")
    
    event_options = [e for e in event_counts['EVENT_TYPE'].to_list() if e != "NORMAL"]
    selected_events = st.multiselect(
        "Select Event Types to Display",
        options=event_options,
        default=event_options
    )
    
    st.markdown("---")
    st.caption("Data Source: NOAA Weather Stations")
    st.caption(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# Key Metrics Row
st.subheader("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h3>{weather['DATE'].min()}</h3>
        <p>to {weather['DATE'].max()}</p>
        <small>Date Range</small>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <h3>{len(weather):,}</h3>
        <p>Total Records</p>
        <small>Processed</small>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <h3>{weather['NAME'].n_unique()}</h3>
        <p>Active Stations</p>
        <small>Monitoring</small>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <h3>{total_extreme}</h3>
        <p>Extreme Events</p>
        <small>Detected</small>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Event Distribution
st.subheader("📈 Event Distribution")

col1, col2 = st.columns(2)

with col1:
    # Bar chart
    plot_data = event_counts.filter(pl.col("EVENT_TYPE") != "NORMAL").to_pandas()
    fig = px.bar(plot_data, x='EVENT_TYPE', y='len', 
                 title='Extreme Events Distribution',
                 labels={'EVENT_TYPE': 'Event Type', 'len': 'Number of Events'},
                 color='EVENT_TYPE',
                 template='plotly_dark')
    fig.update_layout(showlegend=False, height=400, plot_bgcolor='#1e1e1e', paper_bgcolor='#1e1e1e')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Event counts table
    st.dataframe(event_counts.filter(pl.col("EVENT_TYPE") != "NORMAL").to_pandas(), 
                 use_container_width=True)

st.markdown("---")

# Most Severe Event
st.subheader("🏆 Most Severe Event")

if total_extreme > 0:
    most_severe = extreme_events.sort("SEVERITY_SCORE", descending=True).head(1)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.info(f"**Date**\n\n{most_severe['DATE'][0]}")
    
    with col2:
        st.info(f"**Location**\n\n{most_severe['NAME'][0]}")
    
    with col3:
        st.warning(f"**Event Type**\n\n{most_severe['EVENT_TYPE'][0]}")
    
    with col4:
        st.error(f"**Severity Score**\n\n{most_severe['SEVERITY_SCORE'][0]:.2f}")
    
    st.write(f"**Details:** MAX Temp: {most_severe['MAX'][0]:.1f}°F | Min Temp: {most_severe['MIN'][0]:.1f}°F | Rainfall: {most_severe['PRCP'][0]:.2f} inches | Wind Speed: {most_severe['MXSPD'][0]:.1f} mph")

st.markdown("---")

# Analysis Tabs
tab1, tab2, tab3 = st.tabs(["📊 Pivot Table", "📍 Station Analysis", "📅 Monthly Trends"])

with tab1:
    if total_extreme > 0:
        pivot_table = extreme_events.pivot(
            values="EVENT_TYPE",
            index="NAME",
            on="EVENT_TYPE",
            aggregate_function="len"
        ).fill_null(0)
        st.dataframe(pivot_table.to_pandas(), use_container_width=True)
    else:
        st.info("No extreme events found")

with tab2:
    if total_extreme > 0:
        station_summary = extreme_events.group_by("NAME").agg([
            pl.len().alias("Total Events"),
            pl.col("SEVERITY_SCORE").mean().alias("Avg Severity"),
            pl.col("SEVERITY_SCORE").max().alias("Max Severity")
        ]).sort("Total Events", descending=True)
        st.dataframe(station_summary.to_pandas(), use_container_width=True)
    else:
        st.info("No extreme events found")

with tab3:
    if total_extreme > 0:
        monthly = extreme_events.with_columns([
            pl.col("DATE").str.slice(0, 7).alias("Month")
        ]).group_by("Month").agg([
            pl.len().alias("Extreme Events")
        ]).sort("Month")
        
        fig = px.line(monthly.to_pandas(), x='Month', y='Extreme Events',
                      title='Extreme Events Over Time',
                      markers=True, template='plotly_dark')
        fig.update_layout(height=400, plot_bgcolor='#1e1e1e', paper_bgcolor='#1e1e1e')
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(monthly.to_pandas(), use_container_width=True)
    else:
        st.info("No extreme events found")

st.markdown("---")

# Detailed Events Table
st.subheader("🔍 Detailed Events Log")

if total_extreme > 0:
    # Apply filters
    if selected_events:
        display_events = extreme_events.filter(pl.col("EVENT_TYPE").is_in(selected_events))
    else:
        display_events = extreme_events
    
    # Search
    search = st.text_input("🔎 Search by location or date", placeholder="Enter station name or date...")
    if search:
        display_events = display_events.filter(
            (pl.col("NAME").str.contains(search, literal=True)) | 
            (pl.col("DATE").str.contains(search, literal=True))
        )
    
    # Sort options
    col1, col2 = st.columns(2)
    with col1:
        sort_by = st.selectbox("Sort by", ["SEVERITY_SCORE", "DATE", "MAX", "PRCP", "MXSPD"])
    with col2:
        sort_order = st.selectbox("Order", ["Descending", "Ascending"])
    
    if sort_order == "Descending":
        display_events = display_events.sort(sort_by, descending=True)
    else:
        display_events = display_events.sort(sort_by, descending=False)
    
    # Display table
    st.dataframe(
        display_events.select([
            "DATE", "NAME", "EVENT_TYPE", "MAX", "MIN", "PRCP", "MXSPD", "SEVERITY_SCORE"
        ]).to_pandas(),
        use_container_width=True,
        height=400
    )
    
    st.caption(f"Showing {len(display_events)} of {total_extreme} extreme events")

st.markdown("---")

# Raw Data Preview
with st.expander("📄 Raw Data Preview (First 20 rows)"):
    preview_cols = ["DATE", "NAME", "MAX", "MIN", "PRCP", "MXSPD", "EVENT_TYPE", "SEVERITY_SCORE"]
    available_cols = [col for col in preview_cols if col in weather.columns]
    st.dataframe(weather.head(20).select(available_cols).to_pandas(), use_container_width=True)

# Export Section
st.subheader("💾 Export Data")

col1, col2 = st.columns(2)

with col1:
    csv_full = weather.to_pandas().to_csv(index=False)
    st.download_button(
        label="📥 Download Full Dataset (CSV)",
        data=csv_full,
        file_name=f"weather_data_full_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

with col2:
    if total_extreme > 0:
        csv_extreme = extreme_events.to_pandas().to_csv(index=False)
        st.download_button(
            label="⚠️ Download Extreme Events Only (CSV)",
            data=csv_extreme,
            file_name=f"extreme_events_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

# Footer
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: #666666; padding: 20px;'>
    <p>🌩️ Extreme Weather Intelligence Platform | Powered by Polars & Streamlit</p>
    <p>Total Records: {len(weather):,} | Extreme Events: {total_extreme} | Detection Rate: {total_extreme/len(weather)*100:.2f}%</p>
    <p>Data Source: NOAA Weather Stations | Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
</div>
""", unsafe_allow_html=True)