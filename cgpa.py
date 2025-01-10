# Data dictionary with missing credit hours for Fall 2024 assumed as 18.0
data = {
    'Fall 2022': (2.856, 18.0),
    'Spring 2023': (3.1, 18.0),
    'Fall 2023': (2.812, 17.0),
    'Spring 2024': (2.478, 18.0),
    'Fall 2024': (3.435, 17.0),
}

# Calculate total grade points and total credit hours
total_grade_points = sum(gpa * credits for gpa, credits in data.values())
total_credits = sum(credits for _, credits in data.values())

# Calculate CGPA
cgpa = total_grade_points / total_credits
print(cgpa)
