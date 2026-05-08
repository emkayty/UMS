import uuid
from django.db import models
from apps.academic.models import Programme, AcademicSession


# ============================================================
# NIGERIAN UNIVERSITY FEE TYPES
# ============================================================

class FeeType(models.TextChoices):
    # ============================================================
    # NIGERIAN UNIVERSITY FEES
    # ============================================================
    
    # Core Fees
    TUITION = 'tuition', 'Tuition Fee'
    ACCEPTANCE = 'acceptance', 'Acceptance Fee'
    REGISTRATION = 'registration', 'Registration Fee'
    EXAMINATION = 'examination', 'Examination Fee'
    MATRICULATION = 'matriculation', 'Matriculation Fee'
    
    # Facility Fees
    LIBRARY = 'library', 'Library Fee'
    ICT = 'ict', 'ICT Fee'
    SPORTS = 'sports', 'Sports Fee'
    MEDICAL = 'medical', 'Medical Fee'
    DEVELOPMENT = 'development', 'Development Fee'
    HOSTEL = 'hostel', 'Hostel Fee'
    LABORATORY = 'laboratory', 'Laboratory Fee'
    
    # Additional Fees
    FIELD_TRIP = 'field_trip', 'Field Trip Fee'
    PROJECT = 'project', 'Project Fee'
    TRANSPORT = 'transport', 'Transport Fee'
    
    # Polytechnic Specific
    INDUSTRIAL_TRAINING = 'it', 'Industrial Training (SIWES)'
    ENTREPRENEURSHIP = 'ent', 'Entrepreneurship Fee'
    
    # Other
    OTHER = 'other', 'Other Fee'
    
    # ============================================================
    # AMERICAN UNIVERSITY FEE TYPES
    # ============================================================
    
    # Tuition (Semester-based)
    TUITION_RESIDENT = 'tuition_resident', 'In-State Tuition'
    TUITION_NON_RESIDENT = 'tuition_non_resident', 'Out-of-State Tuition'
    TUITION_INTL = 'tuition_intl', 'International Tuition'
    TUITION_PART_TIME = 'tuition_part', 'Part-Time Tuition'
    TUITION_EXTRA_CREDIT = 'tuition_credit', 'Per Credit Hour Fee'
    
    # Fees
    COMPREHENSIVE_FEE = 'comprehensive', 'Comprehensive Fee'
    FACILITY_FEE = 'facility', 'Facility Fee'
    TECHNOLOGY_FEE = 'technology', 'Technology Fee'
    HEALTH_FEE = 'health', 'Health Services Fee'
    RECREATION_FEE = 'recreation', 'Recreation Fee'
    STUDENT_ACTIVITY = 'student_activity', 'Student Activity Fee'
    PARKING_FEE = 'parking', 'Parking Fee'
    HOUSING_FEE = 'housing', 'Housing/Dorm Fee'
    MEAL_PLAN = 'meal', 'Meal Plan Fee'
    
    # Orientation & Training
    ORIENTATION = 'orientation', 'New Student Orientation'
    GRADUATION = 'graduation', 'Graduation Fee'
    
    # Books & Materials
    BOOKS = 'books', 'Bookstore Credit'
    DIGITAL_MATERIALS = 'digital', 'Digital Materials'


class FeeStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    PARTIAL = 'partial', 'Partial'
    PAID = 'paid', 'Paid'


class PaymentStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    SUCCESS = 'success', 'Success'
    FAILED = 'failed', 'Failed'


class FeeItem(models.Model):
    """Fee item - Nigerian university fee structure."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    fee_type = models.CharField(
        max_length=20, choices=FeeType.choices,
        default=FeeType.TUITION
    )
    amount = models.DecimalField(
        max_digits=12, decimal_places=2,
        help_text='Amount in Naira'
    )
    is_compulsory = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    programme = models.ForeignKey(
        Programme, on_delete=models.CASCADE, null=True, blank=True,
        related_name='fee_items'
    )
    session = models.ForeignKey(
        AcademicSession, on_delete=models.CASCADE, null=True, blank=True,
        related_name='fee_items'
    )
    level = models.IntegerField(
        null=True, blank=True,
        help_text='100-600 level'
    )
    semester = models.IntegerField(
        null=True, blank=True,
        help_text='1 or 2'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'fee_items'
        ordering = ['name']
        indexes = [
            models.Index(fields=['programme', 'session']),
            models.Index(fields=['level']),
        ]

    def __str__(self):
        return f"{self.name} - {self.amount}"


class StudentFee(models.Model):
    """Student fee records."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        'student.StudentProfile', on_delete=models.CASCADE,
        related_name='fees'
    )
    fee_item = models.ForeignKey(
        FeeItem, on_delete=models.CASCADE, related_name='student_fees'
    )
    amount_due = models.DecimalField(max_digits=12, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(
        max_length=20, choices=FeeStatus.choices,
        default=FeeStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'student_fees'
        indexes = [
            models.Index(fields=['student', 'status']),
            models.Index(fields=['fee_item']),
        ]
        unique_together = ['student', 'fee_item']

    def __str__(self):
        return f"{self.student} - {self.fee_item.name}"


class Payment(models.Model):
    """Payment records with idempotency support."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        'student.StudentProfile', on_delete=models.CASCADE,
        related_name='payments'
    )
    fee_item = models.ForeignKey(
        FeeItem, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='payments'
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_ref = models.CharField(max_length=50, unique=True)
    gateway = models.CharField(max_length=20)  # paystack, flutterwave
    status = models.CharField(
        max_length=20, choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )
    idempotency_key = models.CharField(
        max_length=100, unique=True, null=True, blank=True
    )
    paid_at = models.DateTimeField(null=True, blank=True)
    invoice_url = models.URLField(blank=True)
    transaction_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payments'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student} - {self.amount} ({self.status})"


class Scholarship(models.Model):
    """Student scholarships."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        'student.StudentProfile', on_delete=models.CASCADE,
        related_name='scholarships'
    )
    name = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    awarded_by = models.CharField(max_length=200)
    session = models.ForeignKey(
        AcademicSession, on_delete=models.CASCADE,
        related_name='scholarships'
    )
    status = models.CharField(max_length=20, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'scholarships'

    def __str__(self):
        return f"{self.student} - {self.name}"


class PayrollRecord(models.Model):
    """Staff payroll records."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    staff = models.ForeignKey(
        'staff.StaffProfile', on_delete=models.CASCADE,
        related_name='payroll_records'
    )
    month = models.CharField(max_length=7)  # YYYY-MM
    basic_salary = models.DecimalField(max_digits=12, decimal_places=2)
    allowances = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_pay = models.DecimalField(max_digits=12, decimal_places=2)
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payroll_records'
        unique_together = ['staff', 'month']

    def save(self, *args, **kwargs):
        self.net_pay = self.basic_salary + self.allowances - self.deductions
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.staff} - {self.month}"