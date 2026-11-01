import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Student Performance Dashboard",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv("data/students.csv")

df = load_data()

st.title("Student Performance Dashboard")
st.write("A simple dashboard using dummy student performance data.")

st.sidebar.header("Filters")

selected_courses = st.sidebar.multiselect(
    "Select course",
    options=sorted(df["course"].unique()),
    default=sorted(df["course"].unique())
)

selected_cities = st.sidebar.multiselect(
    "Select city",
    options=sorted(df["city"].unique()),
    default=sorted(df["city"].unique())
)

min_score = st.sidebar.slider(
    "Minimum final score",
    min_value=0,
    max_value=100,
    value=0
)

filtered_df = df[
    (df["course"].isin(selected_courses)) &
    (df["city"].isin(selected_cities)) &
    (df["final_score"] >= min_score)
]

total_students = len(filtered_df)
average_score = round(filtered_df["final_score"].mean(), 2) if total_students else 0
average_attendance = round(filtered_df["attendance"].mean(), 2) if total_students else 0
top_score = round(filtered_df["final_score"].max(), 2) if total_students else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Students", total_students)
col2.metric("Average Score", average_score)
col3.metric("Average Attendance", average_attendance)
col4.metric("Top Score", top_score)

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Average Score by Course")
    course_scores = filtered_df.groupby("course")["final_score"].mean().sort_values()
    st.bar_chart(course_scores)

with right:
    st.subheader("Grade Distribution")
    grade_counts = filtered_df["grade"].value_counts().sort_index()
    st.bar_chart(grade_counts)

st.subheader("Student Records")
st.dataframe(
    filtered_df.sort_values("final_score", ascending=False),
    use_container_width=True,
    hide_index=True
)

st.subheader("Simple Insight")

if total_students:
    best_course = filtered_df.groupby("course")["final_score"].mean().idxmax()
    st.success(f"Best-performing course in the selected data: {best_course}")
else:
    st.warning("No records match the selected filters.")