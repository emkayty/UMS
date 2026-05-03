"""
Student Clearance System
Final year clearance workflow for Nigerian universities
"""

import uuid
from django.db import models
from apps.accounts.models import User


class ClearanceStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    IN_PROGRESS = 'in_progress', 'In Progress'
    COMPLETED = 'completed', 'Completed'
    REJECTED = 'rejected', 'Rejected'


class ClearanceItemStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    APPROVED = 'approved', 'Approved'
    REJECTED = 'rejected', 'Rejected'


# ============================================================
# CLEARANCE TYPES (Nigerian Universities)
# ============================================================

class ClearanceType(models.TextChoices):
    # Departmental
    DEPARTMENTAL = 'departmental', 'Departmental Clearance'
    ACADEMICS = 'academics', 'Academic Clearance'
    
    # Finance
    FINANCE = 'finance', 'Finance Clearance'
    FEES = 'fees', 'Fee Clearance'
    
    # Library
    LIBRARY = 'library', 'Library Clearance'
    BOOKS = 'books', 'Book Returns'
    
    # Admin
    ADMIN = 'admin', 'Administrative Clearance'
    HOSTEL = 'hostel', 'Hostel Clearance'
    
    # Medical
    MEDICAL = 'medical', 'Medical Clearance'
    
    # Sports
    SPORTS = 'sports', 'Sports Clearance'
    
    # Final
    CENTRAL = 'central', 'Central Clearance'


# ============================================================
# STUDENT CLEARANCE RECORD
# ============================================================

class StudentClearance(models.Model):
    """
    Student clearance record - final year graduation clearance.
    Nigerian: Must clear all departments before convocation.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Student
    student = models.ForeignKey(
        'student.StudentProfile', on_delete=models.CASCADE,
        related_name='clearance_records'
    )
    session = models.ForeignKey(
        'academic.AcademicSession', on_delete=models.CASCADE
    )
    
    # Status
    status = models.CharField(
        max_length=20, choices=ClearanceStatus.choices,
        default=ClearanceStatus.PENDING
    )
    
    # Completion
    completed_at = models.DateTimeField(null=True, blank=True)
    completed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    
    # Notes
    final_remarks = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'student_clearances'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.matric_number} - {self.status}"


# ============================================================
# CLEARANCE ITEMS
# ============================================================

class ClearanceItem(models.Model):
    """
    Individual clearance item within a student clearance.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    clearance = models.ForeignKey(
        StudentClearance, on_delete=models.CASCADE,
        related_name='items'
    )
    clearance_type = models.CharField(
        max_length=20, choices=ClearanceType.choices
    )
    status = models.CharField(
        max_length=20, choices=ClearanceItemStatus.choices,
        default=ClearanceItemStatus.PENDING
    )
    
    # Approval
    approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='clearance_approvals'
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    
    # Notes
    remarks = models.TextField(blank=True)
    rejection_reason = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'clearance_items'
        unique_together = ['clearance', 'clearance_type']

    def __str__(self):
        return f"{self.clearance.clearance_type} - {self.status}"


# ============================================================
# CLEARANCE SETUP
# ============================================================

class ClearanceSetup(models.Model):
    """
    Configurable clearance items per institution.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    clearance_type = models.CharField(
        max_length=20, choices=ClearanceType.choices,
        unique=True
    )
    
    # Department responsible
    department = models.ForeignKey(
        'academic.Department', on_delete=models.SET_NULL,
        null=True, blank=True
    )
    
    # Required for graduation
    is_required = models.BooleanField(default=True)
    
    # Order in process
    sequence = models.IntegerField(default=1)
    
    # Settings
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'clearance_setup'
        ordering = ['sequence']

    def __str__(self):
        return self.get_clearance_type_display()


# ============================================================
# DEPARTMENTS & CLEARANCE OFFICERS
# ============================================================

class ClearanceOfficer(models.Model):
    """
    Officers authorized to approve clearances.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='clearance_roles'
    )
    clearance_type = models.CharField(
        max_length=20, choices=ClearanceType.choices
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'clearance_officers'
        unique_together = ['user', 'clearance_type']

    def __str__(self):
        return f"{self.user.email} - {self.get_clearance_type_display()}"


# ============================================================
# GRADUATION LIST
# ============================================================

class GraduationList(models.Model):
    """
    Students cleared for graduation - convocation list.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    session = models.ForeignKey(
        'academic.AcademicSession', on_delete=models.CASCADE,
        related_name='graduation_lists'
    )
    
    # Convocation details
    convocation_number = models.IntegerField()
    convocation_date = models.DateField()
    venue = models.CharField(max_length=200)
    
    # Students cleared
    students = models.ManyToManyField(
        StudentClearance, related_name='graduated_in'
    )
    
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'graduation_lists'
        unique_together = ['session', 'convocation_number']

    def __str__(self):
        return f"Convocation {self.convocation_number} - {self.session.name}"


# ============================================================
# CONVOCATION REGISTRATION
# ============================================================

class ConvocationRegistration(models.Model):
    """
    Student convocation registration.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    graduation = models.ForeignKey(
        GraduationList, on_delete=models.CASCADE,
        related_name='registrations'
    )
    student = models.ForeignKey(
        'student.StudentProfile', on_delete=models.CASCADE,
        related_name='convocation_registrations'
    )
    
    # Attendance
    is_attending = models.BooleanField(default=True)
    attendance_confirmed = models.BooleanField(default=False)
    
    # Guest passes
    guests = models.IntegerField(default=2)
    
    # Outfit rental
    outfit_size = models.CharField(max_length=10, blank=True)
    outfit_collected = models.BooleanField(default=False)
    
    # Payment
    convocation_fee = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )
    payment_status = models.CharField(
        max_length=20, default='pending',
        choices=[
            ('pending', 'Pending'),
            ('paid', 'Paid'),
            ('waived', 'Waived'),
        ]
    )
    
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'convocation_registrations'
        unique_together = ['graduation', 'student']

    def __str__(self):
        return f"{self.student.matric_number} - Convocation {self.graduation.convocation_number}"