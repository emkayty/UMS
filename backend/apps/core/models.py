"""
CORE MODELS - Consolidated University Models
All core shared models to prevent duplication
"""

from django.db import models
import uuid
from django.conf import settings


# ============================================================
# SHARED ENUMS
# ============================================================

class UserRole(models.TextChoices):
    STUDENT = 'student', 'Student'
    LECTURER = 'lecturer', 'Lecturer'
    HOD = 'hod', 'Head of Department'
    DEAN = 'dean', 'Dean'
    REGISTRAR = 'registrar', 'Registrar'
    BURSAR = 'bursar', 'Bursar'
    INSTITUTION_ADMIN = 'institution_admin', 'Institution Admin'
    PARENT = 'parent', 'Parent'
    GUARDIAN = 'guardian', 'Guardian'


class Gender(models.TextChoices):
    MALE = 'male', 'Male'
    FEMALE = 'female', 'Female'
    OTHER = 'other', 'Other'


class GradeLetter(models.TextChoices):
    A = 'A', 'Excellent'
    B = 'B', 'Very Good'
    C = 'C', 'Good'
    D = 'D', 'Pass'
    F = 'F', 'Fail'


# ============================================================
# CORE ACADEMIC MODELS
# ============================================================

class Faculty(models.Model):
    """Faculty/College."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=10, unique=True)
    dean = models.ForeignKey(
        'staff.StaffProfile',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='faculty_as_dean'
    )
    established_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = 'Faculties'
        ordering = ['name']


class Department(models.Model):
    """Academic Department."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=10, unique=True)
    hod = models.ForeignKey(
        'staff.StaffProfile',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='department_as_hod'
    )
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['faculty__name', 'name']


class Programme(models.Model):
    """Academic Programme."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='programmes')
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    
    DEGREE = [
        ('bachelor', 'Bachelor'),
        ('master', 'Master'),
        ('phd', 'PhD'),
        ('diploma', 'Diploma'),
        ('certificate', 'Certificate'),
    ]
    degree_type = models.CharField(max_length=20, choices=DEGREE)
    
    duration_years = models.IntegerField(default=4)
    minimum_gpa = models.DecimalField(max_digits=3, decimal_places=2, default=1.5)
    is_accredited = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['department__name', 'name']


class Course(models.Model):
    """Course/Unit."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE, related_name='courses')
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    credit_units = models.IntegerField(default=3)
    
    LEVEL = [
        ('100', '100 Level'),
        ('200', '200 Level'),
        ('300', '300 Level'),
        ('400', '400 Level'),
    ]
    level = models.CharField(max_length=10, choices=LEVEL, default='100')
    
    SEMESTER = [
        ('first', 'First'),
        ('second', 'Second'),
    ]
    semester = models.CharField(max_length=10, choices=SEMESTER, default='first')
    
    is_compulsory = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['programme', 'code']
        ordering = ['level', 'code']


class AcademicSession(models.Model):
    """Academic Session."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-start_date']


class Semester(models.Model):
    """Academic Semester."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, related_name='semesters')
    
    SEMESTER = [
        ('first', 'First'),
        ('second', 'Second'),
    ]
    semester = models.CharField(max_length=10, choices=SEMESTER)
    
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['session', 'semester']


# ============================================================
# CORE STUDENT MODELS
# ============================================================

class StudentProfile(models.Model):
    """Student Profile."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )
    student_id = models.CharField(max_length=20, unique=True)
    programme = models.ForeignKey(
        Programme,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    current_level = models.CharField(max_length=10, default='100')
    entry_year = models.IntegerField(null=True, blank=True)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    
    STATUS = [
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('graduated', 'Graduated'),
        ('withdrawn', 'Withdrawn'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='active')
    clearance_complete = models.BooleanField(default=False)
    blood_group = models.CharField(max_length=5, blank=True)
    genotype = models.CharField(max_length=5, blank=True)
    allergies = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['student_id']


class Result(models.Model):
    """Student Result."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='results'
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=5)
    grade_point = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    approved = models.BooleanField(default=False)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, related_name='+'
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='+'
    )
    
    class Meta:
        unique_together = ['student', 'course', 'session', 'semester']


# ============================================================
# CORE STAFF MODELS  
# ============================================================

class StaffProfile(models.Model):
    """Staff Profile."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='staff_profile'
    )
    staff_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    designation = models.CharField(max_length=30, default='lecturer')
    employment_date = models.DateField(null=True, blank=True)
    highest_qualification = models.CharField(max_length=50, blank=True)
    qualification_year = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class LeaveRequest(models.Model):
    """Staff Leave Request."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    staff = models.ForeignKey(
        StaffProfile,
        on_delete=models.CASCADE,
        related_name='leave_requests'
    )
    leave_type = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    days = models.IntegerField(default=0)
    reason = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='+'
    )
    created_at = models.DateTimeField(auto_now_add=True)


# ============================================================
# CORE FINANCE MODELS
# ============================================================

class FeeStructure(models.Model):
    """Fee Structure."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    level = models.CharField(max_length=10)
    school_fees = models.DecimalField(max_digits=14, decimal_places=2)
    acceptance_fee = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    other_fees = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)


class Invoice(models.Model):
    """Student Invoice."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='invoices'
    )
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    description = models.CharField(max_length=200)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('partially_paid', 'Partially Paid'),
            ('paid', 'Paid'),
        ],
        default='pending'
    )
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Payment(models.Model):
    """Payment Records."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    payment_ref = models.CharField(max_length=50, unique=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('success', 'Success'),
            ('failed', 'Failed'),
        ],
        default='pending'
    )
    gateway = models.CharField(max_length=20)
    gateway_ref = models.CharField(max_length=100, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


# ============================================================
# CORE LEARNING MODELS
# ============================================================

class CourseMaterial(models.Model):
    """Course Materials."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    material_type = models.CharField(max_length=20)
    file_url = models.CharField(max_length=500, blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Exam(models.Model):
    """Exam."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams')
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    exam_type = models.CharField(max_length=20)
    date = models.DateField()
    start_time = models.TimeField()
    duration_minutes = models.IntegerField(default=60)
    total_marks = models.IntegerField(default=100)
    pass_mark = models.IntegerField(default=40)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


# ============================================================
# CORE LIBRARY MODELS
# ============================================================

class Book(models.Model):
    """Library Book."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    isbn = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    year = models.IntegerField()
    category = models.CharField(max_length=20, default='textbook')
    total_copies = models.IntegerField(default=1)
    available_copies = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)


# ============================================================
# CORE COMMUNICATION MODELS
# ============================================================

class Announcement(models.Model):
    """Announcement."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    content = models.TextField()
    target = models.CharField(max_length=20, default='all')
    target_levels = models.JSONField(default=list)
    is_published = models.BooleanField(default=False)
    published_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, related_name='+'
    )
    created_at = models.DateTimeField(auto_now_add=True)


# ============================================================
# CONVENIENCE FUNCTIONS
# ============================================================

def get_current_session():
    """Get current academic session."""
    return AcademicSession.objects.filter(is_current=True).first()


def get_current_semester():
    """Get current semester."""
    return Semester.objects.filter(is_current=True).first()


def calculate_gpa(results):
    """Calculate GPA from results."""
    if not results:
        return 0
    total_points = sum(float(r.grade_point * r.course.credit_units) for r in results)
    total_units = sum(r.course.credit_units for r in results)
    return round(total_points / total_units, 2) if total_units > 0 else 0


def get_grade_score(score):
    """Convert score to grade."""
    if score >= 70:
        return 'A', 4.0
    elif score >= 60:
        return 'B', 3.0
    elif score >= 50:
        return 'C', 2.0
    elif score >= 40:
        return 'D', 1.0
    else:
        return 'F', 0.0