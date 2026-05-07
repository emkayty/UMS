"""
Data Validation Utilities for UMS

Provides common validation functions for data integrity.
"""
import re
from typing import Any, List, Optional, Tuple
from datetime import datetime


def validate_email(email: str) -> Tuple[bool, str]:
    """Validate email address"""
    if not email:
        return False, "Email is required"
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Invalid email format"
    
    return True, ""


def validate_phone(phone: str) -> Tuple[bool, str]:
    """Validate phone number"""
    if not phone:
        return False, "Phone is required"
    
    # Remove common characters
    cleaned = re.sub(r'[\s\-\(\)\+]', '', phone)
    
    # Check for digits
    if not cleaned.isdigit():
        return False, "Phone must contain only digits"
    
    # Check length
    if len(cleaned) < 10 or len(cleaned) > 15:
        return False, "Phone must be 10-15 digits"
    
    return True, ""


def validate_student_id(student_id: str) -> Tuple[bool, str]:
    """Validate student ID format"""
    if not student_id:
        return False, "Student ID is required"
    
    # Standard format: YR/DEPT/XXX
    # e.g., 24/CS/001
    pattern = r'^\d{2}/[A-Z]{2,4}/\d{3,5}$'
    if not re.match(pattern, student_id):
        return False, "Invalid student ID format (YY/DEPT/XXX)"
    
    return True, ""


def validate_staff_id(staff_id: str) -> Tuple[bool, str]:
    """Validate staff ID format"""
    if not staff_id:
        return False, "Staff ID is required"
    
    # Standard format: STF/XXX or FAC/XXX
    pattern = r'^(STF|FAC|AD|TS)/\d{3,5}$'
    if not re.match(pattern, staff_id):
        return False, "Invalid staff ID format"
    
    return True, ""


def validate_nigerian_phone(phone: str) -> Tuple[bool, str]:
    """Validate Nigerian phone number"""
    if not phone:
        return False, "Phone is required"
    
    # Remove common characters
    cleaned = re.sub(r'[\s\-\(\)\+]', '', phone)
    
    # Nigerian format: 080XXXXXXXX (11 digits, starts with 0 or 234)
    if cleaned.startswith('234') and len(cleaned) == 13:
        return True, ""
    if cleaned.startswith('0') and len(cleaned) == 11:
        return True, ""
    if len(cleaned) == 10:
        return True, ""
    
    return False, "Invalid Nigerian phone format"


def validate_date_range(start: datetime, end: datetime) -> Tuple[bool, str]:
    """Validate date range"""
    if start >= end:
        return False, "Start date must be before end date"
    
    return True, ""


def validate_gpa(gpa: float) -> Tuple[bool, str]:
    """Validate GPA value"""
    if gpa < 0.0 or gpa > 5.0:
        return False, "GPA must be between 0.0 and 5.0"
    
    return True, ""


def validate_credits(credits: int) -> Tuple[bool, str]:
    """Validate course credits"""
    if credits < 1 or credits > 10:
        return False, "Credits must be between 1 and 10"
    
    return True, ""


def validate_course_code(code: str) -> Tuple[bool, str]:
    """Validate course code format"""
    if not code:
        return False, "Course code is required"
    
    # Format: XXXNNN (e.g., CS101)
    if len(code) < 4 or len(code) > 8:
        return False, "Course code must be 4-8 characters"
    
    return True, ""


def validate_amount(amount: float) -> Tuple[bool, str]:
    """Validate payment amount"""
    if amount <= 0:
        return False, "Amount must be positive"
    
    if amount > 10000000:  # 10 million Naira
        return False, "Amount exceeds maximum"
    
    return True, ""


class ValidationResult:
    """Validation result container"""
    
    def __init__(self, valid: bool = True, errors: List[str] = None):
        self.valid = valid
        self.errors = errors or []
    
    def add_error(self, error: str):
        """Add error"""
        self.valid = False
        self.errors.append(error)
    
    def __bool__(self):
        return self.valid
    
    def __str__(self):
        return ", ".join(self.errors) if self.errors else "Valid"


def validate_student_data(data: dict) -> ValidationResult:
    """Validate complete student data"""
    result = ValidationResult()
    
    if 'email' in data:
        valid, error = validate_email(data['email'])
        if not valid:
            result.add_error(f"email: {error}")
    
    if 'phone' in data:
        valid, error = validate_nigerian_phone(data['phone'])
        if not valid:
            result.add_error(f"phone: {error}")
    
    if 'student_id' in data:
        valid, error = validate_student_id(data['student_id'])
        if not valid:
            result.add_error(f"student_id: {error}")
    
    return result