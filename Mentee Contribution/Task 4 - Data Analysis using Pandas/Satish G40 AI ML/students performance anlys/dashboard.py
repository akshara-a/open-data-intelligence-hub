import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Student Performance Dashboard", layout="wide")

@st.cache_data
def parse_numeric(series: pd.Series) -> pd.Series:
    cleaned = series.astype(str).str.strip()
    cleaned = cleaned.str.replace(r"%", "", regex=True)
    cleaned = cleaned.str.replace(r"[^0-9.\-]+", "", regex=True)
    return pd.to_numeric(cleaned, errors="coerce")

@st.cache_data
def normalize_gender(series: pd.Series) -> pd.Series:
    normalized = series.astype(str).str.strip().str.lower()
    normalized = normalized.replace({
        "m": "Male",
        "male": "Male",
        "f": "Female",
        "female": "Female",
        "n/a": "Unknown",
        "na": "Unknown",
        "": "Unknown",
    })
    normalized = normalized.where(normalized.isin(["Male", "Female"]), "Unknown")
    return normalized

@st.cache_data
def load_and_clean_data(path: str) -> tuple:
    raw_df = pd.read_csv(path, dtype=str)
    raw_df.columns = raw_df.columns.str.strip()
    
    clean_df = raw_df.copy()
    clean_df["Student ID"] = clean_df["Student ID"].astype(str).str.strip()
    clean_df["Name"] = clean_df["Name"].astype(str).str.strip()
    clean_df["Gender"] = normalize_gender(clean_df["Gender"])
    clean_df["Attendance"] = parse_numeric(clean_df["Attendance"])
    for col in ["Math", "Science", "English"]:
        clean_df[col] = parse_numeric(clean_df[col])
    clean_df["GPA"] = parse_numeric(clean_df["GPA"])
    clean_df["Semester"] = clean_df["Semester"].astype(str).str.strip()
    
    for col in ["Attendance", "Math", "Science", "English"]:
        clean_df[col] = clean_df[col].fillna(clean_df[col].median())
    
    missing_gpa = clean_df["GPA"].isna()
    if missing_gpa.any():
        gpa_from_marks = clean_df.loc[missing_gpa, ["Math", "Science", "English"]].sum(axis=1).div(300).mul(4).round(2).clip(upper=4.0)
        clean_df.loc[missing_gpa, "GPA"] = gpa_from_marks
    clean_df["GPA"] = clean_df["GPA"].fillna(clean_df["GPA"].median())
    clean_df.loc[:, ["Math", "Science", "English"]] = clean_df[["Math", "Science", "English"]].clip(lower=0, upper=100)
    clean_df["GPA"] = clean_df["GPA"].clip(lower=0.0, upper=4.0)
    clean_df = clean_df.drop_duplicates(subset=["Student ID"], keep="first")
    
    clean_df["TotalMarks"] = clean_df[["Math", "Science", "English"]].sum(axis=1)
    clean_df["AverageMarks"] = clean_df[["Math", "Science", "English"]].mean(axis=1).round(1)
    clean_df["Grade"] = pd.cut(clean_df["GPA"], bins=[0.0, 2.0, 2.5, 3.0, 3.5, 4.0], labels=["F", "D", "C", "B", "A"], include_lowest=True)
    
    return raw_df, clean_df

st.title("📊 Student Performance Dashboard")
st.markdown("Interactive exploration of student performance data with cleaning, filtering, and visualization.")

data_path = os.path.join("data", "student_performance.csv")
if not os.path.exists(data_path):
    st.error(f"Dataset not found at {data_path}")
    st.stop()

raw_df, clean_df = load_and_clean_data(data_path)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Overview", "Data Quality", "Analysis", "Trends", "Insights"])

with tab1:
    st.header("Dataset Overview")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Students", len(clean_df))
    with col2:
        st.metric("Average GPA", f"{clean_df['GPA'].mean():.2f}")
    with col3:
        st.metric("Average Attendance", f"{clean_df['Attendance'].mean():.1f}%")
    with col4:
        st.metric("Semesters", clean_df["Semester"].nunique())
    
    st.subheader("Sample Data")
    st.dataframe(clean_df[["Student ID", "Name", "Gender", "Attendance", "Math", "Science", "English", "GPA", "Semester"]].head(10), width='stretch')

with tab2:
    st.header("Data Quality Summary")
    quality_metrics = pd.DataFrame({
        "Metric": ["Missing Attendance", "Missing Math", "Missing Science", "Missing English", "Missing GPA", "Unknown Gender", "Duplicate Student ID"],
        "Raw Count": [
            raw_df["Attendance"].isna().sum(),
            raw_df["Math"].isna().sum(),
            raw_df["Science"].isna().sum(),
            raw_df["English"].isna().sum(),
            raw_df["GPA"].isna().sum(),
            raw_df["Gender"].astype(str).str.strip().isin(["", "N/A", "na"]).sum(),
            raw_df["Student ID"].duplicated().sum(),
        ],
        "Cleaned Count": [
            clean_df["Attendance"].isna().sum(),
            clean_df["Math"].isna().sum(),
            clean_df["Science"].isna().sum(),
            clean_df["English"].isna().sum(),
            clean_df["GPA"].isna().sum(),
            (clean_df["Gender"] == "Unknown").sum(),
            clean_df["Student ID"].duplicated().sum(),
        ],
    })
    st.dataframe(quality_metrics, width='stretch')
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Rows Processed:**")
        st.write(f"- Raw: {len(raw_df)}")
        st.write(f"- Cleaned: {len(clean_df)}")
    with col2:
        st.write("**Data Cleaning Applied:**")
        st.write("- Normalized text formatting")
        st.write("- Parsed numeric values with regex")
        st.write("- Filled missing values with medians")
        st.write("- Removed duplicate records")

with tab3:
    st.header("Interactive Analysis")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        semester_options = sorted([s for s in clean_df["Semester"].unique() if pd.notna(s)])
        selected_semester = st.multiselect("Select Semester(s)", semester_options, default=semester_options)
    with col2:
        selected_gender = st.multiselect("Select Gender(s)", clean_df["Gender"].unique(), default=clean_df["Gender"].unique())
    with col3:
        gpa_range = st.slider("GPA Range", float(clean_df["GPA"].min()), float(clean_df["GPA"].max()), (float(clean_df["GPA"].min()), float(clean_df["GPA"].max())))
    
    filtered_df = clean_df[
        (clean_df["Semester"].isin(selected_semester)) &
        (clean_df["Gender"].isin(selected_gender)) &
        (clean_df["GPA"] >= gpa_range[0]) &
        (clean_df["GPA"] <= gpa_range[1])
    ]
    
    st.write(f"**Filtered: {len(filtered_df)} of {len(clean_df)} students**")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Top 10 Students")
        top_students = filtered_df.nlargest(10, "GPA")[["Student ID", "Name", "Gender", "GPA", "TotalMarks"]].reset_index(drop=True)
        st.dataframe(top_students, width='stretch')
    
    with col2:
        st.subheader("Subject-wise Averages")
        subject_avg = pd.DataFrame({
            "Subject": ["Math", "Science", "English"],
            "Average": [filtered_df["Math"].mean(), filtered_df["Science"].mean(), filtered_df["English"].mean()]
        })
        fig = px.bar(subject_avg, x="Subject", y="Average", color="Subject", title="Average Scores by Subject", height=400)
        st.plotly_chart(fig, width='stretch')

with tab4:
    st.header("Trends & Distributions")
    
    col1, col2 = st.columns(2)
    with col1:
        fig_gpa = px.histogram(clean_df, x="GPA", nbins=20, title="GPA Distribution", color_discrete_sequence=["#0066cc"])
        st.plotly_chart(fig_gpa, width='stretch')
    
    with col2:
        fig_attendance = px.box(clean_df, y="Attendance", x="Gender", title="Attendance by Gender", color="Gender")
        st.plotly_chart(fig_attendance, width='stretch')
    
    col1, col2 = st.columns(2)
    with col1:
        fig_scatter = px.scatter(clean_df, x="Attendance", y="AverageMarks", color="Gender", size="GPA", title="Attendance vs Average Marks", hover_data=["Name", "Semester"])
        st.plotly_chart(fig_scatter, width='stretch')
    
    with col2:
        grade_counts = clean_df["Grade"].value_counts().sort_index()
        fig_grade = px.bar(x=grade_counts.index, y=grade_counts.values, title="Grade Distribution", labels={"x": "Grade", "y": "Count"}, color=grade_counts.index, color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig_grade, width='stretch')
    
    st.subheader("GPA by Semester")
    semester_gpa = clean_df.groupby("Semester")["GPA"].mean().sort_index()
    fig_semester = px.line(x=semester_gpa.index, y=semester_gpa.values, title="Average GPA by Semester", labels={"x": "Semester", "y": "Average GPA"}, markers=True)
    st.plotly_chart(fig_semester, width='stretch')

with tab5:
    st.header("Key Insights & Correlation Analysis")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        high_gpa = len(clean_df[clean_df["GPA"] >= 3.5])
        st.metric("High Performers (GPA ≥ 3.5)", high_gpa, f"{high_gpa/len(clean_df)*100:.1f}%")
    with col2:
        avg_attendance = clean_df["Attendance"].mean()
        st.metric("Average Attendance", f"{avg_attendance:.1f}%")
    with col3:
        attendance_gpa_corr = clean_df["Attendance"].corr(clean_df["GPA"])
        st.metric("Attendance-GPA Correlation", f"{attendance_gpa_corr:.3f}")
    
    st.subheader("Correlation Heatmap")
    corr_cols = ["Attendance", "Math", "Science", "English", "GPA", "TotalMarks", "AverageMarks"]
    corr_matrix = clean_df[corr_cols].corr()
    
    fig_corr = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_cols,
        y=corr_cols,
        colorscale="RdBu",
        zmid=0,
        text=np.round(corr_matrix.values, 2),
        texttemplate="%{text}",
        textfont={"size": 10},
    ))
    fig_corr.update_layout(width=800, height=800)
    st.plotly_chart(fig_corr, width='stretch')
    
    st.subheader("Performance Insights")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Top Insights:**")
        best_subject = clean_df[["Math", "Science", "English"]].mean().idxmax()
        worst_subject = clean_df[["Math", "Science", "English"]].mean().idxmin()
        st.write(f"- **Best Subject:** {best_subject} (avg: {clean_df[best_subject].mean():.1f})")
        st.write(f"- **Lowest Subject:** {worst_subject} (avg: {clean_df[worst_subject].mean():.1f})")
        
        gender_stats = clean_df.groupby("Gender")["GPA"].mean()
        best_gender = gender_stats.idxmax()
        st.write(f"- **Top Performer Gender:** {best_gender} (avg GPA: {gender_stats[best_gender]:.2f})")
    
    with col2:
        st.write("**Statistical Summary:**")
        st.write(f"- **GPA Range:** {clean_df['GPA'].min():.2f} - {clean_df['GPA'].max():.2f}")
        st.write(f"- **Attendance Range:** {clean_df['Attendance'].min():.1f}% - {clean_df['Attendance'].max():.1f}%")
        st.write(f"- **Total Marks Range:** {clean_df['TotalMarks'].min():.0f} - {clean_df['TotalMarks'].max():.0f}")

st.sidebar.markdown("---")
st.sidebar.write("**About this Dashboard:**")
st.sidebar.write("Built with Streamlit, Pandas, Plotly, and Seaborn for interactive student performance analysis.")
st.sidebar.write("The dataset includes ~1000 student records with optional data quality issues for cleaning practice.")
