"""
Missing database models and API endpoints
"""

from django.db import models
import uuid


class NotificationTemplate(models.Model):
    """Email/SMS notification templates."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=100)
    CHANNELS = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
        ('whatsapp', 'WhatsApp'),
    ]
    channel = models.CharField(max_length=20, choices=CHANNELS)
    
    subject = models.CharField(max_length=200, blank=True)
    template = models.TextField()
    variables = models.JSONField(default=list)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class EmailLog(models.Model):
    """Email sending logs."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    recipient = models.EmailField()
    subject = models.CharField(max_length=200)
    body = models.TextField()
    status = models.CharField(max_length=20, default='pending')
    error_message = models.TextField(blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class SMSLog(models.Model):
    """SMS sending logs."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    recipient = models.CharField(max_length=20)
    message = models.TextField()
    status = models.CharField(max_length=20, default='pending')
    error_message = models.TextField(blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class WebSocketConnection(models.Model):
    """WebSocket connection tracking for real-time features."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    session_key = models.CharField(max_length=100)
    connected_at = models.DateTimeField(auto_now_add=True)
    disconnected_at = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True)
    
    class Meta:
        db_table = 'websocket_connections'


class APIAccessLog(models.Model):
    """API access logs for monitoring."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    user = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True)
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=500)
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=500, blank=True)
    response_time = models.IntegerField(default=0)
    status_code = models.IntegerField(default=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['path', 'timestamp']),
        ]


class DataExport(models.Model):
    """Data export requests."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    export_type = models.CharField(max_length=50)
    filters = models.JSONField(default=dict)
    file_url = models.URLField(blank=True)
    status = models.CharField(max_length=20, default='pending')
    row_count = models.IntegerField(default=0)
    
    requested_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)


class Backup(models.Model):
    """Database backup records."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    backup_type = models.CharField(max_length=20)
    file_name = models.CharField(max_length=200)
    file_size = models.BigIntegerField(default=0)
    file_url = models.URLField(blank=True)
    status = models.CharField(max_length=20, default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)


class SystemHealth(models.Model):
    """System health monitoring."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    metric_name = models.CharField(max_length=50)
    metric_value = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['metric_name', 'recorded_at']),
        ]