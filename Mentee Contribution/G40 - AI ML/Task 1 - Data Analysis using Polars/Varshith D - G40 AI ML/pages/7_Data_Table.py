"""
📋 Data Table Page
"""

import streamlit as st
import pandas as pd

from utils.data_loader import load_data, get_available_years
from utils.config import get_custom_css, COLORS, FACTOR_COLUMNS_REVERSE

st.markdown(get_custom_css(), unsafe_allow_html=True)

df = load_data()
available_years = get_available_years(df)

st.markdown(
    f"""
    <div style="font-size:2rem; font-weight:800; margin-bottom:1rem; color:{COLORS['text_primary']};">
        📋 Interactive Data Table
    </div>
    <p style="color:{COLORS['text_secondary']};">
        Filter, search, and download the raw data used in this dashboard.
    </p>
    """,
    unsafe_allow_html=True
)

# Sidebar Filters
st.sidebar.header("Data Filters")
selected_years = st.sidebar.multiselect(
    "Filter by Year",
    options=available_years,
    default=available_years
)

search_country = st.sidebar.text_input("Search Country", "")

# Apply Filters
filtered_df = df.copy()

if selected_years:
    filtered_df = filtered_df[filtered_df['Year'].isin(selected_years)]

if search_country:
    filtered_df = filtered_df[filtered_df['Country name'].str.contains(search_country, case=False, na=False)]

st.markdown(f"**Showing {len(filtered_df)} records**")

# Display Table
# Let's format the columns to make them more readable
display_df = filtered_df.copy()

# Rename columns back to short names for display if desired, or keep as is.
# We'll keep them as is but format the numbers.
cols_to_format = ['Life Evaluation', 'Lower whisker', 'Upper whisker'] + list(FACTOR_COLUMNS_REVERSE.keys())
for col in cols_to_format:
    if col in display_df.columns:
        display_df[col] = display_df[col].round(3)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

# Statistics
if not filtered_df.empty:
    st.markdown("### Summary Statistics for Filtered Data")
    numeric_cols = ['Life Evaluation'] + list(FACTOR_COLUMNS_REVERSE.keys())
    stats_df = filtered_df[numeric_cols].describe().T[['mean', '50%', 'min', 'max']].round(3)
    stats_df.columns = ['Mean', 'Median', 'Min', 'Max']
    
    # Rename index to short names for cleaner display
    stats_df.index = [FACTOR_COLUMNS_REVERSE.get(col, col) for col in stats_df.index]
    
    st.dataframe(stats_df, use_container_width=True)

# Export
st.markdown("### Export")
csv = filtered_df.to_csv(index=False).encode('utf-8')

c1, c2 = st.columns([1, 4])
with c1:
    st.download_button(
        label="📥 Download Data as CSV",
        data=csv,
        file_name='social_progress_data.csv',
        mime='text/csv',
    )
