"""
Nigerian University Standards Integration
NUC, JAMB, NYSC, Carry-over systems
"""

from django.db import models
from apps.academic.models import AcademicSession


class NUCConfiguration(models.Model):
    """NUC (National Universities Commission) configuration."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # NUC Benchmark minimums
    student_staff_ratio = models.IntegerField(default=30)
    max_students_per_course = models.IntegerField(default=500)
    min_credit_for_degree = models.IntegerField(default=120)
    
    # Programme accreditation
    accreditation_status = models.CharField(max_length=20, default='pending')
    accreditation_expiry = models.DateField(null=True, blank=True)
    panel_visit_date = models.DateField(null=True, blank=True)
    
    # Quality metrics
    library_hours = models.IntegerField(default=12)
    lab_hours_per_week = models.IntegerField(default=6)
    
    created_at = models.DateTimeField(auto_now_add=True)


class JAMBIntegration(models.Model):
    """JAMB (Joint Admissions and Matriculation Board) integration."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # API Configuration
    jamb_api_key = models.CharField(max_length=200, blank=True)
    jamb_api_url = models.URLField(default='https://caps.jamb.gov.ng/api')
    is_active = models.BooleanField(default=False)
    
    # Batch import settings
    auto_create_applications = models.BooleanField(default=False)
    import_threshold_score = models.IntegerField(default=160)
    
    # CAPS course codes mapping
    caps_course_mapping = models.JSONField(default=dict)
    
    created_at = models.DateTimeField(auto_now_add=True)


class NYSCConfiguration(models.Model):
    """NYSC (National Youth Service Corps) configuration."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # mobilisation settings
    mobilizable_level = models.IntegerField(default=400)
    graduation_year_offset = models.IntegerField(default=1)
    
    # Export fields required by NYSC
    export_fields = models.JSONField(default=[
        'S/N', 'MATRIC_NO', 'SURNAME', 'OTHER_NAMES', 'DATE_OF_BIRTH',
        'SEX', 'STATE_OF_ORIGIN', 'LGA', 'PHONE', 'EMAIL',
        'PROGRAMME', 'CLASS_OF_DEGREE', 'YEAR_OF_GRADUATION'
    ])
    
    # Batch settings
    batch_size = models.IntegerField(default=100)
    
    created_at = models.DateTimeField(auto_now_add=True)


class CarryOverRecord(models.Model):
    """Carry-over course tracking (Nigerian standard)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey(
        'student.StudentProfile', on_delete=models.CASCADE,
        related_name='carry_over_records'
    )
    course = models.ForeignKey(
        'academic.Course', on_delete=models.CASCADE
    )
    session = models.ForeignKey(
        AcademicSession, on_delete=models.CASCADE
    )
    
    # Original failure
    original_score = models.DecimalField(max_digits=5, decimal_places=2)
    original_grade = models.CharField(max_length=2)
    
    # Carry-over attempt
    attempt_number = models.IntegerField(default=1)
    max_attempts = models.IntegerField(default=2)
    
    # Current status
    is_passed = models.BooleanField(default=False)
    last_attempt_date = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)


class AcademicStanding(models.Model):
    """Academic standing - Nigerian academic progress tracking."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey(
        'student.StudentProfile', on_delete=models.CASCADE,
        related_name='academic_standings'
    )
    session = models.ForeignKey(
        AcademicSession, on_delete=models.CASCADE
    )
    
    # Standing status
    PROBATION = 'probation'
    GOOD_STANDING = 'good_standing'
    SUSPENDED = 'suspended'
    WITHDRAWN = 'withdrawn'
    
    status = models.CharField(
        max_length=20,
        choices=[
            (PROBATION, 'Academic Probation'),
            (GOOD_STANDING, 'Good Standing'),
            (SUSPENDED, 'Suspended'),
            (WITHDRAWN, 'Withdrawn'),
        ],
        default=GOOD_STANDING
    )
    
    # GPA thresholds
    probation_gpa = models.DecimalField(max_digits=3, decimal_places=2, default=1.5)
    suspension_gpa = models.DecimalField(max_digits=3, decimal_places=2, default=1.0)
    
    # Reason
    reason = models.TextField(blank=True)
    effective_date = models.DateField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'session']


class CourseRegistrationRule(models.Model):
    """Course registration rules - prerequisites, clash detection."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    course = models.ForeignKey(
        'academic.Course', on_delete=models.CASCADE,
        related_name='registration_rules'
    )
    
    # Prerequisites
    requires_completion = models.ManyToManyField(
        'academic.Course',
        related_name='required_for',
        blank=True
    )
    minimum_pass_grade = models.CharField(max_length=2, default='D')
    
    # Level restrictions
    min_level = models.IntegerField(default=100)
    max_level = models.IntegerField(default=500)
    allow_repeat = models.BooleanField(default=True)
    
    # Co-requisites (courses that must be taken together)
    co_reqs = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False
    )
    
    # Capacity
    max_capacity = models.IntegerField(default=500)
    allow_overload = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Registration rules for {self.course}"