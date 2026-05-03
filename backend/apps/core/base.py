"""
Base Classes for UMS
Standardized, Modular, Professional Foundation
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db.models import Manager
import uuid


# ============================================================
# BASE MANAGERS
# ============================================================

class BaseManager(Manager):
    """Base manager with common query methods."""
    
    def get_active(self):
        return self.filter(is_active=True)
    
    def get_public(self):
        return self.filter(is_public=True)
    
    def recent(self, limit=10):
        return self.order_by('-created_at')[:limit]


class UUIDManager(Manager):
    """Manager for UUID-based models."""
    
    def get_by_uuid(self, uuid_str):
        return self.get(uuid=uuid_str)
    
    def exists_by_uuid(self, uuid_str):
        return self.filter(uuid=uuid_str).exists()


class SoftDeleteManager(Manager):
    """Manager that excludes soft-deleted objects."""
    
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)
    
    def all_with_deleted(self):
        return super().get_queryset()
    
    def deleted_only(self):
        return super().get_queryset().filter(is_deleted=True)


# ============================================================
# BASE MODELS
# ============================================================

class UUIDModel(models.Model):
    """Abstract base model with UUID primary key."""
    
    class Meta:
        abstract = True
    
    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )


class TimestampModel(models.Model):
    """Abstract base model with timestamp fields."""
    
    class Meta:
        abstract = True
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at')
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated at')
    )


class SoftDeleteModel(models.Model):
    """Abstract base model with soft delete."""
    
    class Meta:
        abstract = True
    
    is_deleted = models.BooleanField(
        default=False,
        verbose_name=_('Deleted')
    )
    
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Deleted at')
    )
    
    objects = SoftDeleteManager()
    
    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
    
    def hard_delete(self):
        super().delete()
    
    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save()


class StatusModel(models.Model):
    """Abstract base model with status field."""
    
    class Status(models.TextChoices):
        DRAFT = 'draft', _('Draft')
        PENDING = 'pending', _('Pending')
        ACTIVE = 'active', _('Active')
        INACTIVE = 'inactive', _('Inactive')
        ARCHIVED = 'archived', _('Archived')
        APPROVED = 'approved', _('Approved')
        REJECTED = 'rejected', _('Rejected')
    
    class Meta:
        abstract = True
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name=_('Status')
    )
    
    def is_active(self):
        return self.status == self.Status.ACTIVE
    
    def is_pending(self):
        return self.status == self.Status.PENDING
    
    def is_archived(self):
        return self.status == self.Status.ARCHIVED


class BaseModel(UUIDModel, TimestampModel):
    """Combined base model with UUID and timestamps."""
    
    class Meta:
        abstract = True
    
    objects = BaseManager()
    
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Active')
    )
    
    is_public = models.BooleanField(
        default=False,
        verbose_name=_('Public')
    )
    
    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_created',
        verbose_name=_('Created by')
    )
    
    updated_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_updated',
        verbose_name=_('Updated by')
    )
    
    def clean(self):
        if hasattr(self, 'created_by') and not self.created_by_id:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            try:
                self.created_by = User.objects.get(is_superuser=True)
            except User.DoesNotExist:
                pass
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class BaseModelWithStatus(BaseModel, StatusModel):
    """Base model with status."""
    
    class Meta:
        abstract = True


# ============================================================
# VALIDATORS
# ============================================================

def validate_nigerian_phone(value):
    """Validate Nigerian phone number."""
    import re
    pattern = r'^(\+234|0)[789]\d{9}$'
    if not re.match(pattern, value):
        raise ValidationError(
            _('Enter a valid Nigerian phone number.'),
            code='invalid_phone'
        )


def validate_nigerian_states(value):
    """Validate Nigerian state."""
    from .constants import NIGERIAN_STATES
    if value not in NIGERIAN_STATES:
        raise ValidationError(
            _('Enter a valid Nigerian state.'),
            code='invalid_state'
        )


def validate_year(value):
    """Validate year."""
    current_year = timezone.now().year
    if not (1900 <= value <= current_year + 1):
        raise ValidationError(
            _('Enter a valid year.'),
            code='invalid_year'
        )


def validate_age(min_age=18, max_age=100):
    """Validate age."""
    def validator(value):
        age = timezone.now().year - value
        if not (min_age <= age <= max_age):
            raise ValidationError(
                _('Age must be between %(min)s and %(max)s.'),
                code='invalid_age',
                params={'min': min_age, 'max': max_age}
            )
    return validator


# ============================================================
# CONSTANTS
# ============================================================

NIGERIAN_STATES = [
    'Abia', 'Adamawa', 'Akwa Ibom', 'Anambra', 'Bauchi',
    'Bayelsa', 'Benue', 'Borno', 'Cross River', 'Delta',
    'Ebonyi', 'Edo', 'Ekiti', 'Enugu', 'Gombe',
    'Imo', 'Jigawa', 'Kaduna', 'Kano', 'Katsina',
    'Kebbi', 'Kogi', 'Kwara', 'Lagos', 'Nasarawa',
    'Niger', 'Ogun', 'Ondo', 'Osun', 'Oyo',
    'Plateau', 'Rivers', 'Sokoto', 'Taraba', 'Yobe',
    'Zamfara', 'FCT'
]

GRADING_SCALES = [
    ('british_nigerian', 'British/Nigerian (A=70-100, 5.0)'),
    ('american', 'American (A=90-100, 4.0)'),
    ('standard', 'Standard (A=80-100, 4.0)'),
]

PAYMENT_STATUS = [
    ('pending', 'Pending'),
    ('completed', 'Completed'),
    ('failed', 'Failed'),
    ('refunded', 'Refunded'),
]

ATTENDANCE_STATUS = [
    ('present', 'Present'),
    ('absent', 'Absent'),
    ('late', 'Late'),
    ('excused', 'Excused'),
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def generate_enrollment_number():
    """Generate unique enrollment number."""
    import random
    year = timezone.now().year
    random_part = random.randint(1000, 9999)
    return f'ENR{year}{random_part}'


def generate_staff_id():
    """Generate unique staff ID."""
    import random
    year = timezone.now().year
    random_part = random.randint(1000, 9999)
    return f'STF{year}{random_part}'


def generate_invoice_number():
    """Generate unique invoice number."""
    import random
    year = timezone.now().year
    random_part = random.randint(10000, 99999)
    return f'INV{year}{random_part}'


def format_currency(amount, currency='NGN'):
    """Format currency amount."""
    if currency == 'NGN':
        return f'₦{amount:,.2f}'
    return f'{currency} {amount:,.2f}'


def calculate_gpa(grades):
    """Calculate GPA from grades."""
    if not grades:
        return 0.0
    
    grade_points = {'A': 5.0, 'B': 4.0, 'C': 3.0, 'D': 2.0, 'F': 0.0}
    
    total = sum(grade_points.get(g.upper(), 0) for g in grades)
    return round(total / len(grades), 2)


def get_quarter(date):
    """Get fiscal quarter from date."""
    month = date.month
    if month <= 3:
        return 1
    elif month <= 6:
        return 2
    elif month <= 9:
        return 3
    return 4


def get_academic_year(date=None):
    """Get academic year from date."""
    if date is None:
        date = timezone.now()
    
    year = date.year
    if date.month >= 9:
        return f'{year}/{year + 1}'
    return f'{year - 1}/{year}'


# ============================================================
# DECORATORS
# ============================================================

def require_status(*statuses):
    """Decorator to require specific status."""
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            obj = kwargs.get('obj')
            if obj and obj.status not in statuses:
                from django.http import Http404
                raise Http404()
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def audit_log(action):
    """Decorator to audit log actions."""
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            response = view_func(request, *args, **kwargs)
            if request.user.is_authenticated:
                from .audit import AuditLogger
                AuditLogger.log(action, request.user, request)
            return response
        return wrapper
    return decorator