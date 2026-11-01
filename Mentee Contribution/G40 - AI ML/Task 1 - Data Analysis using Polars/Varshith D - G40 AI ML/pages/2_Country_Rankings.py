"""
🏆 Country Rankings Page
"""

import streamlit as st
import pandas as pd

from utils.data_loader import load_data, filter_by_year, get_available_years, get_latest_year
from utils.charts import create_ranking_bar_chart, create_confidence_interval_chart
from utils.config import get_custom_css, COLORS, format_score

st.markdown(get_custom_css(), unsafe_allow_html=True)

# Load data
df = load_data()
available_years = get_available_years(df)
latest_year = get_latest_year(df)

# Sidebar filters
with st.sidebar:
    st.header("Filters")
    selected_year = st.selectbox(
        "Select Year",
        options=available_years,
        index=available_years.index(latest_year)
    )
    
    top_n = st.slider("Top N Countries", min_value=5, max_value=50, value=20, step=5)
    
    search_term = st.text_input("Search Country", placeholder="e.g., Finland")

st.markdown(
    f"""
    <div style="font-size:2rem; font-weight:800; margin-bottom:1rem; color:{COLORS['text_primary']};">
        🏆 Country Rankings ({selected_year})
    </div>
    """,
    unsafe_allow_html=True
)

# Filter data
year_df = filter_by_year(df, selected_year)

# Compute metrics
if not year_df.empty:
    highest_score_row = year_df.loc[year_df['Life Evaluation'].idxmax()]
    lowest_score_row = year_df.loc[year_df['Life Evaluation'].idxmin()]
    median_score = year_df['Life Evaluation'].median()
    num_countries = len(year_df)

    # Metrics row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Highest Score", f"{highest_score_row['Country name']}", format_score(highest_score_row['Life Evaluation']))
    with c2:
        st.metric("Lowest Score", f"{lowest_score_row['Country name']}", format_score(lowest_score_row['Life Evaluation']))
    with c3:
        st.metric("Median Score", format_score(median_score))
    with c4:
        st.metric("Ranked Countries", str(num_countries))
    
    st.markdown("<hr/>", unsafe_allow_html=True)
    
    # Chart
    st.markdown("### Top Countries by Life Evaluation")
    fig_bar = create_ranking_bar_chart(year_df, top_n, selected_year)
    st.plotly_chart(fig_bar, use_container_width=True)
    
    st.info(f"💡 **Insight:** This chart shows the top {top_n} countries by Life Evaluation score in {selected_year}. The error bars indicate the 95% confidence interval.")

    # Table
    st.markdown("### Detailed Rankings")
    table_df = year_df[['Rank', 'Country name', 'Life Evaluation', 'Lower whisker', 'Upper whisker']].copy()
    if search_term:
        table_df = table_df[table_df['Country name'].str.contains(search_term, case=False, na=False)]
    
    st.dataframe(
        table_df.set_index('Rank'),
        use_container_width=True,
        column_config={
            "Life Evaluation": st.column_config.NumberColumn("Score", format="%.3f"),
            "Lower whisker": st.column_config.NumberColumn("Lower Bound", format="%.3f"),
            "Upper whisker": st.column_config.NumberColumn("Upper Bound", format="%.3f"),
        }
    )

    # Confidence Interval Chart
    st.markdown("### Confidence Intervals (Top 10)")
    top_10_countries = year_df.nlargest(10, 'Life Evaluation')['Country name'].tolist()
    fig_ci = create_confidence_interval_chart(year_df, top_10_countries)
    st.plotly_chart(fig_ci, use_container_width=True)
    st.info("💡 **Insight:** The confidence intervals show the statistical uncertainty of the estimates. Overlapping intervals mean the difference in rank might not be statistically significant.")
else:
    st.warning(f"No data available for {selected_year}.")
