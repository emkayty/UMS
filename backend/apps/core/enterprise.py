"""
ENTERPRISE FEATURES
Advanced enterprise features for the university system
"""

from django.db import models
import uuid
from django.conf import settings


# ============================================================
# CUSTOM FIELDS
# ============================================================

class CustomField(models.Model):
    """Dynamic custom fields."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    FIELD_TYPES = [
        ('text', 'Text'),
        ('number', 'Number'),
        ('date', 'Date'),
        ('select', 'Select'),
        ('multiselect', 'Multi-Select'),
        ('boolean', 'Boolean'),
        ('file', 'File'),
    ]
    
    name = models.CharField(max_length=100)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)
    
    # Model this field applies to
    model = models.CharField(max_length=50)
    # e.g., 'student.StudentProfile', 'staff.StaffProfile'
    
    # Options for select fields
    options = models.JSONField(default=list)
    # ['option1', 'option2']
    
    # Validation
    required = models.BooleanField(default=False)
    default_value = models.JSONField(default=None, null=True)
    min_value = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    max_value = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    
    # Display
    help_text = models.CharField(max_length=200, blank=True)
    placeholder = models.CharField(max_length=100, blank=True)
    
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)


class CustomFieldValue(models.Model):
    """Values for custom fields."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    field = models.ForeignKey(
        CustomField,
        on_delete=models.CASCADE
    )
    
    object_id = models.CharField(max_length=50)
    # The ID of the object this value belongs to
    
    value = models.JSONField(default=None, null=True)
    
    class Meta:
        unique_together = ['field', 'object_id']


# ============================================================
# DATA EXPORT/IMPORT
# ============================================================

class DataExport(models.Model):
    """Data export jobs."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    EXPORT_TYPES = [
        ('csv', 'CSV'),
        ('xlsx', 'Excel'),
        ('json', 'JSON'),
        ('xml', 'XML'),
    ]
    
    name = models.CharField(max_length=100)
    export_type = models.CharField(max_length=20, choices=EXPORT_TYPES)
    
    # Model to export
    model = models.CharField(max_length=50)
    
    # Fields to export
    fields = models.JSONField(default=list)
    # ['field1', 'field2']
    
    # Filters
    filters = models.JSONField(default=dict)
    
    # Status
    STATUS = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    
    file = models.FileField(upload_to='exports/', null=True, blank=True)
    row_count = models.IntegerField(default=0)
    
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, related_name='+'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)


class DataImport(models.Model):
    """Data import jobs."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=100)
    
    IMPORT_TYPES = [
        ('csv', 'CSV'),
        ('xlsx', 'Excel'),
    ]
    
    import_type = models.CharField(max_length=20, choices=IMPORT_TYPES)
    
    # Model to import to
    model = models.CharField(max_length=50)
    
    file = models.FileField(upload_to='imports/')
    
    # Column mapping
    mapping = models.JSONField(default=dict)
    # {'column_name': 'model_field'}
    
    # Options
    update_existing = models.BooleanField(default=False)
    skip_header = models.BooleanField(default=True)
    
    STATUS = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    
    row_count = models.IntegerField(default=0)
    success_count = models.IntegerField(default=0)
    error_count = models.IntegerField(default=0)
    errors = models.JSONField(default=list)
    
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, related_name='+'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)


# ============================================================
# WEBHOOKS
# ============================================================

class Webhook(models.Model):
    """Webhooks for external integrations."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=100)
    url = models.URLField()
    
    # Events to trigger on
    EVENTS = [
        ('student.created', 'Student Created'),
        ('student.updated', 'Student Updated'),
        ('result.uploaded', 'Result Uploaded'),
        ('payment.received', 'Payment Received'),
        ('registration.completed', 'Registration Completed'),
        ('clearance.approved', 'Clearance Approved'),
    ]
    
    events = models.JSONField(default=list)
    # ['student.created', 'result.uploaded']
    
    # Authentication
    AUTH_TYPES = [
        ('none', 'None'),
        ('basic', 'Basic Auth'),
        ('bearer', 'Bearer Token'),
        ('api_key', 'API Key'),
    ]
    
    auth_type = models.CharField(max_length=20, choices=AUTH_TYPES, default='none')
    auth_secret = models.CharField(max_length=200, blank=True)
    
    # Headers
    headers = models.JSONField(default=dict)
    
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)


class WebhookDelivery(models.Model):
    """Webhook delivery logs."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    webhook = models.ForeignKey(
        Webhook,
        on_delete=models.CASCADE,
        related_name='deliveries'
    )
    
    event = models.CharField(max_length=50)
    payload = models.JSONField(default=dict)
    
    STATUS = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    
    response_code = models.IntegerField(null=True, blank=True)
    response_body = models.TextField(blank=True)
    
    attempts = models.IntegerField(default=0)
    max_attempts = models.IntegerField(default=3)
    
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)


# ============================================================
# TASK SCHEDULING
# ============================================================

class ScheduledTask(models.Model):
    """Scheduled tasks."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    # Task to run
    task_name = models.CharField(max_length=100)
    # e.g., 'myapp.tasks.send_reminders'
    
    task_params = models.JSONField(default=dict)
    
    # Schedule
    SCHEDULE_TYPES = [
        ('once', 'Once'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('cron', 'Cron'),
    ]
    
    schedule_type = models.CharField(max_length=20, choices=SCHEDULE_TYPES)
    
    # For daily/weekly/monthly
    time = models.TimeField(null=True, blank=True)
    day_of_week = models.IntegerField(null=True, blank=True)
    day_of_month = models.IntegerField(null=True, blank=True)
    
    # For cron
    cron_expression = models.CharField(max_length=50, blank=True)
    
    # Once specific
    run_at = models.DateTimeField(null=True, blank=True)
    
    STATUS = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='active')
    
    last_run = models.DateTimeField(null=True, blank=True)
    next_run = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)


class TaskExecution(models.Model):
    """Task execution logs."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    task = models.ForeignKey(
        ScheduledTask,
        on_delete=models.CASCADE,
        related_name='executions'
    )
    
    STATUS = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    
    output = models.TextField(blank=True)
    error = models.TextField(blank=True)
    
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)


# ============================================================
# MULTI-TENANT
# ============================================================

class Institution(models.Model):
    """Multi-tenant institution."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=20, unique=True)
    
    # Contact
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    
    # Branding
    logo = models.ImageField(upload_to='institutions/logos/', null=True, blank=True)
    primary_color = models.CharField(max_length=7, default='#000000')
    
    # Settings
    timezone = models.CharField(max_length=50, default='Africa/Lagos')
    date_format = models.CharField(max_length=20, default='Y-m-d')
    currency = models.CharField(max_length=3, default='NGN')
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class InstitutionSettings(models.Model):
    """Institution-specific settings."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    institution = models.OneToOneField(
        Institution,
        on_delete=models.CASCADE,
        related_name='settings'
    )
    
    # Fee settings
    late_fee_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=5)
    late_fee_grace_days = models.IntegerField(default=15)
    
    # Academic settings
    registration_deadline_days = models.IntegerField(default=30)
    min_course_units = models.IntegerField(default=12)
    max_course_units = models.IntegerField(default=24)
    
    # Attendance
    attendance_threshold = models.DecimalField(max_digits=5, decimal_places=2, default=75)
    
    # Features
    enable_online_registration = models.BooleanField(default=True)
    enable_online_payment = models.BooleanField(default=True)
    enable_hostel = models.BooleanField(default=True)
    enable_transcript = models.BooleanField(default=True)


# ============================================================
# NOTIFICATION TEMPLATES
# ============================================================

class NotificationTemplate(models.Model):
    """Email/SMS notification templates."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=100)
    
    CHANNELS = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push'),
        ('whatsapp', 'WhatsApp'),
    ]
    
    channel = models.CharField(max_length=20, choices=CHANNELS)
    
    # Content
    subject = models.CharField(max_length=200, blank=True)
    body = models.TextField()
    footer = models.TextField(blank=True)
    
    # Template variables
    variables = models.JSONField(default=list)
    # ['{{student_name}}', '{{amount}}']
    
    is_active = models.BooleanField(default=True)


class NotificationLog(models.Model):
    """Notification delivery logs."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    recipient = models.CharField(max_length=100)
    channel = models.CharField(max_length=20)
    
    template = models.ForeignKey(
        NotificationTemplate,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    
    subject = models.CharField(max_length=200, blank=True)
    body = models.TextField()
    
    STATUS = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    
    error = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)


# ============================================================
# AUDIT TRAIL (EXTENDED)
# ============================================================

class AuditEntry(models.Model):
    """Extended audit trail."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    
    action = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    object_id = models.CharField(max_length=50)
    
    # Changes
    old_data = models.JSONField(default=dict)
    new_data = models.JSONField(default=dict)
    
    # Context
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=500, blank=True)
    
    # Status
    STATUS = [
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='success')
    
    error_message = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['model', 'object_id']),
        ]


# ============================================================
# DATA RETENTION
# ============================================================

class DataRetentionPolicy(models.Model):
    """Data retention policies."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    # Model to apply policy to
    model = models.CharField(max_length=50)
    
    # Retention period
    RETENTION_ACTIONS = [
        ('archive', 'Archive'),
        ('delete', 'Delete'),
        ('anonymize', 'Anonymize'),
    ]
    
    action = models.CharField(max_length=20, choices=RETENTION_ACTIONS)
    
    # How long to keep
    retention_days = models.IntegerField()
    
    # When to apply
    schedule = models.CharField(max_length=20, default='daily')
    
    is_active = models.BooleanField(default=True)


# ============================================================
# API KEYS
# ============================================================

class APIKey(models.Model):
    """API keys for external integrations."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=100)
    key = models.CharField(max_length=64, unique=True)
    
    # User this key belongs to
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    
    # Permissions
    permissions = models.JSONField(default=list)
    # ['read', 'write', 'admin']
    
    # Rate limiting
    rate_limit = models.IntegerField(default=1000)
    # requests per hour
    
    # Status
    is_active = models.BooleanField(default=True)
    
    last_used = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']