import streamlit as st
import polars as pl

st.set_page_config(page_title="Olympic Analytics", layout="wide")

st.title("🏆 Olympic Medal Intelligence Platform")
st.markdown("### Powered by Polars & Streamlit")
st.write("---")

def run_olympic_engine():
    try:
        df = pl.read_csv("athlete_events.csv", null_values="NA", infer_schema_length=None)
        
        medal_df = df.filter(pl.col("Medal").is_not_null())
        
        country_tally = medal_df.group_by("NOC").agg([
            pl.col("Medal").filter(pl.col("Medal") == "Gold").count().alias("Gold"),
            pl.col("Medal").filter(pl.col("Medal") == "Silver").count().alias("Silver"),
            pl.col("Medal").filter(pl.col("Medal") == "Bronze").count().alias("Bronze")
        ])
        
        ranked_df = country_tally.with_columns(
            ((pl.col("Gold") * 3) + (pl.col("Silver") * 2) + (pl.col("Bronze") * 1)).alias("Performance_Score")
        )
        
        sorted_df = ranked_df.sort("Performance_Score", descending=True)
        final_ranked_df = sorted_df.with_row_index(name="Rank", offset=1)
        return final_ranked_df

    except FileNotFoundError:
        st.error("⚠️ Error: 'athlete_events.csv' file not found!")
        return None

ranked_countries = run_olympic_engine()

if ranked_countries is not None:
    st.sidebar.header("📌 Menu Options")
    selection = st.sidebar.radio("Select a view:", ["Global Leaderboard", "Search Country Details"])

    if selection == "Global Leaderboard":
        st.header("🌍 Global Olympic Rankings")
        st.write("Countries ranked by Performance Score (Gold = 3pts, Silver = 2pts, Bronze = 1pt)")
        
        num_countries = st.slider("Select number of top countries:", min_value=5, max_value=50, value=10)
        top_data = ranked_countries.head(num_countries)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📊 Performance Leaderboard")
            st.dataframe(top_data, use_container_width=True)
            
        with col2:
            st.subheader("📈 Visual Performance Analytics")
            st.bar_chart(data=top_data.to_pandas(), x="NOC", y="Performance_Score", color="#FF4B4B")

    elif selection == "Search Country Details":
        st.header("🔍 Individual Country Analysis")
        
        selected_nation = st.text_input("Enter Country Code (e.g., IND, USA, CHN):", value="USA").upper()
        specific_country_data = ranked_countries.filter(pl.col("NOC") == selected_nation)
        
        if not specific_country_data.is_empty():
            st.write("---")
            st.subheader(f"Analysis Dashboard for {selected_nation}")
            
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Global Rank", f"#{specific_country_data['Rank'][0]}")
            m2.metric("🥇 Gold Medals", specific_country_data['Gold'][0])
            m3.metric("🥈 Silver Medals", specific_country_data['Silver'][0])
            m4.metric("🥉 Bronze Medals", specific_country_data['Bronze'][0])
            
            st.success(f"🎉 {selected_nation} total score is {specific_country_data['Performance_Score'][0]} points!")
        else:
            st.warning(f"⚠️ No data found for Country Code '{selected_nation}'.")