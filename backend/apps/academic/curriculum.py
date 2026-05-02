"""
Academic Calendar & Programme Curriculum Management
Multi-track calendars, curriculum versioning, course repetition
"""

from django.db import models


class AcademicCalendar(models.Model):
    """Academic calendar with multiple tracks."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Calendar type
    CALENDAR_TYPES = [
        ('semester', 'Semester (2 per year)'),
        ('trimester', 'Trimester (3 per year)'),
        ('quarterly', 'Quarterly (4 per year)'),
        ('modex', 'Modular/Extended'),
    ]
    
    calendar_type = models.CharField(max_length=20, choices=CALENDAR_TYPES, default='semester')
    
    # Institution
    institution_name = models.CharField(max_length=200)
    institution_code = models.CharField(max_length=20)
    
    # Current period
    current_session = models.ForeignKey(
        'academic.AcademicSession', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='+'
    )
    current_semester = models.ForeignKey(
        'academic.Semester', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='+'
    )
    
    # Registration windows
    late_registration_days = models.IntegerField(default=14)
    add_drop_days = models.IntegerField(default=7)
    withdrawal_deadline_days = models.IntegerField(default=60)
    
    # Examination
    exam_start_days_before = models.IntegerField(default=7)
    exam_end_days_after = models.IntegerField(default=14)
    
    # Holidays
    public_holidays = models.JSONField(default=list)  # [{date, name}]
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.institution_code} - {self.calendar_type}"


class CurriculumVersion(models.Model):
    """Programme curriculum with versioning."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    programme = models.ForeignKey(
        'academic.Programme', on_delete=models.CASCADE,
        related_name='curriculum_versions'
    )
    
    version = models.CharField(max_length=20)
    effective_session = models.ForeignKey(
        'academic.AcademicSession', on_delete=models.SET_NULL,
        null=True, blank=True
    )
    
    # Curriculum structure (level -> semester -> courses with credits)
    structure = models.JSONField(default=dict)
    # Example: {100: {1: [{course: 'CS101', credits: 3}, ...], 2: [...]}}
    
    # Total credits required
    total_credits_required = models.IntegerField(default=120)
    
    # Minimum/maximum duration
    min_years = models.IntegerField(default=4)
    max_years = models.IntegerField(default=6)
    max_semesters = models.IntegerField(default=12)
    
    # Status
    STATUS = [
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('active', 'Active'),
        ('superseded', 'Superseded'),
        ('archived', 'Archived'),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS, default='draft')
    
    # Approvals
    approved_by = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='+'
    )
    approval_date = models.DateTimeField(null=True, blank=True)
    
    # Change reasons
    change_summary = models.TextField(blank=True)
    change_rationale = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['programme', 'version']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.programme.code} v{self.version}"


class CourseRepetitionPolicy(models.Model):
    """Course repetition limits and policies."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    programme = models.ForeignKey(
        'academic.Programme', on_delete=models.CASCADE,
        related_name='repetition_policies'
    )
    
    # Repetition limits
    max_attempts_per_course = models.IntegerField(default=3)
    max_failed_courses_semester = models.IntegerField(default=2)
    require_exit_interview = models.BooleanField(default=True)
    
    # Carry-over rules
    allow_carry_over = models.BooleanField(default=True)
    max_carry_over = models.IntegerField(default=2)
    carry_over_credits_limit = models.IntegerField(default=15)
    
    # Repeat waiting period
    require_next_offering = models.BooleanField(default=True)
    
    # Academic standing action
    suspend_on_repeat_exhaustion = models.BooleanField(default=True)
    withdraw_on_repeat_exhaustion = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)


class ProgrammeAccreditation(models.Model):
    """Programme accreditation tracking."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    programme = models.ForeignKey(
        'academic.Programme', on_delete=models.CASCADE,
        related_name='accreditations'
    )
    
    # Accreditation body
    ACCREDITATION_BODIES = [
        ('nuc', 'NUC (Nigeria)'),
        ('naat', 'NAAT (Technical)'),
        ('nba', 'NBA (Engineering)'),
        ('nigerian_bar', 'Nigerian Bar Association'),
        ('uk_university', 'UK University'),
        ('us_accreditation', 'US Accreditation'),
        ('euro_eng', 'European Engineering'),
    ]
    
    accreditation_body = models.CharField(max_length=20, choices=ACCREDITATION_BODIES)
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('accredited', 'Full Accreditation'),
            ('interim', 'Interim Accreditation'),
            ('probation', 'On Probation'),
            ('withdrawn', 'Withdrawn'),
            ('denied', 'Denied'),
        ]
    )
    
    # Dates
    application_date = models.DateField(null=True, blank=True)
    accreditation_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    
    # Panel visit
    panel_visit_date = models.DateField(null=True, blank=True)
    panel_report = models.TextField(blank=True)
    
    # Conditions
    conditions = models.TextField(blank=True)
    conditions_met = models.BooleanField(default=False)
    conditions_deadline = models.DateField(null=True, blank=True)
    
    # File uploads
    approval_letter = models.URLField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)


class CurriculumCourse(models.Model):
    """Individual course in curriculum with detailed info."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    curriculum = models.ForeignKey(
        CurriculumVersion, on_delete=models.CASCADE,
        related_name='courses'
    )
    course = models.ForeignKey(
        'academic.Course', on_delete=models.CASCADE
    )
    
    # Placement
    level = models.IntegerField()  # 100, 200, etc.
    semester = models.IntegerField()  # 1 or 2
    
    # Course type
    COURSE_TYPES = [
        ('core', 'Core'),
        ('elective', 'Elective'),
        ('required', 'Required'),
        ('project', 'Project'),
        ('seminar', 'Seminar'),
        ('laboratory', 'Laboratory'),
        ('industrial', 'Industrial Attachment'),
        ('siwes', 'SIWES'),
        ('project', 'Final Year Project'),
    ]
    
    course_type = models.CharField(max_length=20, choices=COURSE_TYPES, default='core')
    
    # Learning hours
    lecture_hours = models.IntegerField(default=3)
    tutorial_hours = models.IntegerField(default=1)
    lab_hours = models.IntegerField(default=0)
    studio_hours = models.IntegerField(default=0)
    self_study_hours = models.IntegerField(default=6)
    total_contact_hours = models.IntegerField(default=4)
    
    # Assessment
    CA_WEIGHT = models.IntegerField(default=30)  # Continuous Assessment
    EXAM_WEIGHT = models.IntegerField(default=70)
    MIN_CA = models.IntegerField(default=10)
    MIN_EXAM = models.IntegerField(default=30)
    
    # Equivalencies
    equivalent_courses = models.JSONField(default=list)  # Other course codes
    
    # Prerequisites check
    passes_required = models.JSONField(default=list)
    corequisites = models.JSONField(default=list)
    
    # Teaching staff
    Lecturers = models.ManyToManyField(
        'accounts.User',
        limit_choices_to={'role': 'lecturer'},
        blank=True
    )
    
    class Meta:
        unique_together = ['curriculum', 'course', 'level', 'semester']
    
    def __str__(self):
        return f"{self.curriculum} - {self.course.code} ({self.level}L{self.semester}S)"