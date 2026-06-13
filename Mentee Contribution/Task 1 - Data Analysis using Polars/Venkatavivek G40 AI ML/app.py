import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ----------------------------------------------------
# Page Configuration & Aesthetics
# ----------------------------------------------------
st.set_page_config(
    page_title="Global Earthquake Analytics Dashboard",
    page_icon="🌋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium CSS styling (dark mode optimization, card layouts)
st.markdown("""
    <style>
    /* Main container background */
    .reportview-container {
        background: #0f172a;
    }
    
    /* Metrics panel custom styling */
    div[data-testid="metric-container"] {
        background-color: #1e293b;
        border: 1px solid #334155;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
        text-align: center;
    }
    
    div[data-testid="metric-container"] label {
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #38bdf8 !important;
        font-size: 28px !important;
        font-weight: 700 !important;
    }
    
    /* Custom header design */
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #94a3b8;
        margin-bottom: 2rem;
    }
    
    /* Section dividers */
    hr {
        border-top: 1px solid #334155;
        margin-top: 2rem;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# Data Loading & Preprocessing
# ----------------------------------------------------
@st.cache_data
def load_and_preprocess_data():
    # Load dataset
    df = pd.read_csv("earthquake_data.csv")
    
    # Drop unnecessary columns (exactly matching Code Cell 4)
    columns_to_drop = [
        'magType', 'nst', 'gap', 'dmin', 'rms', 'net', 'id', 'updated',
        'horizontalError', 'depthError', 'magError', 'magNst', 'locationSource', 'magSource'
    ]
    df = df.drop(columns=[col for col in columns_to_drop if col in df.columns], errors='ignore')
    
    # Drop missing values (exactly matching Code Cell 7)
    df = df.dropna()
    
    # Convert time to datetime & extract year/month (exactly matching Code Cell 8)
    df['time'] = pd.to_datetime(df['time'])
    df['year'] = df['time'].dt.year
    df['month'] = df['time'].dt.month
    
    # Extract country from place (exactly matching Code Cell 31)
    df['country'] = df['place'].str.split(',').str[-1].str.strip()
    
    # Risk Classification (exactly matching Code Cell 25)
    def risk_level(mag):
        if mag >= 7:
            return "High"
        elif mag >= 5:
            return "Medium"
        else:
            return "Low"
            
    df['risk'] = df['mag'].apply(risk_level)
    return df

df_raw = load_and_preprocess_data()

# ----------------------------------------------------
# Sidebar Controls & Filters
# ----------------------------------------------------
st.sidebar.image("https://img.icons8.com/external-flatart-icons-flat-flatarticons/128/external-earthquake-disaster-flatart-icons-flat-flatarticons.png", width=80)
st.sidebar.markdown("### Dashboard Controls")
st.sidebar.markdown("Customize your view by adjusting the filters below:")

# Year Filter
min_year, max_year = int(df_raw['year'].min()), int(df_raw['year'].max())
selected_years = st.sidebar.slider(
    "Select Year Range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# Magnitude Filter
min_mag, max_mag = float(df_raw['mag'].min()), float(df_raw['mag'].max())
selected_mags = st.sidebar.slider(
    "Select Magnitude Range",
    min_value=min_mag,
    max_value=max_mag,
    value=(min_mag, max_mag),
    step=0.1
)

# Depth Filter
min_depth, max_depth = float(df_raw['depth'].min()), float(df_raw['depth'].max())
selected_depths = st.sidebar.slider(
    "Select Depth Range (km)",
    min_value=min_depth,
    max_value=max_depth,
    value=(min_depth, max_depth)
)

# Risk Level Filter
available_risks = sorted(df_raw['risk'].unique())
selected_risks = st.sidebar.multiselect(
    "Filter by Risk Category",
    options=available_risks,
    default=available_risks
)

# Country Filter
available_countries = sorted(df_raw['country'].unique())
selected_countries = st.sidebar.multiselect(
    "Filter by Country/Region",
    options=available_countries,
    default=[]
)

# Reset Button
if st.sidebar.button("Reset Filters"):
    st.rerun()

# Apply Filters
df_filtered = df_raw[
    (df_raw['year'] >= selected_years[0]) & 
    (df_raw['year'] <= selected_years[1]) &
    (df_raw['mag'] >= selected_mags[0]) &
    (df_raw['mag'] <= selected_mags[1]) &
    (df_raw['depth'] >= selected_depths[0]) &
    (df_raw['depth'] <= selected_depths[1]) &
    (df_raw['risk'].isin(selected_risks))
]

if selected_countries:
    df_filtered = df_filtered[df_filtered['country'].isin(selected_countries)]

# ----------------------------------------------------
# Main Dashboard Layout
# ----------------------------------------------------
st.markdown("<div class='main-title'>Global Earthquake Analytics</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>An interactive intelligence dashboard exploring historical earthquake magnitudes, depths, locations, and classifications.</div>", unsafe_allow_html=True)

# ----------------------------------------------------
# Top KPI Metric Cards (Visual Insight #1)
# ----------------------------------------------------
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Total Earthquakes", f"{len(df_filtered):,}")
with col2:
    st.metric("Average Magnitude", f"{df_filtered['mag'].mean():.3f}" if not df_filtered.empty else "N/A")
with col3:
    st.metric("Max Magnitude", f"{df_filtered['mag'].max():.1f}" if not df_filtered.empty else "N/A")
with col4:
    st.metric("Min Magnitude", f"{df_filtered['mag'].min():.1f}" if not df_filtered.empty else "N/A")
with col5:
    high_risk_count = len(df_filtered[df_filtered['risk'] == 'High'])
    high_risk_pct = (high_risk_count / len(df_filtered) * 100) if len(df_filtered) > 0 else 0
    st.metric("High Risk Count (mag≥7)", f"{high_risk_count} ({high_risk_pct:.1f}%)")

# Add an expandable section for the original notebook metrics benchmarking
with st.expander("📊 Compare with Original Notebook Benchmark Insights"):
    st.markdown("""
    Below are the static benchmarking insights extracted from the final cell of the Jupyter Notebook (`Global_Earthquake_Analytics.ipynb`):
    * **Average Magnitude**: `4.805419496613993` | **Minimum**: `4.5` | **Maximum**: `8.8`
    * **Year wise Earthquake count**:
      * **2023**: `1,698` | **2024**: `6,359` | **2025 (Highest)**: `8,515` | **2026**: `2,922`
    * **Top Regions**: `South Sandwich Islands region` (497), `south of the Fiji Islands` (330), `Kermadec Islands region` (271)
    * **Top Countries**: `Russia` (2,239), `Indonesia` (1,820), `Philippines` (1,568), `Japan` (1,153)
    * **Correlation**: Longitude & latitude show minor correlation; depth and magnitude have negligible correlation (`-0.019`)
    * **Risk Categories**: Low (mag<5) - `75.5%` | Medium (mag<7) - `24.3%` | High (mag≥7) - `0.2%`
    """)

# ----------------------------------------------------
# Tabbed Navigation for Analytics sections
# ----------------------------------------------------
tab_temporal, tab_geo = st.tabs([
    "📈 Magnitude & Temporal Trends",
    "🌍 Geographical & Hotspot Analysis"
])

# ----------------------------------------------------
# Tab 1: Magnitude & Temporal Trends
# ----------------------------------------------------
with tab_temporal:
    st.subheader("Magnitude Distributions & Temporal Activity Trends")
    
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        # Magnitude Distribution Histogram (Code Cell 11)
        fig_mag_dist = px.histogram(
            df_filtered, 
            x='mag', 
            nbins=20, 
            title="Magnitude Distribution (Jupyter Cell 11)",
            labels={'mag': 'Magnitude', 'count': 'Frequency'},
            color_discrete_sequence=['#f59e0b']
        )
        fig_mag_dist.update_layout(
            template="plotly_dark",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Magnitude",
            yaxis_title="Frequency",
            bargap=0.05
        )
        st.plotly_chart(fig_mag_dist, use_container_width=True)

    with col_t2:
        # Yearly line count plot (Code Cell 14)
        yearly_counts = df_filtered.groupby('year').size().reset_index(name='count')
        fig_yearly = px.line(
            yearly_counts, 
            x='year', 
            y='count',
            title="Earthquakes Per Year Trend (Jupyter Cell 14)",
            markers=True,
            labels={'year': 'Year', 'count': 'Earthquake Count'},
            color_discrete_sequence=['#6366f1']
        )
        fig_yearly.update_layout(
            template="plotly_dark",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Year",
            yaxis_title="Count",
            xaxis=dict(tickmode='linear', tick0=min_year, dtick=1)
        )
        st.plotly_chart(fig_yearly, use_container_width=True)
        
    st.markdown("---")
    
    # Monthly Frequency (Code Cell 30)
    st.subheader("Monthly Frequency Analysis")
    monthly_counts = df_filtered.groupby('month').size().reset_index(name='count')
    month_names = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 
        7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    monthly_counts['month_name'] = monthly_counts['month'].map(month_names)
    
    fig_monthly = px.bar(
        monthly_counts, 
        x='month', 
        y='count',
        text='count',
        title="Monthly Earthquake Frequency (Jupyter Cell 30)",
        labels={'month': 'Month', 'count': 'Earthquake Count'},
        color_discrete_sequence=['#10b981']
    )
    fig_monthly.update_layout(
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Month (1 = January, 12 = December)",
        yaxis_title="Count",
        xaxis=dict(tickmode='linear', tick0=1, dtick=1)
    )
    fig_monthly.update_traces(textposition='outside')
    st.plotly_chart(fig_monthly, use_container_width=True)

# ----------------------------------------------------
# Tab 2: Geographical & Hotspot Analysis
# ----------------------------------------------------
with tab_geo:
    st.subheader("Geographical Distribution and Interactive Epirentures Map")
    
    if not df_filtered.empty:
        # Interactive Plotly scatter mapbox using free carto-darkmatter style
        fig_map = px.scatter_mapbox(
            df_filtered, 
            lat='latitude', 
            lon='longitude',
            size='mag', 
            color='risk',
            color_discrete_map={'Low': '#22c55e', 'Medium': '#eab308', 'High': '#ef4444'},
            hover_name='place', 
            hover_data={'mag': True, 'depth': True, 'time': True, 'latitude': False, 'longitude': False},
            zoom=1.2, 
            height=600,
            title="Interactive Earthquake Epicenters Map (Color-coded by Risk Level)"
        )
        fig_map.update_layout(
            mapbox_style='carto-darkmatter',
            margin={'r': 0, 't': 40, 'l': 0, 'b': 0},
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff',
            legend=dict(
                title="Risk Category",
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                bgcolor="rgba(15, 23, 42, 0.8)"
            )
        )
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.warning("No records to display on map for current filter selection.")
        
    st.markdown("---")
    
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        # Top 10 Places (Code Cell 17)
        st.subheader("Top 10 Earthquake Locations (Places)")
        top_places = df_filtered['place'].value_counts().head(10).reset_index()
        top_places.columns = ['place', 'count']
        
        fig_places = px.bar(
            top_places, 
            x='count', 
            y='place',
            orientation='h',
            title="Top 10 Locations (Jupyter Cell 17)",
            color_discrete_sequence=['#ef4444'],
            labels={'count': 'Earthquake Count', 'place': 'Location'}
        )
        fig_places.update_layout(
            template="plotly_dark",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            yaxis={'categoryorder': 'total ascending'},
            xaxis_title="Number of Earthquakes",
            yaxis_title=""
        )
        st.plotly_chart(fig_places, use_container_width=True)

    with col_g2:
        # Top 10 Countries (Code Cell 32)
        st.subheader("Top 10 Countries by Earthquake Count")
        top_countries = df_filtered['country'].value_counts().head(10).reset_index()
        top_countries.columns = ['country', 'count']
        
        fig_countries = px.bar(
            top_countries, 
            x='count', 
            y='country',
            orientation='h',
            title="Top 10 Countries (Jupyter Cell 32)",
            color='count',
            color_continuous_scale='viridis',
            labels={'count': 'Earthquake Count', 'country': 'Country'}
        )
        fig_countries.update_layout(
            template="plotly_dark",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            yaxis={'categoryorder': 'total ascending'},
            xaxis_title="Number of Earthquakes",
            yaxis_title=""
        )
        st.plotly_chart(fig_countries, use_container_width=True)
        
    st.markdown("---")
    
    # Hotspot Detection (Code Cell 28)
    st.subheader("🔥 Top Earthquake Hotspot Coordinates (Jupyter Cell 28)")
    hotspots = df_filtered.groupby(['latitude', 'longitude']).size().reset_index(name='Earthquake Count')
    hotspots = hotspots.sort_values(by='Earthquake Count', ascending=False).head(10).reset_index(drop=True)
    
    try:
        st.dataframe(
            hotspots.style.background_gradient(cmap='Oranges', subset=['Earthquake Count']),
            use_container_width=True
        )
    except ImportError:
        st.dataframe(hotspots, use_container_width=True)
