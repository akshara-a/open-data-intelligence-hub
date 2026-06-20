import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------
# PAGE CONFIG
# ----------------------------------
st.set_page_config(
    page_title="Olympic Performance Trends",
    page_icon="🏅",
    layout="wide"
)

# ----------------------------------
# LOAD DATA
# ----------------------------------
@st.cache_data
def load_data():
    DATA_URL = "https://drive.google.com/uc?export=download&id=1oywQz37FV_eBAEUWxOydAhZdER2oRcxM"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)
    df["WonMedal"] = df["Medal"].notna().astype(int)
    return df

    df["WonMedal"] = df["Medal"].notna().astype(int)

    return df

df = load_data()

# ----------------------------------
# SIDEBAR
# ----------------------------------
st.sidebar.title("Filters")

season_filter = st.sidebar.multiselect(
    "Season",
    options=df["Season"].unique(),
    default=df["Season"].unique()
)

year_range = st.sidebar.slider(
    "Year Range",
    int(df["Year"].min()),
    int(df["Year"].max()),
    (int(df["Year"].min()), int(df["Year"].max()))
)

filtered_df = df[
    (df["Season"].isin(season_filter))
    & (df["Year"] >= year_range[0])
    & (df["Year"] <= year_range[1])
]

# ----------------------------------
# TITLE
# ----------------------------------
st.title("🏅 Olympic Performance Trends Dashboard")

st.markdown(
    """
    Analyze Olympic athlete participation,
    medal trends, country performance,
    sports dominance, and demographics.
    """
)

# ----------------------------------
# KPI SECTION
# ----------------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Athletes", f"{filtered_df['Name'].nunique():,}")
col2.metric("Countries", f"{filtered_df['NOC'].nunique():,}")
col3.metric("Sports", f"{filtered_df['Sport'].nunique():,}")
col4.metric("Medals", f"{filtered_df['WonMedal'].sum():,}")

# ----------------------------------
# TABS
# ----------------------------------
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Overview",
        "Countries",
        "Sports",
        "Demographics"
    ]
)

# ==================================
# OVERVIEW
# ==================================
with tab1:

    st.subheader("Olympic Medal Trends")

    medals_by_year = (
        filtered_df[filtered_df["WonMedal"] == 1]
        .groupby("Year")
        .size()
        .reset_index(name="Medals")
    )

    fig = px.line(
        medals_by_year,
        x="Year",
        y="Medals",
        markers=True,
        title="Total Medals by Year"
    )

    st.plotly_chart(fig, use_container_width=True)

# ==================================
# COUNTRIES
# ==================================
with tab2:

    st.subheader("Country Performance")

    top_n = st.slider(
        "Select Top Countries",
        5,
        30,
        10
    )

    country_medals = (
        filtered_df[filtered_df["WonMedal"] == 1]
        .groupby("NOC")
        .size()
        .reset_index(name="Medals")
        .sort_values("Medals", ascending=False)
        .head(top_n)
    )

    fig = px.bar(
        country_medals,
        x="NOC",
        y="Medals",
        text="Medals",
        title="Top Countries by Medals"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(country_medals)

# ==================================
# SPORTS
# ==================================
with tab3:

    st.subheader("Top Sports")

    sport_medals = (
        filtered_df[filtered_df["WonMedal"] == 1]
        .groupby("Sport")
        .size()
        .reset_index(name="Medals")
        .sort_values("Medals", ascending=False)
        .head(20)
    )

    fig = px.bar(
        sport_medals,
        x="Medals",
        y="Sport",
        orientation="h",
        title="Top 20 Sports by Medal Count"
    )

    st.plotly_chart(fig, use_container_width=True)

# ==================================
# DEMOGRAPHICS
# ==================================
with tab4:

    st.subheader("Gender Distribution")

    gender = (
        filtered_df.groupby("Sex")
        .size()
        .reset_index(name="Count")
    )

    fig = px.pie(
        gender,
        names="Sex",
        values="Count",
        title="Male vs Female Athletes"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Age Distribution of Medal Winners")

    medalists = filtered_df[
        filtered_df["WonMedal"] == 1
    ]

    fig = px.histogram(
        medalists,
        x="Age",
        nbins=30,
        title="Age Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

# ----------------------------------
# COUNTRY TREND SECTION
# ----------------------------------
st.header("Country Medal Trend")

country = st.selectbox(
    "Choose Country",
    sorted(filtered_df["NOC"].unique())
)

country_trend = (
    filtered_df[
        (filtered_df["NOC"] == country)
        & (filtered_df["WonMedal"] == 1)
    ]
    .groupby("Year")
    .size()
    .reset_index(name="Medals")
)

fig = px.line(
    country_trend,
    x="Year",
    y="Medals",
    markers=True,
    title=f"{country} Medal Trend"
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------------------
# RAW DATA
# ----------------------------------
with st.expander("View Dataset"):
    st.dataframe(filtered_df)