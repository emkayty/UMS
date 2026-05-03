"""
Alumni Management System
Post-graduation tracking and engagement
"""

import uuid
from django.db import models
from apps.accounts.models import User


class AlumniStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'
    LOST = 'lost', 'Lost Contact'
    DECEASED = 'deceased', 'Deceased'


class EmploymentStatus(models.TextChoices):
    EMPLOYED = 'employed', 'Employed'
    UNEMPLOYED = 'unemployed', 'Unemployed'
    SELF_EMPLOYED = 'self_employed', 'Self-Employed'
    FURTHER_STUDY = 'further_study', 'Further Studies'
    STARTUP = 'startup', 'Running Startup'


# ============================================================
# ALUMNI PROFILE
# ============================================================

class AlumniProfile(models.Model):
    """Alumni record after graduation."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Link to student
    student = models.ForeignKey(
        'student.StudentProfile', on_delete=models.CASCADE,
        related_name='alumni_record'
    )
    
    # Graduation details
    graduation_session = models.ForeignKey(
        'academic.AcademicSession', on_delete=models.SET_NULL,
        null=True, related_name='graduated_students'
    )
    graduation_year = models.IntegerField()
    degree_awarded = models.CharField(max_length=100)
    degree_class = models.CharField(
        max_length=20,
        choices=[
            ('first', 'First Class'),
            ('second_up', 'Second Class Upper'),
            ('second_down', 'Second Class Lower'),
            ('third', 'Third Class'),
            ('pass', 'Pass'),
        ]
    )
    
    # Status
    alumni_status = models.CharField(
        max_length=20, choices=AlumniStatus.choices,
        default=AlumniStatus.ACTIVE
    )
    
    # Contact (may change after graduation)
    current_email = models.EmailField(blank=True)
    current_phone = models.CharField(max_length=20, blank=True)
    current_address = models.TextField(blank=True)
    
    # Social
    linkedin = models.URLField(blank=True)
    twitter = models.CharField(max_length=50, blank=True)
    facebook = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'alumni_profiles'
        ordering = ['-graduation_year']

    def __str__(self):
        return f"{self.student.matric_number} - Class of {self.graduation_year}"


# ============================================================
# EMPLOYMENT RECORD
# ============================================================

class EmploymentRecord(models.Model):
    """Alumni employment history."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    alumni = models.ForeignKey(
        AlumniProfile, on_delete=models.CASCADE,
        related_name='employment_records'
    )
    
    # Employment
    status = models.CharField(
        max_length=20, choices=EmploymentStatus.choices
    )
    company_name = models.CharField(max_length=200)
    position = models.CharField(max_length=100)
    
    # Industry
    industry = models.CharField(max_length=100)
    sector = models.CharField(max_length=100, blank=True)
    
    # Location
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    
    # Dates
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    
    # Salary range
    salary_range = models.CharField(
        max_length=30, blank=True,
        help_text='e.g. 100k-200k, 500k+'
    )
    
    # Description
    job_description = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'employment_records'
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.alumni.student.matric_number} - {self.company_name}"


# ============================================================
# FURTHER STUDIES
# ============================================================

class FurtherStudy(models.Model):
    """Alumni pursuing further studies."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    alumni = models.ForeignKey(
        AlumniProfile, on_delete=models.CASCADE,
        related_name='further_studies'
    )
    
    # Institution
    institution = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    
    # Programme
    programme = models.CharField(max_length=200)
    degree_type = models.CharField(
        max_length=50,
        choices=[
            ('masters', "Master's"),
            ('phd', 'PhD'),
            ('postdoc', 'Postdoctoral'),
            ('certificate', 'Certificate'),
            ('diploma', 'Diploma'),
        ]
    )
    
    # Status
    is_current = models.BooleanField(default=True)
    start_year = models.IntegerField()
    expected_completion = models.IntegerField(null=True, blank=True)
    actual_completion = models.IntegerField(null=True, blank=True)
    
    # Scholarship
    scholarship = models.BooleanField(default=False)
    scholarship_details = models.CharField(max_length=200, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'further_studies'

    def __str__(self):
        return f"{self.alumni.student.matric_number} - {self.programme}"


# ============================================================
# ALUMNI EVENT
# ============================================================

class AlumniEvent(models.Model):
    """Alumni events and gatherings."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    title = models.CharField(max_length=200)
    event_type = models.CharField(
        max_length=30,
        choices=[
            ('reunion', 'Class Reunion'),
            ('networking', 'Networking'),
            ('workshop', 'Workshop/Seminar'),
            ('fundraiser', 'Fundraiser'),
            ('homecoming', 'Homecoming'),
            ('meetup', 'Meetup'),
            ('other', 'Other'),
        ]
    )
    
    # Date & Venue
    event_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)
    venue = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    
    # Details
    description = models.TextField()
    target_class = models.CharField(
        max_length=50, blank=True,
        help_text='e.g. 2020, 2021'
    )
    
    # Registration
    requires_registration = models.BooleanField(default=True)
    registration_deadline = models.DateField(null=True, blank=True)
    max_attendees = models.IntegerField(null=True, blank=True)
    
    # Fee
    fee = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )
    
    # Status
    is_published = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'alumni_events'
        ordering = ['-event_date']

    def __str__(self):
        return f"{self.title} - {self.event_date}"


# ============================================================
# EVENT REGISTRATION
# ============================================================

class AlumniEventRegistration(models.Model):
    """Alumni event registration."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    event = models.ForeignKey(
        AlumniEvent, on_delete=models.CASCADE,
        related_name='registrations'
    )
    alumni = models.ForeignKey(
        AlumniProfile, on_delete=models.CASCADE,
        related_name='event_registrations'
    )
    
    is_confirmed = models.BooleanField(default=False)
    confirmed_at = models.DateField(null=True, blank=True)
    
    guests = models.IntegerField(default=0)
    total_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )
    
    notes = models.TextField(blank=True)
    
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'alumni_event_registrations'
        unique_together = ['event', 'alumni']

    def __str__(self):
        return f"{self.alumni.student.matric_number} - {self.event.title}"


# ============================================================
# ALUMNI DUES
# ============================================================

class AlumniDues(models.Model):
    """Alumni annual dues/contributions."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    session = models.ForeignKey(
        'academic.AcademicSession', on_delete=models.CASCADE
    )
    
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True)
    
    is_active = models.BooleanField(default=True)
    deadline = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'alumni_dues'

    def __str__(self):
        return f"Dues - {self.session.name}"


class AlumniDuePayment(models.Model):
    """Alumni due payment record."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    alumni = models.ForeignKey(
        AlumniProfile, on_delete=models.CASCADE,
        related_name='due_payments'
    )
    dues = models.ForeignKey(
        AlumniDues, on_delete=models.CASCADE
    )
    
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateField()
    payment_ref = models.CharField(max_length=50)
    
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'alumni_due_payments'

    def __str__(self):
        return f"{self.alumni.student.matric_number} - {self.dues.session.name}"


# ============================================================
# JOB POSTING
# ============================================================

class JobPosting(models.Model):
    """Job opportunities for alumni."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    posted_by = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    
    # Job Details
    title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    industry = models.CharField(max_length=100)
    
    # Location
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    
    # Type
    employment_type = models.CharField(
        max_length=20,
        choices=[
            ('full_time', 'Full Time'),
            ('part_time', 'Part Time'),
            ('contract', 'Contract'),
            ('internship', 'Internship'),
        ]
    )
    
    # Salary
    salary_min = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    salary_max = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    
    # Description
    description = models.TextField()
    requirements = models.TextField()
    how_to_apply = models.TextField()
    
    # Deadline
    application_deadline = models.DateField()
    
    # Status
    is_published = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    views = models.IntegerField(default=0)
    applications = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'job_postings'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.company_name}"