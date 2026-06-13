"""
Custom CSS styles for Marine Climate Intelligence Platform
"""

MAIN_CSS = """
<style>
    /* ── Google Fonts ── */
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ── Root Variables ── */
    :root {
        --deep-ocean: #03213F;
        --midnight-blue: #061E3C;
        --abyssal: #010D1E;
        --bioluminescent: #00E5FF;
        --thermal-orange: #FF6B35;
        --reef-teal: #00BFA5;
        --surface-blue: #1565C0;
        --foam-white: #E8F4FD;
        --text-primary: #E8F4FD;
        --text-secondary: #90CAF9;
        --card-bg: rgba(6, 30, 60, 0.85);
        --card-border: rgba(0, 229, 255, 0.15);
        --risk-low: #00BFA5;
        --risk-medium: #FFB300;
        --risk-high: #FF6B35;
        --risk-critical: #E53935;
    }

    /* ── Global Reset ── */
    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif !important;
        background-color: var(--abyssal) !important;
        color: var(--text-primary) !important;
    }

    /* ── Streamlit main container ── */
    .main .block-container {
        padding: 1.5rem 2rem 3rem;
        max-width: 1400px;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #03213F 0%, #010D1E 100%) !important;
        border-right: 1px solid rgba(0, 229, 255, 0.12);
    }
    [data-testid="stSidebar"] .block-container {
        padding: 1.5rem 1rem;
    }
    [data-testid="stSidebarNav"] a {
        color: #90CAF9 !important;
    }

    /* ── Page Header ── */
    .page-header {
        background: linear-gradient(135deg, rgba(3, 33, 63, 0.95) 0%, rgba(21, 101, 192, 0.3) 100%);
        border: 1px solid var(--card-border);
        border-radius: 16px;
        padding: 2rem 2.5rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    .page-header::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--bioluminescent), var(--reef-teal), var(--surface-blue));
    }
    .page-header h1 {
        font-size: 2rem;
        font-weight: 700;
        color: var(--foam-white) !important;
        margin: 0 0 0.4rem;
        letter-spacing: -0.02em;
    }
    .page-header p {
        font-size: 0.95rem;
        color: var(--text-secondary) !important;
        margin: 0;
    }

    /* ── KPI Cards ── */
    .kpi-card {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 14px;
        padding: 1.4rem 1.6rem;
        height: 100%;
        position: relative;
        overflow: hidden;
        transition: border-color 0.2s ease;
    }
    .kpi-card:hover { border-color: rgba(0, 229, 255, 0.35); }
    .kpi-card::after {
        content: '';
        position: absolute;
        bottom: 0; left: 0; right: 0;
        height: 2px;
        background: var(--accent-color, var(--bioluminescent));
        opacity: 0.6;
    }
    .kpi-icon {
        font-size: 1.6rem;
        margin-bottom: 0.6rem;
        display: block;
    }
    .kpi-label {
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: var(--text-secondary);
        margin-bottom: 0.3rem;
    }
    .kpi-value {
        font-size: 2.1rem;
        font-weight: 700;
        color: var(--foam-white);
        line-height: 1.1;
        font-family: 'JetBrains Mono', monospace;
    }
    .kpi-delta {
        font-size: 0.78rem;
        margin-top: 0.4rem;
        font-family: 'JetBrains Mono', monospace;
    }
    .kpi-delta.up { color: var(--thermal-orange); }
    .kpi-delta.down { color: var(--risk-low); }

    /* ── Section Headers ── */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        margin: 1.8rem 0 1rem;
        padding-bottom: 0.6rem;
        border-bottom: 1px solid rgba(0, 229, 255, 0.1);
    }
    .section-header h3 {
        font-size: 1rem;
        font-weight: 600;
        color: var(--bioluminescent) !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin: 0;
    }

    /* ── Info Panels ── */
    .info-panel {
        background: rgba(0, 191, 165, 0.08);
        border: 1px solid rgba(0, 191, 165, 0.25);
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        margin: 1rem 0;
    }
    .warning-panel {
        background: rgba(255, 107, 53, 0.08);
        border: 1px solid rgba(255, 107, 53, 0.25);
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        margin: 1rem 0;
    }

    /* ── Risk Badge ── */
    .risk-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }
    .risk-low    { background: rgba(0,191,165,0.15); color: #00BFA5; border: 1px solid rgba(0,191,165,0.3); }
    .risk-medium { background: rgba(255,179,0,0.15);  color: #FFB300; border: 1px solid rgba(255,179,0,0.3); }
    .risk-high   { background: rgba(255,107,53,0.15); color: #FF6B35; border: 1px solid rgba(255,107,53,0.3); }
    .risk-critical { background: rgba(229,57,53,0.15); color: #EF5350; border: 1px solid rgba(229,57,53,0.3); }

    /* ── Insight Card ── */
    .insight-card {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 14px;
        padding: 1.4rem 1.6rem;
        margin: 0.6rem 0;
    }
    .insight-card h4 {
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--bioluminescent) !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin: 0 0 0.6rem;
    }
    .insight-card p {
        font-size: 0.9rem;
        color: var(--text-secondary) !important;
        margin: 0;
        line-height: 1.6;
    }

    /* ── Streamlit widget overrides ── */
    .stSelectbox label, .stMultiSelect label, .stSlider label,
    .stDateInput label, .stTextInput label, .stTextArea label {
        color: var(--text-secondary) !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.04em !important;
    }
    div[data-baseweb="select"] > div {
        background-color: rgba(6,30,60,0.9) !important;
        border-color: var(--card-border) !important;
        color: var(--foam-white) !important;
    }
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: rgba(6,30,60,0.9) !important;
        border-color: var(--card-border) !important;
        color: var(--foam-white) !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #1565C0, #0D47A1) !important;
        color: white !important;
        border: 1px solid rgba(0,229,255,0.3) !important;
        border-radius: 8px !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #1976D2, #1565C0) !important;
        border-color: var(--bioluminescent) !important;
        box-shadow: 0 0 16px rgba(0,229,255,0.2) !important;
    }
    .stDownloadButton > button {
        background: linear-gradient(135deg, #00695C, #004D40) !important;
        color: white !important;
        border: 1px solid rgba(0,191,165,0.3) !important;
        border-radius: 8px !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(6,30,60,0.6) !important;
        border-radius: 8px !important;
        gap: 0.2rem;
        padding: 0.3rem;
    }
    .stTabs [data-baseweb="tab"] {
        color: var(--text-secondary) !important;
        border-radius: 6px !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(0,229,255,0.12) !important;
        color: var(--bioluminescent) !important;
    }
    [data-testid="metric-container"] {
        background: var(--card-bg) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
    }
    [data-testid="stMetricValue"] { color: var(--foam-white) !important; }
    [data-testid="stMetricDelta"] { font-family: 'JetBrains Mono', monospace !important; }

    /* ── DataFrame ── */
    .stDataFrame { border-radius: 10px; overflow: hidden; }
    .stDataFrame table { background: var(--card-bg) !important; }

    /* ── Divider ── */
    hr { border-color: rgba(0,229,255,0.1) !important; }

    /* ── Sidebar brand ── */
    .sidebar-brand {
        text-align: center;
        padding: 1rem 0 1.5rem;
        border-bottom: 1px solid rgba(0,229,255,0.1);
        margin-bottom: 1rem;
    }
    .sidebar-brand .brand-icon { font-size: 2.8rem; margin-bottom: 0.4rem; }
    .sidebar-brand h2 {
        font-size: 1rem;
        font-weight: 700;
        color: var(--foam-white) !important;
        margin: 0;
        letter-spacing: -0.01em;
    }
    .sidebar-brand p {
        font-size: 0.7rem;
        color: var(--text-secondary) !important;
        margin: 0.2rem 0 0;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: var(--abyssal); }
    ::-webkit-scrollbar-thumb { background: rgba(0,229,255,0.2); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(0,229,255,0.4); }

    /* ── Hide Streamlit chrome ── */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .stDeployButton { display: none; }
</style>
"""

PLOTLY_THEME = {
    "layout": {
        "paper_bgcolor": "rgba(6,30,60,0.0)",
        "plot_bgcolor": "rgba(6,30,60,0.0)",
        "font": {"family": "Space Grotesk, sans-serif", "color": "#90CAF9"},
        "title": {"font": {"color": "#E8F4FD", "size": 15, "family": "Space Grotesk"}},
        "xaxis": {
            "gridcolor": "rgba(0,229,255,0.06)",
            "linecolor": "rgba(0,229,255,0.15)",
            "tickfont": {"color": "#90CAF9"},
            "title": {"font": {"color": "#90CAF9"}}
        },
        "yaxis": {
            "gridcolor": "rgba(0,229,255,0.06)",
            "linecolor": "rgba(0,229,255,0.15)",
            "tickfont": {"color": "#90CAF9"},
            "title": {"font": {"color": "#90CAF9"}}
        },
        "legend": {"font": {"color": "#90CAF9"}, "bgcolor": "rgba(3,33,63,0.8)"},
        "colorway": ["#00E5FF", "#FF6B35", "#00BFA5", "#1565C0", "#FFB300", "#7C4DFF"],
    }
}
