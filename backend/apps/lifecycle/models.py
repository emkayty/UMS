"""
Complete Student & Staff Lifecycle Models
Nigerian & Global University Standards
"""

import uuid
from django.db import models


# ==================== STUDENT LIFECYCLE ====================

class ApplicantData(models.Model):
    """Pre-admission applicant data."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, null=True, blank=True)
    
    # Personal
    title = models.CharField(max_length=10, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=50, default='Nigerian')
    state_of_origin = models.CharField(max_length=50, blank=True)
    local_govt_area = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    
    # Parents/Guardian
    father_name = models.CharField(max_length=100, blank=True)
    father_phone = models.CharField(max_length=20, blank=True)
    mother_name = models.CharField(max_length=100, blank=True)
    mother_phone = models.CharField(max_length=20, blank=True)
    guardian_name = models.CharField(max_length=100, blank=True)
    guardian_phone = models.CharField(max_length=20, blank=True)
    
    # Medical
    blood_group = models.CharField(max_length=5, blank=True)
    genotype = models.CharField(max_length=5, blank=True)
    allergies = models.TextField(blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    
    # Education
    secondary_school = models.CharField(max_length=200, blank=True)
    jamb_registration_number = models.CharField(max_length=20, blank=True)
    jamb_score = models.IntegerField(null=True, blank=True)
    o_level_results = models.JSONField(default=dict)
    
    application_status = models.CharField(max_length=20, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)


class Hostel(models.Model):
    """Hostel management."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    capacity = models.IntegerField()
    occupied = models.IntegerField(default=0)
    location = models.CharField(max_length=100)
    has_wifi = models.BooleanField(default=True)
    has_ac = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


class StudentHostelAllocation(models.Model):
    """Hostel room allocation."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student_id = models.UUIDField()
    session_id = models.UUIDField()
    hostel_id = models.UUIDField()
    block = models.CharField(max_length=20)
    floor = models.IntegerField()
    room_number = models.CharField(max_length=20)
    bed_number = models.IntegerField()
    room_type = models.CharField(max_length=20, default='double')
    hostel_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, default='allocated')
    created_at = models.DateTimeField(auto_now_add=True)


class StudentDiscipline(models.Model):
    """Student disciplinary records."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student_id = models.UUIDField()
    incident_date = models.DateField()
    incident_location = models.CharField(max_length=100)
    incident_description = models.TextField()
    offence_type = models.CharField(max_length=30)
    severity = models.CharField(max_length=20, default='minor')
    action = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20, default='reported')
    created_at = models.DateTimeField(auto_now_add=True)


class AlumniRecord(models.Model):
    """Alumni tracking."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student_id = models.UUIDField()
    graduation_year = models.IntegerField()
    degree_awarded = models.CharField(max_length=100)
    class_of_degree = models.CharField(max_length=30)
    is_employed = models.BooleanField(default=False)
    employer_name = models.CharField(max_length=200, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    updated_at = models.DateTimeField(auto_now=True)


# ==================== STAFF LIFECYCLE ====================

class JobPosting(models.Model):
    """Job vacancy posting."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    department_id = models.UUIDField(null=True, blank=True)
    employment_type = models.CharField(max_length=20, default='permanent')
    level = models.CharField(max_length=50, default='lecturer')
    minimum_qualification = models.CharField(max_length=50, default='PhD')
    job_description = models.TextField()
    posting_date = models.DateField()
    closing_date = models.DateField()
    status = models.CharField(max_length=20, default='open')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class JobApplication(models.Model):
    """Job application tracking."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job_id = models.UUIDField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    cv_url = models.URLField(blank=True)
    highest_qualification = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default='applied')
    applied_at = models.DateTimeField(auto_now_add=True)


class LeaveRequest(models.Model):
    """Staff leave request."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    staff_id = models.UUIDField()
    leave_type = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    working_days = models.IntegerField()
    reason = models.TextField()
    status = models.CharField(max_length=20, default='pending')
    hod_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class LeaveBalance(models.Model):
    """Staff leave balance."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    staff_id = models.UUIDField()
    session_id = models.UUIDField()
    annual_leave_days = models.IntegerField(default=21)
    annual_used = models.IntegerField(default=0)
    sick_leave_days = models.IntegerField(default=14)
    sick_used = models.IntegerField(default=0)


class ParentAccount(models.Model):
    """Parent/Guardian portal access."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student_id = models.UUIDField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    relationship = models.CharField(max_length=20)
    user_id = models.UUIDField(null=True, blank=True)
    can_view_fees = models.BooleanField(default=True)
    can_view_results = models.BooleanField(default=True)
    can_make_payments = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
