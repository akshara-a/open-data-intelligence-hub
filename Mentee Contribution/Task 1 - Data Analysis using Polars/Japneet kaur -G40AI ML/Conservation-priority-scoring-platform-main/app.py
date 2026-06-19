import streamlit as st
import polars as pl
import plotly.express as px

st.set_page_config(
    page_title="Conservation Priority Scoring Platform",
    page_icon="🌿",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: #0b1120;
}
.hero {
    background: linear-gradient(135deg, #052e16, #064e3b, #14532d);
    padding: 28px;
    border-radius: 22px;
    margin-bottom: 25px;
    border: 1px solid #166534;
}
.hero h1 {
    color: #ffffff;
    font-size: 42px;
    font-weight: 900;
    margin-bottom: 8px;
}
.hero p {
    color: #d1fae5;
    font-size: 17px;
    margin: 0;
}
.info-box {
    background: #111827;
    border: 1px solid #374151;
    padding: 18px;
    border-radius: 16px;
    margin-bottom: 20px;
    color: #d1d5db;
}
.card {
    padding: 20px;
    border-radius: 18px;
    background: #111827;
    border: 1px solid #374151;
    text-align: center;
    min-height: 115px;
}
.card h3 {
    font-size: 14px;
    color: #cbd5e1;
    margin-bottom: 10px;
}
.card p {
    font-size: 30px;
    font-weight: 900;
    color: #22c55e;
    margin: 0;
}
.insight-card {
    background: #111827;
    border: 1px solid #374151;
    padding: 18px;
    border-radius: 16px;
    min-height: 105px;
}
.insight-card h4 {
    color: #94a3b8;
    font-size: 14px;
    margin-bottom: 8px;
}
.insight-card p {
    color: #ffffff;
    font-size: 22px;
    font-weight: 800;
    margin: 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🌿 Conservation Priority Scoring Platform</h1>
    <p>Analyze species conservation data, identify high-risk species, and generate priority scores using Python Polars.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
This dashboard converts conservation status into readable labels such as <b>Least Concern</b>, 
<b>Vulnerable</b>, <b>Endangered</b>, and <b>Critically Endangered</b>. 
Higher priority score means higher conservation concern.
</div>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pl.read_csv("filtered_data.csv")

    category_map = {
        "LC": "Least Concern",
        "NT": "Near Threatened",
        "VU": "Vulnerable",
        "EN": "Endangered",
        "CR": "Critically Endangered",
        "EW": "Extinct in Wild",
        "EX": "Extinct",
        "DD": "Data Deficient",
        "LR/lc": "Low Risk - Least Concern",
        "LR/nt": "Low Risk - Near Threatened",
        "LR/cd": "Low Risk - Conservation Dependent"
    }

    df = df.with_columns(
        pl.col("category").replace(category_map).alias("category")
    )

    score_map = {
        "Least Concern": 10,
        "Near Threatened": 30,
        "Vulnerable": 50,
        "Endangered": 70,
        "Critically Endangered": 90,
        "Extinct in Wild": 95,
        "Extinct": 100,
        "Data Deficient": 40,
        "Low Risk - Least Concern": 15,
        "Low Risk - Near Threatened": 25,
        "Low Risk - Conservation Dependent": 35
    }

    df = df.with_columns(
        pl.col("category")
        .replace(score_map)
        .cast(pl.Int64)
        .alias("priority_score")
    )

    df = df.with_columns(
        pl.when(pl.col("priority_score") >= 80)
        .then(pl.lit("Critical"))
        .when(pl.col("priority_score") >= 60)
        .then(pl.lit("High"))
        .when(pl.col("priority_score") >= 40)
        .then(pl.lit("Medium"))
        .otherwise(pl.lit("Low"))
        .alias("priority_level")
    )

    return df

df = load_data()

st.sidebar.title("🔎 Dashboard Filters")
st.sidebar.caption("Filter data by kingdom, conservation category, and priority level.")

kingdoms = ["All"] + sorted(df.select("kingdom_name").unique().drop_nulls().to_series().to_list())
categories = ["All"] + sorted(df.select("category").unique().drop_nulls().to_series().to_list())
priorities = ["All"] + sorted(df.select("priority_level").unique().drop_nulls().to_series().to_list())

selected_kingdom = st.sidebar.selectbox("Kingdom", kingdoms)
selected_category = st.sidebar.selectbox("Conservation Category", categories)
selected_priority = st.sidebar.selectbox("Priority Level", priorities)

filtered_df = df

if selected_kingdom != "All":
    filtered_df = filtered_df.filter(pl.col("kingdom_name") == selected_kingdom)

if selected_category != "All":
    filtered_df = filtered_df.filter(pl.col("category") == selected_category)

if selected_priority != "All":
    filtered_df = filtered_df.filter(pl.col("priority_level") == selected_priority)

total_count = filtered_df.height
critical_count = filtered_df.filter(pl.col("priority_level") == "Critical").height
high_count = filtered_df.filter(pl.col("priority_level") == "High").height
medium_count = filtered_df.filter(pl.col("priority_level") == "Medium").height
low_count = filtered_df.filter(pl.col("priority_level") == "Low").height

c1, c2, c3, c4, c5 = st.columns(5)

c1.markdown(f"<div class='card'><h3>Total Species</h3><p>{total_count}</p></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='card'><h3>Critical Priority</h3><p>{critical_count}</p></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='card'><h3>High Priority</h3><p>{high_count}</p></div>", unsafe_allow_html=True)
c4.markdown(f"<div class='card'><h3>Medium Priority</h3><p>{medium_count}</p></div>", unsafe_allow_html=True)
c5.markdown(f"<div class='card'><h3>Low Priority</h3><p>{low_count}</p></div>", unsafe_allow_html=True)

st.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 EDA Overview",
    "⚠️ Risk Analysis",
    "🔥 Priority Species",
    "📁 Data Explorer",
    "⬇️ Report"
])

with tab1:
    st.subheader("Exploratory Data Analysis Overview")
    st.caption("This section summarizes the main distribution patterns in the conservation dataset.")

    category_df = filtered_df.group_by("category").len().sort("len", descending=True).to_pandas()
    priority_df = filtered_df.group_by("priority_level").len().sort("len", descending=True).to_pandas()
    kingdom_df = filtered_df.group_by("kingdom_name").len().sort("len", descending=True).to_pandas()
    class_df = filtered_df.group_by("class_name").len().sort("len", descending=True).head(12).to_pandas()

    top_category = category_df.iloc[0]["category"] if len(category_df) else "N/A"
    top_kingdom = kingdom_df.iloc[0]["kingdom_name"] if len(kingdom_df) else "N/A"
    top_class = class_df.iloc[0]["class_name"] if len(class_df) else "N/A"

    i1, i2, i3 = st.columns(3)

    i1.markdown(
        f"<div class='insight-card'><h4>Most Common Conservation Status</h4><p>{top_category}</p></div>",
        unsafe_allow_html=True
    )

    i2.markdown(
        f"<div class='insight-card'><h4>Largest Kingdom</h4><p>{top_kingdom}</p></div>",
        unsafe_allow_html=True
    )

    i3.markdown(
        f"<div class='insight-card'><h4>Most Common Biological Class</h4><p>{top_class}</p></div>",
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns(2)

    with left:
        st.subheader("Species by Conservation Category")
        st.caption("Shows how many species belong to each conservation status.")
        fig1 = px.bar(
            category_df,
            x="category",
            y="len",
            text="len",
            color="category",
            title="Conservation Category Distribution"
        )
        fig1.update_layout(
            showlegend=False,
            xaxis_title="Conservation Category",
            yaxis_title="Species Count"
        )
        fig1.update_traces(textposition="outside")
        st.plotly_chart(fig1, use_container_width=True)

    with right:
        st.subheader("Priority Level Share")
        st.caption("Shows how many species are Low, Medium, High, or Critical priority.")
        fig2 = px.pie(
            priority_df,
            names="priority_level",
            values="len",
            hole=0.45,
            title="Priority Level Distribution"
        )
        st.plotly_chart(fig2, use_container_width=True)

    left2, right2 = st.columns(2)

    with left2:
        st.subheader("Species by Kingdom")
        st.caption("Compares total species records across kingdoms.")
        fig3 = px.bar(
            kingdom_df,
            x="kingdom_name",
            y="len",
            text="len",
            color="kingdom_name",
            title="Kingdom-wise Species Count"
        )
        fig3.update_layout(
            showlegend=False,
            xaxis_title="Kingdom",
            yaxis_title="Species Count"
        )
        fig3.update_traces(textposition="outside")
        st.plotly_chart(fig3, use_container_width=True)

    with right2:
        st.subheader("Top Biological Classes")
        st.caption("Displays the top classes by number of species.")
        fig4 = px.bar(
            class_df,
            x="len",
            y="class_name",
            orientation="h",
            text="len",
            color="len",
            title="Top 12 Classes by Species Count"
        )
        fig4.update_layout(
            yaxis={"categoryorder": "total ascending"},
            showlegend=False
        )
        st.plotly_chart(fig4, use_container_width=True)

with tab2:
    st.subheader("Risk Pattern Analysis")
    st.caption("This section helps identify groups with higher conservation concern.")

    scatter_df = (
        filtered_df
        .group_by(["kingdom_name", "category"])
        .agg([
            pl.len().alias("species_count"),
            pl.mean("priority_score").alias("average_priority_score")
        ])
        .sort("species_count", descending=True)
        .to_pandas()
    )

    fig5 = px.scatter(
        scatter_df,
        x="species_count",
        y="average_priority_score",
        size="species_count",
        color="category",
        hover_name="kingdom_name",
        title="Species Count vs Average Priority Score"
    )
    fig5.update_layout(
        xaxis_title="Species Count",
        yaxis_title="Average Priority Score"
    )
    st.plotly_chart(fig5, use_container_width=True)

    st.info("Larger bubbles represent groups with more species. Higher position means higher average conservation concern.")

    risk_table = (
        filtered_df
        .group_by(["kingdom_name", "category", "priority_level"])
        .agg([
            pl.len().alias("species_count"),
            pl.mean("priority_score").round(2).alias("average_score")
        ])
        .sort("average_score", descending=True)
        .head(20)
        .to_pandas()
    )

    st.subheader("Top Risk Groups")
    st.dataframe(risk_table, use_container_width=True)

with tab3:
    st.subheader("Top Conservation Priority Species")
    st.caption("Species with the highest priority score are shown first.")

    top_df = filtered_df.sort("priority_score", descending=True).select([
        "scientific_name",
        "main_common_name",
        "kingdom_name",
        "class_name",
        "category",
        "priority_score",
        "priority_level"
    ])

    st.dataframe(top_df.head(300).to_pandas(), use_container_width=True)

with tab4:
    st.subheader("Filtered Dataset Preview")
    st.caption("Showing first 1000 records for smooth performance.")

    st.dataframe(filtered_df.head(1000).to_pandas(), use_container_width=True)

with tab5:
    st.subheader("Download Conservation Priority Report")
    st.caption("Download the filtered dataset with calculated priority score and priority level.")

    csv_data = filtered_df.write_csv().encode("utf-8")

    st.download_button(
        label="⬇️ Download CSV Report",
        data=csv_data,
        file_name="conservation_priority_report.csv",
        mime="text/csv"
    )
