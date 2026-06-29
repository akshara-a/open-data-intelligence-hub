"""Generate synthetic student enrollment data for the dashboard."""
import pandas as pd
import numpy as np
import random

random.seed(42)
np.random.seed(42)

N = 5000

departments = [
    "Computer Science", "Mathematics", "Physics", "Biology",
    "Chemistry", "English", "History", "Economics",
    "Psychology", "Business Administration",
]

courses_by_dept = {
    "Computer Science": ["Intro to CS", "Data Structures", "Algorithms", "Machine Learning", "Databases", "Web Dev", "Operating Systems", "Networks"],
    "Mathematics": ["Calculus I", "Calculus II", "Linear Algebra", "Statistics", "Discrete Math", "Probability", "Differential Equations"],
    "Physics": ["Mechanics", "Electromagnetism", "Thermodynamics", "Quantum Physics", "Optics", "Relativity"],
    "Biology": ["Cell Biology", "Genetics", "Ecology", "Microbiology", "Anatomy", "Evolution"],
    "Chemistry": ["General Chemistry", "Organic Chemistry", "Biochemistry", "Analytical Chemistry", "Physical Chemistry"],
    "English": ["Creative Writing", "American Literature", "British Literature", "Composition", "Poetry", "Linguistics"],
    "History": ["World History", "US History", "European History", "Ancient Civilizations", "Modern History"],
    "Economics": ["Microeconomics", "Macroeconomics", "Econometrics", "International Economics", "Game Theory"],
    "Psychology": ["Intro to Psychology", "Cognitive Psychology", "Social Psychology", "Abnormal Psychology", "Developmental Psychology"],
    "Business Administration": ["Marketing", "Finance", "Accounting", "Management", "Entrepreneurship", "Business Ethics"],
}

semesters = ["Spring 2023", "Fall 2023", "Spring 2024", "Fall 2024", "Spring 2025"]
statuses = ["Enrolled", "Completed", "Dropped", "Waitlisted"]
status_weights = [0.40, 0.35, 0.10, 0.15]
genders = ["Male", "Female", "Non-binary"]
gender_weights = [0.48, 0.48, 0.04]
years = ["Freshman", "Sophomore", "Junior", "Senior", "Graduate"]

date_ranges = {
    "Spring 2023": ("2023-01-10", "2023-01-30"),
    "Fall 2023":   ("2023-08-15", "2023-09-05"),
    "Spring 2024": ("2024-01-08", "2024-01-28"),
    "Fall 2024":   ("2024-08-12", "2024-09-02"),
    "Spring 2025": ("2025-01-06", "2025-01-26"),
}

rows = []
for i in range(1, N + 1):
    dept = random.choice(departments)
    course = random.choice(courses_by_dept[dept])
    semester = random.choices(semesters, weights=[0.15, 0.18, 0.20, 0.22, 0.25])[0]
    status = random.choices(statuses, weights=status_weights)[0]
    gender = random.choices(genders, weights=gender_weights)[0]
    year = random.choice(years)
    age = np.random.randint(18, 30) if year != "Graduate" else np.random.randint(22, 35)
    gpa = round(np.clip(np.random.normal(3.1, 0.5), 1.5, 4.0), 2)
    credits = random.choice([1, 2, 3, 4])
    tuition_fee = round(np.random.uniform(5000, 25000), 2)
    scholarship_amount = round(np.random.uniform(0, tuition_fee * 0.6), 2)
    start, end = date_ranges[semester]
    enrollment_date = pd.Timestamp(start) + pd.Timedelta(days=np.random.randint(0, (pd.Timestamp(end) - pd.Timestamp(start)).days + 1))

    rows.append({
        "student_id": f"STU{i:05d}",
        "department": dept,
        "course": course,
        "semester": semester,
        "enrollment_status": status,
        "gender": gender,
        "year": year,
        "age": age,
        "gpa": gpa,
        "credits": credits,
        "tuition_fee": tuition_fee,
        "scholarship_amount": scholarship_amount,
        "enrollment_date": enrollment_date.strftime("%Y-%m-%d"),
    })

df = pd.DataFrame(rows)
df.to_csv("data/enrollment_data.csv", index=False)
print(f"Generated {len(df)} rows")
print(f"Columns: {list(df.columns)}")
print(df.head())
