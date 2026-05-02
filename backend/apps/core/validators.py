"""
VALIDATORS - Standardized Validation Functions
Central validation logic for the entire system
"""

import re
from django.core.exceptions import ValidationError
from django.utils import timezone


# ============================================================
# CORE VALIDATORS
# ============================================================

def validate_not_empty(value, field_name: str = 'Field'):
    """Validate field is not empty."""
    if not value or str(value).strip() == '':
        raise ValidationError(f'{field_name} cannot be empty')


def validate_min_length(value: str, min_length: int, field_name: str = 'Field'):
    """Validate minimum length."""
    if len(str(value)) < min_length:
        raise ValidationError(
            f'{field_name} must be at least {min_length} characters'
        )


def validate_max_length(value: str, max_length: int, field_name: str = 'Field'):
    """Validate maximum length."""
    if len(str(value)) > max_length:
        raise ValidationError(
            f'{field_name} must not exceed {max_length} characters'
        )


def validate_length_range(
    value: str, 
    min_length: int, 
    max_length: int, 
    field_name: str = 'Field'
):
    """Validate length within range."""
    validate_min_length(value, min_length, field_name)
    validate_max_length(value, max_length, field_name)


# ============================================================
# EMAIL VALIDATORS
# ============================================================

EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')


def validate_email(value: str):
    """Validate email format."""
    if not EMAIL_PATTERN.match(str(value)):
        raise ValidationError('Enter a valid email address.')
    return True


def validate_student_email(value: str):
    """Validate student email domain."""
    if not value.endswith('@student.university.edu'):
        raise ValidationError('Use your student email address.')
    return True


def validate_staff_email(value: str):
    """Validate staff email domain."""
    if not value.endswith('@university.edu'):
        raise ValidationError('Use your staff email address.')
    return True


# ============================================================
# PHONE VALIDATORS
# ============================================================

PHONE_PATTERN = re.compile(r'^\+?[0-9]{10,15}$')


def validate_phone(value: str):
    """Validate phone number."""
    cleaned = re.sub(r'[\s\-\(\)]', '', str(value))
    if not PHONE_PATTERN.match(cleaned):
        raise ValidationError('Enter a valid phone number.')
    return True


def validate_phone_nigeria(value: str):
    """Validate Nigerian phone number."""
    cleaned = re.sub(r'[\s\-\(\)]', '', str(value))
    if not (cleaned.startswith('+234') or cleaned.startswith('234') or cleaned.startswith('0')):
        raise ValidationError('Enter a valid Nigerian phone number.')
    return True


# ============================================================
# ID VALIDATORS
# ============================================================

def validate_student_id(value: str):
    """Validate student ID format."""
    if not value or len(value) < 6:
        raise ValidationError('Invalid student ID.')
    
    try:
        int(value[:4])
    except ValueError:
        raise ValidationError('Invalid student ID format.')
    return True


def validate_staff_id(value: str):
    """Validate staff ID format."""
    if not value or len(value) < 4:
        raise ValidationError('Invalid staff ID.')
    return True


# ============================================================
# DATE VALIDATORS
# ============================================================

def validate_future_date(value, field_name: str = 'Date'):
    """Validate date is in the future."""
    if value and value <= timezone.now().date():
        raise ValidationError(f'{field_name} must be in the future.')
    return True


def validate_past_date(value, field_name: str = 'Date'):
    """Validate date is in the past."""
    if value and value >= timezone.now().date():
        raise ValidationError(f'{field_name} must be in the past.')
    return True


def validate_date_range(start_date, end_date):
    """Validate date range."""
    if start_date and end_date and start_date > end_date:
        raise ValidationError('End date must be after start date.')
    return True


def validate_not_past_date(value, field_name: str = 'Date'):
    """Validate date is not in the past."""
    if value and value < timezone.now().date():
        raise ValidationError(f'{field_name} cannot be in the past.')
    return True


# ============================================================
# NUMBER VALIDATORS
# ============================================================

def validate_positive(value, field_name: str = 'Value'):
    """Validate positive number."""
    if value and float(value) <= 0:
        raise ValidationError(f'{field_name} must be positive.')
    return True


def validate_negative(value, field_name: str = 'Value'):
    """Validate negative number."""
    if value and float(value) >= 0:
        raise ValidationError(f'{field_name} must be negative.')
    return True


def validate_range(value: float, min_val: float, max_val: float, field_name: str = 'Value'):
    """Validate value within range."""
    if value and (float(value) < min_val or float(value) > max_val):
        raise ValidationError(
            f'{field_name} must be between {min_val} and {max_val}.'
        )
    return True


def validate_percentage(value, field_name: str = 'Percentage'):
    """Validate percentage (0-100)."""
    return validate_range(value, 0, 100, field_name)


# ============================================================
# GRADE VALIDATORS
# ============================================================

def validate_score(value, field_name: str = 'Score'):
    """Validate score (0-100)."""
    return validate_range(value, 0, 100, field_name)


def validate_gpa(value, field_name: str = 'GPA'):
    """Validate GPA (0-4)."""
    return validate_range(value, 0, 4.0, field_name)


def validate_grade(grade: str):
    """Validate letter grade."""
    valid_grades = ['A', 'AB', 'B', 'BC', 'C', 'CD', 'D', 'F']
    if grade.upper() not in valid_grades:
        raise ValidationError('Invalid grade.')
    return True


# ============================================================
# CHOICE VALIDATORS
# ============================================================

def validate_choice(value, choices: list, field_name: str = 'Value'):
    """Validate choice field."""
    if value not in choices:
        raise ValidationError(f'Invalid {field_name}.')
    return True


def validate_level(value):
    """Validate student level."""
    valid_levels = ['100', '200', '300', '400', '500', '600']
    return validate_choice(value, valid_levels, 'Level')


def validate_semester(value):
    """Validate semester."""
    return validate_choice(value, ['first', 'second', 'third'], 'Semester')


def validate_gender(value):
    """Validate gender."""
    return validate_choice(value, ['male', 'female', 'other'], 'Gender')


# ============================================================
# FILE VALIDATORS
# ============================================================

def validate_file_extension(value, allowed: list, field_name: str = 'File'):
    """Validate file extension."""
    import os
    ext = os.path.splitext(str(value))[1].lower().lstrip('.')
    if ext not in allowed:
        raise ValidationError(
            f'Invalid {field_name} type. Allowed: {", ".join(allowed)}'
        )
    return True


def validate_image(value):
    """Validate image file."""
    return validate_file_extension(value, ['jpg', 'jpeg', 'png', 'gif'])


def validate_pdf(value):
    """Validate PDF file."""
    return validate_file_extension(value, ['pdf'])


def validate_document(value):
    """Validate document file."""
    return validate_file_extension(value, ['pdf', 'doc', 'docx', 'xls', 'xlsx'])


def validate_file_size(value, max_mb: int = 10):
    """Validate file size."""
    max_size = max_mb * 1024 * 1024
    if value.size > max_size:
        raise ValidationError(f'File size must not exceed {max_mb}MB.')
    return True


# ============================================================
# PASSWORD VALIDATORS
# ============================================================

def validate_password_strength(value: str):
    """Validate password strength."""
    if len(value) < 8:
        raise ValidationError('Password must be at least 8 characters.')
    
    if not re.search(r'[A-Z]', value):
        raise ValidationError('Password must contain uppercase letter.')
    
    if not re.search(r'[a-z]', value):
        raise ValidationError('Password must contain lowercase letter.')
    
    if not re.search(r'[0-9]', value):
        raise ValidationError('Password must contain a number.')
    
    return True


def validate_password_match(password1, password2):
    """Validate passwords match."""
    if password1 != password2:
        raise ValidationError('Passwords do not match.')
    return True


# ============================================================
# UNIQUE VALIDATORS
# ============================================================

def validate_unique(model, field: str, value, exclude_id: str = None):
    """Validate unique field."""
    qs = model.objects.filter(**{field: value})
    
    if exclude_id:
        qs = qs.exclude(id=exclude_id)
    
    if qs.exists():
        raise ValidationError(f'This {field} is already in use.')
    return True


def validate_unique_email(email, exclude_id: str = None):
    """Validate unique email."""
    from apps.accounts.models import User
    return validate_unique(User, 'email', email, exclude_id)


def validate_unique_student_id(student_id, exclude_id: str = None):
    """Validate unique student ID."""
    from apps.core.models import StudentProfile
    return validate_unique(StudentProfile, 'student_id', student_id, exclude_id)


def validate_unique_staff_id(staff_id, exclude_id: str = None):
    """Validate unique staff ID."""
    from apps.core.models import StaffProfile
    return validate_unique(StaffProfile, 'staff_id', staff_id, exclude_id)


# ============================================================
# CONDITIONAL VALIDATORS
# ============================================================

def validate_required_if(value, condition: bool, field_name: str = 'Field'):
    """Validate required if condition is true."""
    if condition and not value:
        raise ValidationError(f'{field_name} is required.')
    return True


def validate_approval_status(current_status: str, new_status: str):
    """Validate approval status transition."""
    valid_transitions = {
        'pending': ['approved', 'rejected'],
        'approved': ['pending'],
        'rejected': ['pending'],
    }
    
    if new_status not in valid_transitions.get(current_status, []):
        raise ValidationError('Invalid status transition.')
    return True


# ============================================================
# ACADEMIC VALIDATORS
# ============================================================

def validate_course_registration_courses(courses: list, max_units: int = 24):
    """Validate course registration."""
    total_units = sum(c.get('credit_units', 0) for c in courses)
    
    if total_units > max_units:
        raise ValidationError(f'Cannot register more than {max_units} units.')
    
    return True


def validate_prerequisite_met(student, course):
    """Validate prerequisite met."""
    # This would check if student passed prerequisite courses
    return True


def validate_exam_registration_eligibility(student, exam):
    """Validate exam eligibility."""
    # Check if registered for course
    # Check if no outstanding fees
    # Check if clearance complete
    return True


# ============================================================
# FEE VALIDATORS
# ============================================================

def validate_payment_amount(amount: float, expected: float):
    """Validate payment amount."""
    if amount < expected:
        raise ValidationError('Payment amount is less than expected.')
    return True


def validate_installment_plan(installments: list):
    """Validate installment plan."""
    if not installments:
        raise ValidationError('At least one installment required.')
    
    total = sum(i.get('percentage', 0) for i in installments)
    if total != 100:
        raise ValidationError('Installment percentages must total to 100.')
    return True


# ============================================================
# COMPOSITE VALIDATORS
# ============================================================

def validate_profile_complete(user):
    """Validate profile is complete."""
    errors = {}
    
    if not user.first_name:
        errors['first_name'] = 'First name is required.'
    
    if not user.last_name:
        errors['last_name'] = 'Last name is required.'
    
    if not user.email:
        errors['email'] = 'Email is required.'
    
    if errors:
        raise ValidationError(errors)
    
    return True


def validate_registration_eligibility(student):
    """Validate student can register."""
    errors = {}
    
    if student.status != 'active':
        errors['status'] = 'Student is not active.'
    
    if not student.programme:
        errors['programme'] = 'Programme not assigned.'
    
    if errors:
        raise ValidationError(errors)
    
    return True