"""
Payment Integration
Paystack, Flutterwave, and bank transfers
"""

import uuid
from django.db import models
from apps.accounts.models import User


class PaymentGateway(models.TextChoices):
    PAYSTACK = 'paystack', 'Paystack'
    FLUTTERWAVE = 'flutterwave', 'Flutterwave'
    BANK_TRANSFER = 'bank_transfer', 'Bank Transfer'
    POS = 'pos', 'POS Terminal'


class PaymentStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    INITIATED = 'initiated', 'Initiated'
    PROCESSING = 'processing', 'Processing'
    SUCCESS = 'success', 'Success'
    FAILED = 'failed', 'Failed'
    REFUNDED = 'refunded', 'Refunded'


class PaymentType(models.TextChoices):
    SCHOOL_FEE = 'school_fee', 'School Fee'
    ACCEPTANCE = 'acceptance', 'Acceptance Fee'
    HOSTEL = 'hostel', 'Hostel Fee'
    TRANSCRIPT = 'transcript', 'Transcript Fee'
    CONVOCATION = 'convocation', 'Convocation Fee'
    SIWES = 'siwes', 'SIWES Fee'
    OTHER = 'other', 'Other Fee'


# ============================================================
# PAYMENT GATEWAY CONFIG
# ============================================================

class PaymentGatewayConfig(models.Model):
    """Payment gateway configuration."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    gateway = models.CharField(max_length=20, choices=PaymentGateway.choices)
    
    # Keys
    public_key = models.CharField(max_length=200, blank=True)
    secret_key = models.CharField(max_length=200, blank=True)
    merchant_email = models.EmailField(blank=True)
    
    # URLs
    webhook_url = models.URLField(blank=True)
    callback_url = models.URLField(blank=True)
    
    # Status
    is_active = models.BooleanField(default=False)
    is_test_mode = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payment_gateway_configs'

    def __str__(self):
        return f"{self.get_gateway_display()} - {'Active' if self.is_active else 'Inactive'}"


# ============================================================
# PAYMENT TRANSACTION
# ============================================================

class PaymentTransaction(models.Model):
    """Payment transaction record."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # User
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='payment_transactions'
    )
    
    # Amount
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_type = models.CharField(max_length=20, choices=PaymentType.choices)
    
    # Gateway
    gateway = models.CharField(max_length=20, choices=PaymentGateway.choices)
    gateway_ref = models.CharField(max_length=100, blank=True)
    
    # Status
    status = models.CharField(
        max_length=20, choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )
    
    # Reference
    transaction_ref = models.CharField(max_length=50, unique=True)
    invoice_number = models.CharField(max_length=50, unique=True)
    
    # Channel
    channel = models.CharField(max_length=20, blank=True)
    currency = models.CharField(max_length=10, default='NGN')
    
    # Dates
    initiated_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    failed_at = models.DateTimeField(null=True, blank=True)
    
    # Response
    gateway_response = models.JSONField(default=dict)
    
    # Related
    related_id = models.UUIDField(null=True, blank=True)
    related_model = models.CharField(max_length=50, blank=True)
    
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'payment_transactions'
        ordering = ['-initiated_at']

    def __str__(self):
        return f"{self.transaction_ref} - ₦{self.amount}"


# ============================================================
# INVOICE
# ============================================================

class Invoice(models.Model):
    """Student invoice."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey(
        'student.StudentProfile', on_delete=models.CASCADE,
        related_name='invoices'
    )
    
    invoice_number = models.CharField(max_length=50, unique=True)
    session = models.ForeignKey(
        'academic.AcademicSession', on_delete=models.CASCADE
    )
    
    # Items
    items = models.JSONField(default=list)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Status
    status = models.CharField(
        max_length=20, default='pending',
        choices=[
            ('pending', 'Pending'),
            ('partial', 'Partially Paid'),
            ('paid', 'Fully Paid'),
            ('overpaid', 'Over Paid'),
        ]
    )
    
    # Due
    due_date = models.DateField()
    is_overdue = models.BooleanField(default=False)
    
    # Payment
    amount_paid = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )
    balance = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'invoices'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.invoice_number} - ₦{self.total}"


# ============================================================
# REFUND
# ============================================================

class Refund(models.Model):
    """Payment refund request."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    transaction = models.ForeignKey(
        PaymentTransaction, on_delete=models.CASCADE,
        related_name='refunds'
    )
    
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reason = models.TextField()
    
    status = models.CharField(
        max_length=20, default='pending',
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('processed', 'Processed'),
            ('rejected', 'Rejected'),
        ]
    )
    
    requested_by = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, related_name='refund_requests'
    )
    requested_at = models.DateTimeField(auto_now_add=True)
    
    approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    
    processed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='processed_refunds'
    )
    processed_at = models.DateTimeField(null=True, blank=True)
    
    rejection_reason = models.TextField(blank=True)

    class Meta:
        db_table = 'refunds'

    def __str__(self):
        return f"Refund - {self.amount}"


# ============================================================
# BANK ACCOUNT
# ============================================================

class BankAccount(models.Model):
    """Institution bank accounts."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=20)
    account_name = models.CharField(max_length=200)
    
    account_type = models.CharField(
        max_length=10, default='current',
        choices=[
            ('current', 'Current'),
            ('savings', 'Savings'),
        ]
    )
    
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'bank_accounts'

    def __str__(self):
        return f"{self.bank_name} - {self.account_number}"


# ============================================================
# MANUAL PAYMENT VERIFICATION
# ============================================================

class ManualPayment(models.Model):
    """Manual bank transfer verification."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey(
        'student.StudentProfile', on_delete=models.CASCADE,
        related_name='manual_payments'
    )
    
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    bank_account = models.ForeignKey(
        BankAccount, on_delete=models.CASCADE
    )
    
    # Transfer details
    sender_name = models.CharField(max_length=200)
    sender_account = models.CharField(max_length=20)
    sender_bank = models.CharField(max_length=100)
    transfer_date = models.DateField()
    utr = models.CharField(max_length=20, blank=True, help_text='Unique Transaction Reference')
    
    # Status
    status = models.CharField(
        max_length=20, default='pending',
        choices=[
            ('pending', 'Pending'),
            ('verified', 'Verified'),
            ('rejected', 'Rejected'),
        ]
    )
    
    proof = models.FileField(upload_to='payments/proof/', null=True, blank=True)
    
    verified_by = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'manual_payments'

    def __str__(self):
        return f"{self.sender_name} - ₦{self.amount}"