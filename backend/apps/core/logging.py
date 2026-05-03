"""
Error Tracking & Logging System
Centralized error tracking for production
"""

import uuid
from django.db import models
from django.contrib.auth.models import User


class ErrorLevel(models.TextChoices):
    DEBUG = 'debug', 'Debug'
    INFO = 'info', 'Info'
    WARNING = 'warning', 'Warning'
    ERROR = 'error', 'Error'
    CRITICAL = 'critical', 'Critical'


class ErrorStatus(models.TextChoices):
    NEW = 'new', 'New'
    IN_PROGRESS = 'in_progress', 'In Progress'
    RESOLVED = 'resolved', 'Resolved'
    IGNORED = 'ignored', 'Ignored'


# ============================================================
# ERROR LOG
# ============================================================

class ErrorLog(models.Model):
    """Centralized error logging."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Error details
    error_type = models.CharField(max_length=100)
    message = models.TextField()
    file_path = models.CharField(max_length=200, blank=True)
    line_number = models.IntegerField(null=True, blank=True)
    
    # Level
    level = models.CharField(
        max_length=15, choices=ErrorLevel.choices,
        default=ErrorLevel.ERROR
    )
    
    # Stack trace
    stack_trace = models.TextField(blank=True)
    request_data = models.JSONField(default=dict, blank=True)
    
    # User
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    # Status
    status = models.CharField(
        max_length=20, choices=ErrorStatus.choices,
        default=ErrorStatus.NEW
    )
    
    # Resolution
    resolved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='resolved_errors'
    )
    resolution_notes = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'error_logs'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.error_type} - {self.message[:50]}"


# ============================================================
# API REQUEST LOG
# ============================================================

class APIAccessLog(models.Model):
    """API access logging."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Request
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True
    )
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=255)
    query_params = models.JSONField(default=dict)
    
    # Response
    status_code = models.IntegerField()
    response_time = models.IntegerField(
        help_text='in milliseconds'
    )
    response_size = models.IntegerField(
        help_text='in bytes', null=True, blank=True
    )
    
    # Network
    ip_address = models.GenericIPAddressField(null=True)
    user_agent = models.CharField(max_length=500, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'api_access_logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['path', '-created_at']),
        ]

    def __str__(self):
        return f"{self.method} {self.path} - {self.status_code}"


# ============================================================
# SYSTEM HEALTH CHECK
# ============================================================

class SystemHealth(models.Model):
    """System health status."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Component
    component = models.CharField(max_length=50)
    
    # Status
    is_healthy = models.BooleanField(default=True)
    response_time = models.IntegerField(null=True, blank=True)
    
    # Details
    message = models.TextField(blank=True)
    details = models.JSONField(default=dict)
    
    # Checked
    checked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'system_health'

    def __str__(self):
        return f"{self.component} - {'OK' if self.is_healthy else 'FAIL'}"


# ============================================================
# AUDIT LOG
# ============================================================

class AuditLog(models.Model):
    """Audit log for all important actions."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Action
    action = models.CharField(max_length=50)
    model_name = models.CharField(max_length=50)
    
    # Record
    record_id = models.UUIDField(null=True, blank=True)
    
    # User
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True
    )
    
    # Changes
    old_values = models.JSONField(default=dict)
    new_values = models.JSONField(default=dict)
    
    # IP
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'audit_logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['model_name', '-created_at']),
        ]

    def __str__(self):
        return f"{self.action} - {self.model_name}"