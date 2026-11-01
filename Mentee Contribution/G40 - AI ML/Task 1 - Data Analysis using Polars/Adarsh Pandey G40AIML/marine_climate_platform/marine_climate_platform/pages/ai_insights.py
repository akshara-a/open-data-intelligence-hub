"""
AI Climate Insights Page – Marine Climate Intelligence Platform
Sends user questions + dataset summaries to Claude API for climate analysis.
"""

import streamlit as st
import pandas as pd
import json
import requests
from utils.helpers import load_default_data, compute_risk_scores, apply_theme
import plotly.express as px


ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-sonnet-4-20250514"

SYSTEM_PROMPT = """You are an expert marine climate scientist and data analyst for the Marine Climate Intelligence Platform.
Your role is to:
1. Analyze ocean and climate datasets provided as JSON summaries
2. Answer user questions about marine climate trends, risks, and projections
3. Provide clear, actionable insights and recommendations
4. Use scientific terminology but explain it in beginner-friendly terms
5. Always structure responses with clear sections: Key Findings, Trends, Risks, Recommendations

Be specific, cite numbers from the data, and highlight urgent concerns.
Format your responses with clear headings using **bold** text for section titles.
Keep responses informative but concise (300–500 words)."""


def build_data_context(df: pd.DataFrame) -> str:
    """Summarise the dataframe into a compact context string for the AI."""
    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    summary = {
        "dataset_overview": {
            "total_records": len(df),
            "date_range": f"{df['Date'].min().date()} to {df['Date'].max().date()}" if "Date" in df.columns else "N/A",
            "regions": df["Region"].unique().tolist() if "Region" in df.columns else [],
            "columns": list(df.columns),
        },
        "recent_averages": df[df["Date"] >= df["Date"].max() - pd.DateOffset(years=3)][numeric_cols]
                           .mean().round(3).to_dict() if "Date" in df.columns else {},
        "historical_averages": df[df["Date"].dt.year <= 2005][numeric_cols]
                               .mean().round(3).to_dict() if "Date" in df.columns else {},
        "trends": {
            col: "increasing" if df[col].corr(pd.Series(range(len(df)))) > 0.1
                 else "decreasing" if df[col].corr(pd.Series(range(len(df)))) < -0.1
                 else "stable"
            for col in numeric_cols[:6]
        },
        "risk_scores": compute_risk_scores(df),
    }
    return json.dumps(summary, indent=2, default=str)


def call_claude_api(user_question: str, data_context: str) -> str:
    """Call Claude API and return the response text."""
    messages = [
        {
            "role": "user",
            "content": f"""Here is the current marine climate dataset summary:

```json
{data_context}
```

User question: {user_question}

Please provide a thorough scientific analysis based on this data."""
        }
    ]

    payload = {
        "model": MODEL,
        "max_tokens": 1000,
        "system": SYSTEM_PROMPT,
        "messages": messages,
    }

    resp = requests.post(ANTHROPIC_API_URL, json=payload,
                         headers={"Content-Type": "application/json"})
    resp.raise_for_status()
    data = resp.json()
    return data["content"][0]["text"]


def render_quick_prompts():
    """Return a list of pre-built quick-analysis prompts."""
    return [
        "What are the most alarming climate trends in this dataset?",
        "Which ocean region faces the highest risk and why?",
        "How has coral bleaching risk changed over the last decade?",
        "What do the ocean pH trends mean for marine ecosystems?",
        "Summarise the key findings and provide 3 actionable recommendations.",
        "Compare warming rates across different ocean regions.",
    ]


def render(df: pd.DataFrame = None):
    if df is None:
        df = load_default_data()

    st.markdown("""
    <div class="page-header">
        <h1>🤖 AI Climate Insights</h1>
        <p>Ask questions about the marine dataset and receive AI-powered scientific analysis, trend summaries, and actionable recommendations.</p>
    </div>""", unsafe_allow_html=True)

    # ── Quick Prompts ──────────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header"><h3>⚡ Quick Analysis Prompts</h3></div>
    """, unsafe_allow_html=True)

    quick = render_quick_prompts()
    q_cols = st.columns(3)
    selected_prompt = None
    for i, prompt in enumerate(quick):
        with q_cols[i % 3]:
            if st.button(f"💬 {prompt[:45]}…" if len(prompt) > 45 else f"💬 {prompt}",
                         key=f"qprompt_{i}", use_container_width=True):
                selected_prompt = prompt

    st.markdown("---")

    # ── Custom Question Input ─────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header"><h3>💡 Ask Your Own Question</h3></div>
    """, unsafe_allow_html=True)

    default_q = selected_prompt or ""
    user_question = st.text_area(
        "Enter your marine climate question",
        value=default_q,
        height=100,
        placeholder="e.g. What is the projected sea level rise trajectory based on current trends?",
    )

    col_btn, col_info = st.columns([1, 3])
    with col_btn:
        analyze_btn = st.button("🔬 Analyse with AI", type="primary", use_container_width=True)
    with col_info:
        st.markdown("""
        <div style="font-size:0.78rem; color:#90CAF9; padding-top:0.6rem">
        The AI analyses your current dataset and provides scientific insights based on the actual numbers.
        </div>""", unsafe_allow_html=True)

    # ── AI Response ───────────────────────────────────────────────────────────
    if analyze_btn or selected_prompt:
        q = user_question.strip() if analyze_btn else (selected_prompt or "")
        if not q:
            st.warning("Please enter a question first.")
        else:
            with st.spinner("🌊 Analysing ocean data…"):
                try:
                    context = build_data_context(df)
                    response = call_claude_api(q, context)

                    st.markdown("""
                    <div class="section-header"><h3>📋 AI Analysis</h3></div>
                    """, unsafe_allow_html=True)

                    st.markdown(f"""
                    <div class="insight-card">
                        <h4>Question</h4>
                        <p style="color:#E8F4FD; font-style:italic;">"{q}"</p>
                    </div>""", unsafe_allow_html=True)

                    # Render the response with nice markdown
                    with st.container():
                        st.markdown(
                            f'<div class="insight-card"><p style="color:#E8F4FD; line-height:1.8">'
                            + response.replace("\n", "<br>") +
                            "</p></div>",
                            unsafe_allow_html=True
                        )

                    # Download button for the analysis
                    st.download_button(
                        "⬇️ Download Analysis",
                        f"Question:\n{q}\n\nAI Analysis:\n{response}",
                        file_name="marine_ai_analysis.txt",
                        mime="text/plain"
                    )

                except requests.exceptions.HTTPError as e:
                    st.error(f"API error: {e}. Check your Anthropic API key.")
                except Exception as e:
                    st.error(f"Analysis failed: {e}")

    # ── Data Summary Panel ─────────────────────────────────────────────────────
    with st.expander("📊 Dataset Summary Used by the AI"):
        try:
            context = build_data_context(df)
            st.json(json.loads(context))
        except Exception as e:
            st.error(f"Could not build context: {e}")

    # ── Automated Trend Cards ─────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header"><h3>📈 Automated Trend Snapshot</h3></div>
    """, unsafe_allow_html=True)

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if "Date" in df.columns and numeric_cols:
        df_y = df.copy()
        df_y["Year"] = df_y["Date"].dt.year
        yearly = df_y.groupby("Year")[numeric_cols[:4]].mean().reset_index()

        t1, t2 = st.columns(2)
        pairs = list(zip([t1, t2, t1, t2], numeric_cols[:4]))
        for container, col in pairs:
            with container:
                fig = px.area(yearly, x="Year", y=col,
                              title=col.replace("_", " "),
                              labels={col: col.replace("_", " ")})
                fig.update_traces(line_color="#00E5FF", fillcolor="rgba(0,229,255,0.07)")
                fig = apply_theme(fig)
                fig.update_layout(height=260, showlegend=False,
                                  margin=dict(l=10, r=10, t=35, b=10))
                st.plotly_chart(fig, use_container_width=True)
