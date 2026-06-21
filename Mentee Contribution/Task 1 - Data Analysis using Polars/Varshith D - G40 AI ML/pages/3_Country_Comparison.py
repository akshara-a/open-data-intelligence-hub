"""
🔄 Country Comparison Page
"""

import streamlit as st
import pandas as pd

from utils.data_loader import load_data, filter_by_countries, get_available_years, get_latest_year
from utils.charts import create_trend_line_chart, create_radar_chart, create_factor_comparison_grouped_bar, create_rank_bump_chart
from utils.config import get_custom_css, COLORS, FACTOR_COLUMNS, FACTOR_ORDER

st.markdown(get_custom_css(), unsafe_allow_html=True)

df = load_data()
available_years = get_available_years(df)
latest_year = get_latest_year(df)

st.markdown(
    f"""
    <div style="font-size:2rem; font-weight:800; margin-bottom:1rem; color:{COLORS['text_primary']};">
        🔄 Country Comparison
    </div>
    """,
    unsafe_allow_html=True
)

all_countries = sorted(df['Country name'].dropna().unique())
default_countries = ['Finland', 'Denmark'] if 'Finland' in all_countries and 'Denmark' in all_countries else all_countries[:2]

st.sidebar.header("Comparison Settings")
selected_countries = st.sidebar.multiselect(
    "Select Countries to Compare (2-5 recommended)",
    options=all_countries,
    default=default_countries,
    max_selections=5
)

selected_year = st.sidebar.selectbox(
    "Select Year for Static Comparisons",
    options=available_years,
    index=available_years.index(latest_year)
)

if len(selected_countries) < 2:
    st.warning("Please select at least 2 countries from the sidebar to view comparisons.")
else:
    comp_df = filter_by_countries(df, selected_countries)
    year_df = comp_df[comp_df['Year'] == selected_year]
    
    # 1. Metric Cards
    st.markdown(f"### Snapshot for {selected_year}")
    if not year_df.empty:
        cols = st.columns(len(selected_countries))
        for i, country in enumerate(selected_countries):
            country_data = year_df[year_df['Country name'] == country]
            with cols[i]:
                if not country_data.empty:
                    row = country_data.iloc[0]
                    
                    # Find best factor
                    factor_vals = {f: row.get(col, 0) for f, col in FACTOR_COLUMNS.items()}
                    best_factor = max(factor_vals, key=factor_vals.get)
                    best_val = factor_vals[best_factor]
                    
                    st.markdown(
                        f"""
                        <div class="glass-card" style="text-align: center;">
                            <h3 style="margin-top:0; color:{COLORS['accent_blue']};">{country}</h3>
                            <div style="font-size:2rem; font-weight:bold; color:{COLORS['text_primary']};">{row['Life Evaluation']:.3f}</div>
                            <div style="color:{COLORS['text_secondary']};">Rank: {int(row['Rank'])}</div>
                            <hr/>
                            <div style="font-size:0.9rem; color:{COLORS['text_muted']};">Top Factor</div>
                            <div style="font-weight:bold; color:{COLORS['accent_teal']};">{best_factor}</div>
                            <div style="font-size:0.8rem; color:{COLORS['text_secondary']};">({best_val:.3f})</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.info(f"No data for {country} in {selected_year}")
    else:
        st.warning(f"No data available for the selected countries in {selected_year}.")
        
    st.markdown("<br/>", unsafe_allow_html=True)
    
    # 2. Score Trend
    st.markdown("### Life Evaluation Trend")
    fig_trend = create_trend_line_chart(comp_df, selected_countries, metric='Life Evaluation')
    st.plotly_chart(fig_trend, use_container_width=True)
    st.info("💡 **Insight:** Observe how the overall life evaluation score has evolved over time for the selected countries.")
    
    # 3. Rank Change
    st.markdown("### Rank Change Over Time")
    fig_rank = create_rank_bump_chart(comp_df, selected_countries)
    st.plotly_chart(fig_rank, use_container_width=True)
    st.info("💡 **Insight:** This bump chart visualizes the relative ranking changes. A line going up means the rank improved (smaller rank number).")
    
    # 4. Factor Radar
    st.markdown(f"### Factor Profile Comparison ({selected_year})")
    if not year_df.empty:
        c1, c2 = st.columns([1, 1])
        with c1:
            fig_radar = create_radar_chart(year_df)
            st.plotly_chart(fig_radar, use_container_width=True)
        with c2:
            fig_bar = create_factor_comparison_grouped_bar([year_df], selected_countries)
            st.plotly_chart(fig_bar, use_container_width=True)
        
        st.info("💡 **Insight:** The radar chart shows the relative strengths of each country across different well-being factors. The bar chart provides absolute comparisons.")
