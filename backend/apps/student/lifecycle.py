"""
Additional Features for Nigerian/Polytechnic Standards
Student activities, hostel management, medical, sports
"""

from django.db import models


class StudentActivity(models.Model):
    """Student participation in clubs, societies, sports."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey(
        'student.StudentProfile', on_delete=models.CASCADE,
        related_name='activities'
    )
    
    ACTIVITY_TYPES = [
        ('sports', 'Sports'),
        ('cultural', 'Cultural'),
        ('scientific', 'Scientific Society'),
        ('religious', 'Religious'),
        ('volunteer', 'Volunteer Service'),
        ('leadership', 'Student Leadership'),
        ('community', 'Community Service'),
    ]
    
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    activity_name = models.CharField(max_length=100)
    position = models.CharField(max_length=50, blank=True)
    
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    
    # Achievement level
    ACHIEVEMENT_LEVELS = [
        ('participant', 'Participant'),
        ('winner', 'Winner'),
        ('champion', 'Champion'),
        ('record', 'Record Holder'),
    ]
    
    achievement = models.CharField(
        max_length=20, choices=ACHIEVEMENT_LEVELS,
        default='participant'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)


class HostelAllocation(models.Model):
    """Hostel room allocation."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey(
        'student.StudentProfile', on_delete=models.CASCADE,
        related_name='hostel_allocations'
    )
    
    # Hostel details
    hostel_name = models.CharField(max_length=100)
    room_number = models.CharField(max_length=20)
    bed_number = models.IntegerField(default=1)
    
    # Allocation details
    session = models.ForeignKey(
        'academic.AcademicSession', on_delete=models.CASCADE
    )
    semester = models.ForeignKey(
        'academic.Semester', on_delete=models.CASCADE, null=True, blank=True
    )
    
    # Status
    STATUS = [
        ('allocated', 'Allocated'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('pending', 'Pending'),
    ]
    
    status = models.CharField(
        max_length=20, choices=STATUS, default='allocated'
    )
    
    check_in_date = models.DateField(null=True, blank=True)
    check_out_date = models.DateField(null=True, blank=True)
    
    # Charges
    hostel_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'session']


class MedicalRecord(models.Model):
    """Student medical records."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey(
        'student.StudentProfile', on_delete=models.CASCADE,
        related_name='medical_records'
    )
    
    # Medical info
    blood_group = models.CharField(
        max_length=5,
        choices=[
            ('A+', 'A+'), ('A-', 'A-'),
            ('B+', 'B+'), ('B-', 'B-'),
            ('AB+', 'AB+'), ('AB-', 'AB-'),
            ('O+', 'O+'), ('O-', 'O-'),
        ],
        blank=True
    )
    
    genotype = models.CharField(max_length=5, blank=True)  # AA, AS, SS
    
    allergies = models.TextField(blank=True)
    medical_conditions = models.TextField(blank=True)
    current_medications = models.TextField(blank=True)
    
    # Emergency contact
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    emergency_contact_relation = models.CharField(max_length=50, blank=True)
    
    # Medical institution
    hospital_name = models.CharField(max_length=100, blank=True)
    hospital_contact = models.CharField(max_length=50, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)


class DisciplinaryRecord(models.Model):
    """Student disciplinary records."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey(
        'student.StudentProfile', on_delete=models.CASCADE,
        related_name='disciplinary_records'
    )
    
    # Incident details
    incident_date = models.DateField()
    incident_description = models.TextField()
    
    OFFENCE_TYPES = [
        ('academic', 'Academic Dishonesty'),
        ('attendance', 'Poor Attendance'),
        ('conduct', 'Conduct'),
        ('harassment', 'Harassment'),
        ('property', 'Property Damage'),
        ('substance', 'Substance Abuse'),
        ('other', 'Other'),
    ]
    
    offence_type = models.CharField(max_length=20, choices=OFFENCE_TYPES)
    
    # Action taken
    ACTION_TYPES = [
        ('warning', 'Warning'),
        ('counseling', 'Counseling'),
        ('suspension', 'Suspension'),
        ('expulsion', 'Expulsion'),
        ('probation', 'Probation'),
        ('dismissed', 'Case Dismissed'),
    ]
    
    action_taken = models.CharField(max_length=20, choices=ACTION_TYPES)
    action_date = models.DateField(null=True, blank=True)
    
    # Authority
    handled_by = models.CharField(max_length=100, blank=True)
    witness = models.CharField(max_length=100, blank=True)
    
    # Outcomes
    is_expunged = models.BooleanField(default=False)
    expungement_date = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)


class AlumniRecord(models.Model):
    """Alumni tracking."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey(
        'student.StudentProfile', on_delete=models.CASCADE,
        related_name='alumni_record'
    )
    
    # Graduation details
    graduation_year = models.IntegerField()
    convocation_date = models.DateField(null=True, blank=True)
    
    # Degree details
    degree_awarded = models.CharField(max_length=100)
    class_of_degree = models.CharField(
        max_length=30,
        choices=[
            ('first_class', 'First Class'),
            ('second_upper', 'Second Class Upper'),
            ('second_lower', 'Second Class Lower'),
            ('third', 'Third Class'),
            ('pass', 'Pass'),
        ]
    )
    
    # Alumni info
    current_employer = models.CharField(max_length=200, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    employment_sector = models.CharField(
        max_length=30, blank=True,
        choices=[
            ('private', 'Private Sector'),
            ('public', 'Public Sector'),
            ('self', 'Self Employed'),
            ('unemployed', 'Unemployed'),
            ('further_study', 'Further Study'),
        ]
    )
    
    location = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    
    # Social
    linkedin = models.URLField(blank=True)
    twitter = models.CharField(max_length=50, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)


class Convocation(models.Model):
    """Convocation ceremony management."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    session = models.ForeignKey(
        'academic.AcademicSession', on_delete=models.CASCADE
    )
    
    convocation_date = models.DateField()
    venue = models.CharField(max_length=200)
    
    # Important dates
    clearance_start = models.DateField()
    clearance_end = models.DateField()
    gown_pickup_start = models.DateField()
    gown_pickup_end = models.DateField()
    
    # Guest limits
    max_guests_per_student = models.IntegerField(default=2)
    
    # Fee
    convocation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=5000.00)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)