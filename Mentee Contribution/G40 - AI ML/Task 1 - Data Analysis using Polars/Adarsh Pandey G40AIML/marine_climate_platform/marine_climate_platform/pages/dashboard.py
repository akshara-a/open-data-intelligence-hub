"""
Dashboard Page – Marine Climate Intelligence Platform
Shows KPI cards, temperature trends, sea-level rise, and a quick regional snapshot.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.helpers import (
    load_default_data, apply_theme, line_chart,
    compute_risk_scores, risk_label, risk_css_class, yearly_avg
)


def render_kpi_cards(df: pd.DataFrame):
    """Render the four top KPI metric cards."""
    recent_year = df["Date"].dt.year.max()
    recent      = df[df["Date"].dt.year == recent_year]
    prev        = df[df["Date"].dt.year == recent_year - 1]

    def delta(col, fmt=".2f"):
        r = recent[col].mean()
        p = prev[col].mean()
        d = r - p
        sign = "▲" if d > 0 else "▼"
        return r, f"{sign} {abs(d):{fmt}} vs prior year", "up" if d > 0 else "down"

    temp_val, temp_d, temp_dir   = delta("Sea_Surface_Temperature_C")
    sl_val,   sl_d,   sl_dir     = delta("Sea_Level_Rise_mm")
    ph_val,   ph_d,   ph_dir     = delta("Ocean_pH", ".4f")
    coral_val, coral_d, coral_dir = delta("Coral_Bleaching_Risk")

    cards = [
        ("🌡️", "SEA SURFACE TEMP", f"{temp_val:.1f} °C", temp_d, temp_dir, "#FF6B35"),
        ("🌊", "SEA LEVEL RISE",   f"{sl_val:.1f} mm",   sl_d,   sl_dir,   "#00E5FF"),
        ("🧪", "OCEAN pH",         f"{ph_val:.3f}",       ph_d,   ph_dir,   "#00BFA5"),
        ("🪸", "BLEACHING RISK",   f"{coral_val:.1f}%",   coral_d, coral_dir, "#FFB300"),
    ]

    cols = st.columns(4)
    for col, (icon, label, value, delta_txt, direction, accent) in zip(cols, cards):
        with col:
            st.markdown(f"""
            <div class="kpi-card" style="--accent-color:{accent}">
                <span class="kpi-icon">{icon}</span>
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-delta {direction}">{delta_txt}</div>
            </div>
            """, unsafe_allow_html=True)


def render_temperature_trend(df: pd.DataFrame):
    """Ocean temperature trend by region."""
    st.markdown("""
    <div class="section-header">
        <h3>🌡️ Sea Surface Temperature Trends</h3>
    </div>""", unsafe_allow_html=True)

    yearly = (df.groupby([df["Date"].dt.year, "Region"])["Sea_Surface_Temperature_C"]
                .mean().reset_index())
    yearly.columns = ["Year", "Region", "Avg_Temp_C"]

    fig = px.line(
        yearly, x="Year", y="Avg_Temp_C", color="Region",
        title="Annual Average Sea Surface Temperature by Region",
        labels={"Avg_Temp_C": "Avg Temp (°C)", "Year": "Year"},
        markers=True
    )
    fig = apply_theme(fig)
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)


def render_sea_level_chart(df: pd.DataFrame):
    """Sea level rise over time."""
    st.markdown("""
    <div class="section-header">
        <h3>🌊 Sea Level Rise Over Time</h3>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        sl = df.groupby(df["Date"].dt.year)["Sea_Level_Rise_mm"].mean().reset_index()
        sl.columns = ["Year", "Sea_Level_mm"]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=sl["Year"], y=sl["Sea_Level_mm"],
            fill="tozeroy",
            line=dict(color="#00E5FF", width=2.5),
            fillcolor="rgba(0,229,255,0.08)",
            name="Sea Level Rise"
        ))
        # Trend line
        z = pd.Series(sl["Sea_Level_mm"]).rolling(5).mean()
        fig.add_trace(go.Scatter(
            x=sl["Year"], y=z,
            line=dict(color="#FF6B35", width=2, dash="dash"),
            name="5-yr Moving Avg"
        ))
        fig = apply_theme(fig)
        fig.update_layout(
            title="Global Average Sea Level Rise (mm)",
            xaxis_title="Year", yaxis_title="Sea Level Rise (mm)",
            height=380
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # pH decline
        ph_yr = df.groupby(df["Date"].dt.year)["Ocean_pH"].mean().reset_index()
        ph_yr.columns = ["Year", "pH"]
        fig2 = px.area(ph_yr, x="Year", y="pH",
                       title="Ocean pH Decline",
                       labels={"pH": "pH Level"})
        fig2.update_traces(
            line_color="#00BFA5",
            fillcolor="rgba(0,191,165,0.1)"
        )
        fig2 = apply_theme(fig2)
        fig2.update_layout(height=380, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)


def render_regional_snapshot(df: pd.DataFrame):
    """Heatmap of regional risk indicators."""
    st.markdown("""
    <div class="section-header">
        <h3>🗺️ Regional Risk Snapshot</h3>
    </div>""", unsafe_allow_html=True)

    cols_of_interest = [
        "Sea_Surface_Temperature_C", "Sea_Level_Rise_mm",
        "Ocean_pH", "Coral_Bleaching_Risk", "Marine_Heat_Wave_Days"
    ]
    region_summary = df.groupby("Region")[cols_of_interest].mean().round(2)

    # Normalize for heatmap
    normed = (region_summary - region_summary.min()) / (region_summary.max() - region_summary.min())
    normed.columns = ["Temp", "Sea Level", "pH", "Coral Risk", "Heat Wave Days"]

    fig = px.imshow(
        normed,
        color_continuous_scale=[[0, "#00BFA5"], [0.5, "#FFB300"], [1, "#E53935"]],
        title="Normalised Risk Indicators by Region",
        aspect="auto",
        text_auto=".2f"
    )
    fig = apply_theme(fig)
    fig.update_layout(height=300, coloraxis_showscale=True)
    st.plotly_chart(fig, use_container_width=True)


def render_coral_trend(df: pd.DataFrame):
    """Coral bleaching risk over years."""
    yr_coral = df.groupby([df["Date"].dt.year, "Region"])["Coral_Bleaching_Risk"].mean().reset_index()
    yr_coral.columns = ["Year", "Region", "Risk"]

    fig = px.bar(
        yr_coral[yr_coral["Year"] >= 2015],
        x="Year", y="Risk", color="Region", barmode="group",
        title="Coral Bleaching Risk by Region (2015–2024)",
        labels={"Risk": "Bleaching Risk (%)"}
    )
    fig = apply_theme(fig)
    fig.update_layout(height=380)
    st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# Main entry point called from app.py
# ─────────────────────────────────────────────────────────────────────────────

def render(df: pd.DataFrame = None):
    if df is None:
        df = load_default_data()

    st.markdown("""
    <div class="page-header">
        <h1>🌊 Marine Climate Intelligence Dashboard</h1>
        <p>Real-time monitoring of ocean health indicators across global marine regions — 2000 to 2024.</p>
    </div>""", unsafe_allow_html=True)

    render_kpi_cards(df)

    st.markdown("")
    col_info = st.columns([3, 1])
    with col_info[1]:
        scores = compute_risk_scores(df)
        comp   = scores["composite"]
        label  = risk_label(comp)
        css    = risk_css_class(comp)
        st.markdown(f"""
        <div class="kpi-card" style="text-align:center; --accent-color:#00E5FF">
            <div class="kpi-label">Overall Risk Index</div>
            <div class="kpi-value" style="font-size:2.8rem">{comp}</div>
            <div style="margin-top:0.5rem">
                <span class="risk-badge {css}">{label}</span>
            </div>
            <div style="font-size:0.7rem; color:#90CAF9; margin-top:0.6rem">
                Composite of warming, acidification,<br>coral bleaching & sea level metrics
            </div>
        </div>""", unsafe_allow_html=True)
    with col_info[0]:
        render_temperature_trend(df)

    render_sea_level_chart(df)

    col3, col4 = st.columns(2)
    with col3:
        render_coral_trend(df)
    with col4:
        render_regional_snapshot(df)
