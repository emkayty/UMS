"""
Examination & Results Management
Exam timetables, grading, moderation, results upload
"""

from django.db import models
import uuid


class ExaminationMode(models.Model):
    """Examination mode configuration."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=50)
    
    # Mode types
    MODE_TYPES = [
        (' CBT', 'Computer Based Testing (CBT)'),
        ('online', 'Online Proctored'),
        ('paper', 'Paper-Based'),
        ('oral', 'Oral Examination'),
        ('practical', 'Practical'),
        ('project', 'Project/Dissertation'),
        ('thesis', 'Thesis Defence'),
    ]
    
    exam_mode = models.CharField(max_length=20, choices=MODE_TYPES)
    
    # Settings
    duration_minutes = models.IntegerField(default=60)
    passing_score = models.DecimalField(max_digits=5, decimal_places=2, default=40.0)
    attempt_limit = models.IntegerField(default=1)
    
    # CBT specific
    questions_per_page = models.IntegerField(default=1)
    shuffle_questions = models.BooleanField(default=True)
    shuffle_options = models.BooleanField(default=True)
    show_results_immediately = models.BooleanField(default=False)
    show_model_answer = models.BooleanField(default=False)
    
    # Security
    lockdown_browser = models.BooleanField(default=False)
    camera_required = models.BooleanField(default=False)
    copy_paste_disabled = models.BooleanField(default=True)
    
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name


class ExamTimetable(models.Model):
    """Examination timetable."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    session = models.ForeignKey(
        'academic.AcademicSession', on_delete=models.CASCADE,
        related_name='exam_timetables'
    )
    
    # Timetable period
    exam_period = models.CharField(max_length=50)  # e.g., "First Semester Exams"
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Publication
    publish_to_students = models.DateField(null=True, blank=True)
    publish_to_examiners = models.DateField(null=True, blank=True)
    
    # Status
    STATUS = [
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('published', 'Published'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS, default='draft')
    
    approved_by = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL,
        null=True, blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)


class ExamTimetableEntry(models.Model):
    """Individual exam in timetable."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    timetable = models.ForeignKey(
        ExamTimetable, on_delete=models.CASCADE,
        related_name='entries'
    )
    
    course = models.ForeignKey(
        'academic.Course', on_delete=models.CASCADE
    )
    
    # Exam details
    exam_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    venue = models.CharField(max_length=100)
    
    # Invigilators
    chief_invigilator = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL,
        null=True, blank=True,
        limit_choices_to={'role': 'lecturer'},
        related_name='+'
    )
    invigilators = models.JSONField(default=list)
    
    # Students
    total_students = models.IntegerField(default=0)
    
    # Mode
    examination_mode = models.ForeignKey(
        ExaminationMode, on_delete=models.SET_NULL,
        null=True, blank=True
    )
    
    # Status
    is_clash_handled = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['timetable', 'course', 'exam_date', 'start_time']
    
    def __str__(self):
        return f"{self.course.code} - {self.exam_date}"


class GradeModeration(models.Model):
    """Grade moderation before approval."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    course = models.ForeignKey(
        'academic.Course', on_delete=models.CASCADE
    )
    session = models.ForeignKey(
        'academic.AcademicSession', on_delete=models.CASCADE
    )
    semester = models.ForeignKey(
        'academic.Semester', on_delete=models.CASCADE
    )
    
    # Raw statistics
    total_students = models.IntegerField(default=0)
    mean_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    median_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    std_dev = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Grade distribution
    grade_distribution = models.JSONField(default=dict)
    # {'A': 10, 'B': 20, 'C': 30, 'D': 15, 'F': 5}
    
    # Moderation applied
    MODERATION_TYPES = [
        ('none', 'No Moderation'),
        ('linear', 'Linear Scaling'),
        ('percentage', 'Percentage Adjust'),
        ('absolute', 'Absolute Adjust'),
    ]
    
    moderation_type = models.CharField(max_length=20, choices=MODERATION_TYPES, default='none')
    moderation_factor = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    
    # Moderated statistics
    moderated_mean = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    moderated_distribution = models.JSONField(default=dict)
    
    moderator = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL,
        null=True, blank=True
    )
    moderation_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)


class ExamAttendance(models.Model):
    """Student exam attendance tracking."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    entry = models.ForeignKey(
        ExamTimetableEntry, on_delete=models.CASCADE,
        related_name='attendance'
    )
    
    student = models.ForeignKey(
        'student.StudentProfile', on_update=models.CASCADE
    )
    
    # Attendance status
    ATTENDANCE_STATUS = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late Arrival'),
        ('excused', 'Excused'),
    ]
    
    status = models.CharField(max_length=20, choices=ATTENDANCE_STATUS, default='present')
    
    # Arrival time
    arrival_time = models.TimeField(null=True, blank=True)
    
    # Academic Misconduct
    misconduct_reported = models.BooleanField(default=False)
    misconduct_notes = models.TextField(blank=True)
    
    # Score capture
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    grading_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('graded', 'Graded'),
            ('moderated', 'Moderated'),
            ('published', 'Published'),
        ],
        default='pending'
    )
    
    marked_by = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL,
        null=True, blank=True
    )
    marked_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['entry', 'student']


class AcademicMisconduct(models.Model):
    """Exam misconduct records."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey(
        'student.StudentProfile', on_delete=models.CASCADE,
        related_name='misconduct_records'
    )
    
    # Incident
    exam = models.ForeignKey(
        ExamTimetableEntry, on_delete=models.CASCADE,
        null=True, blank=True
    )
    
    incident_date = models.DateField()
    incident_type = models.CharField(max_length=100)
    description = models.TextField()
    
    # Investigation
    investigated_by = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL,
        null=True, blank=True
    )
    investigation_date = models.DateField(null=True, blank=True)
    investigation_findings = models.TextField(blank=True)
    
    # Outcome
    OUTCOME_TYPES = [
        ('not_proven', 'Not Proven'),
        ('warning', 'Written Warning'),
        ('probation', 'Probation'),
        ('suspension', 'Suspension'),
        ('expulsion', 'Expulsion'),
        ('zero_mark', 'Zero Mark'),
    ]
    
    outcome = models.CharField(max_length=20, choices=OUTCOME_TYPES, blank=True)
    outcome_date = models.DateField(null=True, blank=True)
    outcome_notes = models.TextField(blank=True)
    
    # Appeal
    appeal_filed = models.BooleanField(default=False)
    appeal_outcome = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)


class SupplementaryExam(models.Model):
    """Supplementary exams for failed courses."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey(
        'student.StudentProfile', on_delete=models.CASCADE
    )
    course = models.ForeignKey(
        'academic.Course', on_delete=models.CASCADE
    )
    session = models.ForeignKey(
        'academic.AcademicSession', on_update=CASCADE
    )
    
    # Original score
    original_score = models.DecimalField(max_digits=5, decimal_places=2)
    original_grade = models.CharField(max_length=2)
    
    # Application
    application_date = models.DateField(auto_now_add=True)
    fee_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Exam details
    exam_date = models.DateField(null=True, blank=True)
    venue = models.CharField(max_length=100, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    
    # Result
    supplementary_score = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    passed = models.BooleanField(default=False)
    
    # Status
    STATUS = [
        ('applied', 'Applied'),
        ('approved', 'Approved'),
        ('scheduled', 'Scheduled'),
        ('written', 'Written'),
        ('passed', 'Passed'),
        ('failed', 'Failed'),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS, default='applied')
    
    created_at = models.DateTimeField(auto_now_add=True)