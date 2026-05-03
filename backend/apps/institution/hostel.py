"""
Hostel Management Models
Nigerian university hostel/accommodation management
"""

import uuid
from django.db import models
from apps.accounts.models import User


# ============================================================
# HOSTEL TYPES
# ============================================================

class HostelType(models.TextChoices):
    MALE = 'male', 'Male Hostel'
    FEMALE = 'female', 'Female Hostel'
    MIXED = 'mixed', 'Mixed Hostel'
    
    # American style
    DORMITORY = 'dormitory', 'Dormitory (US)'
    APARTMENT = 'apartment', 'Apartment Style'
    SUITE = 'suite', 'Suite Style'


class RoomType(models.TextChoices):
    SINGLE = 'single', 'Single Room'
    DOUBLE = 'double', 'Double Room'
    TRIPLE = 'triple', 'Triple Room'
    QUAD = 'quad', 'Quad (4 sharing)'
    DORMITORY = 'dormitory', 'Dormitory (6-8 sharing)'


class BedStatus(models.TextChoices):
    AVAILABLE = 'available', 'Available'
    OCCUPIED = 'occupied', 'Occupied'
    RESERVED = 'reserved', 'Reserved'
    MAINTENANCE = 'maintenance', 'Maintenance'


class HostelAllocationStatus(models.TextChoices):
    PENDING = 'pending', 'Pending Application'
    APPROVED = 'approved', 'Approved'
    REJECTED = 'rejected', 'Rejected'
    ALLOCATED = 'allocated', 'Allocated'
    CHECKED_IN = 'checked_in', 'Checked In'
    CHECKED_OUT = 'checked_out', 'Checked Out'


# ============================================================
# HOSTEL BUILDING
# ============================================================

class Hostel(models.Model):
    """Hostel building - Nigerian: Male 1, Female 1, New Hostel"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    hostel_type = models.CharField(max_length=15, choices=HostelType.choices)
    
    # Capacity
    total_rooms = models.IntegerField(default=0)
    total_beds = models.IntegerField(default=0)
    available_beds = models.IntegerField(default=0)
    
    # Management
    warden = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='warden_of'
    )
    caretaker = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hostels'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"


# ============================================================
# FLOOR
# ============================================================

class Floor(models.Model):
    """Floor within a hostel."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hostel = models.ForeignKey(
        Hostel, on_delete=models.CASCADE, related_name='floors'
    )
    floor_number = models.IntegerField()
    floor_name = models.CharField(max_length=50, blank=True)
    total_rooms = models.IntegerField(default=0)
    total_beds = models.IntegerField(default=0)

    class Meta:
        db_table = 'hostel_floors'
        unique_together = ['hostel', 'floor_number']

    def __str__(self):
        return f"{self.hostel.code} - Floor {self.floor_number}"


# ============================================================
# ROOM
# ============================================================

class Room(models.Model):
    """Room in a hostel."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    floor = models.ForeignKey(
        Floor, on_delete=models.CASCADE, related_name='rooms'
    )
    room_number = models.CharField(max_length=20)
    room_type = models.CharField(max_length=15, choices=RoomType.choices)
    capacity = models.IntegerField(default=2)
    current_occupancy = models.IntegerField(default=0)
    
    # Fee
    amount = models.DecimalField(
        max_digits=12, decimal_places=2,
        help_text='Hostel fee per session (Naira)'
    )
    
    # Amenities
    has_bathroom = models.BooleanField(default=False)
    has_air_conditioner = models.BooleanField(default=False)
    has_fridge = models.BooleanField(default=False)
    
    # Status
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'hostel_rooms'
        unique_together = ['floor', 'room_number']

    def __str__(self):
        return f"{self.floor.hostel.code}-{self.room_number}"


# ============================================================
# BED
# ============================================================

class Bed(models.Model):
    """Individual bed in a room."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name='beds'
    )
    bed_number = models.CharField(max_length=10)
    status = models.CharField(
        max_length=15, choices=BedStatus.choices,
        default=BedStatus.AVAILABLE
    )

    class Meta:
        db_table = 'hostel_beds'
        unique_together = ['room', 'bed_number']

    def __str__(self):
        return f"{self.room.room_number}-{self.bed_number}"


# ============================================================
# HOSTEL APPLICATION
# ============================================================

class HostelApplication(models.Model):
    """Student hostel application."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Student & Session
    student = models.ForeignKey(
        'student.StudentProfile', on_delete=models.CASCADE,
        related_name='hostel_applications'
    )
    session = models.ForeignKey(
        'academic.AcademicSession', on_delete=models.CASCADE
    )
    
    # Preferences
    preferred_hostel = models.ForeignKey(
        Hostel, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='applications'
    )
    preferred_room_type = models.CharField(
        max_length=15, choices=RoomType.choices,
        blank=True
    )
    
    # Allocation (assigned)
    allocated_hostel = models.ForeignKey(
        Hostel, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='allocations'
    )
    allocated_room = models.ForeignKey(
        Room, on_delete=models.SET_NULL, null=True, blank=True
    )
    allocated_bed = models.ForeignKey(
        Bed, on_delete=models.SET_NULL, null=True, blank=True
    )
    
    # Status
    status = models.CharField(
        max_length=20, choices=HostelAllocationStatus.choices,
        default=HostelAllocationStatus.PENDING
    )
    
    # Notes
    notes = models.TextField(blank=True)
    rejection_reason = models.TextField(blank=True)
    
    # Dates
    applied_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'hostel_applications'
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.student.matric_number} - {self.session.name}"


# ============================================================
# ACTIVE ALLOCATION
# ============================================================

class HostelAllotment(models.Model):
    """Current hostel allocation."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey(
        'student.StudentProfile', on_delete=models.CASCADE,
        related_name='hostel_allotments'
    )
    session = models.ForeignKey(
        'academic.AcademicSession', on_delete=models.CASCADE
    )
    hostel = models.ForeignKey(
        Hostel, on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE
    )
    bed = models.ForeignKey(
        Bed, on_delete=models.CASCADE
    )
    
    # Check-in/out
    check_in_date = models.DateField()
    check_out_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    # Damage report
    damage_report = models.TextField(blank=True)
    damage_cost = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )

    class Meta:
        db_table = 'hostel_allotments'
        ordering = ['-check_in_date']

    def __str__(self):
        return f"{self.student.matric_number} - {self.hostel.code}"


# ============================================================
# HOSTEL FEE
# ============================================================

class HostelFee(models.Model):
    """Hostel fee per session."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    session = models.ForeignKey(
        'academic.AcademicSession', on_delete=models.CASCADE,
        related_name='hostel_fees'
    )
    programme = models.ForeignKey(
        'academic.Programme', on_delete=models.CASCADE,
        null=True, blank=True
    )
    room_type = models.CharField(max_length=15, choices=RoomType.choices)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'hostel_fees'
        unique_together = ['session', 'programme', 'room_type']

    def __str__(self):
        return f"{self.session.name} - {self.room_type} - ₦{self.amount}"