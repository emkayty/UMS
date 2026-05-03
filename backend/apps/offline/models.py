"""
Offline Mode Models
UMS Offline Functionality
"""

from django.db import models
from django.utils import timezone


class OfflineSession(models.Model):
    """Model for offline sync sessions."""
    
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        SYNCING = 'syncing', 'Syncing'
        COMPLETED = 'completed', 'Completed'
        FAILED = 'failed', 'Failed'
    
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='offline_sessions'
    )
    
    device_id = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    
    pending_changes = models.JSONField(default=list)
    synced_changes = models.JSONField(default=list)
    
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"OfflineSession {self.id} - {self.user}"


class SyncQueue(models.Model):
    """Queue for pending sync operations."""
    
    class OperationType(models.TextChoices):
        CREATE = 'create', 'Create'
        UPDATE = 'update', 'Update'
        DELETE = 'delete', 'Delete'
    
    session = models.ForeignKey(
        OfflineSession,
        on_delete=models.CASCADE,
        related_name='sync_queue'
    )
    
    operation = models.CharField(max_length=20, choices=OperationType.choices)
    model_name = models.CharField(max_length=100)
    record_id = models.CharField(max_length=100)
    data = models.JSONField()
    
    synced = models.BooleanField(default=False)
    error_message = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.operation} {self.model_name}.{self.record_id}"


class OfflineData(models.Model):
    """Cached offline data for mobile app."""
    
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='offline_data'
    )
    
    model_name = models.CharField(max_length=100)
    record_id = models.CharField(max_length=100)
    data = models.JSONField()
    
    cached_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    class Meta:
        unique_together = ['user', 'model_name', 'record_id']
        indexes = [
            models.Index(fields=['user', 'model_name']),
        ]
    
    def __str__(self):
        return f"{self.model_name}.{self.record_id}"
    
    def is_expired(self):
        return timezone.now() > self.expires_at