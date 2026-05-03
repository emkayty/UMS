"""
Constants for UMS
Standardized, Professional Constants
"""

# ============================================================
# NIGERIAN STATES
# ============================================================

NIGERIAN_STATES = [
    'Abia', 'Adamawa', 'Akwa Ibom', 'Anambra', 'Bauchi',
    'Bayelsa', 'Benue', 'Borno', 'Cross River', 'Delta',
    'Ebonyi', 'Edo', 'Ekiti', 'Enugu', 'Gombe',
    'Imo', 'Jigawa', 'Kaduna', 'Kano', 'Katsina',
    'Kebbi', 'Kogi', 'Kwara', 'Lagos', 'Nasarawa',
    'Niger', 'Ogun', 'Ondo', 'Osun', 'Oyo',
    'Plateau', 'Rivers', 'Sokoto', 'Taraba', 'Yobe',
    'Zamfara', 'FCT'
]

NIGERIAN_STATES_DICT = {state: i+1 for i, state in enumerate(NIGERIAN_STATES)}


# ============================================================
# GRADING SCALES
# ============================================================

GRADING_SCALES = [
    ('british_nigerian', 'British/Nigerian (A=70-100, 5.0)'),
    ('american', 'American (A=90-100, 4.0)'),
    ('standard', 'Standard (A=80-100, 4.0)'),
    ('custom', 'Custom'),
]

GRADE_POINTS = {
    'british_nigerian': {
        'A': 5.0, 'B': 4.0, 'C': 3.0, 'D': 2.0, 'E': 1.0, 'F': 0.0
    },
    'american': {
        'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0
    },
    'standard': {
        'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0
    }
}

GRADE_BOUNDARIES = {
    'british_nigerian': {'A': 70, 'B': 60, 'C': 50, 'D': 40, 'E': 30},
    'american': {'A': 90, 'B': 80, 'C': 70, 'D': 60},
    'standard': {'A': 80, 'B': 70, 'C': 60, 'D': 50}
}


# ============================================================
# ACADEMIC PROGRAMS
# ============================================================

ACADEMIC_PROGRAMS = [
    ('ND', 'National Diploma'),
    ('HND', 'Higher National Diploma'),
    ('BSC', 'Bachelor of Science'),
    ('BSC_ED', 'Bachelor of Education'),
    ('BA', 'Bachelor of Arts'),
    ('BENG', 'Bachelor of Engineering'),
    ('MBBS', 'Bachelor of Medicine'),
    ('LLB', 'Bachelor of Law'),
    ('MSC', 'Master of Science'),
    ('MA', 'Master of Arts'),
    ('ME', 'Master of Engineering'),
    ('MBA', 'Master of Business Administration'),
    ('PHD', 'Doctor of Philosophy'),
]


# ============================================================
# PAYMENT STATUS
# ============================================================

PAYMENT_STATUS = [
    ('pending', 'Pending'),
    ('processing', 'Processing'),
    ('completed', 'Completed'),
    ('failed', 'Failed'),
    ('refunded', 'Refunded'),
    ('cancelled', 'Cancelled'),
]


# ============================================================
# ATTENDANCE STATUS
# ============================================================

ATTENDANCE_STATUS = [
    ('present', 'Present'),
    ('absent', 'Absent'),
    ('late', 'Late'),
    ('excused', 'Excused'),
]


# ============================================================
# USER ROLES
# ============================================================

USER_ROLES = [
    ('admin', 'Administrator'),
    ('staff', 'Staff'),
    ('teacher', 'Teacher'),
    ('student', 'Student'),
    ('parent', 'Parent'),
    ('guest', 'Guest'),
]

STAFF_ROLES = [
    ('admin', 'Administrator'),
    ('principal', 'Principal'),
    ('vice_principal', 'Vice Principal'),
    ('dean', 'Dean'),
    ('hod', 'Head of Department'),
    ('lecturer', 'Lecturer'),
    ('teacher', 'Teacher'),
    ('counsellor', 'Counsellor'),
    ('librarian', 'Librarian'),
    ('accountant', 'Accountant'),
    ('secretary', 'Secretary'),
    ('security', 'Security'),
    ('cleaner', 'Cleaner'),
]


# ============================================================
# CERTIFICATE TYPES
# ============================================================

CERTIFICATE_TYPES = [
    ('transcript', 'Transcript'),
    ('certificate', 'Certificate'),
    ('degree', 'Degree'),
    ('diploma', 'Diploma'),
    ('completion', 'Completion Letter'),
    ('recommendation', 'Recommendation Letter'),
]


# ============================================================
# FEE TYPES
# ============================================================

FEE_TYPES = [
    ('tuition', 'Tuition Fee'),
    ('registration', 'Registration Fee'),
    ('examination', 'Examination Fee'),
    ('library', 'Library Fee'),
    ('sports', 'Sports Fee'),
    ('medical', 'Medical Fee'),
    ('development', 'Development Fee'),
    ('ICT', 'ICT Fee'),
    ('laboratory', 'Laboratory Fee'),
    ('fieldtrip', 'Field Trip Fee'),
    ('hostel', 'Hostel Fee'),
    ('feeding', 'Feeding Fee'),
    ('transport', 'Transport Fee'),
    ('uniform', 'Uniform Fee'),
    ('books', 'Books Fee'),
    ('other', 'Other'),
]


# ============================================================
# SEMESTER TYPES
# ============================================================

SEMESTER_TYPES = [
    ('first', 'First Semester'),
    ('second', 'Second Semester'),
    ('third', 'Third Semester'),
    ('rain', 'Rain Semester'),
]


# ============================================================
# SESSION STATUS
# ============================================================

SESSION_STATUS = [
    ('draft', 'Draft'),
    ('published', 'Published'),
    ('ongoing', 'Ongoing'),
    ('completed', 'Completed'),
    ('archived', 'Archived'),
]


# ============================================================
# EXAM TYPES
# ============================================================

EXAM_TYPES = [
    ('test', 'Test'),
    ('quiz', 'Quiz'),
    ('midterm', 'Midterm'),
    ('final', 'Final Exam'),
    ('assignment', 'Assignment'),
    ('project', 'Project'),
    ('practical', 'Practical'),
]


# ============================================================
# MARITAL STATUS
# ============================================================

MARITAL_STATUS = [
    ('single', 'Single'),
    ('married', 'Married'),
    ('divorced', 'Divorced'),
    ('widowed', 'Widowed'),
    ('separated', 'Separated'),
]


# ============================================================
# BLOOD TYPES
# ============================================================

BLOOD_TYPES = [
    ('A+', 'A+'), ('A-', 'A-'),
    ('B+', 'B+'), ('B-', 'B-'),
    ('O+', 'O+'), ('O-', 'O-'),
    ('AB+', 'AB+'), ('AB-', 'AB-'),
]


# ============================================================
# GENOTYPES
# ============================================================

GENOTYPES = [
    ('AA', 'AA'), ('AS', 'AS'), ('SS', 'SS'), ('AC', 'AC'),
]


# ============================================================
# TIMEZONES
# ============================================================

TIMEZONES = [
    ('Africa/Lagos', 'Africa/Lagos'),
    ('Africa/Abuja', 'Africa/Abuja'),
    ('Africa/Port Harcourt', 'Africa/Port Harcourt'),
    ('UTC', 'UTC'),
]


# ============================================================
# CURRENCY
# ============================================================

CURRENCY = [
    ('NGN', 'Nigerian Naira'),
    ('USD', 'US Dollar'),
    ('EUR', 'Euro'),
    ('GBP', 'British Pound'),
]


# ============================================================
# DEFAULT CONFIGURATION
# ============================================================

DEFAULT_SETTINGS = {
    'grading_scale_type': 'british_nigerian',
    'currency': 'NGN',
    'timezone': 'Africa/Lagos',
    'academic_year_start': '2024-09-01',
    'academic_year_end': '2025-08-31',
    'semesterDuration': 4,  # months
    'PASS_MARK': 40,
    'MIN_CREDIT': 15,
    'MAX_CREDIT': 24,
}


# ============================================================
# VALIDATION REGEX
# ============================================================

REGEX = {
    'phone_nigerian': r'^(\+234|0)[789]\d{9}$',
    'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    'student_id': r'^STU\d{8}$',
    'staff_id': r'^STF\d{8}$',
    'enrollment': r'^ENR\d{8}$',
    'invoice': r'^INV\d{9}$',
    'nigerian_names': r'^[A-Za-z\s\'-]+$',
}


# ============================================================
# PAGINATION
# ============================================================

PAGINATION = {
    'DEFAULT_PAGE_SIZE': 20,
    'MAX_PAGE_SIZE': 100,
    'MIN_PAGE_SIZE': 5,
}


# ============================================================
# FILE UPLOAD
# ============================================================

FILE_UPLOAD = {
    'MAX_SIZE': 10 * 1024 * 1024,  # 10MB
    'ALLOWED_TYPES': ['jpg', 'jpeg', 'png', 'pdf', 'doc', 'docx'],
    'ALLOWED_MIME': ['image/jpeg', 'image/png', 'application/pdf'],
}


# ============================================================
# API RATE LIMITS
# ============================================================

RATE_LIMITS = {
    'DEFAULT': '100/m',
    'AUTH': '5/m',
    'SEARCH': '30/m',
    'EXPORT': '10/m',
    'UPLOAD': '20/h',
}