import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import joblib

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Global Happiness Analytics",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL CSS THEME
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Root palette ── */
:root {
    --bg-deep:      #0A0D14;
    --bg-card:      #111520;
    --bg-hover:     #161C2D;
    --accent-gold:  #F5C542;
    --accent-teal:  #2DD4BF;
    --accent-coral: #FF6B6B;
    --accent-indigo:#818CF8;
    --accent-green: #34D399;
    --text-primary: #EEF2FF;
    --text-muted:   #8892AA;
    --border:       rgba(129,140,248,0.15);
    --glow-gold:    rgba(245,197,66,0.25);
    --glow-teal:    rgba(45,212,191,0.20);
}

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg-deep) !important;
    color: var(--text-primary) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg-deep); }
::-webkit-scrollbar-thumb { background: var(--accent-indigo); border-radius: 4px; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--bg-card) !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * { color: var(--text-primary) !important; }
[data-testid="stSidebar"] .stSelectbox label { color: var(--accent-teal) !important; font-weight: 600; }

/* ── Main area padding ── */
.main .block-container { padding: 2rem 3rem 4rem; max-width: 1400px; }

/* ── Title ── */
h1 {
    font-family: 'Syne', sans-serif !important;
    font-size: 2.6rem !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, var(--accent-gold) 0%, var(--accent-teal) 60%, var(--accent-indigo) 100%);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    line-height: 1.2 !important;
    margin-bottom: 0.3rem !important;
}

/* ── Subheaders ── */
h2, h3 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
}

h2 { font-size: 1.55rem !important; }
h3 { font-size: 1.2rem !important; color: var(--accent-teal) !important; }

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.2rem 1.4rem !important;
    box-shadow: 0 0 24px var(--glow-gold);
    transition: transform .2s, box-shadow .2s;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 0 36px var(--glow-gold);
}
[data-testid="stMetricLabel"] {
    font-size: 0.78rem !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: var(--accent-gold) !important;
    font-weight: 600 !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.7rem !important;
    font-weight: 800 !important;
    color: var(--text-primary) !important;
}

/* ── Alert boxes ── */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border-left-width: 4px !important;
    font-size: 0.92rem !important;
}
div[data-baseweb="notification"]:has(.st-success) { background: rgba(52,211,153,.08) !important; border-color: var(--accent-green) !important; }
div[data-baseweb="notification"]:has(.st-error)   { background: rgba(255,107,107,.08) !important; border-color: var(--accent-coral) !important; }
div[data-baseweb="notification"]:has(.st-info)    { background: rgba(129,140,248,.08) !important; border-color: var(--accent-indigo) !important; }
div[data-baseweb="notification"]:has(.st-warning) { background: rgba(245,197,66,.08)  !important; border-color: var(--accent-gold) !important; }

/* ── Divider ── */
hr { border-color: var(--border) !important; margin: 1.6rem 0 !important; }

/* ── Expander ── */
[data-testid="stExpander"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
}
[data-testid="stExpander"] summary { color: var(--accent-indigo) !important; font-weight: 600; }

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
}

/* ── Number inputs & selects ── */
[data-testid="stNumberInput"] input,
[data-baseweb="select"] * {
    background: var(--bg-hover) !important;
    border-color: var(--border) !important;
    color: var(--text-primary) !important;
    border-radius: 8px !important;
}

/* ── Button ── */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, var(--accent-gold), var(--accent-teal)) !important;
    color: var(--bg-deep) !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.65rem 2rem !important;
    letter-spacing: 0.5px;
    transition: opacity .2s, transform .2s;
}
[data-testid="stButton"] > button:hover {
    opacity: 0.88;
    transform: translateY(-2px);
}

/* ── Section label helper ── */
.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 2.5px;
    color: var(--text-muted);
    margin-bottom: 0.5rem;
}

/* ── Insight cards (raw HTML) ── */
.insight-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.1rem 1.4rem;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: flex-start;
    gap: 0.9rem;
    box-shadow: 0 2px 16px rgba(0,0,0,.35);
}
.insight-icon {
    font-size: 1.5rem;
    flex-shrink: 0;
    margin-top: 2px;
}
.insight-text { font-size: 0.9rem; color: var(--text-primary); line-height: 1.55; }
.insight-label {
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 3px;
    font-weight: 600;
}

/* ── Score table ── */
.score-table { width:100%; border-collapse: collapse; font-size:0.88rem; }
.score-table th { color: var(--accent-gold); text-transform: uppercase; letter-spacing:1.2px; font-size:0.72rem; padding:8px 12px; border-bottom:1px solid var(--border); }
.score-table td { padding:9px 12px; border-bottom:1px solid var(--border); }
.score-table tr:last-child td { border-bottom:none; }

/* ── Tabs ── */
[data-baseweb="tab-list"] { background: var(--bg-card) !important; border-radius:10px; padding:4px; }
[data-baseweb="tab"] { color: var(--text-muted) !important; font-family:'Syne',sans-serif !important; font-weight:600; }
[aria-selected="true"][data-baseweb="tab"] {
    background: linear-gradient(135deg,var(--accent-gold),var(--accent-teal)) !important;
    color: var(--bg-deep) !important;
    border-radius:8px !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PLOTLY DARK TEMPLATE
# ─────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(17,21,32,0.6)",
    font=dict(family="DM Sans", color="#EEF2FF", size=12),
    title_font=dict(family="Syne", size=17, color="#EEF2FF"),
    colorway=["#F5C542","#2DD4BF","#818CF8","#FF6B6B","#34D399","#F472B6","#38BDF8"],
    xaxis=dict(gridcolor="rgba(129,140,248,0.1)", zerolinecolor="rgba(129,140,248,0.15)"),
    yaxis=dict(gridcolor="rgba(129,140,248,0.1)", zerolinecolor="rgba(129,140,248,0.15)"),
    margin=dict(t=50, b=30, l=20, r=20),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(129,140,248,0.2)"),
)

def apply_layout(fig, title=""):
    fig.update_layout(**PLOTLY_LAYOUT, title=title)
    return fig

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_excel("data/WHR26_Data_Figure_2.1.xlsx")

df = load_data()

# Safe target discovery for the Year column (handles variations like 'year', 'Year', 'YEAR')
year_col = next((col for col in df.columns if col.lower() == 'year'), None)
if year_col is None:
    st.error("⚠️ Could not locate a 'Year' column inside your dataset. Please check your Excel structure.")
    st.stop()

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🌍 Global Happiness")
    st.markdown('<div class="section-label">Select Year</div>', unsafe_allow_html=True)
    selected_year = st.selectbox(
        "",
        sorted(df[year_col].unique(), reverse=True),
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown('<div class="section-label">Navigation</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.85rem; color:#8892AA; line-height:2;">
    📊 &nbsp; Dashboard Overview<br>
    🗺️ &nbsp; World Map<br>
    📈 &nbsp; Country Charts<br>
    🔄 &nbsp; Global Trend<br>
    ⚖️ &nbsp; Country Comparison<br>
    🔮 &nbsp; Predict Happiness
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.72rem; color:#8892AA; text-align:center; line-height:1.6;">
    Data source:<br>
    <span style="color:#818CF8;">World Happiness Report 2024</span>
    </div>
    """, unsafe_allow_html=True)

# Update row filtering to cleanly map against our discovered year column
year_df = df[df[year_col] == selected_year]

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("# 🌍 Global Happiness Analytics")
st.markdown(
    f'<div style="color:#8892AA; font-size:0.92rem; margin-bottom:1.5rem;">'
    f'Exploring wellbeing trends across nations &nbsp;·&nbsp; '
    f'<span style="color:#F5C542; font-weight:600;">{selected_year}</span>'
    f'</div>',
    unsafe_allow_html=True
)

# ─────────────────────────────────────────────
# KPI METRICS
# ─────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

happiest_country    = year_df.loc[year_df["Life evaluation (3-year average)"].idxmax(), "Country name"]
least_happy_country = year_df.loc[year_df["Life evaluation (3-year average)"].idxmin(), "Country name"]
avg_happiness       = round(year_df["Life evaluation (3-year average)"].mean(), 2)
num_countries       = year_df["Country name"].nunique()

col1.metric("🌐  Countries Analysed", num_countries)
col2.metric("😊  Avg Happiness Score", avg_happiness)
col3.metric("🏆  Happiest Nation", happiest_country)
col4.metric("📉  Lowest Happiness", least_happy_country)

st.divider()

# ─────────────────────────────────────────────
# KEY INSIGHTS CARDS
# ─────────────────────────────────────────────
correlation = df.corr(numeric_only=True)
if "Life evaluation (3-year average)" in correlation.columns:
    top_factor = (
        correlation["Life evaluation (3-year average)"]
        .drop("Life evaluation (3-year average)", errors="ignore")
        .sort_values(ascending=False)
        .index[0]
    )
else:
    top_factor = "Log GDP per capita"

st.markdown("## 📈 Key Insights")

c1, c2 = st.columns(2)
with c1:
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-icon">🏆</div>
        <div class="insight-text">
            <div class="insight-label" style="color:#F5C542;">Happiest Country · {selected_year}</div>
            <strong style="font-size:1.05rem;">{happiest_country}</strong> leads the world with the
            highest Life evaluation (3-year average) score of
            <strong style="color:#F5C542;">{year_df["Life evaluation (3-year average)"].max():.2f}</strong>.
        </div>
    </div>
    <div class="insight-card">
        <div class="insight-icon">📊</div>
        <div class="insight-text">
            <div class="insight-label" style="color:#818CF8;">Strongest Predictor</div>
            <strong style="color:#818CF8;">{top_factor}</strong> has the highest positive
            correlation with happiness scores across all nations.
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-icon">📉</div>
        <div class="insight-text">
            <div class="insight-label" style="color:#FF6B6B;">Lowest Happiness · {selected_year}</div>
            <strong style="font-size:1.05rem;">{least_happy_country}</strong> records the lowest
            score of <strong style="color:#FF6B6B;">{year_df["Life evaluation (3-year average)"].min():.2f}</strong>,
            highlighting significant global inequality in wellbeing.
        </div>
    </div>
    <div class="insight-card">
        <div class="insight-icon">💡</div>
        <div class="insight-text">
            <div class="insight-label" style="color:#2DD4BF;">Global Pattern</div>
            Nations with higher GDP, stronger social support, and better health outcomes
            consistently rank among the world's happiest countries.
        </div>
    </div>
    """, unsafe_allow_html=True)

# Analytics Summary Expander
with st.expander("📄 View Full Analytics Summary"):
    sc1, sc2 = st.columns([1, 1])
    with sc1:
        st.markdown(f"""
**Total Countries:** {num_countries}  
**Average Score:** {avg_happiness}  
**Happiest Nation:** {happiest_country}  
**Least Happy:** {least_happy_country}  
**Top Predictor:** {top_factor}
        """)
    with sc2:
        st.markdown("""
> Countries with robust social support systems, high GDP per capita,  
> and strong healthy life expectancy consistently achieve the highest  
> happiness scores — underscoring the multidimensional nature of wellbeing.
        """)

st.divider()

# ─────────────────────────────────────────────
# WORLD MAP
# ─────────────────────────────────────────────
st.markdown("## 🗺️ Global Happiness Map")

# Clean up any accidental whitespaces in the country names column
year_df["Country name"] = year_df["Country name"].astype(str).str.strip()

fig_map = px.choropleth(
    year_df,
    locations="Country name",
    locationmode="country names",  # <-- Explicitly tells Plotly to parse names instead of codes
    color="Life evaluation (3-year average)",
    hover_name="Country name",
    color_continuous_scale=[
        (0.0, "#FF6B6B"),
        (0.4, "#F5C542"),
        (0.7, "#2DD4BF"),
        (1.0, "#34D399"),
    ],
    range_color=[year_df["Life evaluation (3-year average)"].min(), year_df["Life evaluation (3-year average)"].max()],
)
fig_map.update_layout(
    **PLOTLY_LAYOUT,
    title=f"Happiness Score by Country — {selected_year}",
    geo=dict(
        bgcolor="rgba(0,0,0,0)",
        landcolor="#1E2535",
        oceancolor="#0A0D14",
        showocean=True,
        lakecolor="#0A0D14",
        showland=True,
        showframe=False,
        coastlinecolor="rgba(129,140,248,0.25)",
        projection_type="natural earth",
    ),
    coloraxis_colorbar=dict(
        title=dict(
            text="Happiness",
            font=dict(color="#F5C542"),
        ),
        tickfont=dict(color="#8892AA", size=11),
        bgcolor="rgba(17,21,32,0.7)",
        bordercolor="rgba(129,140,248,0.2)",
    ),
)
st.plotly_chart(fig_map, use_container_width=True)

st.divider()

# ─────────────────────────────────────────────
# BAR + SCATTER SIDE BY SIDE
# ─────────────────────────────────────────────
st.markdown("## 📊 Country Rankings & GDP Relationship")

bc1, bc2 = st.columns([1, 1])

with bc1:
    top10 = year_df.sort_values("Life evaluation (3-year average)", ascending=False).head(10)
    fig1 = px.bar(
        top10,
        x="Life evaluation (3-year average)",
        y="Country name",
        orientation="h",
        color="Life evaluation (3-year average)",
        color_continuous_scale=["#2DD4BF", "#F5C542"],
        text=top10["Life evaluation (3-year average)"].round(2),
    )
    fig1.update_traces(textposition="outside", textfont_color="#EEF2FF")
    fig1.update_yaxes(categoryorder="total ascending")
    apply_layout(fig1, f"🏆 Top 10 Happiest Countries — {selected_year}")
    fig1.update_layout(showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(fig1, use_container_width=True)

with bc2:
    # Safely look for GDP column configuration matching dataset keys
    gdp_col = "Explained by: Log GDP per capita" if "Explained by: Log GDP per capita" in year_df.columns else year_df.columns[2]
    fig2 = px.scatter(
        year_df,
        x=gdp_col,
        y="Life evaluation (3-year average)",
        hover_name="Country name",
        color="Life evaluation (3-year average)",
        color_continuous_scale=["#FF6B6B", "#F5C542", "#2DD4BF"],
        size_max=14,
        opacity=0.85,
    )
    apply_layout(fig2, f"💰 GDP vs Happiness — {selected_year}")
    fig2.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ─────────────────────────────────────────────
# GLOBAL TREND
# ─────────────────────────────────────────────
st.markdown("## 🔄 Global Happiness Trend Over Time")

trend = df.groupby(year_col)["Life evaluation (3-year average)"].mean().reset_index()

fig3 = go.Figure()
fig3.add_trace(go.Scatter(
    x=trend[year_col],
    y=trend["Life evaluation (3-year average)"],
    mode="lines+markers",
    line=dict(color="#F5C542", width=3),
    marker=dict(size=9, color="#2DD4BF", line=dict(color="#F5C542", width=2)),
    fill="tozeroy",
    fillcolor="rgba(245,197,66,0.08)",
    hovertemplate="<b>%{x}</b><br>Avg Happiness: %{y:.3f}<extra></extra>",
))
apply_layout(fig3, "📈 Average Global Happiness Score (All Years)")
fig3.update_xaxes(dtick=1)
st.plotly_chart(fig3, use_container_width=True)

st.divider()

# ─────────────────────────────────────────────
# COUNTRY COMPARISON
# ─────────────────────────────────────────────
st.markdown("## ⚖️ Country Comparison")

countries = sorted(df["Country name"].unique())
cc1, cc2 = st.columns(2)

with cc1:
    country1 = st.selectbox("🔵 Country 1", countries, index=countries.index("India") if "India" in countries else 0)
with cc2:
    country2 = st.selectbox("🟡 Country 2", countries, index=countries.index("Finland") if "Finland" in countries else 1)

compare_df = year_df[year_df["Country name"].isin([country1, country2])].reset_index(drop=True)
st.dataframe(
    compare_df.style.set_properties(**{
        "background-color": "#111520",
        "color": "#EEF2FF",
        "border-color": "rgba(129,140,248,0.15)"
    }).highlight_max(subset=["Life evaluation (3-year average)"], color="#1A3A2A").highlight_min(subset=["Life evaluation (3-year average)"], color="#3A1A1A"),
    use_container_width=True
)

# Radar chart comparison mapping columns directly present in source Excel
radar_cols = [
    "Explained by: Log GDP per capita", 
    "Explained by: Social support",
    "Explained by: Healthy life expectancy",
    "Explained by: Freedom to make life choices",
    "Explained by: Generosity", 
    "Explained by: Perceptions of corruption"
]
available_radar = [c for c in radar_cols if c in compare_df.columns]

if len(compare_df) >= 1 and available_radar:
    fig_radar = go.Figure()
    colors = ["#2DD4BF", "#F5C542"]
    for i, (_, row) in enumerate(compare_df.iterrows()):
        vals = [row[c] for c in available_radar if pd.notna(row[c])]
        cols = [c.replace("Explained by: ", "") for c in available_radar if pd.notna(row[c])]
        fig_radar.add_trace(go.Scatterpolar(
            r=vals + [vals[0]],
            theta=cols + [cols[0]],
            fill="toself",
            fillcolor=f"rgba({','.join(str(int(int(colors[i].lstrip('#')[j:j+2], 16)) ) for j in (0,2,4))},0.15)",
            line=dict(color=colors[i], width=2),
            name=row["Country name"],
        ))
    fig_radar.update_layout(
        **PLOTLY_LAYOUT,
        title=f"🕸️ Happiness Factors Comparison — {country1} vs {country2}",
        polar=dict(
            bgcolor="rgba(17,21,32,0.5)",
            radialaxis=dict(visible=True, color="#8892AA", gridcolor="rgba(129,140,248,0.15)"),
            angularaxis=dict(color="#8892AA", gridcolor="rgba(129,140,248,0.1)"),
        ),
    )
    st.plotly_chart(fig_radar, use_container_width=True)

st.divider()

# ─────────────────────────────────────────────
# ML PREDICTION
# ─────────────────────────────────────────────
st.markdown("## 🔮 Happiness Score Predictor")
st.markdown(
    '<div style="color:#8892AA; font-size:0.88rem; margin-bottom:1.4rem;">'
    'Adjust the factors below and click <strong style="color:#F5C542;">Predict</strong> '
    'to estimate a country\'s happiness score using a trained ML model.</div>',
    unsafe_allow_html=True
)

model = joblib.load("models/happiness_model.pkl")

p1, p2, p3 = st.columns(3)
with p1:
    gdp        = st.number_input("💰 Log GDP per Capita Contribution",       value=1.0, step=0.1, format="%.2f")
    support    = st.number_input("🤝 Social Support Contribution",           value=1.0, step=0.01, format="%.2f")
with p2:
    health     = st.number_input("🏥 Healthy Life Expectancy Contribution",  value=1.0, step=0.5, format="%.1f")
    freedom    = st.number_input("🕊️ Freedom of Choice Contribution",        value=0.5, step=0.01, format="%.2f")
with p3:
    generosity = st.number_input("💝 Generosity Contribution",               value=0.1, step=0.01, format="%.2f")
    corruption = st.number_input("⚠️ Perceptions of Corruption Contribution", value=0.1, step=0.01, format="%.2f")

dystopia = st.number_input("🔮 Dystopia + Residual", value=1.5, step=0.1, format="%.2f")

if st.button("✨  Predict Happiness Score"):
    prediction = model.predict([[gdp, support, health, freedom, generosity, corruption, dystopia]])[0]

    score_color = (
        "#FF6B6B" if prediction < 3 else
        "#FF9B6B" if prediction < 5 else
        "#F5C542" if prediction < 6 else
        "#2DD4BF" if prediction < 7 else
        "#34D399"
    )
    emoji = "🔴" if prediction < 3 else "🟠" if prediction < 5 else "🟡" if prediction < 6 else "🟢" if prediction < 7 else "🌟"

    st.markdown(f"""
    <div style="
        background: var(--bg-card);
        border: 1px solid {score_color};
        border-radius: 16px;
        padding: 1.6rem 2rem;
        margin-top: 1rem;
        display: flex;
        align-items: center;
        gap: 1.4rem;
        box-shadow: 0 0 32px rgba({','.join(str(int(score_color.lstrip('#')[i:i+2],16)) for i in (0,2,4))}, 0.25);
    ">
        <div style="font-size:2.8rem;">{emoji}</div>
        <div>
            <div style="font-size:0.72rem; text-transform:uppercase; letter-spacing:2px; color:#8892AA; margin-bottom:4px;">
                Predicted Happiness Score
            </div>
            <div style="font-family:'Syne',sans-serif; font-size:3rem; font-weight:800; color:{score_color}; line-height:1;">
                {prediction:.2f}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("### 📊 Score Interpretation Guide")
st.markdown("""
<table class="score-table">
  <tr>
    <th>Score Range</th><th>Category</th><th>Indicator</th>
  </tr>
  <tr><td>0 – 3</td><td>Very Low Happiness</td><td>🔴 Critical</td></tr>
  <tr><td>3 – 5</td><td>Low Happiness</td><td>🟠 Below Average</td></tr>
  <tr><td>5 – 6</td><td>Moderate Happiness</td><td>🟡 Average</td></tr>
  <tr><td>6 – 7</td><td>High Happiness</td><td>🟢 Above Average</td></tr>
  <tr><td>7 – 10</td><td>Very High Happiness</td><td>🌟 Excellent</td></tr>
</table>
""", unsafe_allow_html=True)

st.divider()

# ─────────────────────────────────────────────
# FEATURE IMPORTANCE
# ─────────────────────────────────────────────
st.markdown("## 🧠 Model Feature Importance")

feature_names = [
    "Log GDP per capita",
    "Social support",
    "Healthy life expectancy",
    "Freedom to make life choices",
    "Generosity",
    "Perceptions of corruption",
    "Dystopia + residual",
]
importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": model.feature_importances_,
}).sort_values("Importance", ascending=True)

fig_imp = go.Figure(go.Bar(
    x=importance_df["Importance"],
    y=importance_df["Feature"],
    orientation="h",
    marker=dict(
        color=importance_df["Importance"],
        colorscale=[[0, "#818CF8"], [0.5, "#2DD4BF"], [1, "#F5C542"]],
        showscale=False,
    ),
    text=importance_df["Importance"].round(4),
    textposition="outside",
    textfont=dict(color="#EEF2FF", size=11),
))
apply_layout(fig_imp, "🧠 Feature Importance for Happiness Prediction")
st.plotly_chart(fig_imp, use_container_width=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; color:#8892AA; font-size:0.78rem; margin-top:3rem; padding-top:1.5rem; border-top:1px solid rgba(129,140,248,0.12);">
    🌍 &nbsp; Global Happiness Analytics &nbsp;·&nbsp; Powered by the World Happiness Report &nbsp;·&nbsp;
    Built with <span style="color:#F5C542;">Streamlit</span> &amp; <span style="color:#2DD4BF;">Plotly</span>
</div>
""", unsafe_allow_html=True)