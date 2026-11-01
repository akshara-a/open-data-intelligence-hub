"""
🏠 Home — Social Progress Analytics Dashboard.

Overview page showing dataset KPIs, top-level global insights,
about information, and quick navigation to other sections.
"""

from __future__ import annotations

import streamlit as st

from utils.config import (
    APP_TITLE,
    COLORS,
    get_custom_css,
    kpi_card_html,
    format_score,
)
from utils.data_loader import load_data, get_latest_year_data, get_latest_year

# ── Inject global theme CSS ─────────────────────────────────────────────────
st.markdown(get_custom_css(), unsafe_allow_html=True)

# ── Load data ────────────────────────────────────────────────────────────────
df = load_data()
latest_year = get_latest_year(df)
latest_df = get_latest_year_data(df)


# =============================================================================
# 1. Hero Section
# =============================================================================

st.markdown(
    f"""
    <style>
        @keyframes heroGlow {{
            0%, 100% {{ text-shadow: 0 0 20px rgba(59,130,246,0.3); }}
            50% {{ text-shadow: 0 0 40px rgba(59,130,246,0.5), 0 0 60px rgba(20,184,166,0.3); }}
        }}
        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to   {{ opacity: 1; transform: translateY(0); }}
        }}
        @keyframes gradientShift {{
            0%   {{ background-position: 0% 50%; }}
            50%  {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        .hero-container {{
            text-align: center;
            padding: 2.5rem 1rem 1.5rem;
            animation: fadeInUp 0.8s ease-out;
        }}
        .hero-title {{
            font-size: 2.8rem;
            font-weight: 800;
            letter-spacing: 0.06em;
            background: linear-gradient(135deg, {COLORS['accent_blue']}, {COLORS['accent_teal']},
                                                 {COLORS['accent_purple']}, {COLORS['accent_blue']});
            background-size: 300% 300%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: gradientShift 6s ease infinite, heroGlow 4s ease-in-out infinite;
            margin-bottom: 0.5rem;
            line-height: 1.15;
        }}
        .hero-subtitle {{
            font-size: 1.15rem;
            color: {COLORS['text_secondary']};
            font-weight: 400;
            max-width: 700px;
            margin: 0 auto;
            line-height: 1.6;
        }}
        .gradient-divider {{
            height: 3px;
            border: none;
            border-radius: 2px;
            background: linear-gradient(90deg,
                transparent 0%,
                {COLORS['accent_blue']} 20%,
                {COLORS['accent_teal']} 50%,
                {COLORS['accent_purple']} 80%,
                transparent 100%);
            margin: 1.8rem auto 2.2rem;
            max-width: 600px;
            opacity: 0.7;
        }}
    </style>

    <div class="hero-container">
        <div class="hero-title">SOCIAL PROGRESS ANALYTICS ENGINE</div>
        <p class="hero-subtitle">
            Exploring global well-being, happiness, and country performance
            from the World Happiness Report
        </p>
    </div>
    <hr class="gradient-divider">
    """,
    unsafe_allow_html=True,
)


# =============================================================================
# 2. Dataset Summary KPI Cards
# =============================================================================

total_countries: int = df["Country name"].nunique()
total_records: int = len(df)
year_min: int = int(df["Year"].min())
year_max: int = int(df["Year"].max())
avg_life_eval: float = float(df["Life Evaluation"].mean())

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        kpi_card_html(
            title="Total Countries",
            value=str(total_countries),
            icon="🌍",
        ),
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        kpi_card_html(
            title="Total Records",
            value=f"{total_records:,}",
            icon="📊",
        ),
        unsafe_allow_html=True,
    )
with c3:
    st.markdown(
        kpi_card_html(
            title="Year Range",
            value=f"{year_min} – {year_max}",
            icon="📅",
        ),
        unsafe_allow_html=True,
    )
with c4:
    st.markdown(
        kpi_card_html(
            title="Avg Life Evaluation",
            value=format_score(avg_life_eval),
            icon="⭐",
        ),
        unsafe_allow_html=True,
    )

st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)


# =============================================================================
# 3. Global Top-Level Insights
# =============================================================================

st.markdown(
    f"""
    <div style="
        font-size:1.35rem; font-weight:700;
        color:{COLORS['text_primary']};
        margin-bottom:0.6rem;
        display:flex; align-items:center; gap:0.5rem;
    ">
        <span style="font-size:1.4rem;">🏆</span>
        Global Insights — {latest_year}
    </div>
    <p style="color:{COLORS['text_secondary']}; font-size:0.92rem; margin-bottom:1.2rem;">
        Highlights from the most recent year in the dataset
    </p>
    """,
    unsafe_allow_html=True,
)

# ── Top 3 Happiest Countries ────────────────────────────────────────────────
top3 = (
    latest_df.sort_values("Life Evaluation", ascending=False)
    .head(3)
    .reset_index(drop=True)
)

MEDAL_STYLES: list[dict[str, str]] = [
    {
        "emoji": "🥇",
        "gradient": f"linear-gradient(135deg, #b8860b22, #ffd70015)",
        "border": "#ffd700",
        "label_color": "#ffd700",
    },
    {
        "emoji": "🥈",
        "gradient": f"linear-gradient(135deg, #c0c0c022, #e0e0e015)",
        "border": "#c0c0c0",
        "label_color": "#c0c0c0",
    },
    {
        "emoji": "🥉",
        "gradient": f"linear-gradient(135deg, #cd7f3222, #e8a86015)",
        "border": "#cd7f32",
        "label_color": "#cd7f32",
    },
]

cols = st.columns(3)
for idx, col in enumerate(cols):
    row = top3.iloc[idx]
    style = MEDAL_STYLES[idx]
    country_name = row["Country name"]
    score = format_score(float(row["Life Evaluation"]))
    rank_val = int(row["Rank"]) if "Rank" in row and not (row.get("Rank") is None) else idx + 1

    with col:
        st.markdown(
            f"""
            <div style="
                background: {style['gradient']};
                backdrop-filter: blur(16px);
                border: 1.5px solid {style['border']}44;
                border-radius: 16px;
                padding: 1.3rem 1.2rem;
                text-align: center;
                transition: transform 0.2s ease, border-color 0.2s ease;
            " onmouseenter="this.style.borderColor='{style['border']}88';this.style.transform='translateY(-3px)'"
               onmouseleave="this.style.borderColor='{style['border']}44';this.style.transform='translateY(0)'">
                <div style="font-size:2.2rem; margin-bottom:0.3rem;">{style['emoji']}</div>
                <div style="
                    font-size:0.72rem; font-weight:600;
                    color:{style['label_color']};
                    text-transform:uppercase;
                    letter-spacing:0.1em;
                    margin-bottom:0.25rem;
                ">Rank #{rank_val}</div>
                <div style="
                    font-size:1.2rem; font-weight:700;
                    color:{COLORS['text_primary']};
                    margin-bottom:0.3rem;
                ">{country_name}</div>
                <div style="
                    font-size:1.6rem; font-weight:800;
                    color:{style['label_color']};
                ">{score}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

# ── Additional global stats row ──────────────────────────────────────────────
global_avg_latest: float = float(latest_df["Life Evaluation"].mean())
num_years: int = df["Year"].nunique()

g1, g2 = st.columns(2)
with g1:
    st.markdown(
        kpi_card_html(
            title=f"Global Average ({latest_year})",
            value=format_score(global_avg_latest),
            icon="🌐",
        ),
        unsafe_allow_html=True,
    )
with g2:
    st.markdown(
        kpi_card_html(
            title="Years Covered",
            value=str(num_years),
            icon="🗓️",
        ),
        unsafe_allow_html=True,
    )

st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)


# =============================================================================
# 4. About This Dashboard
# =============================================================================

st.markdown(
    f"""
    <div style="
        background: {COLORS['bg_card']};
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid {COLORS['border']};
        border-radius: 16px;
        padding: 1.8rem 2rem;
        margin-bottom: 1.5rem;
        animation: fadeInUp 1s ease-out;
    ">
        <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.8rem;">
            <span style="font-size:1.4rem;">📖</span>
            <span style="font-size:1.2rem; font-weight:700; color:{COLORS['text_primary']};">
                About This Dashboard
            </span>
        </div>
        <p style="color:{COLORS['text_secondary']}; font-size:0.95rem; line-height:1.75; margin:0;">
            The <strong style="color:{COLORS['text_primary']};">{APP_TITLE}</strong> dashboard
            provides an interactive, data-driven exploration of global well-being using the
            <strong style="color:{COLORS['accent_teal']};">World Happiness Report</strong> dataset.
            It analyses how factors such as
            <strong style="color:{COLORS['accent_blue']};">GDP per capita</strong>,
            <strong style="color:{COLORS['accent_emerald']};">social support</strong>,
            <strong style="color:{COLORS['accent_gold']};">healthy life expectancy</strong>,
            <strong style="color:{COLORS['accent_purple']};">freedom</strong>,
            <strong style="color:{COLORS['accent_coral']};">generosity</strong>, and
            <strong style="color:{COLORS['accent_rose']};">perceptions of corruption</strong>
            contribute to the overall life evaluation score (Cantril ladder) of countries around
            the world. Use the sidebar to navigate between in-depth analytical sections covering
            rankings, trends, factor decomposition, country deep-dives, and more.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# =============================================================================
# 5. Quick Navigation Cards
# =============================================================================

st.markdown(
    f"""
    <div style="
        font-size:1.2rem; font-weight:700;
        color:{COLORS['text_primary']};
        margin-bottom:0.8rem;
        display:flex; align-items:center; gap:0.5rem;
    ">
        <span style="font-size:1.3rem;">🧭</span>
        Quick Navigation
    </div>
    <p style="color:{COLORS['text_secondary']}; font-size:0.9rem; margin-bottom:1.2rem;">
        Jump to any section of the dashboard
    </p>
    """,
    unsafe_allow_html=True,
)

NAV_CARDS: list[dict[str, str]] = [
    {
        "icon": "📊",
        "title": "Rankings & Scores",
        "description": "Compare countries by life evaluation scores with interactive bar charts and tables.",
        "color": COLORS["accent_blue"],
    },
    {
        "icon": "📈",
        "title": "Trends Over Time",
        "description": "Track how happiness scores have evolved across years for any country or region.",
        "color": COLORS["accent_teal"],
    },
    {
        "icon": "🧩",
        "title": "Factor Analysis",
        "description": "Decompose life evaluation into contributing factors and explore correlations.",
        "color": COLORS["accent_purple"],
    },
    {
        "icon": "🔍",
        "title": "Country Deep Dive",
        "description": "Get a detailed profile for any country including rank history, score breakdown, and comparisons.",
        "color": COLORS["accent_gold"],
    },
]

nav_cols = st.columns(len(NAV_CARDS))
for i, card in enumerate(NAV_CARDS):
    with nav_cols[i]:
        st.markdown(
            f"""
            <div style="
                background: {COLORS['bg_card']};
                backdrop-filter: blur(16px);
                -webkit-backdrop-filter: blur(16px);
                border: 1px solid {COLORS['border']};
                border-radius: 16px;
                padding: 1.4rem 1.2rem;
                min-height: 180px;
                transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
                cursor: pointer;
            " onmouseenter="this.style.borderColor='{card['color']}55';this.style.transform='translateY(-4px)';this.style.boxShadow='0 8px 30px {card['color']}15'"
               onmouseleave="this.style.borderColor='{COLORS['border']}';this.style.transform='translateY(0)';this.style.boxShadow='none'">
                <div style="font-size:2rem; margin-bottom:0.6rem;">{card['icon']}</div>
                <div style="
                    font-size:1rem; font-weight:700;
                    color:{card['color']};
                    margin-bottom:0.4rem;
                ">{card['title']}</div>
                <p style="
                    font-size:0.82rem;
                    color:{COLORS['text_muted']};
                    line-height:1.55;
                    margin:0;
                ">{card['description']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ── Footer spacer ───────────────────────────────────────────────────────────
st.markdown("<div style='height:3rem'></div>", unsafe_allow_html=True)
