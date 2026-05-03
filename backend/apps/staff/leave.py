"""
Staff Leave Management System
Full leave application and approval workflow
"""

import uuid
from django.db import models
from apps.accounts.models import User


class LeaveType(models.TextChoices):
    # Leave Types
    ANNUAL = 'annual', 'Annual Leave'
    SICK = 'sick', 'Sick Leave'
    CASUAL = 'casual', 'Casual Leave'
    STUDY = 'study', 'Study Leave'
    MATERNITY = 'maternity', 'Maternity Leave'
    PATERNITY = 'paternity', 'Paternity Leave'
    COMPASSIONATE = 'compassionate', 'Compassionate Leave'
    EXAM = 'exam', 'Examination Leave'
    UNPAID = 'unpaid', 'Unpaid Leave'
    SABATICAL = 'sabbatical', 'Sabbatical Leave'
    
    # US Types
    VACATION = 'vacation', 'Vacation Leave'
    PERSONAL = 'personal', 'Personal Leave'
    BEREAVEMENT = 'bereavement', 'Bereavement Leave'
    JURY_DUTY = 'jury_duty', 'Jury Duty'
    VOTING = 'voting', 'Voting Leave'


class LeaveStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    APPROVED = 'approved', 'Approved'
    REJECTED = 'rejected', 'Rejected'
    CANCELLED = 'cancelled', 'Cancelled'


class LeaveDuration(models.TextChoices):
    FULL = 'full', 'Full Day'
    HALF = 'half', 'Half Day'
    HOURS = 'hours', 'Hours'


# ============================================================
# LEAVE ENTITLEMENT
# ============================================================

class LeaveEntitlement(models.Model):
    """Staff leave entitlement per year."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Staff & Type
    staff = models.ForeignKey(
        'staff.StaffProfile', on_delete=models.CASCADE,
        related_name='leave_entitlements'
    )
    leave_type = models.CharField(max_length=20, choices=LeaveType.choices)
    
    # Days
    total_days = models.IntegerField(default=0)
    used_days = models.IntegerField(default=0)
    remaining_days = models.IntegerField(default=0)
    
    # Session
    session = models.ForeignKey(
        'academic.AcademicSession', on_delete=models.CASCADE
    )
    
    class Meta:
        db_table = 'leave_entitlements'
        unique_together = ['staff', 'leave_type', 'session']

    def __str__(self):
        return f"{self.staff.staff_id} - {self.leave_type}"


# ============================================================
# LEAVE APPLICATION
# ============================================================

class LeaveApplication(models.Model):
    """Staff leave application."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Staff
    staff = models.ForeignKey(
        'staff.StaffProfile', on_delete=models.CASCADE,
        related_name='leave_applications'
    )
    leave_type = models.CharField(max_length=20, choices=LeaveType.choices)
    
    # Duration
    start_date = models.DateField()
    end_date = models.DateField()
    duration_type = models.CharField(
        max_length=10, choices=LeaveDuration.choices,
        default=LeaveDuration.FULL
    )
    hours_requested = models.IntegerField(default=0, blank=True)
    
    # Reason
    reason = models.TextField()
    
    # Coverage
    lecture_notes = models.TextField(blank=True)
    cover_lecturer = models.ForeignKey(
        'staff.StaffProfile', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='covering_leaves'
    )
    
    # Attachments
    medical_certificate = models.FileField(
        upload_to='leave/certificates/', null=True, blank=True
    )
    other_attachments = models.JSONField(default=list)
    
    # Status
    status = models.CharField(
        max_length=20, choices=LeaveStatus.choices,
        default=LeaveStatus.PENDING
    )
    
    # Approvals
    recommended_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='recommended_leaves'
    )
    recommended_at = models.DateTimeField(null=True, blank=True)
    recommended_remark = models.TextField(blank=True)
    
    approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='approved_leaves'
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    approval_remark = models.TextField(blank=True)
    
    rejected_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='rejected_leaves'
    )
    rejected_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    
    # Dates
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'leave_applications'
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.staff.staff_id} - {self.leave_type}"


# ============================================================
# LEAVE ROSTER
# ============================================================

class LeaveRoster(models.Model):
    """Staff leave roster/calendar."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    session = models.ForeignKey(
        'academic.AcademicSession', on_delete=models.CASCADE
    )
    
    staff = models.ForeignKey(
        'staff.StaffProfile', on_delete=models.CASCADE
    )
    
    leave_type = models.CharField(max_length=20, choices=LeaveType.choices)
    start_date = models.DateField()
    end_date = models.DateField()
    
    is_approved = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'leave_roster'

    def __str__(self):
        return f"{self.staff.staff_id} - {self.start_date}"


# ============================================================
# LEAVE REPORT
# ============================================================

class LeaveReport(models.Model):
    """Annual leave report."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    staff = models.ForeignKey(
        'staff.StaffProfile', on_delete=models.CASCADE
    )
    session = models.ForeignKey(
        'academic.AcademicSession', on_delete=models.CASCADE
    )
    
    total_entitled = models.IntegerField(default=0)
    total_taken = models.IntegerField(default=0)
    total_remaining = models.IntegerField(default=0)
    carry_over = models.IntegerField(default=0)
    
    summary = models.JSONField(default=dict)
    
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'leave_reports'
        unique_together = ['staff', 'session']

    def __str__(self):
        return f"{self.staff.staff_id} - {self.session.name}"