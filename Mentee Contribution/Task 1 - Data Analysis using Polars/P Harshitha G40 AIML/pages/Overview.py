import streamlit as st
import plotly.express as px
from utils import load_data

# Page config
st.set_page_config(page_title="Overview - Student Enrollment Analytics", layout="wide")

# Styling tweaks for cards
st.markdown("""
<style>
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("📊 Dashboard Overview")
st.write("Snapshot of all enrollment activity across semesters and departments.")

# Load data
df = load_data()

if df.empty:
    st.warning("No dataset loaded.")
else:
    # Calculations
    total = len(df)
    enrolled = len(df[df.enrollment_status == "Enrolled"])
    avg_gpa = df.gpa.mean()
    departments = df.department.nunique()
    courses = df.course.nunique()
    dropped_pct = round(len(df[df.enrollment_status == "Dropped"]) / total * 100, 1)

    # KPI row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f'<div class="metric-card"><h3 style="color:#4F6EF7; margin:0;">{total:,}</h3><p style="margin:0; font-size:14px; color:#64748B;">Total Students</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><h3 style="color:#22C55E; margin:0;">{enrolled:,}</h3><p style="margin:0; font-size:14px; color:#64748B;">Currently Enrolled</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><h3 style="color:#F59E0B; margin:0;">{avg_gpa:.2f}</h3><p style="margin:0; font-size:14px; color:#64748B;">Average GPA</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><h3 style="color:#10B981; margin:0;">{departments}</h3><p style="margin:0; font-size:14px; color:#64748B;">Departments</p></div>', unsafe_allow_html=True)
    with col5:
        st.markdown(f'<div class="metric-card"><h3 style="color:#EF4444; margin:0;">{dropped_pct}%</h3><p style="margin:0; font-size:14px; color:#64748B;">Drop Rate</p></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Row 1 Charts
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("🏢 Students by Department")
        dept_counts = df.groupby("department").size().reset_index(name="count").sort_values("count", ascending=True)
        fig_dept = px.bar(
            dept_counts, x="count", y="department", orientation="h",
            color="count", color_continuous_scale=["#C7D2FE", "#4F6EF7"],
            template="plotly_white",
        )
        fig_dept.update_layout(
            margin=dict(l=10, r=10, t=10, b=40),
            coloraxis_showscale=False,
            xaxis_title="Students",
            yaxis_title="",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", size=12, color="#1E293B"),
        )
        st.plotly_chart(fig_dept, use_container_width=True)

    with col_right:
        st.subheader("✅ Enrollment Status Breakdown")
        status_counts = df.enrollment_status.value_counts().reset_index()
        status_counts.columns = ["status", "count"]
        color_map = {"Enrolled": "#4F6EF7", "Completed": "#22C55E", "Waitlisted": "#F59E0B", "Dropped": "#EF4444"}
        fig_status = px.pie(
            status_counts, names="status", values="count",
            hole=0.55, color="status", color_discrete_map=color_map,
            template="plotly_white",
        )
        fig_status.update_traces(textposition="outside", textinfo="percent+label")
        fig_status.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", size=12, color="#1E293B"),
        )
        st.plotly_chart(fig_status, use_container_width=True)

    # Row 2 Charts
    col_left2, col_right2 = st.columns(2)

    with col_left2:
        st.subheader("🎯 GPA Distribution")
        fig_gpa = px.histogram(
            df, x="gpa", nbins=30, color_discrete_sequence=["#4F6EF7"],
            template="plotly_white",
        )
        fig_gpa.update_layout(
            margin=dict(l=10, r=10, t=10, b=40),
            xaxis_title="GPA",
            yaxis_title="Students",
            bargap=0.05,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", size=12, color="#1E293B"),
        )
        st.plotly_chart(fig_gpa, use_container_width=True)

    with col_right2:
        st.subheader("👨‍🎓 Gender Distribution")
        gender_counts = df.gender.value_counts().reset_index()
        gender_counts.columns = ["gender", "count"]
        fig_gender = px.pie(
            gender_counts, names="gender", values="count", hole=0.5,
            color_discrete_sequence=["#4F6EF7", "#A78BFA", "#F59E0B", "#64748B"],
            template="plotly_white",
        )
        fig_gender.update_traces(textposition="outside", textinfo="percent+label")
        fig_gender.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", size=12, color="#1E293B"),
        )
        st.plotly_chart(fig_gender, use_container_width=True)

    st.markdown("---")
    st.subheader("📋 Dataset Preview")
    st.dataframe(df.head(), use_container_width=True)