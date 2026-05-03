import uuid
from django.db import models
from django.utils import timezone
from apps.accounts.models import User
from apps.academic.models import Department, Faculty


# ============================================================
# NIGERIAN STAFF RANKS
# ============================================================

class StaffRank(models.TextChoices):
    # ============================================================
    # NIGERIAN ACADEMIC RANKS (Universities)
    # ============================================================
    LECTURER_III = 'lecturer_iii', 'Lecturer III'
    LECTURER_II = 'lecturer_ii', 'Lecturer II'
    LECTURER_I = 'lecturer_i', 'Lecturer I'
    SENIOR_LECTURER = 'senior_lecturer', 'Senior Lecturer'
    READER = 'reader', 'Reader (Associate Professor)'
    PROFESSOR = 'professor', 'Professor'
    
    # ============================================================
    # NIGERIAN POLYTECHNIC RANKS
    # ============================================================
    CHIEF_LECTURER = 'chief_lecturer', 'Chief Lecturer'
    PRINCIPAL_LECTURER = 'principal_lecturer', 'Principal Lecturer'
    SENIOR_LECTURER_P = 'senior_lecturer_p', 'Senior Lecturer'
    LECTURER_P = 'lecturer_p', 'Lecturer'
    
    # ============================================================
    # NIGERIAN ADMINISTRATIVE RANKS
    # ============================================================
    HOD = 'hod', 'Head of Department'
    DEAN = 'dean', 'Dean'
    REGISTRAR = 'registrar', 'Registrar'
    BURSAR = 'bursar', 'Bursar'
    VICE_CHANCELLOR = 'vc', 'Vice Chancellor'
    CHANCELLOR = 'chancellor', 'Chancellor'
    
    # Support Staff
    SENIOR_STAFF = 'senior_staff', 'Senior Staff'
    JUNIOR_STAFF = 'junior_staff', 'Junior Staff'
    
    # ============================================================
    # AMERICAN ACADEMIC RANKS
    # ============================================================
    INSTRUCTOR = 'instructor', 'Instructor'
    ADJUNCT_PROF = 'adjunct_prof', 'Adjunct Professor'
    ASSISTANT_PROF = 'assistant_prof', 'Assistant Professor'
    ASSOCIATE_PROF = 'associate_prof', 'Associate Professor'
    FULL_PROF = 'full_prof', 'Professor'
    ENDOWED_CHAIR = 'endowed_chair', 'Endowed Chair'
    UNIVERSITY_PROF = 'university_prof', 'University Professor'
    
    # ============================================================
    # AMERICAN ADMINISTRATIVE RANKS
    # ============================================================
    DEPARTMENT_CHAIR = 'dept_chair', 'Department Chair'
    DIRECTOR = 'director', 'Director'
    DEAN_US = 'dean_us', 'Dean'
    PROVOST = 'provost', 'Provost'
    PRESIDENT = 'president', 'President'
    CHANCELLOR_US = 'chancellor_us', 'Chancellor'


class LeaveRequestStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    APPROVED = 'approved', 'Approved'
    REJECTED = 'rejected', 'Rejected'


class LeaveType(models.TextChoices):
    ANNUAL = 'annual', 'Annual Leave'
    SICK = 'sick', 'Sick Leave'
    CASUAL = 'casual', 'Casual Leave'
    STUDIES = 'studies', 'Study Leave'
    MATERNITY = 'maternity', 'Maternity Leave'
    PATERNITY = 'paternity', 'Paternity Leave'
    UNPAID = 'unpaid', 'Unpaid Leave'


class StaffProfile(models.Model):
    """Extended staff profile with complete HR data."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='staff_profile'
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    staff_id = models.CharField(max_length=20, unique=True, db_index=True)
    
    # Organization
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, related_name='staff'
    )
    faculty = models.ForeignKey(
        Faculty, on_delete=models.SET_NULL, null=True, related_name='staff'
    )
    
    # Employment details
    employment_date = models.DateField()
    confirmation_date = models.DateField(null=True, blank=True)
    rank = models.CharField(
        max_length=20, choices=StaffRank.choices,
        blank=True
    )
    grade = models.CharField(
        max_length=10, blank=True,
        help_text='GL10, GL12, etc.'
    )
    step = models.IntegerField(default=1)
    contract_type = models.CharField(
        max_length=20, default='permanent'
    )
    scheme_of_service = models.CharField(
        max_length=100, blank=True
    )
    
    # Contact
    phone = models.CharField(max_length=20, blank=True)
    alternative_phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    termination_date = models.DateField(null=True, blank=True)
    termination_reason = models.TextField(blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'staff_profiles'
        ordering = ['staff_id']
        indexes = [
            models.Index(fields=['staff_id']),
            models.Index(fields=['department', 'is_active']),
            models.Index(fields=['faculty', 'is_active']),
        ]

    def __str__(self):
        return f"{self.staff_id} - {self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.middle_name or ''} {self.last_name}".strip()
    
    @property
    def is_confirmed(self) -> bool:
        """Check if staff is confirmed."""
        return self.confirmation_date is not None
    
    @property
    def years_of_service(self) -> int:
        """Calculate years of service."""
        if not self.employment_date:
            return 0
        today = timezone.now().date()
        return (today - self.employment_date).days // 365


class LeaveRequest(models.Model):
    """Staff leave requests with full workflow support."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    staff = models.ForeignKey(
        StaffProfile, on_delete=models.CASCADE, related_name='leave_requests'
    )
    leave_type = models.CharField(max_length=20, choices=LeaveType.choices)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(
        max_length=20, choices=LeaveRequestStatus.choices,
        default=LeaveRequestStatus.PENDING
    )
    approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='approved_leaves'
    )
    approval_comment = models.TextField(blank=True)
    rejection_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'leave_requests'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['staff', 'status']),
            models.Index(fields=['start_date']),
        ]

    def __str__(self):
        return f"{self.staff} - {self.leave_type} ({self.start_date} to {self.end_date})"
    
    def duration_days(self) -> int:
        """Calculate leave duration in days."""
        return (self.end_date - self.start_date).days + 1
    
    def save(self, *args, **kwargs):
        # Validate date range
        if self.end_date < self.start_date:
            raise ValueError("End date must be after start date")
        super().save(*args, **kwargs)


class LeaveBalance(models.Model):
    """Staff leave balances by type and year."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    staff = models.ForeignKey(
        StaffProfile, on_delete=models.CASCADE, related_name='leave_balances'
    )
    leave_type = models.CharField(max_length=20, choices=LeaveType.choices)
    year = models.IntegerField(default=timezone.now().year)
    total_days = models.IntegerField(default=0)
    used_days = models.IntegerField(default=0)
    
    # Additional accrual
    accrued_days = models.IntegerField(default=0)
    carried_over_days = models.IntegerField(default=0)

    class Meta:
        db_table = 'leave_balances'
        unique_together = ['staff', 'leave_type', 'year']
        ordering = ['-year']

    def __str__(self):
        return f"{self.staff} - {self.leave_type} ({self.year})"
    
    @property
    def remaining_days(self) -> int:
        return self.total_days - self.used_days
    
    @property
    def available_days(self) -> int:
        return self.total_days - self.used_days


class PromotionRecord(models.Model):
    """Staff promotion records."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    staff = models.ForeignKey(
        StaffProfile, on_delete=models.CASCADE, related_name='promotions'
    )
    from_rank = models.CharField(max_length=100)
    to_rank = models.CharField(max_length=100)
    from_grade = models.CharField(max_length=10, blank=True)
    to_grade = models.CharField(max_length=10, blank=True)
    effective_date = models.DateField()
    approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'promotion_records'
        ordering = ['-effective_date']

    def __str__(self):
        return f"{self.staff} promoted to {self.to_rank}"


class StaffAppraisal(models.Model):
    """Staff appraisals."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    staff = models.ForeignKey(
        StaffProfile, on_delete=models.CASCADE, related_name='appraisals'
    )
    session = models.ForeignKey(
        'academic.AcademicSession', on_delete=models.CASCADE,
        related_name='staff_appraisals'
    )
    score = models.DecimalField(max_digits=3, decimal_places=2)
    comment = models.TextField(blank=True)
    reviewer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'staff_appraisals'
        unique_together = ['staff', 'session']

    def __str__(self):
        return f"{self.staff} - Score: {self.score}"


# Leave Accrual Configuration
class LeaveAccrualConfig(models.Model):
    """Configure leave accrual rates per leave type."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    leave_type = models.CharField(max_length=20, unique=True)
    annual_days = models.IntegerField(default=21)
    accrual_frequency = models.CharField(
        max_length=20, 
        choices=[
            ('monthly', 'Monthly'),
            ('quarterly', 'Quarterly'),
            ('yearly', 'Yearly'),
        ],
        default='monthly'
    )
    max_carry_over = models.IntegerField(default=5)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'leave_accrual_config'
    
    def __str__(self):
        return f"{self.leave_type}: {self.annual_days} days/{self.accrual_frequency}"
