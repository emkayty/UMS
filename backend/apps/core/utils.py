"""
UTILS - Standardized Utilities
Common helper functions for the entire system
"""

import hashlib
import random
import string
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any


# ============================================================
# UUID HELPERS
# ============================================================

def generate_uuid():
    """Generate a new UUID."""
    import uuid
    return uuid.uuid4()


def generate_short_code(length: int = 6):
    """Generate short alphanumeric code."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def generate_student_id(year: int, sequence: int):
    """Generate standardized student ID."""
    return f"{year}{sequence:04d}"


def generate_staff_id(department_code: str, sequence: int):
    """Generate standardized staff ID."""
    return f"{department_code}{sequence:04d}"


# ============================================================
# DATE HELPERS
# ============================================================

def parse_date(date_str: str):
    """Parse date from string."""
    for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Invalid date format: {date_str}")


def calculate_age(birth_date) -> int:
    """Calculate age from birth date."""
    today = datetime.now().date()
    return today.year - birth_date.year - (
        (today.month, today.day) < (birth_date.month, birth_date.day)
    )


def academic_year(start_date, end_date) -> str:
    """Get academic year string."""
    return f"{start_date.year}/{end_date.year}"


def session_dates(session_name: str) -> tuple:
    """Get session start and end dates."""
    year = int(session_name.split('/')[0])
    return (
        datetime(year, 9, 1).date(),
        datetime(year + 1, 8, 31).date()
    )


# ============================================================
# GRADE HELPERS
# ============================================================

def score_to_grade(score: float) -> str:
    """Convert numeric score to letter grade."""
    if score >= 70:
        return 'A'
    elif score >= 60:
        return 'B'
    elif score >= 50:
        return 'C'
    elif score >= 40:
        return 'D'
    else:
        return 'F'


def score_to_grade_point(score: float) -> float:
    """Convert numeric score to grade point."""
    if score >= 70:
        return 4.0
    elif score >= 60:
        return 3.0
    elif score >= 50:
        return 2.0
    elif score >= 40:
        return 1.0
    else:
        return 0.0


def grade_to_points(grade: str) -> float:
    """Convert letter grade to grade points."""
    grades = {
        'A': 4.0,
        'AB': 3.5,
        'B': 3.0,
        'BC': 2.5,
        'C': 2.0,
        'CD': 1.5,
        'D': 1.0,
        'F': 0.0,
    }
    return grades.get(grade.upper(), 0.0)


def calculate_gpa(results: List) -> float:
    """Calculate GPA from results."""
    if not results:
        return 0.0
    
    total_points = sum(
        r.grade_point * r.course.credit_units 
        for r in results 
        if hasattr(r, 'grade_point') and hasattr(r, 'course')
    )
    total_units = sum(
        r.course.credit_units 
        for r in results 
        if hasattr(r, 'course')
    )
    
    return round(total_points / total_units, 2) if total_units > 0 else 0.0


def calculate_cgpa(results: List) -> float:
    """Calculate CGPA from all results."""
    return calculate_gpa(results)


# ============================================================
# FEE HELPERS
# ============================================================

def calculate_fee_balance(invoices: List, payments: List) -> float:
    """Calculate outstanding fee balance."""
    total_invoiced = sum(float(i.amount) for i in invoices)
    total_paid = sum(float(p.amount) for p in payments if p.status == 'success')
    return round(total_invoiced - total_paid, 2)


def calculate_late_fee(amount: float, due_date, paid_date) -> float:
    """Calculate late payment fee."""
    if not due_date or not paid_date:
        return 0
    
    if paid_date <= due_date:
        return 0
    
    days_late = (paid_date - due_date.days)
    late_percentage = min(days_late * 0.01, 0.10)  # Max 10%
    
    return round(amount * late_percentage, 2)


def calculate_installment(amount: float, percentage: float) -> float:
    """Calculate installment amount."""
    return round(amount * (percentage / 100), 2)


# ============================================================
# ATTENDANCE HELPERS
# ============================================================

def calculate_attendance_percentage(records: List) -> float:
    """Calculate attendance percentage."""
    if not records:
        return 0.0
    
    total = len(records)
    present = sum(1 for r in records if r.status == 'present')
    
    return round((present / total) * 100, 1) if total > 0 else 0.0


def mark_attendance_status(percentage: float) -> str:
    """Mark attendance status."""
    if percentage >= 75:
        return 'excellent'
    elif percentage >= 60:
        return 'good'
    elif percentage >= 50:
        return 'warning'
    else:
        return 'critical'


# ============================================================
# NAME HELPERS
# ============================================================

def format_full_name(first: str, last: str, middle: str = '') -> str:
    """Format full name."""
    if middle:
        return f"{first} {middle} {last}"
    return f"{first} {last}"


def format_initials(name: str) -> str:
    """Get name initials."""
    parts = name.split()
    return ''.join(p[0].upper() for p in parts[:2])


def generate_username(first_name: str, last_name: str) -> str:
    """Generate username from name."""
    base = f"{first_name.lower()}.{last_name.lower()}"
    return base.replace(' ', '')


# ============================================================
# EMAIL HELPERS
# ============================================================

def generate_email(name: str, domain: str = 'university.edu') -> str:
    """Generate email from name."""
    username = name.lower().replace(' ', '.')
    return f"{username}@{domain}"


def generate_student_email(student_id: str) -> str:
    """Generate student email."""
    return f"{student_id}@student.university.edu"


def generate_staff_email(staff_id: str) -> str:
    """Generate staff email."""
    return f"{staff_id}@university.edu"


# ============================================================
# PASSWORD HELPERS
# ============================================================

def generate_password(length: int = 12) -> str:
    """Generate random password."""
    chars = string.ascii_letters + string.digits + '!@#$%^&*'
    return ''.join(random.choices(chars, k=length))


def hash_password(password: str) -> str:
    """Hash password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash."""
    return hash_password(password) == hashed


# ============================================================
# FILE HELPERS
# ============================================================

def get_file_extension(filename: str) -> str:
    """Get file extension."""
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''


def generate_file_path(instance, filename: str) -> str:
    """Generate upload file path."""
    import uuid
    ext = get_file_extension(filename)
    date = datetime.now().strftime('%Y/%m/%d')
    return f"uploads/{date}/{uuid.uuid4()}.{ext}"


def validate_file_type(filename: str, allowed: List[str]) -> bool:
    """Validate file type."""
    return get_file_extension(filename) in allowed


def validate_file_size(file_size: int, max_size: int = 10 * 1024 * 1024) -> bool:
    """Validate file size (default 10MB)."""
    return file_size <= max_size


# ============================================================
# PAGINATION HELPERS
# ============================================================

def paginate_queryset(queryset, page: int = 1, per_page: int = 20):
    """Paginate queryset."""
    start = (page - 1) * per_page
    end = start + per_page
    return queryset[start:end]


def paginate_response(data: List, page: int = 1, per_page: int = 20) -> Dict:
    """Create pagination response."""
    total = len(data)
    start = (page - 1) * per_page
    end = start + per_page
    
    return {
        'data': data[start:end],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': (total + per_page - 1) // per_page
        }
    }


# ============================================================
# RESPONSE HELPERS
# ============================================================

def success_response(data: Any = None, message: str = 'Success'):
    """Standard success response."""
    return {
        'success': True,
        'message': message,
        'data': data
    }


def error_response(message: str, errors: Dict = None):
    """Standard error response."""
    return {
        'success': False,
        'message': message,
        'errors': errors or {}
    }


def validation_error_response(errors: Dict):
    """Validation error response."""
    return error_response('Validation failed', errors)


# ============================================================
# FILTER HELPERS
# ============================================================

def build_filter_params(params: Dict) -> Dict:
    """Build filter params from request."""
    filters = {}
    
    for key, value in params.items():
        if value and value not in ['', 'null', 'None']:
            filters[key] = value
    
    return filters


def apply_filters(queryset, filters: Dict):
    """Apply filters to queryset."""
    for field, value in filters.items():
        if hasattr(queryset.model, field):
            queryset = queryset.filter(**{field: value})
    return queryset


# ============================================================
# VALIDATION HELPERS
# ============================================================

def validate_required(value, field_name: str):
    """Validate required field."""
    if not value:
        raise ValueError(f"{field_name} is required")


def validate_min_length(value: str, min_length: int, field_name: str):
    """Validate minimum length."""
    if len(value) < min_length:
        raise ValueError(f"{field_name} must be at least {min_length} characters")


def validate_max_length(value: str, max_length: int, field_name: str):
    """Validate maximum length."""
    if len(value) > max_length:
        raise ValueError(f"{field_name} must not exceed {max_length} characters")


def validate_range(value: float, min_val: float, max_val: float, field_name: str):
    """Validate numeric range."""
    if value < min_val or value > max_val:
        raise ValueError(f"{field_name} must be between {min_val} and {max_val}")


def validate_choice(value, choices: List, field_name: str):
    """Validate choice field."""
    if value not in choices:
        raise ValueError(f"Invalid {field_name}")


# ============================================================
# EXPORT HELPERS
# ============================================================

def to_csv_response(queryset, fields: List[str], filename: str):
    """Generate CSV response."""
    import csv
    from django.http import HttpResponse
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(fields)
    
    for obj in queryset:
        row = [getattr(obj, f, '') for f in fields]
        writer.writerow(row)
    
    return response


def to_json_response(data, pretty: bool = True):
    """Generate JSON response."""
    import json
    from django.http import HttpResponse
    
    indent = 2 if pretty else None
    return HttpResponse(
        json.dumps(data, indent=indent, default=str),
        content_type='application/json'
    )


# ============================================================
# CACHE HELPERS
# ============================================================

def cache_key(prefix: str, *args) -> str:
    """Generate cache key."""
    parts = [prefix] + [str(a) for a in args]
    return ':'.join(parts)


def invalidate_cache(prefix: str):
    """Invalidate cache by prefix."""
    from django.core.cache import cache
    # This would need Redis/memcached configured
    pass


# ============================================================
# LOGGING HELPERS
# ============================================================

def log_action(user, action: str, model: str, object_id: str, changes: Dict = None):
    """Log user action."""
    from apps.core.models import AuditLog
    
    return AuditLog.objects.create(
        user=user,
        action=action,
        model_name=model,
        object_id=str(object_id),
        changes=changes or {}
    )


def log_access(user, resource: str):
    """Log resource access."""
    log_action(user, 'access', resource, str(user.id))


# ============================================================
# PERMISSION HELPERS
# ============================================================

def has_role(user, role: str) -> bool:
    """Check if user has role."""
    if not hasattr(user, 'profile'):
        return False
    return user.profile.role == role


def is_student(user) -> bool:
    """Check if user is student."""
    return has_role(user, 'student')


def is_staff_user(user) -> bool:
    """Check if user is staff."""
    return has_role(user, 'lecturer')


def is_admin(user) -> bool:
    """Check if user is admin."""
    return user.is_superuser or has_role(user, 'institution_admin')