"""
Student Disciplinary System
Misconduct, hearings, sanctions
"""

from django.db import models
import uuid


class DisciplinaryCase(models.Model):
    """Student disciplinary case."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        'student.StudentProfile',
        on_delete=models.CASCADE,
        related_name='disciplinary_cases'
    )
    
    # Incident
    incident_date = models.DateField()
    incident_location = models.CharField(max_length=200)
    
    CATEGORY = [
        ('academic_dishonesty', 'Academic Dishonesty'),
        ('assault', 'Assault'),
        ('theft', 'Theft'),
        ('vandalism', 'Vandalism'),
        ('drugs', 'Drug/Substance Abuse'),
        ('harassment', 'Harassment'),
        ('exam_misconduct', 'Exam Misconduct'),
        (' disobey', 'Disobeying Authority'),
        ('other', 'Other'),
    ]
    category = models.CharField(max_length=30, choices=CATEGORY)
    
    description = models.TextField()
    
    # Witness info
    witnesses = models.JSONField(default=list)
    # [{'name': '...', 'statement': '...'}]
    
    # Evidence
    evidence = models.JSONField(default=list)
    
    # Reporting
    reported_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True, related_name='+'
    )
    
    # Handling
    STATUS = [
        ('reported', 'Reported'),
        ('investigating', 'Under Investigation'),
        ('hearing_scheduled', 'Hearing Scheduled'),
        ('decided', 'Decision Given'),
        ('appealed', 'Appealed'),
        ('closed', 'Closed'),
    ]
    status = models.CharField(max_length=30, choices=STATUS, default='reported')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DisciplinaryHearing(models.Model):
    """Disciplinary hearing."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    case = models.ForeignKey(
        DisciplinaryCase,
        on_delete=models.CASCADE,
        related_name='hearings'
    )
    
    # Hearing details
    hearing_date = models.DateField()
    hearing_time = models.TimeField()
    venue = models.CharField(max_length=100)
    
    # Panel
    panel_members = models.JSONField(default=list)
    # [{'name': '...', 'role': 'Chairman/Member'}]
    
    # Student response
    student_response = models.TextField(blank=True)
    student_present = models.BooleanField(default=False)
    
    # Decision
    decision = models.CharField(
        max_length=30,
        choices=[
            ('exonerated', 'Exonerated'),
            ('warned', 'Warned'),
            ('suspended', 'Suspended'),
            ('dismissed', 'Dismissed'),
            ('probation', 'Probation'),
            ('withdrawn', 'Withdrawn'),
        ],
        blank=True
    )
    
    sanction_details = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)


class DisciplinaryAppeal(models.Model):
    """Appeal of disciplinary decision."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    case = models.ForeignKey(
        DisciplinaryCase,
        on_delete=models.CASCADE,
        related_name='appeals'
    )
    
    # Appeal details
    grounds = models.TextField()
    appeal_date = models.DateField(auto_now_add=True)
    
    # Hearing
    hearing_date = models.DateField(null=True, blank=True)
    venue = models.CharField(max_length=100, blank=True)
    
    STATUS = [
        ('pending', 'Pending'),
        ('upheld', 'Upheld'),
        ('dismissed', 'Dismissed'),
        ('varied', 'Varied'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    
    decision = models.TextField(blank=True)
    decided_at = models.DateTimeField(null=True, blank=True)


class StudentWarning(models.Model):
    """Academic warnings."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey(
        'student.StudentProfile',
        on_delete=models.CASCADE,
        related_name='warnings'
    )
    
    TYPE = [
        ('attendance', 'Low Attendance'),
        ('academic', 'Poor Academic Performance'),
        ('financial', 'Owing Fees'),
        ('conduct', 'Conduct'),
    ]
    warning_type = models.CharField(max_length=20, choices=TYPE)
    
    reason = models.TextField()
    
    # Action required
    action_required = models.CharField(max_length=200, blank=True)
    deadline = models.DateField(null=True, blank=True)
    
    # Status
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    issued_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True, related_name='+'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)


class CoursePrerequisite(models.Model):
    """Course prerequisites."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    course = models.ForeignKey(
        'academic.Course',
        on_delete=models.CASCADE,
        related_name='prerequisites'
    )
    
    prerequisite = models.ForeignKey(
        'academic.Course',
        on_delete=models.CASCADE,
        related_name='required_for'
    )
    
    TYPE = [
        ('required', 'Required'),
        ('recommended', 'Recommended'),
    ]
    prereq_type = models.CharField(max_length=20, choices=TYPE, default='required')
    
    min_grade = models.CharField(max_length=5, blank=True)
    # Minimum grade required (e.g., 'D' or 40)
    
    class Meta:
        unique_together = ['course', 'prerequisite']


class CourseRegistrationOverride(models.Model):
    """Override course registration rules."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey(
        'student.StudentProfile',
        on_delete=models.CASCADE
    )
    
    course = models.ForeignKey('academic.Course', on_delete=models.CASCADE)
    
    session = models.ForeignKey('academic.AcademicSession', on_delete=models.CASCADE)
    semester = models.ForeignKey('academic.Semester', on_delete=models.CASCADE)
    
    # Override reason
    REASON = [
        ('prerequisite', 'Prerequisite Not Met'),
        ('capacity', 'Capacity'),
        ('timetable', 'Timetable Clash'),
        ('level', 'Wrong Level'),
        ('special', 'Special Permission'),
    ]
    reason = models.CharField(max_length=20, choices=REASON)
    
    # Approval
    approved_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True, related_name='+'
    )
    
    is_approved = models.BooleanField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)