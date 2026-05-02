"""
MANAGERS - Standardized Django Model Managers
Provides reusable querysets with common filters
"""

from django.db import models
from django.utils import timezone


class ActiveManager(models.Manager):
    """Manager for active records only."""
    
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class CurrentSessionManager(models.Manager):
    """Manager for current academic session."""
    
    def get_queryset(self):
        return super().get_queryset().filter(is_current=True)


class ApprovedManager(models.Manager):
    """Manager for approved records."""
    
    def get_queryset(self):
        return super().get_queryset().filter(approved=True)


class PublishedManager(models.Manager):
    """Manager for published records."""
    
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


class DateRangeManager(models.Manager):
    """Manager with date range queries."""
    
    def for_date(self, date):
        return self.filter(start_date__lte=date, end_date__gte=date)
    
    def active_today(self):
        today = timezone.now().date()
        return self.filter(start_date__lte=today, end_date__gte=today)


class StudentLevelManager(models.Manager):
    """Manager for student level filtering."""
    
    def by_level(self, level):
        return self.filter(current_level=level)
    
    def levels(self):
        return self.values_list('current_level', flat=True).distinct()


class FeeBalanceManager(models.Manager):
    """Manager for fee balance queries."""
    
    def outstanding(self):
        return self.filter(balance__gt=0)
    
    def defaulters(self):
        from . import Invoice
        threshold = 50000
        return self.annotate(
            total=Sum('invoices__amount')
        ).filter(total__gt=threshold)


class AttendanceManager(models.Manager):
    """Manager for attendance queries."""
    
    def present_today(self):
        return self.filter(status='present', date=timezone.now().date())
    
    def absent_today(self):
        return self.filter(status='absent', date=timezone.now().date())
    
    def by_course(self, course):
        return self.filter(course=course)


class ResultManager(models.Manager):
    """Manager for result queries."""
    
    def approved(self):
        return self.filter(approved=True)
    
    def pending(self):
        return self.filter(approved=False)
    
    def by_session(self, session):
        return self.filter(session=session)
    
    def by_student(self, student):
        return self.filter(student=student)


# ============================================================
# ABSTRACT MODELS - Reusable base classes
# ============================================================

class AbstractBaseModel(models.Model):
    """Abstract base with common fields."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class AbstractActiveModel(AbstractBaseModel):
    """Abstract with is_active flag."""
    
    is_active = models.BooleanField(default=True)
    
    objects = models.Manager()
    active = ActiveManager()
    
    class Meta:
        abstract = True


class AbstractTimestampModel(AbstractBaseModel):
    """Abstract with timestamp fields."""
    
    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='+'
    )
    
    class Meta:
        abstract = True


class AbstractApprovalModel(AbstractBaseModel):
    """Abstract with approval workflow."""
    
    STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    
    approved_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='+'
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    
    objects = models.Manager()
    approved = ApprovedManager()
    
    class Meta:
        abstract = True
    
    def approve(self, user):
        self.status = 'approved'
        self.approved_by = user
        self.approved_at = timezone.now()
        self.save()
    
    def reject(self, user):
        self.status = 'rejected'
        self.approved_by = user
        self.approved_at = timezone.now()
        self.save()


class AbstractPaymentModel(AbstractBaseModel):
    """Abstract with payment status."""
    
    STATUS = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    
    gateway = models.CharField(max_length=20, blank=True)
    gateway_ref = models.CharField(max_length=100, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        abstract = True
    
    def mark_paid(self, gateway_ref):
        self.status = 'success'
        self.gateway_ref = gateway_ref
        self.paid_at = timezone.now()
        self.save()


# ============================================================
# ENUM HELPERS
# ============================================================

class ChoiceMixin:
    """Mixin for choice field helpers."""
    
    @classmethod
    def choices(cls):
        return [(c.value, c.label) for c in cls.choices]
    
    @classmethod
    def values(cls):
        return [c.value for c in cls.choices]


# ============================================================
# VALIDATION HELPERS
# ============================================================

class ValidationMixin:
    """Mixin for model validation."""
    
    def clean(self):
        from django.core.exceptions import ValidationError
        
        errors = {}
        
        # Add custom validation logic in subclasses
        if hasattr(self, 'validate_custom'):
            errors.update(self.validate_custom())
        
        if errors:
            raise ValidationError(errors)
    
    def validate_unique(self, exclude=None):
        from django.core.exceptions import ValidationError
        
        errors = {}
        
        if hasattr(self, 'validate_custom_unique'):
            errors.update(self.validate_custom_unique())
        
        if errors:
            raise ValidationError(errors)


# ============================================================
# PERMISSION HELPERS
# ============================================================

class PermissionMixin:
    """Mixin for permission checks."""
    
    def can_edit(self, user):
        if user.is_superuser:
            return True
        if hasattr(self, 'created_by') and self.created_by == user:
            return True
        return False
    
    def can_delete(self, user):
        if user.is_superuser:
            return True
        return False
    
    def can_approve(self, user):
        if user.is_superuser:
            return True
        if hasattr(self, 'approved_by'):
            return self.approved_by is None
        return False


# ============================================================
# NOTIFICATION HELPERS
# ============================================================

class NotificationMixin:
    """Mixin for notification triggers."""
    
    def notify_created(self):
        # Override in subclass
        pass
    
    def notify_approved(self):
        # Override in subclass
        pass
    
    def notify_rejected(self):
        # Override in subclass
        pass
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
            self.notify_created()


# ============================================================
# SLUG HELPERS
# ============================================================

class SlugMixin(models.Model):
    """Mixin that auto-generates slugs."""
    
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        if not self.slug and hasattr(self, 'name'):
            from django.utils.text import slugify
            self.slug = slugify(self.name)
            
            # Ensure uniqueness
            if type(self).objects.filter(slug=self.slug).exists():
                self.slug = f"{self.slug}-{self.pk}"
        
        super().save(*args, **kwargs)


# ============================================================
# AUDIT HELPERS
# ============================================================

class AuditMixin(models.Model):
    """Mixin for audit trail."""
    
    changes = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        abstract = True
    
    def log_change(self, field, old_value, new_value):
        self.changes = {
            **self.changes,
            field: {
                'old': str(old_value),
                'new': str(new_value),
                'at': str(timezone.now())
            }
        }
        self.save()


# ============================================================
# IMPORT/EXPORT HELPERS
# ============================================================

class ImportExportMixin:
    """Mixin for CSV import/export."""
    
    @classmethod
    def from_csv_row(cls, row):
        """Create instance from CSV row."""
        raise NotImplementedError
    
    def to_csv_row(self):
        """Convert instance to CSV row."""
        raise NotImplementedError
    
    @classmethod
    def import_from_file(cls, file):
        """Import from CSV file."""
        import csv
        reader = csv.DictReader(file)
        return [cls.from_csv_row(row) for row in reader]
    
    def export_to_file(self, file):
        """Export to CSV file."""
        import csv
        writer = csv.DictWriter(file, fieldnames=self.csv_fields)
        writer.writeheader()
        for obj in self.__class__.objects.all():
            writer.writerow(obj.to_csv_row())


# ============================================================
# UUID STANDARDIZATION
# ============================================================

def generate_uuid():
    """Generate standardized UUID."""
    return uuid.uuid4()


def get_pk(model_class, pk):
    """Get object by UUID or raise 404."""
    from django.shortcuts import get_object_or_404
    return get_object_or_404(model_class, pk=pk)


# ============================================================
# DATABASE OPTIMIZATION
# ============================================================

class SelectRelatedMixin:
    """Standard select_related for queries."""
    
    @classmethod
    def select_related_fields(cls):
        return []
    
    def get_queryset(self):
        qs = super().get_queryset()
        if hasattr(cls, 'select_related_fields'):
            return qs.select_related(*cls.select_related_fields())
        return qs


class PrefetchRelatedMixin:
    """Standard prefetch_related for queries."""
    
    @classmethod
    def prefetch_related_fields(cls):
        return []
    
    def get_queryset(self):
        qs = super().get_queryset()
        if hasattr(cls, 'prefetch_related_fields'):
            return qs.prefetch_related(*cls.prefetch_related_fields())
        return qs