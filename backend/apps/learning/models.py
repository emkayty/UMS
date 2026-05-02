import uuid
from django.db import models
from apps.accounts.models import User
from apps.academic.models import Course


class MaterialType(models.TextChoices):
    PDF = 'pdf', 'PDF Document'
    VIDEO = 'video', 'Video'
    LINK = 'link', 'External Link'
    OTHER = 'other', 'Other'


class Material(models.Model):
    """Learning materials."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='materials'
    )
    lecturer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='uploaded_materials'
    )
    title = models.CharField(max_length=200)
    file_url = models.URLField(blank=True)
    file_type = models.CharField(
        max_length=20, choices=MaterialType.choices,
        default=MaterialType.PDF
    )
    description = models.TextField(blank=True)
    is_offline_available = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'learning_materials'
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['course']),
            models.Index(fields=['lecturer']),
        ]

    def __str__(self):
        return f"{self.course.code} - {self.title}"


class AssignmentStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    PUBLISHED = 'published', 'Published'
    CLOSED = 'closed', 'Closed'


class Assignment(models.Model):
    """Course assignments."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='assignments'
    )
    lecturer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='created_assignments'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    max_score = models.DecimalField(max_digits=5, decimal_places=2)
    grading_rubric = models.JSONField(default=dict)
    status = models.CharField(
        max_length=20, choices=AssignmentStatus.choices,
        default=AssignmentStatus.DRAFT
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'assignments'
        ordering = ['due_date']
        indexes = [
            models.Index(fields=['course', 'status']),
            models.Index(fields=['due_date']),
        ]

    def __str__(self):
        return f"{self.course.code} - {self.title}"


class SubmissionStatus(models.TextChoices):
    NOT_STARTED = 'not_started', 'Not Started'
    SUBMITTED = 'submitted', 'Submitted'
    GRADED = 'graded', 'Graded'
    LATE = 'late', 'Late'


class AssignmentSubmission(models.Model):
    """Assignment submissions."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE, related_name='submissions'
    )
    student = models.ForeignKey(
        'student.StudentProfile', on_delete=models.CASCADE,
        related_name='assignment_submissions'
    )
    file_url = models.URLField(blank=True)
    text_answer = models.TextField(blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    score = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    feedback = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, choices=SubmissionStatus.choices,
        default=SubmissionStatus.NOT_STARTED
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'assignment_submissions'
        unique_together = ['assignment', 'student']

    def __str__(self):
        return f"{self.assignment} - {self.student}"


class Quiz(models.Model):
    """Course quizzes."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='quizzes'
    )
    lecturer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='created_quizzes'
    )
    title = models.CharField(max_length=200)
    duration_minutes = models.IntegerField(default=30)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    questions = models.JSONField(default=list)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'quizzes'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.course.code} - {self.title}"


class QuizAttempt(models.Model):
    """Quiz attempts."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name='attempts'
    )
    student = models.ForeignKey(
        'student.StudentProfile', on_delete=models.CASCADE,
        related_name='quiz_attempts'
    )
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    answers = models.JSONField(default=dict)
    score_total = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    is_passed = models.BooleanField(default=False)

    class Meta:
        db_table = 'quiz_attempts'
        unique_together = ['quiz', 'student']

    def __str__(self):
        return f"{self.quiz} - {self.student}"


class AttendanceMethod(models.TextChoices):
    QR = 'qr', 'QR Code'
    MANUAL = 'manual', 'Manual'


class AttendanceSession(models.Model):
    """Attendance sessions."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='attendance_sessions'
    )
    lecturer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='attendance_sessions'
    )
    date = models.DateField()
    qr_code_token = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'attendance_sessions'
        unique_together = ['course', 'date']

    def __str__(self):
        return f"{self.course} - {self.date}"


class AttendanceRecord(models.Model):
    """Attendance records."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(
        AttendanceSession, on_delete=models.CASCADE,
        related_name='records'
    )
    student = models.ForeignKey(
        'student.StudentProfile', on_delete=models.CASCADE,
        related_name='attendance_records'
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    method = models.CharField(
        max_length=20, choices=AttendanceMethod.choices
    )
    is_valid = models.BooleanField(default=True)

    class Meta:
        db_table = 'attendance_records'
        unique_together = ['session', 'student']

    def __str__(self):
        return f"{self.session} - {self.student}"