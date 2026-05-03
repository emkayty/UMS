"""
Parent/Guardian Management
Family information
"""

import uuid
from django.db import models


class RelationType(models.TextChoices):
    FATHER = 'father', 'Father'
    MOTHER = 'mother', 'Mother'
    GUARDIAN = 'guardian', 'Guardian'
    SPOUSE = 'spouse', 'Spouse'
    SIBLING = 'sibling', 'Sibling'


# ============================================================
# PARENT/GUARDIAN
# ============================================================

class Guardian(models.Model):
    """Parent/guardian information."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey(
        'student.StudentProfile', on_delete=models.CASCADE,
        related_name='guardians'
    )
    
    # Information
    relation = models.CharField(max_length=15, choices=RelationType.choices)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    # Contact
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20)
    alt_phone = models.CharField(max_length=20, blank=True)
    
    # Address
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default='Nigeria')
    
    # Employment
    occupation = models.CharField(max_length=100, blank=True)
    employer = models.CharField(max_length=200, blank=True)
    employer_address = models.TextField(blank=True)
    
    # Is emergency contact
    is_emergency_contact = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'guardians'

    def __str__(self):
        return f"{self.relation} - {self.first_name} {self.last_name}"


# ============================================================
# NEXT OF KIN
# ============================================================

class NextOfKin(models.Model):
    """Next of kin information."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey(
        'student.StudentProfile', on_delete=models.CASCADE,
        related_name='next_of_kin'
    )
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    relation = models.CharField(max_length=50)
    
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField()
    
    is_emergency = models.BooleanField(default=True)

    class Meta:
        db_table = 'next_of_kin'

    def __str__(self):
        return f"{self.student.matric_number} - {self.relation}"