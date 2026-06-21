"""
🌍 Country Profile Page
"""

import streamlit as st
import pandas as pd

from utils.data_loader import load_data, get_country_profile, get_latest_year, filter_by_country
from utils.charts import create_trend_line_chart, create_factor_stacked_bar, create_radar_chart, create_rank_bump_chart
from utils.config import get_custom_css, COLORS, FACTOR_COLUMNS, format_score, kpi_card_html

st.markdown(get_custom_css(), unsafe_allow_html=True)

df = load_data()
latest_year = get_latest_year(df)

st.markdown(
    f"""
    <div style="font-size:2rem; font-weight:800; margin-bottom:1rem; color:{COLORS['text_primary']};">
        🌍 Country Profile Deep Dive
    </div>
    """,
    unsafe_allow_html=True
)

all_countries = sorted(df['Country name'].dropna().unique())
selected_country = st.selectbox(
    "Select a Country",
    options=all_countries,
    index=all_countries.index("Finland") if "Finland" in all_countries else 0
)

if selected_country:
    country_df = filter_by_country(df, selected_country).sort_values('Year')
    profile = get_country_profile(df, selected_country)
    
    if profile and not country_df.empty:
        latest_data = country_df.iloc[-1]
        current_year = int(latest_data['Year'])
        current_rank = int(latest_data['Rank'])
        current_score = latest_data['Life Evaluation']
        
        # Calculate rank change
        if len(country_df) > 1:
            prev_rank = int(country_df.iloc[-2]['Rank'])
            rank_change = prev_rank - current_rank # Positive means improvement (smaller rank)
            delta_str = f"+{rank_change}" if rank_change > 0 else str(rank_change)
            delta_color = COLORS['positive'] if rank_change > 0 else COLORS['negative'] if rank_change < 0 else COLORS['neutral']
        else:
            delta_str = None
            delta_color = None
            
        # Find best and worst factors for latest year
        factor_vals = {f: latest_data.get(col, 0) for f, col in FACTOR_COLUMNS.items()}
        best_factor = max(factor_vals, key=factor_vals.get)
        worst_factor = min(factor_vals, key=factor_vals.get)
        
        # 1. Summary Cards
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(kpi_card_html(f"Rank ({current_year})", str(current_rank), delta=f"Change: {delta_str}" if delta_str else None, delta_color=delta_color, icon="🏆"), unsafe_allow_html=True)
        with c2:
            st.markdown(kpi_card_html("Score", format_score(current_score), icon="⭐"), unsafe_allow_html=True)
        with c3:
            st.markdown(kpi_card_html("Strongest Factor", best_factor, icon="💪"), unsafe_allow_html=True)
        with c4:
            st.markdown(kpi_card_html("Weakest Factor", worst_factor, icon="⚠️"), unsafe_allow_html=True)
            
        st.markdown("<br/>", unsafe_allow_html=True)
        
        # 2. Narrative Insight
        st.markdown(
            f"""
            <div class="glass-card">
                <h4 style="margin-top:0; color:{COLORS['accent_gold']};">🤖 Automated Insight</h4>
                <p>
                    <strong>{selected_country}</strong> currently ranks <strong>{current_rank}</strong> in {current_year} with a score of <strong>{current_score:.3f}</strong>. 
                    Historically, its best rank was <strong>{profile['best_rank']}</strong> (in {profile['best_year']}) and its worst was <strong>{profile['worst_rank']}</strong> (in {profile['worst_year']}).
                    Currently, its well-being is most strongly supported by <strong>{best_factor}</strong> ({factor_vals[best_factor]:.3f}) and most limited by <strong>{worst_factor}</strong> ({factor_vals[worst_factor]:.3f}).
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # 3. Charts
        st.markdown("### Score and Rank Trends")
        c1, c2 = st.columns(2)
        with c1:
            fig_score = create_trend_line_chart(df, [selected_country], metric='Life Evaluation')
            st.plotly_chart(fig_score, use_container_width=True)
        with c2:
            fig_rank = create_rank_bump_chart(df, [selected_country])
            st.plotly_chart(fig_rank, use_container_width=True)
            
        st.markdown("### Factor Contribution Breakdown Over Time")
        fig_stacked = create_factor_stacked_bar(country_df, selected_country)
        st.plotly_chart(fig_stacked, use_container_width=True)
        
        st.markdown(f"### Factor Profile ({current_year})")
        # Need to pass a DataFrame with just one row for the radar chart
        latest_df = country_df[country_df['Year'] == current_year]
        fig_radar = create_radar_chart(latest_df)
        st.plotly_chart(fig_radar, use_container_width=True)

    else:
        st.warning("Insufficient data to build a complete profile for this country.")
