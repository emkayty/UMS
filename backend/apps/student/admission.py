"""
Online Application System
New student admissions portal
"""

import uuid
from django.db import models


class ApplicationStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    SUBMITTED = 'submitted', 'Submitted'
    SCREENING = 'screening', 'Screening'
    SCREENED = 'screened', 'Screened'
    ACCEPTED = 'accepted', 'Accepted'
    REJECTED = 'rejected', 'Rejected'
    DEFERRED = 'deferred', 'Deferred'


class ApplicationSource(models.TextChoices):
    ONLINE = 'online', 'Online Portal'
    MANUAL = 'manual', 'Manual'
    TRANSFER = 'transfer', 'Transfer'


# ============================================================
# APPLICATION SETTINGS
# ============================================================

class ApplicationSettings(models.Model):
    """Online application settings."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    session = models.ForeignKey(
        'academic.AcademicSession', on_delete=models.CASCADE,
        related_name='application_settings'
    )
    
    # Status
    is_active = models.BooleanField(default=False)
    application_open = models.BooleanField(default=False)
    application_deadline = models.DateField(null=True, blank=True)
    
    # Requirements
    require_olevel = models.BooleanField(default=True)
    require_utme = models.BooleanField(default=True)
    require_utme_min_score = models.IntegerField(default=180)
    
    # Screening
    auto_screen = models.BooleanField(default=False)
    screening_criteria = models.JSONField(default=dict)
    
    # Fees
    application_fee = models.DecimalField(max_digits=12, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'application_settings'

    def __str__(self):
        return f"{self.session.name} - Application"


# ============================================================
# ONLINE APPLICATION
# ============================================================

class OnlineApplication(models.Model):
    """New student online application."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    application_number = models.CharField(max_length=20, unique=True)
    session = models.ForeignKey(
        'academic.AcademicSession', on_delete=models.CASCADE
    )
    
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    other_names = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    # Date of Birth
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=[
            ('male', 'Male'),
            ('female', 'Female'),
        ]
    )
    
    # Origin
    nationality = models.CharField(max_length=50, default='Nigerian')
    state_of_origin = models.CharField(max_length=50, blank=True)
    lga = models.CharField(max_length=50, blank=True)
    
    # Address
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    
    # JAMB/UTME
    jamb_number = models.CharField(max_length=20, blank=True)
    jamb_score = models.IntegerField(null=True, blank=True)
    jamb_year = models.IntegerField(null=True, blank=True)
    
    # Programme Choices
    first_choice = models.ForeignKey(
        'academic.Programme', on_delete=models.SET_NULL,
        null=True, related_name='first_choice_apps'
    )
    second_choice = models.ForeignKey(
        'academic.Programme', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='second_choice_apps'
    )
    
    # Secondary School
    secondary_school = models.CharField(max_length=200, blank=True)
    secondary_school_type = models.CharField(
        max_length=20, blank=True,
        choices=[
            ('public', 'Public'),
            ('private', 'Private'),
        ]
    )
    ssce_year = models.IntegerField(null=True, blank=True)
    
    # Status
    status = models.CharField(
        max_length=20, choices=ApplicationStatus.choices,
        default=ApplicationStatus.DRAFT
    )
    source = models.CharField(
        max_length=20, choices=ApplicationSource.choices,
        default=ApplicationSource.ONLINE
    )
    
    # Payment
    payment_status = models.CharField(
        max_length=20, default='pending',
        choices=[
            ('pending', 'Pending'),
            ('paid', 'Paid'),
        ]
    )
    payment_ref = models.CharField(max_length=50, blank=True)
    amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )
    
    # Screening
    screening_score = models.IntegerField(null=True, blank=True)
    screening_remark = models.TextField(blank=True)
    screened_by = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL,
        null=True, blank=True
    )
    screened_at = models.DateTimeField(null=True, blank=True)
    
    #木提交
    submitted_at = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'online_applications'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.application_number} - {self.last_name}"


# ============================================================
# O-LEVEL RESULT
# ============================================================

class OLevelResult(models.Model):
    """O-Level results."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    application = models.ForeignKey(
        OnlineApplication, on_delete=models.CASCADE,
        related_name='olevel_results'
    )
    
    exam_type = models.CharField(
        max_length=10,
        choices=[
            ('waec', 'WAEC'),
            ('neco', 'NECO'),
            ('nabteb', 'NABTEB'),
            ('gce', 'GCE'),
        ]
    )
    exam_year = models.IntegerField()
    exam_number = models.CharField(max_length=20)
    
    subjects = models.JSONField(default=list)
    
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'olevel_results'

    def __str__(self):
        return f"{self.application.applicat_number} - {self.exam_type}"


# ============================================================
# POST-UTME
# ============================================================

class PostUtmeResult(models.Model):
    """Post-UTME screening result."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    application = models.ForeignKey(
        OnlineApplication, on_delete=models.CASCADE,
        related_name='postutme_results'
    )
    
    score = models.IntegerField()
    total = models.IntegerField(default=100)
    percentile = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    
    exam_date = models.DateField()
    venue = models.CharField(max_length=100, blank=True)
    
    marked_by = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL,
        null=True, blank=True
    )
    marked_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'postutme_results'

    def __str__(self):
        return f"{self.application.application_number} - {self.score}"


# ============================================================
# ADMISSION LETTER
# ============================================================

class AdmissionLetter(models.Model):
    """Admission offer letter."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    application = models.ForeignKey(
        OnlineApplication, on_delete=models.CASCADE,
        related_name='admission_letter'
    )
    
    # Programme admitted to
    admitted_programme = models.ForeignKey(
        'academic.Programme', on_delete=models.CASCADE
    )
    
    # Admission details
    admisson_number = models.CharField(max_length=20, unique=True)
    admission_session = models.ForeignKey(
        'academic.AcademicSession', on_delete=models.CASCADE
    )
    admission_level = models.IntegerField(default=100)
    
    # Offer
    is_accepted = models.BooleanField(default=False)
    acceptance_deadline = models.DateField()
    accepted_at = models.DateTimeField(null=True, blank=True)
    
    # Fee
    acceptance_fee = models.DecimalField(max_digits=12, decimal_places=2)
    acceptance_fee_paid = models.BooleanField(default=False)
    
    # Generated
    letter_sent = models.BooleanField(default=False)
    letter_sent_at = models.DateTimeField(null=True, blank=True)
    
    pdf_file = models.FileField(
        upload_to='admission/letters/', null=True, blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'admission_letters'

    def __str__(self):
        return f"{self.application.application_number} - {self.admitted_programme.code}"