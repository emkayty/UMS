"""
Biometric Data Management
Fingerprint, face recognition data
"""

import uuid
from django.db import models


class BiometricType(models.TextChoices):
    FINGERPRINT = 'fingerprint', 'Fingerprint'
    FACE = 'face', 'Face Recognition'
    IRIS = 'iris', 'Iris Scan'
    PALM = 'palm', 'Palm Vein'


class BiometricStatus(models.TextChoices):
    ENROLLED = 'enrolled', 'Enrolled'
    VERIFIED = 'verified', 'Verified'
    FAILED = 'failed', 'Failed'
    PENDING = 'pending', 'Pending'


# ============================================================
# BIOMETRIC TEMPLATE
# ============================================================

class Biometric(models.Model):
    """Biometric data template."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey(
        'student.StudentProfile', on_delete=models.CASCADE,
        null=True, blank=True, related_name='biometrics'
    )
    staff = models.ForeignKey(
        'staff.StaffProfile', on_delete=models.CASCADE,
        null=True, blank=True, related_name='biometrics'
    )
    
    biometric_type = models.CharField(
        max_length=20, choices=BiometricType.choices
    )
    
    # Template data (encrypted)
    template_data = models.TextField()
    template_hash = models.CharField(max_length=64, unique=True)
    
    # Status
    status = models.CharField(
        max_length=20, choices=BiometricStatus.choices,
        default=BiometricStatus.ENROLLED
    )
    
    enrolled_at = models.DateTimeField(auto_now_add=True)
    last_verified = models.DateTimeField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'biometrics'
        unique_together = ['student', 'staff', 'biometric_type']

    def __str__(self):
        person = self.student or self.staff
        return f"{person} - {self.biometric_type}"


# ============================================================
# BIOMETRIC VERIFICATION LOG
# ============================================================

class BiometricLog(models.Model):
    """Biometric verification log."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    biometric = models.ForeignKey(
        Biometric, on_delete=models.CASCADE,
        related_name='logs'
    )
    
    # Verification
    is_successful = models.BooleanField()
    confidence = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    
    # Location
    location = models.CharField(max_length=100, blank=True)
    device_id = models.CharField(max_length=50, blank=True)
    
    # Time
    verified_at = models.DateTimeField(auto_now_add=True)
    
    # Notes
    error_message = models.TextField(blank=True)

    class Meta:
        db_table = 'biometric_logs'
        ordering = ['-verified_at']

    def __str__(self):
        return f"{self.biometric} - {self.verified_at}"


# ============================================================
# ATTENDANCE DEVICE
# ============================================================

class AttendanceDevice(models.Model):
    """Biometric attendance device."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=100)
    device_id = models.CharField(max_length=50, unique=True)
    device_type = models.CharField(max_length=50)
    
    # Location
    location = models.CharField(max_length=200)
    department = models.ForeignKey(
        'academic.Department', on_delete=models.SET_NULL,
        null=True, blank=True
    )
    
    # Settings
    is_active = models.BooleanField(default=True)
    auto_sync = models.BooleanField(default=True)
    
    # Network
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    port = models.IntegerField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'attendance_devices'

    def __str__(self):
        return f"{self.name} - {self.device_id}"