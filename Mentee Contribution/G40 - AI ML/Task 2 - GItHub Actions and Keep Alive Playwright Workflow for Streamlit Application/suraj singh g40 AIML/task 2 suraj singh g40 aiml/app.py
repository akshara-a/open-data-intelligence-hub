import streamlit as st
import pandas as pd

st.set_page_config(page_title="Student Analytics Platform", layout="wide")

@st.cache_data
def get_data():
    return pd.read_csv("data/student.csv")

df = get_data()

st.title("Student Performance Analytics System")
st.write("An enterprise-grade analytical interface for monitoring and evaluating academic performance across cohorts.")

st.sidebar.subheader("Dashboard Controls")

c_opt = sorted(df["course"].unique().tolist())
c_sel = st.sidebar.multiselect("Select Courses", options=c_opt, default=c_opt)

g_opt = sorted(df["grade"].unique().tolist())
g_sel = st.sidebar.multiselect("Select Grades", options=g_opt, default=g_opt)

t_df = df[(df["course"].isin(c_sel)) & (df["grade"].isin(g_sel))]

st.subheader("Key Performance Indicators")
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric(label="Total Enrolled", value=len(t_df))
with m2:
    val = round(t_df["attendance"].mean(), 1) if not t_df.empty else 0
    st.metric(label="Average Attendance", value=f"{val}%")
with m3:
    val = round(t_df["final_score"].mean(), 1) if not t_df.empty else 0
    st.metric(label="Class Average Score", value=f"{val}%")
with m4:
    val = t_df.loc[t_df["final_score"].idxmax()]["name"] if not t_df.empty else "N/A"
    st.metric(label="Top Performer", value=val)

st.subheader("Distribution Analysis")
col1, col2 = st.columns(2)

with col1:
    st.write("Enrollment Density by Course")
    c_counts = t_df["course"].value_counts()
    st.bar_chart(c_counts)

with col2:
    st.write("Grade Distribution Analysis")
    g_counts = t_df["grade"].value_counts().sort_index()
    st.bar_chart(g_counts)

st.subheader("Granular Data Records")
q = st.text_input("Filter Records by Student Name")
if q:
    t_df = t_df[t_df["name"].str.contains(q, case=False)]

st.dataframe(t_df, use_container_width=True, hide_index=True)
