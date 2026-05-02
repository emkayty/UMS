"""
Additional Academic Features
Partnerships, Awards, Convocation, Assessments
"""

from django.db import models
import uuid


class Partnership(models.Model):
    """International/Local partnerships."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    institution_name = models.CharField(max_length=200)
    country = models.CharField(max_length=50)
    
    TYPE = [
        ('university', 'University'),
        ('company', 'Company'),
        ('organization', 'Organization'),
        ('ngo', 'NGO'),
    ]
    partner_type = models.CharField(max_length=20, choices=TYPE)
    
    # Contact
    contact_person = models.CharField(max_length=100, blank=True)
    contact_email = models.EmailField(blank=True)
    
    # Agreement
    agreement_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    
    STATUS = [
        ('active', 'Active'),
        ('pending', 'Pending'),
        ('expired', 'Expired'),
        ('terminated', 'Terminated'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    
    benefits = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class StudentAward(models.Model):
    """Student awards/scholarships."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    
    TYPE = [
        ('academic', 'Academic'),
        ('sports', 'Sports'),
        ('leadership', 'Leadership'),
        ('community', 'Community Service'),
        ('scholarship', 'Scholarship'),
        ('research', 'Research'),
    ]
    award_type = models.CharField(max_length=20, choices=TYPE)
    
    # Amount
    amount = models.DecimalField(
        max_digits=14, decimal_places=2, default=0
    )
    
    # Criteria
    criteria = models.TextField(blank=True)
    minimum_cgpa = models.DecimalField(
        max_digits=3, decimal_places=2, null=True, blank=True
    )
    
    # Deadline
    application_deadline = models.DateField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True)


class AwardRecipient(models.Model):
    """Award recipients."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    award = models.ForeignKey(
        StudentAward,
        on_delete=models.CASCADE,
        related_name='recipients'
    )
    
    student = models.ForeignKey(
        'student.StudentProfile',
        on_delete=models.CASCADE,
        related_name='awards'
    )
    
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    
    # Selection
    selection_date = models.DateField(auto_now_add=True)
    awarded_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL, null=True, related_name='+'
    )
    
    STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('disbursed', 'Disbursed'),
        ('revoked', 'Revoked'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='pending')


class Convocation(models.Model):
    """Convocation ceremonies."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    ceremony_number = models.IntegerField()
    year = models.IntegerField()
    
    TYPE = [
        ('inaugural', 'Inaugural'),
        ('regular', 'Regular'),
        ('special', 'Special'),
    ]
    convocation_type = models.CharField(max_length=20, choices=TYPE)
    
    # Date & Venue
    ceremony_date = models.DateField()
    venue = models.CharField(max_length=100)
    
    # Guest
    guest_of_honor = models.CharField(max_length=200, blank=True)
    keynote_speaker = models.CharField(max_length=200, blank=True)
    
    # Schedule
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    # Status
    STATUS = [
        ('planning', 'Planning'),
        ('invites', 'Invites Out'),
        ('rsvp', 'RSVP'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='planning')
    
    created_at = models.DateTimeField(auto_now_add=True)


class ConvocationGraduate(models.Model):
    """Graduates attending convocation."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    convocation = models.ForeignKey(
        Convocation,
        on_delete=models.CASCADE,
        related_name='graduates'
    )
    
    student = models.ForeignKey(
        'student.StudentProfile',
        on_delete=models.CASCADE
    )
    
    # Attendance
    has_confirmed = models.BooleanField(default=False)
    guest_count = models.IntegerField(default=0)
    
    # Academic details
    degree = models.CharField(max_length=50)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2)
    
    # Requirements
    clearance_complete = models.BooleanField(default=False)
    gown_collected = models.BooleanField(default=False)
    ticket_collected = models.BooleanField(default=False)
    
    STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='pending')


class OnlineAssessment(models.Model):
    """Online quizzes/exams."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    course = models.ForeignKey('academic.Course', on_delete=models.CASCADE)
    
    title = models.CharField(max_length=200)
    instructions = models.TextField()
    
    # Timing
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    duration_minutes = models.IntegerField()
    
    # Settings
    total_marks = models.IntegerField()
    pass_mark = models.IntegerField(default=40)
    
    # Attempts
    allow_multiple = models.BooleanField(default=False)
    max_attempts = models.IntegerField(default=1)
    
    # Shuffling
    shuffle_questions = models.BooleanField(default=False)
    shuffle_options = models.BooleanField(default=False)
    
    # Proctoring
    proctored = models.BooleanField(default=False)
    record_video = models.BooleanField(default=False)
    
    is_published = models.BooleanField(default=False)


class AssessmentQuestion(models.Model):
    """Assessment questions."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    assessment = models.ForeignKey(
        OnlineAssessment,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    
    question_text = models.TextField()
    question_type = models.CharField(
        max_length=20,
        choices=[
            ('mcq', 'Multiple Choice'),
            ('true_false', 'True/False'),
            ('short', 'Short Answer'),
            ('long', 'Long Answer'),
        ]
    )
    
    marks = models.IntegerField(default=1)
    
    # Options (for MCQ)
    options = models.JSONField(default=list)
    correct_answer = models.CharField(max_length=50)
    
    order = models.IntegerField(default=0)


class AssessmentAttempt(models.Model):
    """Student assessment attempts."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    assessment = models.ForeignKey(
        OnlineAssessment,
        on_delete=models.CASCADE,
        related_name='attempts'
    )
    
    student = models.ForeignKey(
        'student.StudentProfile',
        on_delete=models.CASCADE
    )
    
    attempt_number = models.IntegerField(default=1)
    
    # Answers (JSON)
    answers = models.JSONField(default=dict)
    
    # Results
    score = models.DecimalField(
        max_digits=5, decimal_places=2, default=0
    )
    passed = models.BooleanField(default=False)
    
    started_at = models.DateTimeField(null=True, blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['assessment', 'student', 'attempt_number']


class AuditLog(models.Model):
    """System audit log."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL, null=True, blank=True
    )
    
    action = models.CharField(max_length=50)
    model_name = models.CharField(max_length=50)
    object_id = models.CharField(max_length=50)
    
    changes = models.JSONField(default=dict)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['model_name', 'object_id']),
        ]


class DocumentTemplate(models.Model):
    """Document templates."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=100)
    
    TYPE = [
        ('letter', 'Letter'),
        ('certificate', 'Certificate'),
        ('transcript', 'Transcript'),
        ('id_card', 'ID Card'),
        ('id', 'Invoice'),
        ('receipt', 'Receipt'),
    ]
    document_type = models.CharField(max_length=20, choices=TYPE)
    
    template_content = models.TextField()
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class GeneratedDocument(models.Model):
    """Generated documents."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    template = models.ForeignKey(
        DocumentTemplate,
        on_delete=models.CASCADE
    )
    
    student = models.ForeignKey(
        'student.StudentProfile',
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    
    # Content
    content = models.TextField()
    
    # Status
    is_signed = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=50, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['verification_code']),
        ]