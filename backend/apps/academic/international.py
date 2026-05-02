"""
European/UK University Standards Integration
ECTS, Bologna Process, Degree Classifications
"""

from django.db import models


class ECTSConfiguration(models.Model):
    """ECTS (European Credit Transfer and Accumulation System) configuration."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # ECTS to local credit conversion
    ects_to_local_ratio = models.DecimalField(max_digits=4, decimal_places=2, default=2.0)
    ects_per_year = models.IntegerField(default=60)
    ects_per_semester = models.IntegerField(default=30)
    
    # Bologna cycle
    BACHELOR = 'bachelor'
    MASTER = 'master'
    DOCTORATE = 'doctorate'
    
    cycle = models.CharField(
        max_length=20,
        choices=[
            (BACHELOR, 'Bachelor (180-240 ECTS)'),
            (MASTER, 'Master (60-120 ECTS)'),
            (DOCTORATE, 'Doctorate'),
        ],
        default=BACHELOR
    )
    
    # Bologna descriptors
    dublin_descriptors = models.JSONField(default=dict)


class DegreeClassificationUK(models.Model):
    """UK degree classification system."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # UK Classification thresholds
    first_class = models.DecimalField(max_digits=3, decimal_places=2, default=70.0)
    upper_second = models.DecimalField(max_digits=3, decimal_places=2, default=60.0)
    lower_second = models.DecimalField(max_digits=3, decimal_places=2, default=50.0)
    third = models.DecimalField(max_digits=3, decimal_places=2, default=40.0)
    
    # Weighted calculation method
    weighted_by_credits = models.BooleanField(default=True)
    year_weightings = models.JSONField(
        default=[0.3, 0.3, 0.4],
        help_text="Year 1, Year 2, Year 3 weights for final classification"
    )
    
    name = models.CharField(max_length=50, default='UK Standard')


class GPAConfiguration(models.Model):
    """American GPA (4.0 scale) system."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # American 4.0 scale
    a_plus = models.DecimalField(max_digits=3, decimal_places=2, default=4.0)
    a = models.DecimalField(max_digits=3, decimal_places=2, default=4.0)
    a_minus = models.DecimalField(max_digits=3, decimal_places=2, default=3.7)
    b_plus = models.DecimalField(max_digits=3, decimal_places=2, default=3.3)
    b = models.DecimalField(max_digits=3, decimal_places=2, default=3.0)
    b_minus = models.DecimalField(max_digits=3, decimal_places=2, default=2.7)
    c_plus = models.DecimalField(max_digits=3, decimal_places=2, default=2.3)
    c = models.DecimalField(max_digits=3, decimal_places=2, default=2.0)
    c_minus = models.DecimalField(max_digits=3, decimal_places=2, default=1.7)
    d = models.DecimalField(max_digits=3, decimal_places=2, default=1.0)
    f = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    
    pass_mark = models.DecimalField(max_digits=3, decimal_places=2, default=2.0)
    include_plus_minus = models.BooleanField(default=True)
    name = models.CharField(max_length=50, default='US Standard')


class SemesterCreditSystem(models.Model):
    """American semester credit hour system."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    credits_per_course = models.IntegerField(default=3)
    min_credits_per_semester = models.IntegerField(default=12)
    max_credits_per_semester = models.IntegerField(default=18)
    full_time_load = models.IntegerField(default=15)
    
    satisfactory_academic_progress = models.DecimalField(max_digits=3, decimal_places=2, default=2.0)
    academic_probation = models.DecimalField(max_digits=3, decimal_places=2, default=2.0)
    financial_aid_sap = models.DecimalField(max_digits=3, decimal_places=2, default=2.5)
    
    name = models.CharField(max_length=50, default='US Semester System')


class TranscriptTemplate(models.Model):
    """Transcript template configurations for different regions."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    REGION_CHOICES = [
        ('nigerian', 'Nigerian'),
        ('uk', 'UK/European'),
        ('american', 'American'),
        ('custom', 'Custom'),
    ]
    
    region = models.CharField(max_length=20, choices=REGION_CHOICES, default='nigerian')
    name = models.CharField(max_length=100)
    
    include_gpa = models.BooleanField(default=True)
    include_cgpa = models.BooleanField(default=True)
    include_credits = models.BooleanField(default=True)
    include_hours = models.BooleanField(default=False)
    include_rank = models.BooleanField(default=True)
    
    show_letter_grade = models.BooleanField(default=True)
    show_percentage = models.BooleanField(default=True)
    show_grade_points = models.BooleanField(default=True)
    
    footer_text = models.TextField(blank=True)
    include_qr_code = models.BooleanField(default=True)
    include_verification_url = models.BooleanField(default=True)
    
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.region})"