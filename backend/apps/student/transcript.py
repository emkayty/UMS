"""
Transcript Request Management
Student transcript requests and generation
"""

import uuid
from django.db import models


class TranscriptStatus(models.TextChoices):
    PENDING = 'pending', 'Pending Payment'
    PAID = 'paid', 'Paid'
    PROCESSING = 'processing', 'Processing'
    READY = 'ready', 'Ready for Collection'
    COLLECTED = 'collected', 'Collected'
    MAILED = 'mailed', 'Mailed'
    REJECTED = 'rejected', 'Rejected'


class TranscriptType(models.TextChoices):
    OFFICIAL = 'official', 'Official Transcript'
    UNOFFICIAL = 'unofficial', ' unofficial'

class TranscriptDelivery(models.TextChoices):
    COLLECTION = 'collection', 'Self Collection'
    MAIL = 'mail', 'Mail to Address'
    EMAIL = 'email', 'Email to Institution'
    DIGITAL = 'digital', 'Digital Link'


# ============================================================
# TRANSCRIPT REQUEST
# ============================================================

class TranscriptRequest(models.Model):
    """Student transcript request."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey(
        'student.StudentProfile', on_delete=models.CASCADE,
        related_name='transcript_requests'
    )
    
    # Request details
    transcript_type = models.CharField(
        max_length=20, choices=TranscriptType.choices,
        default=TranscriptType.OFFICIAL
    )
    delivery_method = models.CharField(
        max_length=20, choices=TranscriptDelivery.choices,
        default=TranscriptDelivery.COLLECTION
    )
    
    # Copies
    copies = models.IntegerField(default=1)
    
    # Destination (if mailing)
    recipient_name = models.CharField(max_length=200, blank=True)
    recipient_institution = models.CharField(max_length=200, blank=True)
    recipient_address = models.TextField(blank=True)
    recipient_city = models.CharField(max_length=100, blank=True)
    recipient_country = models.CharField(max_length=100, blank=True)
    recipient_email = models.EmailField(blank=True)
    
    # Purpose
    purpose = models.CharField(
        max_length=50, blank=True,
        choices=[
            ('employment', 'Employment'),
            ('further_study', 'Further Studies'),
            ('migration', 'Migration'),
            ('visa', 'Visa Application'),
            ('other', 'Other'),
        ]
    )
    
    # Status
    status = models.CharField(
        max_length=20, choices=TranscriptStatus.choices,
        default=TranscriptStatus.PENDING
    )
    
    # Payment
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_status = models.CharField(
        max_length=20, default='pending',
        choices=[
            ('pending', 'Pending'),
            ('paid', 'Paid'),
            ('failed', 'Failed'),
        ]
    )
    payment_ref = models.CharField(max_length=100, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    # Processing
    processed_by = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='transcript_processed'
    )
    processed_at = models.DateTimeField(null=True, blank=True)
    
    # Collection
    collected_at = models.DateTimeField(null=True, blank=True)
    collected_by = models.CharField(max_length=100, blank=True)
    
    # File
    pdf_file = models.FileField(upload_to='transcripts/', null=True, blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    rejection_reason = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'transcript_requests'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.matric_number} - {self.transcript_type}"


# ============================================================
# TRANSCRIPT CONTENT
# ============================================================

class TranscriptRecord(models.Model):
    """Individual transcript record."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    request = models.ForeignKey(
        TranscriptRequest, on_delete=models.CASCADE,
        related_name='records'
    )
    
    # Academic record
    session = models.ForeignKey(
        'academic.AcademicSession', on_delete=models.CASCADE
    )
    
    # Courses taken
    courses = models.JSONField(default=list)
    
    # Summary
    total_units = models.IntegerField(default=0)
    total_courses = models.IntegerField(default=0)
    gpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    
    # Classification
    class_of_degree = models.CharField(max_length=30, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'transcript_records'
        unique_together = ['request', 'session']

    def __str__(self):
        return f"{self.request.student.matric_number} - {self.session.name}"


# ============================================================
# TRANSCRIPT SETTINGS
# ============================================================

class TranscriptSettings(models.Model):
    """Transcript pricing and settings."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Pricing (Naira)
    domestic_price = models.DecimalField(max_digits=12, decimal_places=2)
    international_price = models.DecimalField(max_digits=12, decimal_places=2)
    additional_copy_price = models.DecimalField(max_digits=12, decimal_places=2)
    urgent_processing_fee = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Processing time (days)
    standard_days = models.IntegerField(default=14)
    urgent_days = models.IntegerField(default=3)
    
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'transcript_settings'

    def __str__(self):
        return f"Transcript Settings"