import uuid
from django.db import models
from apps.accounts.models import User


class ResultStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    APPROVED_HOD = 'approved_hod', 'Approved by HOD'
    APPROVED_DEAN = 'approved_dean', 'Approved by Dean'
    APPROVED_SENATE = 'approved_senate', 'Approved by Senate'
    REJECTED = 'rejected', 'Rejected'


class Result(models.Model):
    """Student results."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    registration = models.ForeignKey(
        'student.CourseRegistration', on_delete=models.CASCADE,
        related_name='results'
    )
    session = models.ForeignKey(
        'academic.AcademicSession', on_delete=models.CASCADE,
        related_name='results'
    )
    semester = models.ForeignKey(
        'academic.Semester', on_delete=models.CASCADE,
        related_name='results'
    )
    lecturer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='submitted_results'
    )
    score = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=2)
    grade_point = models.DecimalField(max_digits=3, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=ResultStatus.choices,
        default=ResultStatus.PENDING
    )
    
    # Approval workflow
    approved_by_hod = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='hod_approved_results'
    )
    hod_comment = models.TextField(blank=True)
    approved_by_dean = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='dean_approved_results'
    )
    dean_comment = models.TextField(blank=True)
    approved_by_senate = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='senate_approved_results'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'results'
        unique_together = ['registration', 'session', 'semester']

    def __str__(self):
        return f"{self.registration} - {self.grade}"


class CGPAHistory(models.Model):
    """CGPA history."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        'student.StudentProfile', on_delete=models.CASCADE,
        related_name='cgpa_history'
    )
    session = models.ForeignKey(
        'academic.AcademicSession', on_delete=models.CASCADE,
        related_name='student_gpas'
    )
    semester = models.ForeignKey(
        'academic.Semester', on_delete=models.CASCADE,
        related_name='student_gpas'
    )
    gpa = models.DecimalField(max_digits=3, decimal_places=2)
    cumulative_gpa = models.DecimalField(max_digits=3, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cgpa_history'
        unique_together = ['student', 'session', 'semester']

    def __str__(self):
        return f"{self.student} - GPA: {self.gpa}, CGPA: {self.cumulative_gpa}"


class GraduationClearance(models.Model):
    """Graduation clearance status."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.OneToOneField(
        'student.StudentProfile', on_delete=models.CASCADE,
        related_name='clearance'
    )
    cleared_by_library = models.BooleanField(default=False)
    cleared_by_hostel = models.BooleanField(default=False)
    cleared_by_bursary = models.BooleanField(default=False)
    cleared_by_department = models.BooleanField(default=False)
    cleared_at = models.DateTimeField(null=True, blank=True)
    eligible_to_graduate = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'graduation_clearance'

    def __str__(self):
        return f"{self.student} - Eligible: {self.eligible_to_graduate}"


class Transcript(models.Model):
    """Transcript requests."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        'student.StudentProfile', on_delete=models.CASCADE,
        related_name='transcripts'
    )
    status = models.CharField(max_length=20, default='pending')
    issued_at = models.DateTimeField(null=True, blank=True)
    pdf_url = models.URLField(blank=True)
    qr_verification_code = models.CharField(max_length=50, unique=True)
    requested_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'transcripts'
        ordering = ['-requested_at']

    def __str__(self):
        return f"{self.student} - {self.status}"


class Certificate(models.Model):
    """Certificates."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        'student.StudentProfile', on_delete=models.CASCADE,
        related_name='certificates'
    )
    certificate_type = models.CharField(max_length=50)
    issued_at = models.DateTimeField(null=True, blank=True)
    pdf_url = models.URLField(blank=True)
    qr_verification_code = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'certificates'

    def __str__(self):
        return f"{self.student} - {self.certificate_type}"