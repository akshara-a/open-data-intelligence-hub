import csv
import random

first_names = [
    "Aiden", "Olivia", "Ethan", "Emma", "Noah", "Ava", "Logan", "Isabella",
    "Lucas", "Sophia", "Mason", "Mia", "Amelia", "James", "Harper", "Oliver",
    "Charlotte", "Benjamin", "Evelyn", "Elijah", "William", "Zoey", "Henry",
    "Lily", "Alexander", "Ella", "Jack", "Scarlett", "Daniel", "Chloe", "Matthew",
    "Grace", "Samuel", "Sofia", "David", "Victoria", "Andrew", "Joseph", "Avery",
    "Wyatt", "Lillian", "Jackson", "Zoe", "Levi", "Stella", "Aaron", "Nora",
    "Caleb", "Brooklyn", "Madison", "Nathan", "Luna", "Ryan", "Hannah", "Dylan",
    "Thomas", "Jordan", "Mila", "Connor", "Aria", "Austin", "Leah", "Owen",
    "Luke", "Penelope", "Cameron", "Riley", "Eli", "Savannah", "Ian", "Victoria",
    "Adam", "Jason", "Claire", "Sadie", "Cole", "Sarah", "Gavin", "Anna",
    "Sean", "Audrey", "Victor", "Maya", "Justin", "Alexa", "Evan", "Julia",
    "Miles", "Rachel", "Blake", "Samantha", "Leo", "Mackenzie", "Arianna", "Brandon",
    "Lydia", "Zachary", "Peyton", "Cody", "Allison", "Nathaniel", "Gianna", "Carter",
    "Morgan"
]
last_names = [
    "Walker", "Bennett", "Carter", "Collins", "Reed", "Foster", "Price", "Young",
    "Morgan", "Rivera", "Powell", "Brooks", "Kelly", "Barnes", "Scott", "James",
    "Hayes", "Bailey", "Parker", "Long", "Graham", "Russell", "Hughes", "Cooper",
    "Lewis", "Cox", "Turner", "Peterson", "Jenkins", "Wood", "Diaz", "Knight",
    "Bell", "Gray", "Mitchell", "Roberts", "Evans", "Torres", "Nguyen", "Murphy",
    "Phillips", "Campbell", "Edwards", "Stewart", "Morris", "Rogers"
]
raw_genders = ["Male", "Female", "M", "F", "male", "female", " female ", "N/A", "na"]
semesters = ["1", "2", "3", "4", "01", "02", "03", "04", "N/A"]

rows = []
for i in range(1, 981):
    sid = f"S{i:04d}"
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    if random.random() < 0.08:
        name = name.lower()
    if random.random() < 0.05:
        name = f" {name} "

    gender = random.choice(raw_genders)

    attendance_value = round(random.uniform(65, 100), 1)
    if random.random() < 0.04:
        attendance = f"{int(attendance_value)}%"
    elif random.random() < 0.02:
        attendance = "N/A"
    else:
        attendance = attendance_value

    math = random.randint(50, 100)
    science = random.randint(50, 100)
    english = random.randint(50, 100)

    if random.random() < 0.03:
        math = ""
    if random.random() < 0.03:
        science = "N/A"
    if random.random() < 0.03:
        english = "na"

    computed_total = 0
    for value in [math, science, english]:
        try:
            computed_total += float(value)
        except ValueError:
            pass
    gpa = round(min(4.0, max(0.0, (computed_total / 300) * 4)), 2)

    if random.random() < 0.05:
        gpa = ""

    semester = random.choice(semesters)
    rows.append([sid, name, gender, attendance, math, science, english, gpa, semester])

# add duplicate rows
for _ in range(10):
    rows.append(rows[random.randint(0, len(rows) - 1)])

# add duplicate student IDs with messy variations
for _ in range(10):
    original = rows[random.randint(0, len(rows) - 1)]
    duplicate = original.copy()
    duplicate[1] = duplicate[1].strip().upper()
    duplicate[2] = random.choice(raw_genders)
    rows.append(duplicate)

random.shuffle(rows)

with open("data/student_performance.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Student ID", "Name", "Gender", "Attendance", "Math", "Science", "English", "GPA", "Semester"])
    writer.writerows(rows)

print("Generated 1000-row dirty dataset at data/student_performance.csv")
