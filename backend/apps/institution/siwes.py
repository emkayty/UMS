"""
SIWES & Industrial Training Management
Nigerian Polytechnic Industrial Training (SIWES)
Also covers American Co-op programs
"""

import uuid
from django.db import models
from apps.accounts.models import User


class ITStatus(models.TextChoices):
    PENDING = 'pending', 'Pending Approval'
    APPROVED = 'approved', 'Approved'
    REJECTED = 'rejected', 'Rejected'
    IN_PROGRESS = 'in_progress', 'In Progress'
    COMPLETED = 'completed', 'Completed'
    GRADED = 'graded', 'Graded'


class SupervisorRating(models.TextChoices):
    EXCELLENT = 'excellent', 'Excellent (5)'
    VERY_GOOD = 'very_good', 'Very Good (4)'
    GOOD = 'good', 'Good (3)'
    FAIR = 'fair', 'Fair (2)'
    POOR = 'poor', 'Poor (1)'


# ============================================================
# SIWES/INDUSTRIAL TRAINING TYPES
# ============================================================

class ITType(models.TextChoices):
    # Nigerian
    SIWES = 'siwes', 'Student Industrial Work Experience Scheme'
    IT = 'it', 'Industrial Training'
    ES = 'es', 'Embeded Sing'
    
    # American
    COOP = 'coop', 'Co-operative Education'
    INTERNSHIP = 'internship', 'Internship'
    PRACTICUM = 'practicum', 'Practicum'
    FIELD_WORK = 'field_work', 'Field Work'


# ============================================================
# SIWES COMPANY/INDUSTRY
# ============================================================

class ITCompany(models.Model):
    """Industry placement for SIWES/Industrial Training."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    
    # Industry details
    industry = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    
    # Location
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    lga = models.CharField(max_length=100, blank=True)
    
    # Contact
    contact_person = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    
    # SIWES Coordinator
    siwes_coordinator = models.CharField(max_length=100, blank=True)
    
    # Approval
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    
    # Capacity
    max_students = models.IntegerField(default=5)
    current_students = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'it_companies'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"


# ============================================================
# SIWES PLACEMENT
# ============================================================

class ITPlacement(models.Model):
    """
    Student Industrial Training Placement.
    Nigerian: SIWES placement - 6 months minimum.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Student & Session
    student = models.ForeignKey(
        'student.StudentProfile', on_delete=models.CASCADE,
        related_name='it_placements'
    )
    session = models.ForeignKey(
        'academic.AcademicSession', on_delete=models.CASCADE
    )
    it_type = models.CharField(max_length=20, choices=ITType.choices)
    
    # Company
    company = models.ForeignKey(
        ITCompany, on_delete=models.CASCADE
    )
    
    # Dates
    start_date = models.DateField()
    end_date = models.DateField()
    actual_start = models.DateField(null=True, blank=True)
    actual_end = models.DateField(null=True, blank=True)
    
    # Status
    status = models.CharField(
        max_length=20, choices=ITStatus.choices,
        default=ITStatus.PENDING
    )
    
    # Logbook
    weekly_logbook_submitted = models.IntegerField(default=0)
    total_weeks = models.IntegerField(default=12)
    
    # Supervisor
    company_supervisor = models.CharField(max_length=100)
    supervisor_email = models.EmailField(blank=True)
    supervisor_phone = models.CharField(max_length=20, blank=True)
    
    # School supervisor
    school_supervisor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='supervised_placements'
    )
    
    # Approval
    approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='approved_placements'
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    
    # Notes
    rejection_reason = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'it_placements'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.matric_number} - {self.company.name}"


# ============================================================
# WEEKLY LOG
# ============================================================

class ITLogbook(models.Model):
    """Weekly logbook entry."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    placement = models.ForeignKey(
        ITPlacement, on_delete=models.CASCADE,
        related_name='logbooks'
    )
    week_number = models.IntegerField()
    week_start = models.DateField()
    week_end = models.DateField()
    
    # Activities
    activities = models.TextField(help_text='Tasks performed')
    skills_acquired = models.TextField(blank=True)
    challenges = models.TextField(blank=True)
    
    # Submission status
    is_submitted = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(null=True, blank=True)
    
    # Supervisor feedback
    supervisor_remark = models.TextField(blank=True)
    supervisor_approved = models.BooleanField(default=False)
    
    # School supervisor feedback
    school_remark = models.TextField(blank=True)
    school_approved = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'it_logbooks'
        unique_together = ['placement', 'week_number']

    def __str__(self):
        return f"{self.placement.student.matric_number} - Week {self.week_number}"


# ============================================================
# ASSESSMENT
# ============================================================

class ITAssessment(models.Model):
    """SIWES assessment/evaluation."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    placement = models.ForeignKey(
        ITPlacement, on_delete=models.CASCADE,
        related_name='assessments'
    )
    
    # Company Assessment (by supervisor)
    attendance_score = models.IntegerField(
        default=0, help_text='/10'
    )
    performance_score = models.IntegerField(
        default=0, help_text='/20'
    )
    initiative_score = models.IntegerField(
        default=0, help_text='/10'
    )
    report_score = models.IntegerField(
        default=0, help_text='/10'
    )
    supervisor_rating = models.CharField(
        max_length=15, choices=SupervisorRating.choices,
        blank=True
    )
    total_score = models.IntegerField(default=0)
    company_remark = models.TextField(blank=True)
    company_supervisor = models.CharField(max_length=100)
    company_signed = models.DateField(null=True, blank=True)
    
    # School Assessment (by supervisor)
    school_score = models.IntegerField(default=0, help_text='/30')
    logbook_score = models.IntegerField(default=0, help_text='/10')
    school_remark = models.TextField(blank=True)
    school_supervisor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    school_signed = models.DateField(null=True, blank=True)
    
    # Final
    final_grade = models.CharField(max_length=2, blank=True)
    final_grade_point = models.DecimalField(
        max_digits=3, decimal_places=2, null=True, blank=True
    )
    
    # Status
    is_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'it_assessments'

    def __str__(self):
        return f"{self.placement.student.matric_number} - Assessment"


# ============================================================
# SIWES LOG LETTER
# ============================================================

class ITLetter(models.Model):
    """SIWES log letter for students."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    placement = models.ForeignKey(
        ITPlacement, on_delete=models.CASCADE,
        related_name='letters'
    )
    
    letter_type = models.CharField(
        max_length=30,
        choices=[
            ('intro', 'Introduction Letter'),
            ('logbook', 'Logbook Collection'),
            ('clearance', 'Company Clearance'),
            ('completion', 'Completion Certificate'),
        ]
    )
    
    letter_date = models.DateField()
    is_generated = models.BooleanField(default=False)
    is_collected = models.BooleanField(default=False)
    collected_at = models.DateField(null=True, blank=True)
    
    # File
    pdf_file = models.FileField(upload_to='it/letters/', null=True, blank=True)

    class Meta:
        db_table = 'it_letters'
        unique_together = ['placement', 'letter_type']

    def __str__(self):
        return f"{self.placement.student.matric_number} - {self.letter_type}"