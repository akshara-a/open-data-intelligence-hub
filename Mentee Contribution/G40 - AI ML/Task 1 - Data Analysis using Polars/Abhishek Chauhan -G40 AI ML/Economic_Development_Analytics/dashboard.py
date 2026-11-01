import streamlit as st
import pandas as pd
import numpy as np
import polars as pl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import time
import warnings
warnings.filterwarnings('ignore')

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Economic Development Analytics",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .metric-card {
        background: linear-gradient(135deg, #1e2a3a, #162032);
        border: 1px solid #2e4060;
        border-radius: 12px;
        padding: 18px 22px;
        text-align: center;
        margin: 4px;
    }
    .metric-label { color: #8899aa; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; }
    .metric-value { color: #e8f4fd; font-size: 28px; font-weight: 700; }
    .metric-delta { font-size: 12px; margin-top: 4px; }
    .section-header {
        background: linear-gradient(90deg, #1f4e79, #2e75b6);
        color: white;
        padding: 10px 18px;
        border-radius: 8px;
        font-size: 16px;
        font-weight: 600;
        margin: 16px 0 12px 0;
    }
    .insight-box {
        background: #1a2332;
        border-left: 4px solid #2e75b6;
        border-radius: 0 8px 8px 0;
        padding: 12px 16px;
        margin: 8px 0;
        font-size: 14px;
        color: #c8d8e8;
    }
    .shock-badge {
        background: #3d1515;
        border: 1px solid #c0392b;
        color: #e74c3c;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }
    div[data-testid="stSidebar"] { background-color: #111827; }
    h1 { color: #e8f4fd !important; }
    h2, h3 { color: #a8c8e8 !important; }
    .stTabs [data-baseweb="tab"] { background-color: #1e2a3a; color: #8899aa; border-radius: 6px 6px 0 0; }
    .stTabs [aria-selected="true"] { background-color: #2e75b6 !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

COLORS = ['#2196F3','#FF9800','#4CAF50','#F44336','#9C27B0',
          '#795548','#E91E63','#00BCD4']

# ─── Data Loading ─────────────────────────────────────────────────────────────
@st.cache_data
def load_data(uploaded_file):
    df_raw = pd.read_csv(uploaded_file)

    # Clean column names
    df = df_raw.copy()
    df.columns = df.columns.str.replace(r'\s*\[YR\d+\]', '', regex=True).str.strip()

    # Drop 2025
    df = df.drop(columns=[c for c in ['2025'] if c in df.columns])

    id_cols = ['Country Name', 'Country Code', 'Series Name', 'Series Code']
    year_cols = [c for c in df.columns if c.isdigit()]

    df_long = df.melt(id_vars=id_cols, value_vars=year_cols, var_name='Year', value_name='Value')
    df_long['Year']  = df_long['Year'].astype(int)
    df_long['Value'] = pd.to_numeric(df_long['Value'], errors='coerce')
    df_long = df_long.dropna(subset=['Value'])
    df_long = df_long.rename(columns={
        'Country Name': 'Country', 'Country Code': 'Code',
        'Series Name': 'Indicator', 'Series Code': 'Indicator_Code'
    })

    indicator_map = {
        'Unemployment, total (% of total labor force) (modeled ILO estimate)': 'Unemployment %',
        'Poverty headcount ratio at $3.00 a day (2021 PPP) (% of population)': 'Poverty %',
        'GDP (current US$)': 'GDP',
        'GDP growth (annual %)': 'GDP Growth %',
        'GDP per capita (current US$)': 'GDP per Capita',
        'Inflation, consumer prices (annual %)': 'Inflation %',
        'Gini index': 'Gini Index',
        'Population, total': 'Population',
        'Life expectancy at birth, total (years)': 'Life Expectancy',
        'School enrollment, primary (% gross)': 'School Enrollment %',
        'Exports of goods and services (% of GDP)': 'Exports % GDP',
        'Access to electricity (% of population)': 'Electricity Access %'
    }
    df_long['Indicator_Short'] = df_long['Indicator'].map(indicator_map).fillna(df_long['Indicator'])
    return df_long

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌍 Economic Analytics")
    st.markdown("**World Bank WDI Data**")
    st.markdown("---")

    uploaded = st.file_uploader("Upload WDI_data.csv", type=['csv'], help="Upload your World Bank WDI_data.csv file")

    if uploaded:
        st.success("✅ File loaded")

    st.markdown("---")
    st.markdown("**About**")
    st.markdown("""
    - 📊 9 Countries · 12 Indicators
    - 📅 2000 – 2024
    - 🔧 NumPy · Pandas · Polars
    """)

# ─── Main Content ─────────────────────────────────────────────────────────────
st.markdown("# 🌍 Economic Development Analytics")
st.markdown("**Source:** World Bank — World Development Indicators (WDI) &nbsp;|&nbsp; **Period:** 2000–2024")
st.markdown("---")

if not uploaded:
    st.info("👈 Upload your **WDD.csv** file from the sidebar to begin.")
    st.markdown("""
    **How to get the file:**
    1. Go to [databank.worldbank.org](https://databank.worldbank.org)
    2. Select **World Development Indicators**
    3. Choose your countries, indicators, and years
    4. Download as **CSV** and upload here
    """)
    st.stop()

df_long = load_data(uploaded)
countries_all   = sorted(df_long['Country'].unique().tolist())
countries_noworld = [c for c in countries_all if c != 'World']
indicators      = sorted(df_long['Indicator_Short'].unique().tolist())
years           = sorted(df_long['Year'].unique().tolist())

# ─── KPI Row ──────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Countries</div>
        <div class="metric-value">{len(countries_all)}</div>
    </div>""", unsafe_allow_html=True)
with k2:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Indicators</div>
        <div class="metric-value">{len(indicators)}</div>
    </div>""", unsafe_allow_html=True)
with k3:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Years</div>
        <div class="metric-value">{min(years)}–{max(years)}</div>
    </div>""", unsafe_allow_html=True)
with k4:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Data Points</div>
        <div class="metric-value">{len(df_long):,}</div>
    </div>""", unsafe_allow_html=True)
with k5:
    gdp_world = df_long[(df_long['Country']=='World') & (df_long['Indicator_Short']=='GDP')].sort_values('Year').iloc[-1]['Value']
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">World GDP (Latest)</div>
        <div class="metric-value">${gdp_world/1e12:.1f}T</div>
    </div>""", unsafe_allow_html=True)

st.markdown("")

# ─── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 GDP Trends", "💸 Poverty & Inequality", "🧠 HDI Proxy",
    "🔥 Inflation Shocks", "📊 Dashboard"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — GDP TRENDS
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-header">📈 GDP Growth Rate Analysis</div>', unsafe_allow_html=True)

    col_ctrl, _ = st.columns([2, 3])
    with col_ctrl:
        selected_countries = st.multiselect(
            "Select countries", countries_noworld,
            default=countries_noworld, key="gdp_countries"
        )
        show_rolling = st.toggle("Show 3-year rolling average", value=True)

    if not selected_countries:
        st.warning("Select at least one country.")
    else:
        gdp_data = df_long[
            (df_long['Indicator_Short'] == 'GDP Growth %') &
            (df_long['Country'].isin(selected_countries))
        ].copy()

        gdp_pivot = gdp_data.pivot_table(index='Year', columns='Country', values='Value')

        # Rolling avg via numpy
        if show_rolling:
            gdp_array  = gdp_pivot.values
            rolling    = np.array([np.convolve(col, np.ones(3)/3, mode='same') for col in gdp_array.T]).T
            gdp_rolling = pd.DataFrame(rolling, index=gdp_pivot.index, columns=gdp_pivot.columns)

        fig, axes = plt.subplots(1, 2 if show_rolling else 1,
                                  figsize=(14, 5), facecolor='#0e1117')
        axes = [axes] if not show_rolling else axes

        for ax in axes:
            ax.set_facecolor('#0e1117')
            ax.tick_params(colors='#8899aa')
            ax.spines['bottom'].set_color('#2e4060')
            ax.spines['left'].set_color('#2e4060')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.yaxis.label.set_color('#8899aa')
            ax.xaxis.label.set_color('#8899aa')
            ax.title.set_color('#c8d8e8')

        ax1 = axes[0]
        for i, country in enumerate(gdp_pivot.columns):
            ax1.plot(gdp_pivot.index, gdp_pivot[country],
                     marker='o', markersize=3, linewidth=2,
                     label=country, color=COLORS[i % len(COLORS)])
        ax1.axhline(0, color='#e74c3c', linestyle='--', linewidth=1, alpha=0.6, label='Zero growth')
        ax1.axvspan(2019.5, 2020.5, alpha=0.12, color='red')
        ax1.text(2020, ax1.get_ylim()[0]*0.9 if ax1.get_ylim()[0] < 0 else -6,
                 'COVID\n2020', color='#e74c3c', fontsize=8, ha='center')
        ax1.set_title('Actual GDP Growth %', fontsize=13)
        ax1.set_xlabel('Year')
        ax1.set_ylabel('GDP Growth (%)')
        ax1.legend(fontsize=7, facecolor='#1e2a3a', edgecolor='#2e4060', labelcolor='#c8d8e8')
        ax1.grid(True, alpha=0.15, color='#2e4060')

        if show_rolling:
            ax2 = axes[1]
            for i, country in enumerate(gdp_rolling.columns):
                ax2.plot(gdp_rolling.index, gdp_rolling[country],
                         linewidth=2.5, label=country, color=COLORS[i % len(COLORS)])
            ax2.axhline(0, color='#e74c3c', linestyle='--', linewidth=1, alpha=0.6)
            ax2.set_title('3-Year Rolling Average', fontsize=13)
            ax2.set_xlabel('Year')
            ax2.legend(fontsize=7, facecolor='#1e2a3a', edgecolor='#2e4060', labelcolor='#c8d8e8')
            ax2.grid(True, alpha=0.15, color='#2e4060')

        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

        # Stats table
        st.markdown('<div class="section-header">Country Statistics</div>', unsafe_allow_html=True)
        stats = []
        for country in gdp_pivot.columns:
            data = gdp_pivot[country].dropna()
            rec  = data[data < 0].index.tolist()
            stats.append({
                'Country': country,
                'Avg Growth': f"{np.mean(data):.2f}%",
                'Best Year': f"{data.idxmax()} ({data.max():.1f}%)",
                'Worst Year': f"{data.idxmin()} ({data.min():.1f}%)",
                'Recessions': ', '.join(map(str, rec)) if rec else '—'
            })
        st.dataframe(pd.DataFrame(stats).set_index('Country'), use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — POVERTY & INEQUALITY
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-header">💸 Poverty vs GDP per Capita</div>', unsafe_allow_html=True)

    poverty = df_long[(df_long['Indicator_Short']=='Poverty %') & (df_long['Country']!='World')]
    gdp_pc  = df_long[(df_long['Indicator_Short']=='GDP per Capita') & (df_long['Country']!='World')]

    merged = pd.merge(
        poverty[['Country','Year','Value']].rename(columns={'Value':'Poverty'}),
        gdp_pc[['Country','Year','Value']].rename(columns={'Value':'GDP_PC'}),
        on=['Country','Year']
    ).dropna()

    if merged.empty:
        st.warning("No overlapping Poverty & GDP per Capita data found.")
    else:
        x = merged['GDP_PC'].values
        y = merged['Poverty'].values
        corr = np.corrcoef(x, y)[0, 1]

        # Manual linear regression
        x_n = x - x.mean()
        slope = np.sum(x_n * (y - y.mean())) / np.sum(x_n**2)
        intercept = y.mean() - slope * x.mean()
        x_line = np.linspace(x.min(), x.max(), 200)
        y_line  = slope * x_line + intercept

        fig, axes = plt.subplots(1, 2, figsize=(14, 5), facecolor='#0e1117')
        for ax in axes:
            ax.set_facecolor('#0e1117')
            ax.tick_params(colors='#8899aa')
            for sp in ['bottom','left']:  ax.spines[sp].set_color('#2e4060')
            for sp in ['top','right']:    ax.spines[sp].set_visible(False)
            ax.title.set_color('#c8d8e8')
            ax.xaxis.label.set_color('#8899aa')
            ax.yaxis.label.set_color('#8899aa')

        ax1 = axes[0]
        for i, c in enumerate(merged['Country'].unique()):
            sub = merged[merged['Country']==c]
            ax1.scatter(sub['GDP_PC'], sub['Poverty'],
                        color=COLORS[i % len(COLORS)], alpha=0.75, s=45, label=c)
        ax1.plot(x_line, y_line, color='#FFD700', linewidth=2,
                 linestyle='--', label=f'Trend (r={corr:.2f})')
        ax1.set_title('Poverty % vs GDP per Capita')
        ax1.set_xlabel('GDP per Capita (US$)')
        ax1.set_ylabel('Poverty % ($3/day)')
        ax1.legend(fontsize=7, facecolor='#1e2a3a', edgecolor='#2e4060', labelcolor='#c8d8e8')
        ax1.grid(True, alpha=0.15, color='#2e4060')

        ax2 = axes[1]
        latest = merged.sort_values('Year').groupby('Country').last().reset_index()
        latest = latest.sort_values('Poverty', ascending=True)
        bars = ax2.barh(latest['Country'], latest['Poverty'],
                        color=[COLORS[i % len(COLORS)] for i in range(len(latest))])
        ax2.set_title('Latest Poverty Rate by Country')
        ax2.set_xlabel('Poverty % ($3/day)')
        ax2.grid(True, alpha=0.15, color='#2e4060', axis='x')
        for bar, val in zip(bars, latest['Poverty']):
            ax2.text(bar.get_width()+0.5, bar.get_y()+bar.get_height()/2,
                     f'{val:.1f}%', va='center', fontsize=9, color='#c8d8e8')

        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

        c1, c2, c3 = st.columns(3)
        direction = "Strong Negative ✅" if corr < -0.5 else "Weak Negative" if corr < 0 else "Positive ⚠️"
        c1.metric("Pearson Correlation", f"{corr:.4f}")
        c2.metric("Relationship", direction)
        c3.metric("Regression Slope", f"{slope:.2e}")

        st.markdown(f"""<div class="insight-box">
        📌 <b>Interpretation:</b> A correlation of <b>{corr:.2f}</b> confirms a strong negative relationship —
        countries with higher GDP per capita consistently show lower poverty rates.
        The regression slope of {slope:.4f} means every $1,000 increase in GDP per capita
        is associated with a ~{abs(slope)*1000:.1f}% reduction in poverty rate.
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — HDI PROXY
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-header">🧠 Human Development Index (Proxy)</div>', unsafe_allow_html=True)

    components = {'Life Expectancy': 'life', 'School Enrollment %': 'edu', 'GDP per Capita': 'gdp'}
    dfs = []
    for ind, short in components.items():
        temp = df_long[(df_long['Indicator_Short']==ind) & (df_long['Country']!='World')][['Country','Year','Value']].rename(columns={'Value': short})
        dfs.append(temp)

    hdi_df = dfs[0]
    for d in dfs[1:]:
        hdi_df = pd.merge(hdi_df, d, on=['Country','Year'], how='inner')
    hdi_df = hdi_df.dropna()

    def minmax(arr): return (arr - arr.min()) / (arr.max() - arr.min())

    hdi_df['life_norm'] = minmax(hdi_df['life'].values)
    hdi_df['edu_norm']  = minmax(hdi_df['edu'].values)
    hdi_df['gdp_norm']  = minmax(np.log(hdi_df['gdp'].values))
    hdi_df['HDI_Proxy'] = (hdi_df['life_norm'] + hdi_df['edu_norm'] + hdi_df['gdp_norm']) / 3

    hdi_pivot = hdi_df.pivot_table(index='Year', columns='Country', values='HDI_Proxy')

    fig, axes = plt.subplots(1, 2, figsize=(14, 5), facecolor='#0e1117')
    for ax in axes:
        ax.set_facecolor('#0e1117')
        ax.tick_params(colors='#8899aa')
        for sp in ['bottom','left']:  ax.spines[sp].set_color('#2e4060')
        for sp in ['top','right']:    ax.spines[sp].set_visible(False)
        ax.title.set_color('#c8d8e8')
        ax.xaxis.label.set_color('#8899aa')
        ax.yaxis.label.set_color('#8899aa')

    ax1 = axes[0]
    for i, country in enumerate(hdi_pivot.columns):
        ax1.plot(hdi_pivot.index, hdi_pivot[country],
                 marker='o', markersize=3, linewidth=2,
                 label=country, color=COLORS[i % len(COLORS)])
    ax1.set_title('HDI Proxy Score Over Time (0–1)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('HDI Proxy Score')
    ax1.legend(fontsize=7, facecolor='#1e2a3a', edgecolor='#2e4060', labelcolor='#c8d8e8')
    ax1.grid(True, alpha=0.15, color='#2e4060')
    ax1.set_ylim(0, 1)

    ax2 = axes[1]
    latest_hdi = hdi_df.sort_values('Year').groupby('Country').last().reset_index()
    latest_hdi = latest_hdi.sort_values('HDI_Proxy', ascending=True)
    bars = ax2.barh(latest_hdi['Country'], latest_hdi['HDI_Proxy'],
                    color=[COLORS[i % len(COLORS)] for i in range(len(latest_hdi))])
    ax2.set_title('Latest HDI Proxy Ranking')
    ax2.set_xlabel('HDI Proxy (0 = low, 1 = high)')
    ax2.set_xlim(0, 1.15)
    ax2.grid(True, alpha=0.15, color='#2e4060', axis='x')
    for bar, val in zip(bars, latest_hdi['HDI_Proxy']):
        ax2.text(bar.get_width()+0.01, bar.get_y()+bar.get_height()/2,
                 f'{val:.3f}', va='center', fontsize=9, color='#c8d8e8')

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.markdown('<div class="section-header">Rankings</div>', unsafe_allow_html=True)
    ranking = latest_hdi.sort_values('HDI_Proxy', ascending=False)[['Country','HDI_Proxy','life','edu','gdp']].reset_index(drop=True)
    ranking.index += 1
    ranking.columns = ['Country', 'HDI Proxy', 'Life Exp (yrs)', 'School Enroll %', 'GDP per Capita']
    ranking['HDI Proxy'] = ranking['HDI Proxy'].apply(lambda x: f"{x:.4f}")
    ranking['Life Exp (yrs)'] = ranking['Life Exp (yrs)'].apply(lambda x: f"{x:.1f}")
    ranking['School Enroll %'] = ranking['School Enroll %'].apply(lambda x: f"{x:.1f}%")
    ranking['GDP per Capita'] = ranking['GDP per Capita'].apply(lambda x: f"${x:,.0f}")
    st.dataframe(ranking, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — INFLATION SHOCKS
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-header">🔥 Inflation Outlier Detection (Z-Score)</div>', unsafe_allow_html=True)

    inf_df = df_long[(df_long['Indicator_Short']=='Inflation %') & (df_long['Country']!='World')].copy()
    vals = inf_df['Value'].values
    mu, sigma = np.mean(vals), np.std(vals)
    inf_df['Z_Score'] = (vals - mu) / sigma
    inf_df['Shock']   = inf_df['Z_Score'].abs() > 2

    threshold = st.slider("Z-Score threshold for shock detection", 1.0, 3.0, 2.0, 0.1)
    inf_df['Shock'] = inf_df['Z_Score'].abs() > threshold

    fig, axes = plt.subplots(1, 2, figsize=(14, 5), facecolor='#0e1117')
    for ax in axes:
        ax.set_facecolor('#0e1117')
        ax.tick_params(colors='#8899aa')
        for sp in ['bottom','left']:  ax.spines[sp].set_color('#2e4060')
        for sp in ['top','right']:    ax.spines[sp].set_visible(False)
        ax.title.set_color('#c8d8e8')
        ax.xaxis.label.set_color('#8899aa')
        ax.yaxis.label.set_color('#8899aa')

    country_color = {c: COLORS[i % len(COLORS)] for i, c in enumerate(inf_df['Country'].unique())}

    ax1 = axes[0]
    for c in inf_df['Country'].unique():
        sub = inf_df[inf_df['Country']==c].sort_values('Year')
        ax1.plot(sub['Year'], sub['Value'], linewidth=1.5,
                 alpha=0.8, color=country_color[c], label=c)
    shocks = inf_df[inf_df['Shock']]
    ax1.scatter(shocks['Year'], shocks['Value'], color='#FFD700',
                zorder=5, s=100, marker='*', label=f'Shock |z|>{threshold}')
    ax1.axhline(mu, color='#00BCD4', linestyle='--', linewidth=1, label=f'Mean ({mu:.1f}%)')
    ax1.set_title('Inflation % — Shocks Highlighted')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Inflation (%)')
    ax1.legend(fontsize=7, facecolor='#1e2a3a', edgecolor='#2e4060', labelcolor='#c8d8e8')
    ax1.grid(True, alpha=0.15, color='#2e4060')

    ax2 = axes[1]
    z_pivot = inf_df.pivot_table(index='Country', columns='Year', values='Z_Score')
    im = ax2.imshow(z_pivot.values, cmap='RdYlGn_r', aspect='auto', vmin=-3, vmax=3)
    ax2.set_xticks(range(len(z_pivot.columns)))
    ax2.set_xticklabels(z_pivot.columns, rotation=45, fontsize=7, color='#8899aa')
    ax2.set_yticks(range(len(z_pivot.index)))
    ax2.set_yticklabels(z_pivot.index, fontsize=8, color='#8899aa')
    ax2.set_title('Z-Score Heatmap (Red = Shock)')
    cb = plt.colorbar(im, ax=ax2)
    cb.ax.tick_params(colors='#8899aa')
    cb.set_label('Z-Score', color='#8899aa')

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    col1, col2, col3 = st.columns(3)
    col1.metric("Global Mean Inflation", f"{mu:.2f}%")
    col2.metric("Std Deviation", f"{sigma:.2f}%")
    col3.metric("Shocks Detected", f"{inf_df['Shock'].sum()}")

    st.markdown('<div class="section-header">Detected Shock Events</div>', unsafe_allow_html=True)
    shock_table = shocks.sort_values('Z_Score', ascending=False)[['Country','Year','Value','Z_Score']].copy()
    shock_table.columns = ['Country', 'Year', 'Inflation %', 'Z-Score']
    shock_table['Inflation %'] = shock_table['Inflation %'].apply(lambda x: f"{x:.2f}%")
    shock_table['Z-Score']     = shock_table['Z-Score'].apply(lambda x: f"{x:.2f}")
    st.dataframe(shock_table.reset_index(drop=True), use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-header">📊 Summary Dashboard — All Indicators</div>', unsafe_allow_html=True)

    fig, axes = plt.subplots(2, 3, figsize=(18, 10), facecolor='#0e1117')
    fig.suptitle('Economic Development Analytics — Summary Dashboard',
                 fontsize=15, fontweight='bold', color='#e8f4fd', y=1.01)

    for ax in axes.flat:
        ax.set_facecolor('#0e1117')
        ax.tick_params(colors='#8899aa')
        for sp in ['bottom','left']:  ax.spines[sp].set_color('#2e4060')
        for sp in ['top','right']:    ax.spines[sp].set_visible(False)
        ax.title.set_color('#c8d8e8')
        ax.xaxis.label.set_color('#8899aa')
        ax.yaxis.label.set_color('#8899aa')

    # Panel 1: GDP Growth
    ax = axes[0, 0]
    for i, c in enumerate(countries_noworld):
        sub = df_long[(df_long['Country']==c) & (df_long['Indicator_Short']=='GDP Growth %')].sort_values('Year')
        ax.plot(sub['Year'], sub['Value'], linewidth=1.5, label=c, color=COLORS[i%len(COLORS)])
    ax.axhline(0, color='#e74c3c', linestyle='--', linewidth=0.8, alpha=0.6)
    ax.set_title('GDP Growth %')
    ax.legend(fontsize=6, facecolor='#1e2a3a', edgecolor='#2e4060', labelcolor='#c8d8e8')
    ax.grid(True, alpha=0.15, color='#2e4060')

    # Panel 2: Life Expectancy
    ax = axes[0, 1]
    for i, c in enumerate(countries_noworld):
        sub = df_long[(df_long['Country']==c) & (df_long['Indicator_Short']=='Life Expectancy')].sort_values('Year')
        ax.plot(sub['Year'], sub['Value'], linewidth=1.5, label=c, color=COLORS[i%len(COLORS)])
    ax.set_title('Life Expectancy (years)')
    ax.legend(fontsize=6, facecolor='#1e2a3a', edgecolor='#2e4060', labelcolor='#c8d8e8')
    ax.grid(True, alpha=0.15, color='#2e4060')

    # Panel 3: Electricity Access
    ax = axes[0, 2]
    latest_e = df_long[(df_long['Indicator_Short']=='Electricity Access %') & (df_long['Country']!='World')].sort_values('Year').groupby('Country').last().reset_index().sort_values('Value')
    ax.barh(latest_e['Country'], latest_e['Value'], color=[COLORS[i%len(COLORS)] for i in range(len(latest_e))])
    ax.axvline(100, color='#4CAF50', linestyle='--', linewidth=0.8)
    ax.set_title('Electricity Access % (Latest)')
    ax.grid(True, alpha=0.15, color='#2e4060', axis='x')

    # Panel 4: Unemployment
    ax = axes[1, 0]
    for i, c in enumerate(countries_noworld):
        sub = df_long[(df_long['Country']==c) & (df_long['Indicator_Short']=='Unemployment %')].sort_values('Year')
        ax.plot(sub['Year'], sub['Value'], linewidth=1.5, label=c, color=COLORS[i%len(COLORS)])
    ax.set_title('Unemployment %')
    ax.legend(fontsize=6, facecolor='#1e2a3a', edgecolor='#2e4060', labelcolor='#c8d8e8')
    ax.grid(True, alpha=0.15, color='#2e4060')

    # Panel 5: GDP per Capita
    ax = axes[1, 1]
    latest_g = df_long[(df_long['Indicator_Short']=='GDP per Capita') & (df_long['Country']!='World')].sort_values('Year').groupby('Country').last().reset_index().sort_values('Value')
    bars = ax.barh(latest_g['Country'], latest_g['Value'], color=[COLORS[i%len(COLORS)] for i in range(len(latest_g))])
    for bar, val in zip(bars, latest_g['Value']):
        ax.text(bar.get_width()+200, bar.get_y()+bar.get_height()/2, f'${val:,.0f}', va='center', fontsize=7, color='#c8d8e8')
    ax.set_title('GDP per Capita US$ (Latest)')
    ax.grid(True, alpha=0.15, color='#2e4060', axis='x')

    # Panel 6: HDI Proxy
    ax = axes[1, 2]
    if not hdi_pivot.empty:
        for i, c in enumerate(hdi_pivot.columns):
            ax.plot(hdi_pivot.index, hdi_pivot[c], linewidth=2, label=c, color=COLORS[i%len(COLORS)])
    ax.set_title('HDI Proxy Score (0–1)')
    ax.legend(fontsize=6, facecolor='#1e2a3a', edgecolor='#2e4060', labelcolor='#c8d8e8')
    ax.grid(True, alpha=0.15, color='#2e4060')
    ax.set_ylim(0, 1)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    # Summary stats
    st.markdown('<div class="section-header">Global Summary Statistics (NumPy)</div>', unsafe_allow_html=True)
    stats_rows = []
    for ind in ['GDP Growth %', 'Inflation %', 'Unemployment %', 'Life Expectancy']:
        d = df_long[(df_long['Indicator_Short']==ind) & (df_long['Country']!='World')]['Value'].dropna().values
        stats_rows.append({
            'Indicator': ind,
            'Mean': f"{np.mean(d):.2f}",
            'Std Dev': f"{np.std(d):.2f}",
            'Min': f"{np.min(d):.2f}",
            'Median': f"{np.median(d):.2f}",
            'Max': f"{np.max(d):.2f}",
        })
    st.dataframe(pd.DataFrame(stats_rows).set_index('Indicator'), use_container_width=True)