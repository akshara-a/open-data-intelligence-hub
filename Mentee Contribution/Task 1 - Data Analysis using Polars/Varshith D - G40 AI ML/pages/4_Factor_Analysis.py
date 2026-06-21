"""
📊 Factor Analysis Page
"""

import streamlit as st
import pandas as pd

from utils.data_loader import load_data, compute_correlations, filter_by_year, get_available_years, get_latest_year
from utils.charts import create_correlation_heatmap, create_scatter_plot, create_factor_stacked_bar, create_box_violin_chart
from utils.config import get_custom_css, COLORS, FACTOR_COLUMNS, FACTOR_ORDER

st.markdown(get_custom_css(), unsafe_allow_html=True)

df = load_data()
available_years = get_available_years(df)
latest_year = get_latest_year(df)

st.markdown(
    f"""
    <div style="font-size:2rem; font-weight:800; margin-bottom:1rem; color:{COLORS['text_primary']};">
        📊 Factor Analysis
    </div>
    <p style="color:{COLORS['text_secondary']};">
        Understand how different factors (GDP, Social Support, Health, Freedom, Generosity, Corruption) 
        contribute to the overall Life Evaluation score.
    </p>
    """,
    unsafe_allow_html=True
)

st.sidebar.header("Analysis Settings")
selected_year = st.sidebar.selectbox(
    "Select Year for Static Analysis",
    options=["All Years"] + available_years,
    index=1
)

factor_to_highlight = st.sidebar.selectbox(
    "Select Factor to Highlight in Deep Dive",
    options=FACTOR_ORDER
)

if selected_year == "All Years":
    analysis_df = df.copy()
    year_label = "All Years"
else:
    analysis_df = filter_by_year(df, selected_year)
    year_label = str(selected_year)

if not analysis_df.empty:
    # 1. Factor Importance Overview
    st.markdown(f"### Factor Importance Overview ({year_label})")
    
    # Calculate mean contribution of each factor
    factor_means = {}
    for short_name, full_col in FACTOR_COLUMNS.items():
        if full_col in analysis_df.columns:
            factor_means[short_name] = analysis_df[full_col].mean()
    
    mean_df = pd.DataFrame(list(factor_means.items()), columns=['Factor', 'Mean Contribution']).sort_values('Mean Contribution', ascending=True)
    
    import plotly.express as px
    fig_importance = px.bar(
        mean_df, 
        x='Mean Contribution', 
        y='Factor', 
        orientation='h',
        color='Factor',
        color_discrete_map=COLORS, # Custom colors mapped if defined in config
        title=f"Average Contribution of Each Factor ({year_label})"
    )
    from utils.config import PLOTLY_LAYOUT_DEFAULTS
    fig_importance.update_layout(**PLOTLY_LAYOUT_DEFAULTS)
    fig_importance.update_layout(showlegend=False)
    st.plotly_chart(fig_importance, use_container_width=True)
    
    top_factor = mean_df.iloc[-1]['Factor']
    st.info(f"💡 **Insight:** On average, **{top_factor}** contributes the most to the Life Evaluation score across all countries in the selected timeframe.")

    st.markdown("<hr/>", unsafe_allow_html=True)
    
    # 2. Correlation Analysis
    st.markdown(f"### Correlation Analysis ({year_label})")
    
    # Compute full NxN correlation matrix
    cols_to_correlate = ['Life Evaluation'] + [col for col in FACTOR_COLUMNS.values() if col in analysis_df.columns]
    corr_matrix = analysis_df[cols_to_correlate].corr()
    
    # Rename index and columns to short names for the heatmap
    from utils.config import FACTOR_COLUMNS_REVERSE
    rename_dict = {full: short for full, short in FACTOR_COLUMNS_REVERSE.items()}
    corr_matrix = corr_matrix.rename(columns=rename_dict, index=rename_dict)
    
    if corr_matrix is not None and not corr_matrix.empty:
        fig_corr = create_correlation_heatmap(corr_matrix)
        st.plotly_chart(fig_corr, use_container_width=True)
        st.info("💡 **Insight:** This heatmap shows how strongly each factor correlates with Life Evaluation and with each other. A value closer to 1 (red) means a strong positive relationship.")

    st.markdown("<hr/>", unsafe_allow_html=True)
    
    # 3. Factor Deep Dive
    st.markdown(f"### Deep Dive: {factor_to_highlight} vs Life Evaluation")
    full_col_name = FACTOR_COLUMNS[factor_to_highlight]
    fig_scatter = create_scatter_plot(
        analysis_df, 
        x_col=full_col_name, 
        y_col='Life Evaluation', 
        color_col='Year' if selected_year == "All Years" else None
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.markdown("<hr/>", unsafe_allow_html=True)
    
    # 4. Factor Distribution
    st.markdown(f"### Distribution of {factor_to_highlight}")
    fig_dist = create_box_violin_chart(analysis_df, metric=full_col_name, group_by='Year' if selected_year == "All Years" else None)
    st.plotly_chart(fig_dist, use_container_width=True)
    
    st.markdown("<hr/>", unsafe_allow_html=True)
    
    # 5. Stacked Breakdown for top 20
    if selected_year != "All Years":
        st.markdown(f"### Factor Breakdown: Top 20 Countries ({year_label})")
        top_20 = analysis_df.nlargest(20, 'Life Evaluation')
        fig_stacked = create_factor_stacked_bar(top_20, int(selected_year))
        st.plotly_chart(fig_stacked, use_container_width=True)
else:
    st.warning("No data available for the selected analysis.")
