"""
Database Backup & Restore System
Automated backups for PostgreSQL/MySQL
"""

import uuid
from django.db import models
from django.contrib.auth.models import User


class BackupStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    IN_PROGRESS = 'in_progress', 'In Progress'
    COMPLETED = 'completed', 'Completed'
    FAILED = 'failed', 'Failed'


class BackupType(models.TextChoices):
    FULL = 'full', 'Full Database'
    PARTIAL = 'partial', 'Partial (Tables)'
    INCREMENTAL = 'incremental', 'Incremental'


# ============================================================
# BACKUP SCHEDULE
# ============================================================

class BackupSchedule(models.Model):
    """Automated backup schedule."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=100)
    
    # Schedule
    backup_type = models.CharField(
        max_length=15, choices=BackupType.choices,
        default=BackupType.FULL
    )
    
    frequency = models.CharField(
        max_length=20,
        choices=[
            ('hourly', 'Hourly'),
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
        ]
    )
    time_of_day = models.TimeField()
    day_of_week = models.IntegerField(
        null=True, blank=True,
        help_text='0=Monday, 6=Sunday'
    )
    day_of_month = models.IntegerField(
        null=True, blank=True,
        help_text='1-31'
    )
    
    # Retention
    keep_local_copies = models.IntegerField(default=7)
    keep_remote_copies = models.IntegerField(default=30)
    
    # Storage
    remote_enabled = models.BooleanField(default=False)
    remote_bucket = models.CharField(max_length=100, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'backup_schedules'

    def __str__(self):
        return f"{self.name} - {self.frequency}"


# ============================================================
# BACKUP RECORD
# ============================================================

class BackupRecord(models.Model):
    """Backup execution record."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    schedule = models.ForeignKey(
        BackupSchedule, on_delete=models.SET_NULL,
        null=True, blank=True
    )
    
    # Backup details
    backup_type = models.CharField(
        max_length=15, choices=BackupType.choices
    )
    
    # Status
    status = models.CharField(
        max_length=20, choices=BackupStatus.choices,
        default=BackupStatus.PENDING
    )
    
    # File info
    file_name = models.CharField(max_length=200, blank=True)
    file_size = models.BigIntegerField(
        null=True, blank=True, help_text='bytes'
    )
    file_hash = models.CharField(max_length=64, blank=True)
    
    # Storage
    local_path = models.CharField(max_length=300, blank=True)
    remote_path = models.CharField(max_length=300, blank=True)
    remote_url = models.URLField(blank=True)
    
    # Timing
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(
        null=True, blank=True, help_text='seconds'
    )
    
    # Errors
    error_message = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'backup_records'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.backup_type} - {self.status}"


# ============================================================
# RESTORE RECORD
# ============================================================

class RestoreRecord(models.Model):
    """Database restore record."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    backup = models.ForeignKey(
        BackupRecord, on_delete=models.CASCADE
    )
    
    # User
    requested_by = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True
    )
    
    # Status
    status = models.CharField(
        max_length=20, choices=BackupStatus.choices,
        default=BackupStatus.PENDING
    )
    
    # Timing
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Errors
    error_message = models.TextField(blank=True)
    
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'restore_records'

    def __str__(self):
        return f"Restore - {self.backup.file_name}"