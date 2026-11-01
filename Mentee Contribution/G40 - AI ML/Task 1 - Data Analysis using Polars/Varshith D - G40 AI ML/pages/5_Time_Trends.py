"""
📈 Time Trends Page
"""

import streamlit as st
import pandas as pd

from utils.data_loader import load_data, yearly_averages, top_gainers_losers, get_available_years
from utils.charts import create_trend_line_chart, create_top_movers_chart, create_year_comparison_chart
from utils.config import get_custom_css, COLORS

st.markdown(get_custom_css(), unsafe_allow_html=True)

df = load_data()
available_years = sorted(get_available_years(df))

st.markdown(
    f"""
    <div style="font-size:2rem; font-weight:800; margin-bottom:1rem; color:{COLORS['text_primary']};">
        📈 Time Trend Analysis
    </div>
    <p style="color:{COLORS['text_secondary']};">
        Explore how global well-being and individual country rankings have evolved over the years.
    </p>
    """,
    unsafe_allow_html=True
)

# 1. Global Average Trend
st.markdown("### Global Average Life Evaluation Over Time")
yearly_avg_df = yearly_averages(df)
if not yearly_avg_df.empty:
    import plotly.express as px
    from utils.config import PLOTLY_LAYOUT_DEFAULTS
    
    fig_global = px.line(
        yearly_avg_df, 
        x='Year', 
        y='Life Evaluation',
        markers=True,
        title='Global Average Happiness Trend'
    )
    fig_global.update_traces(line_color=COLORS['accent_blue'], marker=dict(size=8))
    fig_global.update_layout(**PLOTLY_LAYOUT_DEFAULTS)
    st.plotly_chart(fig_global, use_container_width=True)
    
    # Calculate overall change
    first_year = yearly_avg_df['Year'].min()
    last_year = yearly_avg_df['Year'].max()
    first_val = yearly_avg_df[yearly_avg_df['Year'] == first_year]['Life Evaluation'].values[0]
    last_val = yearly_avg_df[yearly_avg_df['Year'] == last_year]['Life Evaluation'].values[0]
    trend_dir = "increased" if last_val > first_val else "decreased"
    
    st.info(f"💡 **Insight:** From {first_year} to {last_year}, the global average life evaluation score has {trend_dir} from {first_val:.2f} to {last_val:.2f}.")

st.markdown("<hr/>", unsafe_allow_html=True)

# 2. Top Movers
st.markdown("### Top Rank Movers")
if len(available_years) >= 2:
    st.sidebar.header("Trend Settings")
    c1, c2 = st.sidebar.columns(2)
    with c1:
        start_year = st.selectbox("Start Year", options=available_years, index=0)
    with c2:
        end_year = st.selectbox("End Year", options=available_years, index=len(available_years)-1)
    
    if start_year < end_year:
        gainers, losers = top_gainers_losers(df, start_year, end_year)
        if not gainers.empty and not losers.empty:
            fig_movers = create_top_movers_chart(gainers, losers)
            st.plotly_chart(fig_movers, use_container_width=True)
            
            st.info(f"💡 **Insight:** This chart highlights the countries that have improved or declined the most in rankings between {start_year} and {end_year}.")
        else:
            st.warning("Not enough overlapping countries between these two years to calculate movers.")
    else:
        st.warning("End Year must be greater than Start Year.")

st.markdown("<hr/>", unsafe_allow_html=True)

# 3. Country-specific Trend
st.markdown("### Individual Country Trend")
all_countries = sorted(df['Country name'].dropna().unique())
selected_country = st.selectbox("Select a country to view its historical trend", options=all_countries)

if selected_country:
    country_df = df[df['Country name'] == selected_country].sort_values('Year')
    if not country_df.empty:
        fig_country_trend = create_trend_line_chart(df, [selected_country], metric='Life Evaluation')
        st.plotly_chart(fig_country_trend, use_container_width=True)
        
        fig_country_rank = create_trend_line_chart(df, [selected_country], metric='Rank')
        fig_country_rank.update_yaxes(autorange="reversed") # Invert rank
        fig_country_rank.update_layout(title=f"Rank Trend for {selected_country}")
        st.plotly_chart(fig_country_rank, use_container_width=True)
