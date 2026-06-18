import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

DATA_PATH = os.path.join("data", "student_performance.csv")
OUTPUT_DIR = "output"


def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def parse_numeric(series: pd.Series) -> pd.Series:
    text = series.astype(str).str.strip()
    text = text.str.replace(r"%", "", regex=True)
    text = text.str.replace(r"[^0-9.\-]+", "", regex=True)
    return pd.to_numeric(text, errors="coerce")


def normalize_gender(series: pd.Series) -> pd.Series:
    normalized = series.astype(str).str.strip().str.lower()
    normalized = normalized.replace({
        "m": "male",
        "male": "male",
        "f": "female",
        "female": "female",
        "nan": "unknown",
        "n/a": "unknown",
        "na": "unknown",
        "": "unknown",
    })
    normalized = normalized.where(normalized.isin(["male", "female"]), "unknown")
    return normalized.str.title()


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, dtype=str)
    df = df.rename(columns=str.strip)

    for col in ["Student ID", "Name", "Gender", "Attendance", "Math", "Science", "English", "GPA", "Semester"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    if "Gender" in df.columns:
        df["Gender"] = normalize_gender(df["Gender"])

    for col in ["Attendance", "Math", "Science", "English", "GPA"]:
        if col in df.columns:
            df[col] = parse_numeric(df[col])

    if "Semester" in df.columns:
        df["Semester"] = df["Semester"].astype(str).str.strip()
    return df


def summarize_data_quality(df: pd.DataFrame) -> pd.DataFrame:
    quality = pd.DataFrame(
        {
            "Metric": [
                "Rows",
                "Duplicate rows",
                "Duplicate student IDs",
                "Missing Attendance",
                "Missing Math",
                "Missing Science",
                "Missing English",
                "Missing GPA",
                "Unknown gender",
            ],
            "Count": [
                len(df),
                int(df.duplicated().sum()),
                int(df["Student ID"].duplicated().sum()) if "Student ID" in df.columns else 0,
                int(df["Attendance"].isna().sum()) if "Attendance" in df.columns else 0,
                int(df["Math"].isna().sum()) if "Math" in df.columns else 0,
                int(df["Science"].isna().sum()) if "Science" in df.columns else 0,
                int(df["English"].isna().sum()) if "English" in df.columns else 0,
                int(df["GPA"].isna().sum()) if "GPA" in df.columns else 0,
                int((df["Gender"] == "Unknown").sum()) if "Gender" in df.columns else 0,
            ],
        }
    )
    return quality


def compute_gpa_from_marks(df: pd.DataFrame) -> pd.Series:
    if {"Math", "Science", "English"}.issubset(df.columns):
        return df[["Math", "Science", "English"]].sum(axis=1).div(300).mul(4).round(2).clip(upper=4.0)
    return pd.Series(index=df.index, dtype=float)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "Student ID" in df.columns:
        df["Student ID"] = df["Student ID"].astype(str).str.strip()

    if "Name" in df.columns:
        df["Name"] = df["Name"].astype(str).str.strip()

    if "Gender" in df.columns:
        df["Gender"] = normalize_gender(df["Gender"])

    if "Semester" in df.columns:
        df["Semester"] = df["Semester"].astype(str).str.strip()

    for col in ["Attendance", "Math", "Science", "English", "GPA"]:
        if col in df.columns:
            df[col] = parse_numeric(df[col])

    for col in ["Attendance", "Math", "Science", "English"]:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())

    if "GPA" in df.columns:
        missing_gpa = df["GPA"].isna()
        if missing_gpa.any():
            df.loc[missing_gpa, "GPA"] = compute_gpa_from_marks(df.loc[missing_gpa])
        df["GPA"] = df["GPA"].fillna(df["GPA"].median())
        df["GPA"] = df["GPA"].clip(lower=0.0, upper=4.0)

    if "Student ID" in df.columns:
        df = df.drop_duplicates(subset=["Student ID"], keep="first")
    df = df.drop_duplicates()
    return df


def compute_top_students(df: pd.DataFrame, count: int = 10) -> pd.DataFrame:
    df = df.copy()
    df["TotalMarks"] = df[["Math", "Science", "English"]].sum(axis=1)
    return df.sort_values(["GPA", "TotalMarks"], ascending=False).head(count)


def subject_averages(df: pd.DataFrame) -> pd.Series:
    return df[["Math", "Science", "English"]].mean().round(2)


def make_grade_distribution(df: pd.DataFrame) -> pd.Series:
    bins = [0.0, 2.0, 2.5, 3.0, 3.5, 4.0]
    labels = ["F", "D", "C", "B", "A"]
    df["Grade"] = pd.cut(df["GPA"], bins=bins, labels=labels, include_lowest=True)
    return df["Grade"].value_counts().reindex(labels, fill_value=0)


def plot_attendance_vs_marks(df: pd.DataFrame) -> str:
    df = df.copy()
    df["AverageMarks"] = df[["Math", "Science", "English"]].mean(axis=1)
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x="Attendance", y="AverageMarks", hue="Gender", style="Semester", s=100)
    plt.title("Attendance vs Average Marks")
    plt.xlabel("Attendance (%)")
    plt.ylabel("Average Marks")
    plt.grid(True, linestyle="--", alpha=0.5)
    output_path = os.path.join(OUTPUT_DIR, "attendance_vs_marks.png")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    return output_path


def plot_grade_distribution(dist: pd.Series) -> str:
    plt.figure(figsize=(8, 5))
    sns.barplot(x=dist.index, y=dist.values, palette="Blues_d")
    plt.title("Grade Distribution")
    plt.xlabel("Grade")
    plt.ylabel("Count")
    output_path = os.path.join(OUTPUT_DIR, "grade_distribution.png")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    return output_path


def plot_subject_averages(avg: pd.Series) -> str:
    plt.figure(figsize=(8, 5))
    sns.barplot(x=avg.index, y=avg.values, palette="Set2")
    plt.title("Subject-wise Average Scores")
    plt.xlabel("Subject")
    plt.ylabel("Average Score")
    output_path = os.path.join(OUTPUT_DIR, "subject_averages.png")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    return output_path


def run_analysis():
    ensure_output_dir()
    raw_df = load_data(DATA_PATH)
    quality = summarize_data_quality(raw_df)

    print("Student Performance Analysis")
    print("============================")
    print(f"Raw dataset loaded: {len(raw_df)} rows")
    print()
    print("Data Quality Summary")
    print("---------------------")
    print(quality.to_string(index=False))
    print()

    df = clean_data(raw_df)
    print(f"Cleaned dataset rows: {len(df)}")
    print()

    print("Top Students")
    print("--------------")
    top_students = compute_top_students(df, count=10)
    print(top_students[["Student ID", "Name", "Gender", "Semester", "Attendance", "Math", "Science", "English", "GPA"]].to_string(index=False))
    print()

    print("Subject-wise Averages")
    print("-----------------------")
    avg = subject_averages(df)
    print(avg.to_string())
    print()

    print("Grade Distribution")
    print("-------------------")
    distribution = make_grade_distribution(df)
    print(distribution.to_string())
    print()

    plot_paths = []
    plot_paths.append(plot_attendance_vs_marks(df))
    plot_paths.append(plot_subject_averages(avg))
    plot_paths.append(plot_grade_distribution(distribution))

    print("Charts generated:")
    for path in plot_paths:
        print(f" - {path}")


if __name__ == "__main__":
    run_analysis()
