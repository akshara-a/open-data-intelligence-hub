"""
Marine Risk Analysis Page – Marine Climate Intelligence Platform
Calculates and visualises risk scores for coral bleaching, ocean warming, acidification, and sea level.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.helpers import (
    load_default_data, apply_theme, gauge_chart,
    compute_risk_scores, risk_label, risk_css_class
)


def render_risk_overview(scores: dict):
    """Top row of risk gauge cards."""
    st.markdown("""
    <div class="section-header"><h3>🎯 Risk Gauges</h3></div>
    """, unsafe_allow_html=True)

    g1, g2, g3, g4 = st.columns(4)
    gauge_specs = [
        (g1, scores["ocean_warming"],   "Ocean Warming Risk"),
        (g2, scores["coral_bleaching"], "Coral Bleaching Risk"),
        (g3, scores["acidification"],   "Acidification Risk"),
        (g4, scores["sea_level"],       "Sea Level Risk"),
    ]

    for col, score, title in gauge_specs:
        with col:
            st.plotly_chart(gauge_chart(score, title), use_container_width=True)
            label = risk_label(score)
            css   = risk_css_class(score)
            st.markdown(
                f'<div style="text-align:center; margin-top:-0.5rem">'
                f'<span class="risk-badge {css}">{label}</span></div>',
                unsafe_allow_html=True
            )


def render_composite_risk(scores: dict):
    """Composite risk score card + radar chart."""
    c_score = scores["composite"]
    c_label = risk_label(c_score)
    c_css   = risk_css_class(c_score)

    col_gauge, col_radar = st.columns([1, 2])

    with col_gauge:
        st.markdown("""
        <div class="section-header"><h3>🌐 Composite Risk</h3></div>
        """, unsafe_allow_html=True)
        st.plotly_chart(
            gauge_chart(c_score, "Overall Marine Risk Index", max_val=100),
            use_container_width=True
        )
        st.markdown(f"""
        <div style="text-align:center">
            <div class="kpi-value" style="font-size:2.4rem">{c_score}</div>
            <span class="risk-badge {c_css}">{c_label}</span>
            <p style="font-size:0.75rem; color:#90CAF9; margin-top:0.6rem">
                Composite of 4 risk dimensions
            </p>
        </div>""", unsafe_allow_html=True)

    with col_radar:
        st.markdown("""
        <div class="section-header"><h3>📡 Risk Profile Radar</h3></div>
        """, unsafe_allow_html=True)
        categories = ["Ocean Warming", "Coral Bleaching", "Acidification", "Sea Level"]
        values = [
            scores["ocean_warming"], scores["coral_bleaching"],
            scores["acidification"], scores["sea_level"]
        ]
        # Close the polygon
        categories += [categories[0]]
        values += [values[0]]

        fig = go.Figure(go.Scatterpolar(
            r=values, theta=categories,
            fill="toself",
            line=dict(color="#00E5FF", width=2),
            fillcolor="rgba(0,229,255,0.1)",
            name="Risk Score"
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], tickfont={"color": "#90CAF9"},
                                gridcolor="rgba(0,229,255,0.12)"),
                angularaxis=dict(tickfont={"color": "#E8F4FD"}, gridcolor="rgba(0,229,255,0.08)"),
                bgcolor="rgba(6,30,60,0.5)"
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"family": "Space Grotesk", "color": "#90CAF9"},
            showlegend=False,
            height=380,
            margin=dict(l=50, r=50, t=30, b=30)
        )
        st.plotly_chart(fig, use_container_width=True)


def render_region_risk_table(df: pd.DataFrame):
    """Risk breakdown table per region."""
    st.markdown("""
    <div class="section-header"><h3>🗺️ Regional Risk Breakdown</h3></div>
    """, unsafe_allow_html=True)

    recent = df[df["Date"] >= df["Date"].max() - pd.DateOffset(years=3)]
    grp = recent.groupby("Region").agg(
        Avg_Temp=("Sea_Surface_Temperature_C", "mean"),
        Avg_Bleaching_Risk=("Coral_Bleaching_Risk", "mean"),
        Avg_pH=("Ocean_pH", "mean"),
        Avg_Sea_Level=("Sea_Level_Rise_mm", "mean"),
        Heat_Wave_Days=("Marine_Heat_Wave_Days", "sum")
    ).round(2).reset_index()

    # Composite risk per region
    grp["Risk_Score"] = (
        (grp["Avg_Temp"] - grp["Avg_Temp"].min()) / (grp["Avg_Temp"].max() - grp["Avg_Temp"].min() + 1e-9) * 30 +
        grp["Avg_Bleaching_Risk"] * 0.25 +
        (8.2 - grp["Avg_pH"]) / 0.3 * 25 +
        (grp["Avg_Sea_Level"] / grp["Avg_Sea_Level"].max()) * 20
    ).clip(0, 100).round(1)

    grp["Risk_Label"] = grp["Risk_Score"].apply(risk_label)

    # Display with coloured risk labels
    display_df = grp[["Region", "Avg_Temp", "Avg_Bleaching_Risk", "Avg_pH", "Heat_Wave_Days", "Risk_Score", "Risk_Label"]]
    display_df.columns = ["Region", "Avg Temp (°C)", "Bleach Risk (%)", "pH", "Heat Wave Days", "Risk Score", "Risk Level"]

    st.dataframe(display_df, use_container_width=True, height=230)

    # Bar chart of risk scores
    fig = px.bar(
        grp.sort_values("Risk_Score", ascending=True),
        x="Risk_Score", y="Region", orientation="h",
        title="Risk Score by Region (last 3 years)",
        color="Risk_Score",
        color_continuous_scale=[[0, "#00BFA5"], [0.5, "#FFB300"], [1, "#E53935"]],
        labels={"Risk_Score": "Composite Risk Score"}
    )
    fig = apply_theme(fig)
    fig.update_layout(height=320, showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)


def render_warming_timeline(df: pd.DataFrame):
    """Ocean warming anomaly timeline."""
    st.markdown("""
    <div class="section-header"><h3>🌡️ Ocean Warming Anomaly Timeline</h3></div>
    """, unsafe_allow_html=True)

    baseline = df[df["Date"].dt.year <= 2005].groupby("Region")["Sea_Surface_Temperature_C"].mean()
    df_anom = df.copy()
    df_anom["Anomaly"] = df_anom.apply(
        lambda r: r["Sea_Surface_Temperature_C"] - baseline.get(r["Region"], np.nan), axis=1
    )

    yearly = df_anom.groupby([df_anom["Date"].dt.year, "Region"])["Anomaly"].mean().reset_index()
    yearly.columns = ["Year", "Region", "Anomaly_C"]

    fig = px.line(
        yearly, x="Year", y="Anomaly_C", color="Region",
        title="Temperature Anomaly from 2000–2005 Baseline (°C)",
        labels={"Anomaly_C": "Temp Anomaly (°C)"},
    )
    fig.add_hline(y=0, line_dash="dot", line_color="rgba(255,255,255,0.3)")
    fig.add_hrect(y0=1.5, y1=10, fillcolor="rgba(229,57,53,0.06)",
                  line_width=0, annotation_text="1.5°C threshold")
    fig = apply_theme(fig)
    fig.update_layout(height=380)
    st.plotly_chart(fig, use_container_width=True)


def render_coral_risk_map(df: pd.DataFrame):
    """Coral bleaching risk over time per region as a heatmap."""
    st.markdown("""
    <div class="section-header"><h3>🪸 Coral Bleaching Risk Over Time</h3></div>
    """, unsafe_allow_html=True)

    yearly = df.copy()
    yearly["Year"] = yearly["Date"].dt.year
    pivot = yearly.pivot_table(
        values="Coral_Bleaching_Risk", index="Region", columns="Year", aggfunc="mean"
    ).round(1)

    fig = px.imshow(
        pivot,
        color_continuous_scale=[[0, "#00BFA5"], [0.4, "#FFB300"], [0.7, "#FF6B35"], [1, "#E53935"]],
        title="Coral Bleaching Risk (%) by Region & Year",
        aspect="auto",
        text_auto=".0f"
    )
    fig = apply_theme(fig)
    fig.update_layout(height=320)
    st.plotly_chart(fig, use_container_width=True)


def render_risk_recommendations(scores: dict):
    """Contextual recommendations based on risk scores."""
    st.markdown("""
    <div class="section-header"><h3>💡 Risk-Based Recommendations</h3></div>
    """, unsafe_allow_html=True)

    recs = []

    if scores["ocean_warming"] >= 60:
        recs.append(("🌡️ Ocean Warming — High Priority",
                     "Sea surface temperatures are significantly elevated above baseline. "
                     "Immediate monitoring of marine heat-wave events and thermal stress on "
                     "marine organisms is recommended. Consider expanding mooring buoy networks."))
    else:
        recs.append(("🌡️ Ocean Warming — Monitor",
                     "Warming trends are within moderate bounds. Continue routine monitoring "
                     "and maintain historical baseline datasets for future comparison."))

    if scores["coral_bleaching"] >= 50:
        recs.append(("🪸 Coral Bleaching — Urgent Action",
                     "Bleaching risk levels are critically high. Deploy thermal stress alerts, "
                     "restrict tourism in high-risk reef zones, and accelerate coral restoration programs."))
    else:
        recs.append(("🪸 Coral Bleaching — Stable",
                     "Coral bleaching risk is within acceptable ranges. Maintain water quality "
                     "monitoring and protect existing reef ecosystems from local stressors."))

    if scores["acidification"] >= 50:
        recs.append(("🧪 Ocean Acidification — Concern",
                     "pH levels show a concerning downward trend. Shellfish and calcifying "
                     "organisms are at risk. Advocate for CO₂ emission reductions and study "
                     "alkalinity enhancement as a potential intervention."))

    if scores["sea_level"] >= 60:
        recs.append(("🌊 Sea Level Rise — Infrastructure Risk",
                     "Projected sea level rise poses risks to coastal communities. "
                     "Review coastal infrastructure resilience and update flood risk maps."))

    for title, body in recs:
        severity = "warning" if any(x in title for x in ["Urgent", "High", "Concern"]) else "info"
        st.markdown(f"""
        <div class="{'warning-panel' if severity == 'warning' else 'info-panel'}">
            <strong>{title}</strong><br>
            <span style="font-size:0.88rem; color:#E8F4FD">{body}</span>
        </div>""", unsafe_allow_html=True)


def render(df: pd.DataFrame = None):
    if df is None:
        df = load_default_data()

    st.markdown("""
    <div class="page-header">
        <h1>⚠️ Marine Risk Analysis</h1>
        <p>Quantified risk assessments for ocean warming, coral bleaching, acidification, and sea level rise across global marine regions.</p>
    </div>""", unsafe_allow_html=True)

    scores = compute_risk_scores(df)

    render_risk_overview(scores)
    st.markdown("")
    render_composite_risk(scores)
    render_region_risk_table(df)

    col_warm, col_coral = st.columns(2)
    with col_warm:
        render_warming_timeline(df)
    with col_coral:
        render_coral_risk_map(df)

    render_risk_recommendations(scores)
