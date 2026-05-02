"""
Sports & Games Management
Teams, facilities, activities
"""

from django.db import models
import uuid


class SportsFacility(models.Model):
    """Sports facilities."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    
    TYPE = [
        ('football', 'Football Field'),
        ('basketball', 'Basketball Court'),
        ('tennis', 'Tennis Court'),
        ('volleyball', 'Volleyball Court'),
        ('swimming', 'Swimming Pool'),
        ('gym', 'Gym'),
        ('track', 'Track'),
        ('hall', 'Sports Hall'),
    ]
    facility_type = models.CharField(max_length=20, choices=TYPE)
    
    capacity = models.IntegerField(default=50)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    
    is_active = models.BooleanField(default=True)


class SportsTeam(models.Model):
    """Sports teams."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=100)
    sport = models.CharField(max_length=50)
    
    TYPE = [
        ('football', 'Football'),
        ('basketball', 'Basketball'),
        ('volleyball', 'Volleyball'),
        ('athletics', 'Athletics'),
        ('table_tennis', 'Table Tennis'),
        ('tennis', 'Tennis'),
    ]
    game_type = models.CharField(max_length=20, choices=TYPE)
    
    # Coach
    coach = models.ForeignKey(
        'staff.StaffProfile',
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name='+'
    )
    
    captain = models.ForeignKey(
        'student.StudentProfile',
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name='+'
    )
    
    training_day = models.CharField(max_length=20, blank=True)
    training_time = models.TimeField(blank=True)
    
    STATUS = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='active')


class TeamMember(models.Model):
    """Team members."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    team = models.ForeignKey(
        SportsTeam,
        on_delete=models.CASCADE,
        related_name='members'
    )
    
    student = models.ForeignKey(
        'student.StudentProfile',
        on_delete=models.CASCADE,
        related_name='teams'
    )
    
    ROLE = [
        ('player', 'Player'),
        ('captain', 'Captain'),
        ('vice_captain', 'Vice Captain'),
        ('manager', 'Manager'),
    ]
    role = models.CharField(max_length=20, choices=ROLE, default='player')
    
    jersey_number = models.CharField(max_length=10, blank=True)
    
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['team', 'student']


class SportsActivity(models.Model):
    """Sports activities/events."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    facility = models.ForeignKey(
        SportsFacility,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    TYPE = [
        ('training', 'Training'),
        ('match', 'Match'),
        ('competition', 'Competition'),
        ('trial', 'Trial'),
    ]
    activity_type = models.CharField(max_length=20, choices=TYPE)
    
    is_compulsory = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)


class FitnessRecord(models.Model):
    """Student fitness records."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey(
        'student.StudentProfile',
        on_delete=models.CASCADE,
        related_name='fitness_records'
    )
    
    activity = models.ForeignKey(
        SportsActivity,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    
    # Activity tracking
    activity_type = models.CharField(max_length=50)
    duration_minutes = models.IntegerField()
    date = models.DateField()
    
    notes = models.TextField(blank=True)


class SportsAchievement(models.Model):
    """Sports achievements."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey(
        'student.StudentProfile',
        on_delete=models.CASCADE,
        related_name='sports_achievements'
    )
    
    competition = models.CharField(max_length=200)
    sport = models.CharField(max_length=50)
    
    POSITION = [
        ('first', 'First Place'),
        ('second', 'Second Place'),
        ('third', 'Third Place'),
        ('participant', 'Participant'),
    ]
    position = models.CharField(max_length=20, choices=POSITION)
    
    date = models.DateField()
    certificate_issued = models.BooleanField(default=False)


class ClinicRecord(models.Model):
    """Student clinic/medical records."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey(
        'student.StudentProfile',
        on_delete=models.CASCADE,
        related_name='clinic_records'
    )
    
    visit_date = models.DateField()
    complaint = models.CharField(max_length=200)
    diagnosis = models.CharField(max_length=200)
    treatment = models.TextField()
    
    # Prescribed medication
    medication = models.TextField(blank=True)
    
    # Referral
    referred_to = models.CharField(max_length=100, blank=True)
    
    # Vital signs
    temperature = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True
    )
    blood_pressure = models.CharField(max_length=20, blank=True)
    pulse = models.IntegerField(null=True, blank=True)
    
    seen_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL, null=True, related_name='+'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)


class SecurityIncident(models.Model):
    """Security incidents."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    incident_date = models.DateField()
    incident_time = models.TimeField()
    
    TYPE = [
        ('theft', 'Theft'),
        ('assault', 'Assault'),
        ('vandalism', 'Vandalism'),
        ('trespassing', 'Trespassing'),
        ('harassment', 'Harassment'),
        ('other', 'Other'),
    ]
    incident_type = models.CharField(max_length=20, choices=TYPE)
    
    description = models.TextField()
    location = models.CharField(max_length=100)
    
    # Involved parties
    reported_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL, null=True, related_name='+'
    )
    
    STATUS = [
        ('reported', 'Reported'),
        ('investigating', 'Investigating'),
        ('resolved', 'Resolved'),
        ('police', 'Police Notified'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='reported')
    
    resolution = models.TextField(blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)


class VisitorLog(models.Model):
    """Visitor log."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    visitor_name = models.CharField(max_length=100)
    visitor_phone = models.CharField(max_length=20, blank=True)
    
    host = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='visitors'
    )
    
    purpose = models.CharField(max_length=200)
    
    entry_time = models.DateTimeField(auto_now_add=True)
    exit_time = models.DateTimeField(null=True, blank=True)
    
    valid_until = models.DateField()


class QualityAssurance(models.Model):
    """Quality assurance records."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    TYPE = [
        ('accreditation', 'Accreditation'),
        ('audit', 'Audit'),
        ('inspection', 'Inspection'),
        ('review', 'Review'),
    ]
    qa_type = models.CharField(max_length=20, choices=TYPE)
    
    body = models.CharField(max_length=100)
    
    date = models.DateField()
    
    STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('passed', 'Passed'),
        ('failed', 'Failed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    
    report = models.TextField(blank=True)
    score = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)


class ResearchEthics(models.Model):
    """Research ethics approval."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    researcher = models.ForeignKey(
        'staff.StaffProfile',
        on_delete=models.CASCADE,
        related_name='ethics_applications'
    )
    
    title = models.CharField(max_length=500)
    description = models.TextField()
    
    APPROVAL = [
        ('pending', 'Pending'),
        ('conditional', 'Conditional Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=APPROVAL, default='pending')
    
    # Review
    reviewers = models.JSONField(default=list)
    
    conditions = models.TextField(blank=True)
    
    approval_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)