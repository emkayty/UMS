"""
ID Card Management System
Student and staff ID cards
"""

import uuid
from django.db import models


class IDCardStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    APPROVED = 'approved', 'Approved'
    PRINTED = 'printed', 'Printed'
    ISSUED = 'issued', 'Issued'
    EXPIRED = 'expired', 'Expired'
    LOST = 'lost', 'Lost'


# ============================================================
# ID CARD TYPE
# ============================================================

class CardType(models.TextChoices):
    STUDENT = 'student', 'Student ID'
    STAFF = 'staff', 'Staff ID'
    VISITOR = 'visitor', 'Visitor Pass'
    TEMPORARY = 'temporary', 'Temporary Pass'


# ============================================================
# ID CARD
# ============================================================

class IDCard(models.Model):
    """ID Card record."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Person
    student = models.ForeignKey(
        'student.StudentProfile', on_delete=models.CASCADE,
        null=True, blank=True, related_name='id_cards'
    )
    staff = models.ForeignKey(
        'staff.StaffProfile', on_delete=models.CASCADE,
        null=True, blank=True, related_name='id_cards'
    )
    
    card_type = models.CharField(max_length=20, choices=CardType.choices)
    
    # Card details
    card_number = models.CharField(max_length=20, unique=True)
    barcode = models.CharField(max_length=50, unique=True)
    qr_code = models.CharField(max_length=100, unique=True)
    
    # Photo
    photo = models.URLField(blank=True)
    
    # Status
    status = models.CharField(
        max_length=20, choices=IDCardStatus.choices,
        default=IDCardStatus.PENDING
    )
    
    # Expiry
    issued_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField()
    is_permanent = models.BooleanField(default=True)
    
    # Issue
    issued_by = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL,
        null=True, blank=True
    )
    issued_at = models.DateTimeField(null=True, blank=True)
    
    # Print
    printed_by = models.CharField(max_length=100, blank=True)
    printed_at = models.DateTimeField(null=True, blank=True)
    
    # Notes
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'id_cards'

    def __str__(self):
        return f"{self.card_number} - {self.card_type}"


# ============================================================
# ID CARD REQUEST
# ============================================================

class IDCardRequest(models.Model):
    """ID card request (replacement, new)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    card = models.ForeignKey(
        IDCard, on_delete=models.CASCADE,
        null=True, blank=True
    )
    
    student = models.ForeignKey(
        'student.StudentProfile', on_delete=models.CASCADE,
        null=True, blank=True
    )
    staff = models.ForeignKey(
        'staff.StaffProfile', on_delete=models.CASCADE,
        null=True, blank=True
    )
    
    request_type = models.CharField(
        max_length=20,
        choices=[
            ('new', 'New Card'),
            ('replacement', 'Replacement'),
            ('update', 'Information Update'),
        ]
    )
    
    reason = models.TextField(blank=True)
    photo = models.URLField(blank=True)
    
    status = models.CharField(
        max_length=20, default='pending',
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ]
    )
    
    fee = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )
    fee_paid = models.BooleanField(default=False)
    
    processed_by = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL,
        null=True, blank=True
    )
    processed_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'id_card_requests'

    def __str__(self):
        return f"{self.request_type} - {self.card.card_number}"