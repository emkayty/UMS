"""
Notification System
Email, SMS, Push notifications for the university
"""

import uuid
from django.db import models
from django.conf import settings
from apps.accounts.models import User


class NotificationType(models.TextChoices):
    EMAIL = 'email', 'Email'
    SMS = 'sms', 'SMS'
    PUSH = 'push', 'Push Notification'
    IN_APP = 'in_app', 'In-App'


class NotificationPriority(models.TextChoices):
    LOW = 'low', 'Low'
    NORMAL = 'normal', 'Normal'
    HIGH = 'high', 'High'
    URGENT = 'urgent', 'Urgent'


class NotificationStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    SENT = 'sent', 'Sent'
    FAILED = 'failed', 'Failed'
    DELIVERED = 'delivered', 'Delivered'


# ============================================================
# EMAIL NOTIFICATION
# ============================================================

class EmailNotification(models.Model):
    """Email notifications."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Recipients
    to_emails = models.JSONField(default=list)
    cc_emails = models.JSONField(default=list, blank=True)
    bcc_emails = models.JSONField(default=list, blank=True)
    
    # Content
    subject = models.CharField(max_length=255)
    body = models.TextField()
    html_body = models.TextField(blank=True)
    
    # Template
    email_template = models.ForeignKey(
        'EmailTemplate', on_delete=models.SET_NULL,
        null=True, blank=True
    )
    
    # Status
    status = models.CharField(
        max_length=20, choices=NotificationStatus.choices,
        default=NotificationStatus.PENDING
    )
    priority = models.CharField(
        max_length=10, choices=NotificationPriority.choices,
        default=NotificationPriority.NORMAL
    )
    
    # Sending
    sent_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    
    # Meta
    related_model = models.CharField(max_length=50, blank=True)
    related_id = models.UUIDField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'email_notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject} - {self.status}"


# ============================================================
# EMAIL TEMPLATE
# ============================================================

class EmailTemplate(models.Model):
    """Email templates for university communications."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=50, unique=True)
    
    subject = models.CharField(max_length=255)
    body = models.TextField()
    html_body = models.TextField(blank=True)
    
    # Variables: {{student_name}}, {{matric_number}}, {{session}}, etc.
    variables = models.JSONField(default=list)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'email_templates'

    def __str__(self):
        return self.name


# ============================================================
# SMS NOTIFICATION
# ============================================================

class SMSNotification(models.Model):
    """SMS notifications (using Twilio/Paystack)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Recipients
    to_phones = models.JSONField(default=list)
    
    # Content
    message = models.CharField(max_length=160)
    
    # Status
    status = models.CharField(
        max_length=20, choices=NotificationStatus.choices,
        default=NotificationStatus.PENDING
    )
    
    # Sending
    sent_at = models.DateTimeField(null=True, blank=True)
    external_id = models.CharField(max_length=100, blank=True)
    error_message = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sms_notifications'

    def __str__(self):
        return f"SMS to {len(self.to_phones)} - {self.status}"


# ============================================================
# IN-APP NOTIFICATION
# ============================================================

class InAppNotification(models.Model):
    """In-app notifications for users."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='notifications'
    )
    
    # Content
    title = models.CharField(max_length=200)
    message = models.TextField()
    link = models.CharField(max_length=255, blank=True)
    
    # Type
    notification_type = models.CharField(
        max_length=20, choices=NotificationType.choices,
        default=NotificationType.IN_APP
    )
    
    # Status
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Related
    related_model = models.CharField(max_length=50, blank=True)
    related_id = models.UUIDField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'in_app_notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.title}"


# ============================================================
# BULK NOTIFICATION CAMPAIGN
# ============================================================

class NotificationCampaign(models.Model):
    """Bulk notification campaigns."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=200)
    campaign_type = models.CharField(
        max_length=20, choices=NotificationType.choices
    )
    
    # Target
    target_users = models.JSONField(default=list)
    target_roles = models.JSONField(default=list)
    target_programmes = models.JSONField(default=list)
    target_levels = models.JSONField(default=list)
    
    # Content
    subject = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    
    # Schedule
    scheduled_at = models.DateTimeField(null=True, blank=True)
    is_scheduled = models.BooleanField(default=False)
    
    # Status
    total_recipients = models.IntegerField(default=0)
    sent_count = models.IntegerField(default=0)
    failed_count = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    
    # Template
    email_template = models.ForeignKey(
        EmailTemplate, on_delete=models.SET_NULL,
        null=True, blank=True
    )
    
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, related_name='campaigns'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notification_campaigns'

    def __str__(self):
        return self.name


# ============================================================
# NOTIFICATION PREFERENCES
# ============================================================

class NotificationPreference(models.Model):
    """User notification preferences."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        related_name='notification_preferences'
    )
    
    # Email preferences
    email_admission = models.BooleanField(default=True)
    email_academic = models.BooleanField(default=True)
    email_finance = models.BooleanField(default=True)
    email_results = models.BooleanField(default=True)
    email_genera = models.BooleanField(default=True)
    
    # SMS preferences
    sms_important = models.BooleanField(default=True)
    sms_emergency = models.BooleanField(default=True)
    sms_finance = models.BooleanField(default=False)
    
    # Push preferences
    push_enabled = models.BooleanField(default=True)
    push_sound = models.BooleanField(default=True)
    
    # In-app
    in_app_enabled = models.BooleanField(default=True)
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notification_preferences'

    def __str__(self):
        return f"{self.user.email} preferences"