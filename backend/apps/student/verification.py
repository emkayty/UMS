"""
WAEC/NECO Verification Integration
For Nigerian O'Level results verification
"""

from django.db import models


class WAECVerification(models.Model):
    """WAEC (West African Examinations Council) verification."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # API Configuration
    api_key = models.CharField(max_length=200, blank=True)
    api_url = models.URLField(
        default='https://api.waecdirect.org/verify'
    )
    is_active = models.BooleanField(default=False)
    
    # Verification settings
    verification_fee = models.DecimalField(
        max_digits=10, decimal_places=2, default=500.00
    )
    cache_validity_days = models.IntegerField(default=90)
    
    # Auto-verify on admission
    auto_verify_on_application = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)


class WAECResult(models.Model):
    """Stored WAEC results."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey(
        'student.StudentProfile', on_delete=models.CASCADE,
        related_name='waec_results'
    )
    
    exam_year = models.IntegerField()
    exam_type = models.CharField(
        max_length=10,  # WAEC, NECO, GCE
        choices=[
            ('waec', 'WAEC'),
            ('neco', 'NECO'),
            ('gce', 'GCE'),
        ]
    )
    exam_number = models.CharField(max_length=20)
    
    # Raw results (subject: grade)
    results = models.JSONField(default=dict)
    
    # Verification status
    is_verified = models.BooleanField(default=False)
    verification_date = models.DateTimeField(null=True, blank=True)
    verification_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('verified', 'Verified'),
            ('failed', 'Failed'),
            ('not_found', 'Not Found'),
        ],
        default='pending'
    )
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['exam_type', 'exam_number', 'exam_year']
    
    def __str__(self):
        return f"{self.exam_type} {self.exam_number} ({self.exam_year})"


class NABTEBVerification(models.Model):
    """NABTEB (National Business and Technical Examination Board)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    api_key = models.CharField(max_length=200, blank=True)
    api_url = models.URLField(default='https://api.nabteb.org/verify')
    is_active = models.BooleanField(default=False)
    
    verification_fee = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)
    created_at = models.DateTimeField(auto_now_add=True)


class GradeEquivalence(models.Model):
    """Grade equivalence tables for international conversions."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=50)
    
    # Subject categories
    SUBJECT_CATEGORIES = [
        ('english', 'English Language'),
        ('mathematics', 'Mathematics'),
        ('sciences', 'Sciences'),
        ('arts', 'Arts'),
        ('commercial', 'Commercial'),
        ('technical', 'Technical'),
        ('other', 'Other'),
    ]
    
    category = models.CharField(max_length=20, choices=SUBJECT_CATEGORIES, default='other')
    
    # Waec grade to numeric
    waec_numeric = models.JSONField(
        default={
            'A1': 8, 'A2': 7, 'B3': 6, 'C4': 5, 'C5': 4, 'C6': 3,
            'D7': 2, 'D8': 1, 'F9': 0
        }
    )
    
    # UCAS tariff points (UK)
    ucas_points = models.JSONField(
        default={
            'A1': 56, 'A2': 48, 'B3': 40, 'C4': 32, 'C5': 24, 'C6': 16,
            'D7': 12, 'D8': 8
        }
    )
    
    # US grade equivalent
    us_grade = models.JSONField(
        default={
            'A1': 'A', 'A2': 'A', 'B3': 'B+', 'C4': 'B', 'C5': 'B-',
            'C6': 'C+', 'D7': 'C', 'D8': 'C-', 'F9': 'F'
        }
    )
    
    # Minimum requirement
    minimum_for_admission = models.CharField(max_length=2, default='C6')


class CreditEquivalence(models.Model):
    """Credit hour equivalence between systems."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    system_name = models.CharField(max_length=50)
    
    # Local credit mapping
    local_credits = models.IntegerField(default=3)
    
    # Equivalent credits
    ects = models.DecimalField(max_digits=4, decimal_places=2, default=6.0)
    credit_hours = models.DecimalField(max_digits=4, decimal_places=2, default=3.0)
    
    # Notional learning hours
    learning_hours = models.IntegerField(default=150)
    
    def __str__(self):
        return f"{self.system_name}: {self.local_credits} credits = {self.ects} ECTS"