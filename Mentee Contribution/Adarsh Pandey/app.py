"""
Marine Climate Intelligence Platform
=====================================
Main Streamlit application entry point.

Run:  streamlit run app.py
"""

import streamlit as st
from utils.styles import MAIN_CSS
from utils.helpers import load_default_data

# ── Page config (must be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="Marine Climate Intelligence Platform",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Inject global CSS ─────────────────────────────────────────────────────────
st.markdown(MAIN_CSS, unsafe_allow_html=True)

# ── Load shared data once (cached in session) ─────────────────────────────────
@st.cache_data(ttl=3600)
def get_default_data():
    return load_default_data()

df = get_default_data()

# ── Sidebar Navigation ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="brand-icon">🌊</div>
        <h2>Marine Climate</h2>
        <p>Intelligence Platform</p>
    </div>""", unsafe_allow_html=True)

    page = st.radio(
        "Navigate",
        options=[
            "🏠  Dashboard",
            "🔬  Data Explorer",
            "🤖  AI Climate Insights",
            "⚠️  Marine Risk Analysis",
            "📄  Reports",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.72rem; color:#546E7A; line-height:1.6; padding:0 0.2rem">
        <strong style="color:#90CAF9">Data Source</strong><br>
        NOAA Ocean Data · 2000–2024<br>
        5 Ocean Regions · 1,500 Records<br><br>
        <strong style="color:#90CAF9">Built with</strong><br>
        Streamlit · Plotly · Claude AI
    </div>
    """, unsafe_allow_html=True)

# ── Route to pages ────────────────────────────────────────────────────────────
if "Dashboard" in page:
    from pages import dashboard
    dashboard.render(df)

elif "Data Explorer" in page:
    from pages import data_explorer
    data_explorer.render(df)

elif "AI Climate Insights" in page:
    from pages import ai_insights
    ai_insights.render(df)

elif "Marine Risk Analysis" in page:
    from pages import risk_analysis
    risk_analysis.render(df)

elif "Reports" in page:
    from pages import reports
    reports.render(df)
