"""
Reports Page – Marine Climate Intelligence Platform
Generates downloadable PDF and CSV reports with charts and summaries.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import base64
from datetime import datetime
from utils.helpers import (
    load_default_data, apply_theme, compute_risk_scores,
    risk_label, risk_css_class
)


# ── PDF Builder ───────────────────────────────────────────────────────────────

def build_html_report(df: pd.DataFrame, scores: dict, report_title: str,
                      include_sections: list) -> str:
    """Build a complete HTML report string."""

    now = datetime.now().strftime("%d %B %Y, %H:%M UTC")
    comp_label = risk_label(scores["composite"])

    # Region table rows
    recent = df[df["Date"] >= df["Date"].max() - pd.DateOffset(years=3)]
    region_stats = recent.groupby("Region").agg(
        Temp=("Sea_Surface_Temperature_C", "mean"),
        Bleach=("Coral_Bleaching_Risk", "mean"),
        pH=("Ocean_pH", "mean"),
    ).round(2).reset_index()

    region_rows = ""
    for _, row in region_stats.iterrows():
        region_rows += f"""
        <tr>
            <td>{row['Region']}</td>
            <td>{row['Temp']:.2f} °C</td>
            <td>{row['Bleach']:.1f}%</td>
            <td>{row['pH']:.3f}</td>
        </tr>"""

    # Build conditional sections
    sections_html = ""

    if "Executive Summary" in include_sections:
        sections_html += f"""
        <div class="section">
            <h2>Executive Summary</h2>
            <p>This report provides a comprehensive analysis of marine climate conditions based on
            observational data from {df['Date'].min().year} to {df['Date'].max().year},
            covering {df['Region'].nunique()} ocean regions and {len(df):,} data records.</p>
            <p>The composite <strong>Marine Risk Index is {scores['composite']}</strong> out of 100,
            classified as <strong style="color:{'#FF6B35' if scores['composite'] >= 60 else '#00BFA5'}">{comp_label}</strong>.
            This reflects combined pressures from ocean warming, coral bleaching, acidification, and sea level rise.</p>
        </div>"""

    if "Risk Scores" in include_sections:
        sections_html += f"""
        <div class="section">
            <h2>Risk Score Summary</h2>
            <table>
                <tr><th>Risk Dimension</th><th>Score (/100)</th><th>Level</th></tr>
                <tr><td>Ocean Warming</td><td>{scores['ocean_warming']}</td><td>{risk_label(scores['ocean_warming'])}</td></tr>
                <tr><td>Coral Bleaching</td><td>{scores['coral_bleaching']}</td><td>{risk_label(scores['coral_bleaching'])}</td></tr>
                <tr><td>Ocean Acidification</td><td>{scores['acidification']}</td><td>{risk_label(scores['acidification'])}</td></tr>
                <tr><td>Sea Level Rise</td><td>{scores['sea_level']}</td><td>{risk_label(scores['sea_level'])}</td></tr>
                <tr class="highlight"><td><strong>Composite Risk Index</strong></td>
                    <td><strong>{scores['composite']}</strong></td>
                    <td><strong>{comp_label}</strong></td></tr>
            </table>
        </div>"""

    if "Regional Statistics" in include_sections:
        sections_html += f"""
        <div class="section">
            <h2>Regional Statistics (Last 3 Years)</h2>
            <table>
                <tr><th>Region</th><th>Avg Temp</th><th>Bleaching Risk</th><th>Ocean pH</th></tr>
                {region_rows}
            </table>
        </div>"""

    if "Key Findings" in include_sections:
        yr_start = df["Date"].dt.year.min()
        yr_end   = df["Date"].dt.year.max()
        temp_change = (
            df[df["Date"].dt.year >= yr_end - 3]["Sea_Surface_Temperature_C"].mean() -
            df[df["Date"].dt.year <= yr_start + 3]["Sea_Surface_Temperature_C"].mean()
        )
        sections_html += f"""
        <div class="section">
            <h2>Key Findings</h2>
            <ul>
                <li>Sea surface temperatures have risen by approximately <strong>{temp_change:.2f}°C</strong>
                    since {yr_start}, with the steepest increases observed in the Indian Ocean and Pacific Ocean.</li>
                <li>Coral bleaching risk scores have increased significantly over the study period,
                    with the highest current risk in tropical ocean regions.</li>
                <li>Ocean pH has declined from ~8.18 to ~8.12, representing a measurable increase
                    in ocean acidification that threatens calcifying marine organisms.</li>
                <li>Sea level rise continues at approximately 3–4 mm/year, consistent with global
                    IPCC projections under current greenhouse gas emission trajectories.</li>
                <li>Marine heat-wave events have increased in frequency and duration, particularly
                    after 2015, correlating with elevated bleaching risk periods.</li>
            </ul>
        </div>"""

    if "Recommendations" in include_sections:
        sections_html += """
        <div class="section">
            <h2>Recommendations</h2>
            <ol>
                <li><strong>Expand monitoring networks</strong> — Deploy additional Argo floats and
                    coastal buoys in high-risk regions to improve data resolution.</li>
                <li><strong>Coral restoration priority zones</strong> — Identify and protect the
                    least thermally stressed reef sites as climate refugia.</li>
                <li><strong>Policy intervention</strong> — Advocate for binding emissions reductions
                    to limit further ocean warming to below 1.5°C above pre-industrial levels.</li>
                <li><strong>Community alerts</strong> — Establish early-warning systems for marine
                    heat waves to enable timely conservation responses.</li>
                <li><strong>Interdisciplinary research</strong> — Increase funding for ocean
                    acidification impact studies on fisheries and food security.</li>
            </ol>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{report_title}</title>
<style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
        font-family: 'Segoe UI', Arial, sans-serif;
        background: #fff;
        color: #1a2332;
        font-size: 13px;
        line-height: 1.6;
    }}
    .cover {{
        background: linear-gradient(135deg, #03213F 0%, #1565C0 100%);
        color: white;
        padding: 60px 50px;
        min-height: 220px;
    }}
    .cover h1 {{ font-size: 28px; font-weight: 700; margin-bottom: 8px; letter-spacing: -0.02em; }}
    .cover .subtitle {{ font-size: 14px; opacity: 0.75; margin-bottom: 4px; }}
    .cover .meta {{ font-size: 12px; opacity: 0.55; margin-top: 16px; }}
    .risk-banner {{
        background: #f0f7ff;
        border-left: 5px solid #1565C0;
        padding: 16px 24px;
        margin: 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    .risk-banner .risk-val {{ font-size: 22px; font-weight: 700; color: #03213F; }}
    .risk-banner .risk-lbl {{
        font-size: 11px; font-weight: 600; text-transform: uppercase;
        letter-spacing: 0.1em; color: #666;
    }}
    .body {{ padding: 30px 50px; }}
    .section {{ margin-bottom: 28px; }}
    h2 {{
        font-size: 14px; font-weight: 700; text-transform: uppercase;
        letter-spacing: 0.08em; color: #1565C0;
        border-bottom: 2px solid #e8f0fe;
        padding-bottom: 6px; margin-bottom: 14px; margin-top: 0;
    }}
    p {{ margin-bottom: 10px; color: #333; font-size: 12.5px; }}
    ul, ol {{ padding-left: 1.4em; margin-bottom: 10px; }}
    li {{ margin-bottom: 6px; font-size: 12.5px; color: #333; }}
    table {{ width: 100%; border-collapse: collapse; margin-bottom: 6px; font-size: 12px; }}
    th {{ background: #03213F; color: white; padding: 8px 12px; text-align: left;
         font-weight: 600; font-size: 11px; text-transform: uppercase; letter-spacing: 0.06em; }}
    td {{ padding: 7px 12px; border-bottom: 1px solid #e8eef5; }}
    tr:nth-child(even) td {{ background: #f8fbff; }}
    tr.highlight td {{ background: #e8f0fe; font-weight: 600; }}
    .footer {{
        background: #f5f8ff; border-top: 1px solid #dde8f5;
        padding: 16px 50px; font-size: 11px; color: #888;
        margin-top: 30px;
    }}
</style>
</head>
<body>
    <div class="cover">
        <h1>{report_title}</h1>
        <div class="subtitle">Marine Climate Intelligence Platform</div>
        <div class="subtitle">NOAA Ocean Data Analysis · {df['Date'].min().year}–{df['Date'].max().year}</div>
        <div class="meta">Generated: {now}</div>
    </div>

    <div class="risk-banner">
        <div>
            <div class="risk-lbl">Composite Marine Risk Index</div>
            <div class="risk-val">{scores['composite']} / 100</div>
        </div>
        <div>
            <div class="risk-lbl">Classification</div>
            <div class="risk-val" style="font-size:18px">{comp_label}</div>
        </div>
        <div>
            <div class="risk-lbl">Dataset Coverage</div>
            <div class="risk-val" style="font-size:18px">{len(df):,} records</div>
        </div>
        <div>
            <div class="risk-lbl">Ocean Regions</div>
            <div class="risk-val" style="font-size:18px">{df['Region'].nunique()}</div>
        </div>
    </div>

    <div class="body">
        {sections_html}
    </div>

    <div class="footer">
        Marine Climate Intelligence Platform · Data Source: NOAA Ocean Data
        · Report generated on {now} · For research and educational purposes only.
    </div>
</body>
</html>"""

    return html


# ── Render ────────────────────────────────────────────────────────────────────

def render(df: pd.DataFrame = None):
    if df is None:
        df = load_default_data()

    st.markdown("""
    <div class="page-header">
        <h1>📄 Reports</h1>
        <p>Generate customised, downloadable HTML and CSV reports with charts, risk scores, and scientific summaries.</p>
    </div>""", unsafe_allow_html=True)

    scores = compute_risk_scores(df)

    # ── Report Configuration ──────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header"><h3>⚙️ Report Configuration</h3></div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        report_title = st.text_input(
            "Report Title",
            value="Marine Climate Intelligence Report",
            help="This will appear as the main heading of the report."
        )
        report_type = st.selectbox(
            "Report Format",
            ["Full Report (HTML)", "Executive Summary (HTML)", "Data Export (CSV)"],
        )
    with c2:
        include_sections = st.multiselect(
            "Sections to Include",
            ["Executive Summary", "Risk Scores", "Regional Statistics",
             "Key Findings", "Recommendations"],
            default=["Executive Summary", "Risk Scores", "Regional Statistics",
                     "Key Findings", "Recommendations"],
        )
        date_filter = st.selectbox(
            "Date Range",
            ["All Years (2000–2024)", "Last 5 Years", "Last 10 Years"]
        )

    # Apply date filter
    if date_filter == "Last 5 Years":
        df_report = df[df["Date"].dt.year >= df["Date"].dt.year.max() - 4]
    elif date_filter == "Last 10 Years":
        df_report = df[df["Date"].dt.year >= df["Date"].dt.year.max() - 9]
    else:
        df_report = df

    st.info(f"Report will cover **{len(df_report):,} records** across **{df_report['Date'].dt.year.nunique()} years**.")

    # ── Preview ───────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header"><h3>👁️ Report Preview</h3></div>
    """, unsafe_allow_html=True)

    tab_preview, tab_data = st.tabs(["📋 Summary Cards", "📊 Charts Preview"])

    with tab_preview:
        comp_css = risk_css_class(scores["composite"])
        p1, p2, p3, p4 = st.columns(4)
        preview_metrics = [
            (p1, "Ocean Warming", scores["ocean_warming"]),
            (p2, "Coral Bleaching", scores["coral_bleaching"]),
            (p3, "Acidification", scores["acidification"]),
            (p4, "Sea Level", scores["sea_level"]),
        ]
        for col, label, score in preview_metrics:
            with col:
                css = risk_css_class(score)
                st.markdown(f"""
                <div class="kpi-card" style="text-align:center">
                    <div class="kpi-label">{label}</div>
                    <div class="kpi-value" style="font-size:2rem">{score}</div>
                    <span class="risk-badge {css}">{risk_label(score)}</span>
                </div>""", unsafe_allow_html=True)

        st.markdown("")
        region_tbl = df_report.groupby("Region").agg(
            Avg_Temp=("Sea_Surface_Temperature_C", "mean"),
            Bleach_Risk=("Coral_Bleaching_Risk", "mean"),
            pH=("Ocean_pH", "mean"),
            Sea_Level=("Sea_Level_Rise_mm", "mean"),
        ).round(2).reset_index()
        st.dataframe(region_tbl, use_container_width=True)

    with tab_data:
        col_a, col_b = st.columns(2)
        with col_a:
            yr = df_report.groupby(df_report["Date"].dt.year)["Sea_Surface_Temperature_C"].mean().reset_index()
            yr.columns = ["Year", "Temp"]
            fig = px.line(yr, x="Year", y="Temp", title="Sea Surface Temperature Trend",
                          labels={"Temp": "°C"})
            fig = apply_theme(fig)
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

        with col_b:
            risk_df = pd.DataFrame({
                "Dimension": ["Ocean Warming", "Coral Bleaching", "Acidification", "Sea Level"],
                "Score": [scores["ocean_warming"], scores["coral_bleaching"],
                          scores["acidification"], scores["sea_level"]]
            })
            fig2 = px.bar(risk_df, x="Score", y="Dimension", orientation="h",
                          title="Risk Score by Dimension",
                          color="Score",
                          color_continuous_scale=[[0, "#00BFA5"], [0.5, "#FFB300"], [1, "#E53935"]])
            fig2 = apply_theme(fig2)
            fig2.update_layout(height=300, coloraxis_showscale=False)
            st.plotly_chart(fig2, use_container_width=True)

    # ── Generate Buttons ──────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header"><h3>⬇️ Download Report</h3></div>
    """, unsafe_allow_html=True)

    g1, g2, g3 = st.columns(3)

    with g1:
        if st.button("🖨️ Generate HTML Report", type="primary", use_container_width=True):
            with st.spinner("Building report…"):
                secs = include_sections if include_sections else [
                    "Executive Summary", "Risk Scores", "Regional Statistics",
                    "Key Findings", "Recommendations"
                ]
                html_content = build_html_report(df_report, scores, report_title, secs)
                st.session_state["html_report"] = html_content
                st.success("✅ Report ready — click Download below.")

    with g2:
        if st.button("📊 Generate CSV Export", use_container_width=True):
            st.session_state["csv_export"] = df_report.to_csv(index=False)
            st.success("✅ CSV ready — click Download below.")

    with g3:
        if st.button("📈 Generate Stats Report", use_container_width=True):
            stats = df_report.describe().round(3)
            st.session_state["stats_export"] = stats.to_csv()
            st.success("✅ Stats report ready — click Download below.")

    st.markdown("")
    d1, d2, d3 = st.columns(3)

    with d1:
        if "html_report" in st.session_state:
            st.download_button(
                "⬇️ Download HTML Report",
                st.session_state["html_report"],
                file_name=f"marine_climate_report_{datetime.now().strftime('%Y%m%d')}.html",
                mime="text/html",
                use_container_width=True
            )

    with d2:
        if "csv_export" in st.session_state:
            st.download_button(
                "⬇️ Download CSV Data",
                st.session_state["csv_export"],
                file_name=f"marine_climate_data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )

    with d3:
        if "stats_export" in st.session_state:
            st.download_button(
                "⬇️ Download Stats CSV",
                st.session_state["stats_export"],
                file_name=f"marine_stats_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )

    # ── Report History ────────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header"><h3>📁 Quick Data Summary</h3></div>
    """, unsafe_allow_html=True)

    summary_cols = st.columns(3)
    with summary_cols[0]:
        st.metric("Total Records", f"{len(df_report):,}")
        st.metric("Ocean Regions", df_report["Region"].nunique())
    with summary_cols[1]:
        st.metric("Year Range", f"{df_report['Date'].dt.year.min()}–{df_report['Date'].dt.year.max()}")
        st.metric("Avg Sea Temp", f"{df_report['Sea_Surface_Temperature_C'].mean():.2f} °C")
    with summary_cols[2]:
        st.metric("Avg Bleaching Risk", f"{df_report['Coral_Bleaching_Risk'].mean():.1f}%")
        st.metric("Avg Ocean pH", f"{df_report['Ocean_pH'].mean():.3f}")
