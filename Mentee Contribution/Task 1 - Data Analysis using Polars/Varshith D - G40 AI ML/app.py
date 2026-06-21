"""
Main entry point for the Social Progress Analytics Engine.
"""

import streamlit as st
from utils.config import get_custom_css, APP_TITLE, APP_PAGE_ICON, APP_LAYOUT, APP_INITIAL_SIDEBAR_STATE, APP_SUBTITLE, APP_DESCRIPTION

# Must be the first Streamlit command
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_PAGE_ICON,
    layout=APP_LAYOUT,
    initial_sidebar_state=APP_INITIAL_SIDEBAR_STATE,
)

# Inject CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Sidebar setup
with st.sidebar:
    st.markdown(f"## {APP_PAGE_ICON} {APP_TITLE}")
    st.markdown(f"**{APP_SUBTITLE}**")
    st.markdown("---")
    st.markdown(APP_DESCRIPTION)
    st.markdown("---")
    st.markdown("Select a page above to navigate.")
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<small>Data source: World Happiness Report</small>", unsafe_allow_html=True)

# Main page content
# Since this is a multipage app, Streamlit uses the pages/ folder for navigation.
# However, if the user goes directly to the root URL, this file runs.
# Streamlit >= 1.30 actually auto-loads the first page in `pages/` alphabetically if we use native multipage navigation.
# If this file runs, we want it to act as a fallback or simply redirect/show the home page.
# The simplest approach is to import and run the Home page here, or just show a welcome message instructing them to use the sidebar.
st.markdown(f"# Welcome to {APP_TITLE}")
st.info("👈 Please select **Home** or any other section from the sidebar navigation to begin exploring the dashboard.")
