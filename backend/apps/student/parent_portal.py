"""
Parent Portal System
Parent/guardian access to student information
"""

import uuid
from django.db import models
from django.contrib.auth.models import User


class ParentAccessStatus(models.TextChoices):
    PENDING = 'pending', 'Pending Approval'
    APPROVED = 'approved', 'Approved'
    SUSPENDED = 'suspended', 'Suspended'
    REVOKED = 'revoked', 'Revoked'


# ============================================================
# PARENT ACCOUNT LINK
# ============================================================

class ParentAccount(models.Model):
    """Linked parent/guardian account."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # User account
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        related_name='parent_account'
    )
    
    # Linked students
    students = models.ManyToManyField(
        'student.StudentProfile',
        related_name='linked_parents'
    )
    
    # Relationship
    relation = models.CharField(max_length=50)
    
    # Access
    can_view_results = models.BooleanField(default=True)
    can_view_attendance = models.BooleanField(default=True)
    can_view_fees = models.BooleanField(default=True)
    can_receive_alerts = models.BooleanField(default=True)
    
    # Status
    status = models.CharField(
        max_length=20, choices=ParentAccessStatus.choices,
        default=ParentAccessStatus.PENDING
    )
    
    approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'parent_accounts'

    def __str__(self):
        return f"{self.user.email} - {self.relation}"


# ============================================================
# PARENT NOTIFICATION
# ============================================================

class ParentNotification(models.Model):
    """Notifications sent to parents."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    parent = models.ForeignKey(
        ParentAccount, on_delete=models.CASCADE,
        related_name='notifications'
    )
    student = models.ForeignKey(
        'student.StudentProfile', on_delete=models.CASCADE
    )
    
    # Notification
    notification_type = models.CharField(
        max_length=20,
        choices=[
            ('result', 'New Results'),
            ('attendance', 'Attendance Issue'),
            ('fee', 'Fee Balance'),
            ('disciplinary', 'Disciplinary'),
            ('announcement', 'Announcement'),
        ]
    )
    
    title = models.CharField(max_length=200)
    message = models.TextField()
    
    # Delivery
    sent_via_email = models.BooleanField(default=False)
    sent_via_sms = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'parent_notifications'
        ordering = ['-sent_at']

    def __str__(self):
        return f"{self.parent.user.email} - {self.title}"


# ============================================================
# PARENT LOGIN REQUEST
# ============================================================

class ParentLoginRequest(models.Model):
    """Parent login code requests."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey(
        'student.StudentProfile', on_delete=models.CASCADE,
        related_name='parent_login_requests'
    )
    
    # Parent info
    parent_name = models.CharField(max_length=100)
    parent_phone = models.CharField(max_length=20)
    parent_email = models.EmailField()
    relation = models.CharField(max_length=50)
    
    # Request
    request_token = models.CharField(max_length=64, unique=True)
    expires_at = models.DateTimeField()
    
    # Status
    is_used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'parent_login_requests'

    def __str__(self):
        return f"{self.student.matric_number} - {self.parent_name}"