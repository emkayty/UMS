"""
Application & Extended Student Services
Online application, hostel, transcripts, complaints, alumni
"""

from django.db import models
import uuid


class Applicant(models.Model):
    """Prospective student applicant."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Personal info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    
    # Application
    application_number = models.CharField(max_length=20, unique=True)
    
    # Programme applied
    programme = models.ForeignKey(
        'academic.Programme',
        on_delete=models.CASCADE,
        related_name='applicants'
    )
    
    # JAMB details
    jamb_number = models.CharField(max_length=20, blank=True)
    jamb_score = models.IntegerField(null=True, blank=True)
    
    # O-Level results
    olevel_results = models.JSONField(default=list)
    
    # Status
    STATUS = [
        ('submitted', 'Submitted'),
        ('screening', 'Under Screening'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('admitted', 'Admitted'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='submitted')
    
    # Screening
    screening_score = models.IntegerField(default=0)
    screening_date = models.DateField(null=True, blank=True)
    
    # Admission
    admission_letter_sent = models.BooleanField(default=False)
    admission_date = models.DateField(null=True, blank=True)
    portal_created = models.BooleanField(default=False)
    student_id = models.CharField(max_length=20, blank=True)
    
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Hostel(models.Model):
    """Hostel/Accommodation."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=100)
    type = models.CharField(
        max_length=20,
        choices=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('mixed', 'Mixed'),
        ]
    )
    
    total_beds = models.IntegerField(default=0)
    available_beds = models.IntegerField(default=0)
    gender = models.CharField(max_length=10)
    floor_count = models.IntegerField(default=3)
    rooms_per_floor = models.IntegerField(default=10)
    amenities = models.JSONField(default=list)
    rules = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)


class HostelRoom(models.Model):
    """Individual hostel room."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    hostel = models.ForeignKey(
        Hostel,
        on_delete=models.CASCADE,
        related_name='rooms'
    )
    
    room_number = models.CharField(max_length=20)
    floor = models.IntegerField()
    capacity = models.IntegerField(default=4)
    occupied = models.IntegerField(default=0)
    
    TYPE = [
        ('standard', 'Standard'),
        ('self_attached', 'Self-Contained'),
        ('special', 'Special Needs'),
    ]
    room_type = models.CharField(max_length=20, choices=TYPE, default='standard')
    gender = models.CharField(max_length=10)
    
    STATUS = [
        ('available', 'Available'),
        ('full', 'Full'),
        ('maintenance', 'Under Maintenance'),
        ('closed', 'Closed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='available')
    
    class Meta:
        unique_together = ['hostel', 'room_number']


class HostelApplication(models.Model):
    """Student hostel applications."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey(
        'student.StudentProfile',
        on_delete=models.CASCADE,
        related_name='hostel_applications'
    )
    
    hostel = models.ForeignKey(
        Hostel,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    room_type = models.CharField(max_length=20)
    session = models.ForeignKey('academic.AcademicSession', on_delete=models.CASCADE)
    
    STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('allocated', 'Allocated'),
        ('checked_in', 'Checked In'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    
    allocated_room = models.ForeignKey(
        HostelRoom,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    bed_number = models.CharField(max_length=10, blank=True)
    check_in_date = models.DateField(null=True, blank=True)
    check_out_date = models.DateField(null=True, blank=True)
    
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TranscriptRequest(models.Model):
    """Transcript request system."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey(
        'student.StudentProfile',
        on_delete=models.CASCADE,
        related_name='transcript_requests'
    )
    
    recipient_name = models.CharField(max_length=200)
    recipient_institution = models.CharField(max_length=200)
    recipient_address = models.TextField()
    recipient_email = models.EmailField()
    
    PURPOSE = [
        ('admission', 'Further Studies'),
        ('employment', 'Employment'),
        ('migration', 'Migration'),
        ('legal', 'Legal'),
        ('other', 'Other'),
    ]
    purpose = models.CharField(max_length=20, choices=PURPOSE)
    
    DELIVERY = [
        ('pickup', 'Pickup'),
        ('courier', 'Courier'),
        ('email', 'Email'),
    ]
    delivery_method = models.CharField(max_length=20, choices=DELIVERY, default='pickup')
    courier_address = models.TextField(blank=True)
    tracking_number = models.CharField(max_length=50, blank=True)
    
    STATUS = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('ready', 'Ready for Pickup'),
        ('dispatched', 'Dispatched'),
        ('delivered', 'Delivered'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    
    processed_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='+'
    )
    
    fee_amount = models.DecimalField(max_digits=10, decimal_places=2, default=5000)
    fee_paid = models.BooleanField(default=False)
    
    processed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Complaint(models.Model):
    """Student complaint/grievance system."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey(
        'student.StudentProfile',
        on_delete=models.CASCADE,
        related_name='complaints'
    )
    
    category = models.CharField(
        max_length=30,
        choices=[
            ('academic', 'Academic'),
            ('administrative', 'Administrative'),
            ('financial', 'Financial'),
            ('harassment', 'Harassment'),
            ('discrimination', 'Discrimination'),
            ('facility', 'Facility'),
            ('other', 'Other'),
        ]
    )
    
    subject = models.CharField(max_length=200)
    description = models.TextField()
    is_anonymous = models.BooleanField(default=False)
    attachments = models.JSONField(default=list)
    
    STATUS = [
        ('submitted', 'Submitted'),
        ('acknowledged', 'Acknowledged'),
        ('investigating', 'Under Investigation'),
        ('resolved', 'Resolved'),
        ('escalated', 'Escalated'),
        ('closed', 'Closed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='submitted')
    
    assigned_to = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='+'
    )
    
    response = models.TextField(blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    satisfaction_rating = models.IntegerField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Alumni(models.Model):
    """Alumni tracking."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey(
        'student.StudentProfile',
        on_delete=models.CASCADE,
        related_name='alumni_record'
    )
    
    graduation_session = models.ForeignKey(
        'academic.AcademicSession',
        on_delete=models.CASCADE
    )
    degree = models.CharField(max_length=50)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2)
    
    STATUS = [
        ('job_searching', 'Job Searching'),
        ('employed', 'Employed'),
        ('self_employed', 'Self Employed'),
        ('further_studies', 'Further Studies'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='job_searching')
    
    employer = models.CharField(max_length=200, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    salary_bracket = models.CharField(max_length=20, blank=True)
    institution = models.CharField(max_length=200, blank=True)
    program = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    linkedin = models.CharField(max_length=100, blank=True)
    is_donated = models.BooleanField(default=False)
    donation_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    willing_to_mentor = models.BooleanField(default=True)
    
    updated_at = models.DateTimeField(auto_now=True)