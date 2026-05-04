import uuid
from django.db import models
from apps.accounts.models import User
from apps.academic.models import Programme


class AdmissionStatus(models.TextChoices):
    APPLIED = 'applied', 'Applied'
    SCREENING = 'screening', 'Screening'
    ADMITTED = 'admitted', 'Admitted'
    REJECTED = 'rejected', 'Rejected'
    DEFERRED = 'deferred', 'Deferred'


class StudentProfile(models.Model):
    """Extended student profile."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='student_profile_dup'
    )
    matric_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    other_names = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    nationality = models.CharField(max_length=50, default='Nigerian')
    state_of_origin = models.CharField(max_length=50, blank=True)
    lga = models.CharField(max_length=50, blank=True)
    admission_session = models.ForeignKey(
        'academic.AcademicSession', on_delete=models.SET_NULL, 
        null=True, related_name='admitted_students'
    )
    admission_status = models.CharField(
        max_length=20, choices=AdmissionStatus.choices, 
        default=AdmissionStatus.APPLIED
    )
    current_level = models.IntegerField(default=100)
    programme = models.ForeignKey(
        Programme, on_delete=models.SET_NULL, null=True, 
        related_name='students'
    )
    clearance_status = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'student_profiles'
        ordering = ['matric_number']
        indexes = [
            models.Index(fields=['matric_number']),
            models.Index(fields=['admission_status']),
            models.Index(fields=['current_level']),
            models.Index(fields=['programme', 'admission_status']),
        ]

    def __str__(self):
        return self.matric_number or self.user.email

    @property
    def full_name(self):
        parts = [self.first_name]
        if self.other_names:
            parts.append(self.other_names)
        parts.append(self.last_name)
        return ' '.join(parts)

    def get_cgpa(self):
        """Calculate current CGPA from results."""
        # Will be implemented with Result model
        return None


class AdmissionApplication(models.Model):
    """Admission application."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        StudentProfile, on_delete=models.CASCADE, 
        related_name='applications'
    )
    jamb_reg_no = models.CharField(max_length=20, blank=True)
    jamb_score = models.IntegerField(null=True, blank=True)
    o_level_result = models.JSONField(default=dict)
    application_session = models.ForeignKey(
        'academic.AcademicSession', on_delete=models.CASCADE,
        related_name='applications'
    )
    status = models.CharField(
        max_length=20, choices=AdmissionStatus.choices,
        default=AdmissionStatus.APPLIED
    )
    reviewer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='reviewed_applications'
    )
    review_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'admission_applications'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student} - {self.application_session}"


class RegistrationStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    DROPPED = 'dropped', 'Dropped'
    COMPLETED = 'completed', 'Completed'


class CourseRegistration(models.Model):
    """Student course registration."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        StudentProfile, on_delete=models.CASCADE,
        related_name='registrations'
    )
    course = models.ForeignKey(
        'academic.Course', on_delete=models.CASCADE,
        related_name='registrations'
    )
    session = models.ForeignKey(
        'academic.AcademicSession', on_delete=models.CASCADE,
        related_name='registrations'
    )
    semester = models.ForeignKey(
        'academic.Semester', on_delete=models.CASCADE,
        related_name='registrations'
    )
    status = models.CharField(
        max_length=20, choices=RegistrationStatus.choices,
        default=RegistrationStatus.ACTIVE
    )
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'course_registrations'
        unique_together = ['student', 'course', 'session', 'semester']

    def __str__(self):
        return f"{self.student} - {self.course}"


class TimetableEntry(models.Model):
    """Timetable entry for courses."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(
        'academic.Course', on_delete=models.CASCADE,
        related_name='timetable'
    )
    day_of_week = models.IntegerField(help_text='0=Monday, 6=sunday')
    start_time = models.TimeField()
    end_time = models.TimeField()
    venue = models.CharField(max_length=100)
    semester = models.ForeignKey(
        'academic.Semester', on_delete=models.CASCADE,
        related_name='timetable'
    )

    class Meta:
        db_table = 'timetable_entries'
        unique_together = ['course', 'day_of_week', 'semester']

    def __str__(self):
        return f"{self.course} - {self.day_of_week} {self.start_time}"