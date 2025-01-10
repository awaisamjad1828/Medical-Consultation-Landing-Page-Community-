# Data for each semester
semesters = {
    "Fall 2022": [
        {"credit": 3.00, "grade_point": 2.3},  # CS-161 Programming Fundamentals
        {"credit": 1.00, "grade_point": 3.0},  # CS-161L Programming Fundamentals Lab
        {"credit": 3.00, "grade_point": 3.3},  # CS-102 Introduction to Computing
        {"credit": 1.00, "grade_point": 3.0},  # CS-102L Introduction to Computing Lab
        {"credit": 3.00, "grade_point": 2.3},  # MA-123 Calculus
        {"credit": 3.00, "grade_point": 3.7},  # HU-102 Functional English
        {"credit": 2.00, "grade_point": 2.3},  # PHY-111 Applied Physics
        {"credit": 1.00, "grade_point": 2.7},  # ME-100L Workshop Practice
        {"credit": 1.00, "grade_point": 3.3},  # PHY-111L Applied Physics Lab
    ],
    "Spring 2022": [
        {"credit": 3.00, "grade_point": 3.3},  # MA-224 Multivariate Calculus
        {"credit": 1.00, "grade_point": 3.0},  # QT-101 Translation of the Holy Quran - I
        {"credit": 3.00, "grade_point": 2.7},  # MA-343 Applied Probability and Statistics
        {"credit": 1.00, "grade_point": 4.0},  # CS-162L Object Oriented Programming Lab
        {"credit": 1.00, "grade_point": 3.7},  # HU-111L Communication Skills Lab
        {"credit": 3.00, "grade_point": 3.0},  # CMPE-222 Digital Logic Design
        {"credit": 3.00, "grade_point": 2.0},  # CS-162 Object Oriented Programming
        {"credit": 1.00, "grade_point": 3.7},  # CMPE-222L Digital Logic Design Lab
        {"credit": 2.00, "grade_point": 2.7},  # HU-240 Psychology
    ],
    "Fall 2023": [
        {"credit": 1.00, "grade_point": 3.7},  # CS-261L Data Structures and Algorithms Lab
        {"credit": 3.00, "grade_point": 3.0},  # CS-270 Discrete Mathematics
        {"credit": 3.00, "grade_point": 2.7},  # CS-261 Data Structures and Algorithms
        {"credit": 3.00, "grade_point": 2.7},  # CS-271 Computer Organization and Assembly Language
        {"credit": 1.00, "grade_point": 3.0},  # CS-271L Computer Organization Lab
        {"credit": 3.00, "grade_point": 2.3},  # MA-234 Linear Algebra
        {"credit": 3.00, "grade_point": 3.0},  # HU-221 Technical Writing & Presentation Skills
    ],
    "Spring 2023": [
        {"credit": 3.00, "grade_point": 2.3},  # CS-272 Design and Analysis of Algorithms
        {"credit": 3.00, "grade_point": 2.0},  # CS-273 Theory of Automata
        {"credit": 3.00, "grade_point": 2.0},  # CS-263 Operating Systems
        {"credit": 1.00, "grade_point": 3.0},  # CS-263L Operating Systems Lab
        {"credit": 1.00, "grade_point": 3.7},  # CS-262L Database Systems Lab
        {"credit": 1.00, "grade_point": 4.0},  # QT-201 Translation of the Holy Quran - II
        {"credit": 3.00, "grade_point": 2.7},  # CS-262 Database Systems
        {"credit": 3.00, "grade_point": 2.3},  # MA-228 Differential Equations
    ],
}

# Function to calculate GPA
def calculate_gpa(courses):
    total_credits = sum(course["credit"] for course in courses)
    total_grade_points = sum(course["credit"] * course["grade_point"] for course in courses)
    gpa = total_grade_points / total_credits if total_credits > 0 else 0
    return round(gpa, 3), total_credits

# Calculate GPAs for each semester
semester_gpas = {semester: calculate_gpa(courses) for semester, courses in semesters.items()}
print(semester_gpas)
