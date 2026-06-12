<<<<<<< HEAD
import streamlit as st
import pandas as pd
import plotly.express as px

# PAGE CONFIG
st.set_page_config(
    page_title="World Population Intelligence Platform",
    page_icon="🌍",
    layout="wide"
)

# ---------------- TITLE ----------------
st.title("World Population Intelligence Platform")

st.markdown("""
### About Project

This platform analyzes global population trends using World Bank data.
Users can explore country-wise population growth, compare countries,
and visualize worldwide demographic changes through interactive charts.
""")

# LOAD DATA 
df = pd.read_csv(
    "API_SP.POP.TOTL_DS2_en_csv_v2_282912.csv",
    skiprows=4
)

# Remove empty rows
df = df.dropna(subset=["Country Name"])

# ---------------- FIND LATEST YEAR ----------------
year_columns = df.columns[4:]

latest_year = None

for col in reversed(year_columns):
    if df[col].notna().sum() > 0:
        latest_year = col
        break

# Convert all year columns to numeric
for col in year_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

valid_df = df.dropna(subset=[latest_year])

#  KPI CARDS 
st.subheader("Key Statistics")

total_countries = valid_df["Country Name"].nunique()
world_population = valid_df[latest_year].sum()

highest_country = valid_df.loc[
    valid_df[latest_year].idxmax(),
    "Country Name"
]

lowest_country = valid_df.loc[
    valid_df[latest_year].idxmin(),
    "Country Name"
]

col1, col2, col3, col4 = st.columns(4)

col1.metric("Countries", total_countries)
col2.metric("Latest Year", latest_year)
col3.metric("Highest Population", highest_country)
col4.metric("Lowest Population", lowest_country)

st.metric(
    "World Population",
    f"{world_population:,.0f}"
)

# DATASET PREVIEW
st.subheader("Dataset Preview")
st.dataframe(valid_df.head())

# TOP 10 COUNTRIES 
st.subheader("Top 10 Most Populated Countries")

top10 = valid_df.nlargest(10, latest_year)

fig1 = px.bar(
    top10,
    x="Country Name",
    y=latest_year,
    title=f"Top 10 Countries by Population ({latest_year})"
)

st.plotly_chart(fig1, use_container_width=True)

#  WORLD POPULATION TREND
st.subheader(" Global Population Growth Trend")

world_population_yearly = valid_df[year_columns].sum()

trend_df = pd.DataFrame({
    "Year": year_columns,
    "Population": world_population_yearly.values
})

fig2 = px.line(
    trend_df,
    x="Year",
    y="Population",
    title="World Population Growth Over Time"
)

st.plotly_chart(fig2, use_container_width=True)

# COUNTRY ANALYSIS
st.subheader("Country Population Analysis")

country = st.selectbox(
    "Select Country",
    sorted(valid_df["Country Name"].unique())
)

country_data = valid_df[
    valid_df["Country Name"] == country
]

country_trend = pd.DataFrame({
    "Year": year_columns,
    "Population": country_data.iloc[0, 4:].values
})

fig3 = px.line(
    country_trend,
    x="Year",
    y="Population",
    title=f"Population Trend - {country}"
)

st.plotly_chart(fig3, use_container_width=True)

# SEARCH
st.subheader("Search Country")

search = st.text_input("Enter Country Name")

if search:
    result = valid_df[
        valid_df["Country Name"].str.contains(
            search,
            case=False,
            na=False
        )
    ]

    if not result.empty:
        st.dataframe(
            result[["Country Name", latest_year]]
        )
    else:
        st.warning("Country not found")

# COUNTRY COMPARISON 
st.subheader("Compare Two Countries")

country1 = st.selectbox(
    "Country 1",
    sorted(valid_df["Country Name"].unique()),
    key="c1"
)

country2 = st.selectbox(
    "Country 2",
    sorted(valid_df["Country Name"].unique()),
    index=1,
    key="c2"
)

c1 = valid_df[
    valid_df["Country Name"] == country1
]

c2 = valid_df[
    valid_df["Country Name"] == country2
]

compare_df = pd.DataFrame({
    "Year": year_columns,
    country1: c1.iloc[0, 4:].values,
    country2: c2.iloc[0, 4:].values
})

fig4 = px.line(
    compare_df,
    x="Year",
    y=[country1, country2],
    title=f"{country1} vs {country2}"
)

st.plotly_chart(fig4, use_container_width=True)

# INSIGHTS
st.subheader("💡 Insights")

st.success(
    f"{highest_country} has the highest population in the latest available year."
)

st.info(
    f"Dataset contains population records for {total_countries} countries."
)

st.warning(
    "Global population has grown significantly over the past decades."
)

# FOOTER 
st.markdown("---")
st.markdown(
    "Developed using Python, Pandas, Plotly and Streamlit | Data Source: World Bank"
=======
import streamlit as st
import pandas as pd
import plotly.express as px

# PAGE CONFIG
st.set_page_config(
    page_title="World Population Intelligence Platform",
    page_icon="🌍",
    layout="wide"
)

# ---------------- TITLE ----------------
st.title("World Population Intelligence Platform")

st.markdown("""
### About Project

This platform analyzes global population trends using World Bank data.
Users can explore country-wise population growth, compare countries,
and visualize worldwide demographic changes through interactive charts.
""")

# LOAD DATA 
df = pd.read_csv(
    "API_SP.POP.TOTL_DS2_en_csv_v2_282912.csv",
    skiprows=4
)

# Remove empty rows
df = df.dropna(subset=["Country Name"])

# ---------------- FIND LATEST YEAR ----------------
year_columns = df.columns[4:]

latest_year = None

for col in reversed(year_columns):
    if df[col].notna().sum() > 0:
        latest_year = col
        break

# Convert all year columns to numeric
for col in year_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

valid_df = df.dropna(subset=[latest_year])

#  KPI CARDS 
st.subheader("Key Statistics")

total_countries = valid_df["Country Name"].nunique()
world_population = valid_df[latest_year].sum()

highest_country = valid_df.loc[
    valid_df[latest_year].idxmax(),
    "Country Name"
]

lowest_country = valid_df.loc[
    valid_df[latest_year].idxmin(),
    "Country Name"
]

col1, col2, col3, col4 = st.columns(4)

col1.metric("Countries", total_countries)
col2.metric("Latest Year", latest_year)
col3.metric("Highest Population", highest_country)
col4.metric("Lowest Population", lowest_country)

st.metric(
    "World Population",
    f"{world_population:,.0f}"
)

# DATASET PREVIEW
st.subheader("Dataset Preview")
st.dataframe(valid_df.head())

# TOP 10 COUNTRIES 
st.subheader("Top 10 Most Populated Countries")

top10 = valid_df.nlargest(10, latest_year)

fig1 = px.bar(
    top10,
    x="Country Name",
    y=latest_year,
    title=f"Top 10 Countries by Population ({latest_year})"
)

st.plotly_chart(fig1, use_container_width=True)

#  WORLD POPULATION TREND
st.subheader(" Global Population Growth Trend")

world_population_yearly = valid_df[year_columns].sum()

trend_df = pd.DataFrame({
    "Year": year_columns,
    "Population": world_population_yearly.values
})

fig2 = px.line(
    trend_df,
    x="Year",
    y="Population",
    title="World Population Growth Over Time"
)

st.plotly_chart(fig2, use_container_width=True)

# COUNTRY ANALYSIS
st.subheader("Country Population Analysis")

country = st.selectbox(
    "Select Country",
    sorted(valid_df["Country Name"].unique())
)

country_data = valid_df[
    valid_df["Country Name"] == country
]

country_trend = pd.DataFrame({
    "Year": year_columns,
    "Population": country_data.iloc[0, 4:].values
})

fig3 = px.line(
    country_trend,
    x="Year",
    y="Population",
    title=f"Population Trend - {country}"
)

st.plotly_chart(fig3, use_container_width=True)

# SEARCH
st.subheader("Search Country")

search = st.text_input("Enter Country Name")

if search:
    result = valid_df[
        valid_df["Country Name"].str.contains(
            search,
            case=False,
            na=False
        )
    ]

    if not result.empty:
        st.dataframe(
            result[["Country Name", latest_year]]
        )
    else:
        st.warning("Country not found")

# COUNTRY COMPARISON 
st.subheader("Compare Two Countries")

country1 = st.selectbox(
    "Country 1",
    sorted(valid_df["Country Name"].unique()),
    key="c1"
)

country2 = st.selectbox(
    "Country 2",
    sorted(valid_df["Country Name"].unique()),
    index=1,
    key="c2"
)

c1 = valid_df[
    valid_df["Country Name"] == country1
]

c2 = valid_df[
    valid_df["Country Name"] == country2
]

compare_df = pd.DataFrame({
    "Year": year_columns,
    country1: c1.iloc[0, 4:].values,
    country2: c2.iloc[0, 4:].values
})

fig4 = px.line(
    compare_df,
    x="Year",
    y=[country1, country2],
    title=f"{country1} vs {country2}"
)

st.plotly_chart(fig4, use_container_width=True)

# INSIGHTS
st.subheader("💡 Insights")

st.success(
    f"{highest_country} has the highest population in the latest available year."
)

st.info(
    f"Dataset contains population records for {total_countries} countries."
)

st.warning(
    "Global population has grown significantly over the past decades."
)

# FOOTER 
st.markdown("---")
st.markdown(
    "Developed using Python, Pandas, Plotly and Streamlit | Data Source: World Bank"
>>>>>>> c7fee184d1e58738b1b6d8190e0acaa8351e399c
)