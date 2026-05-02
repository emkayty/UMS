import uuid
from django.db import models
from apps.accounts.models import User


class PaymentGateway(models.TextChoices):
    PAYSTACK = 'paystack', 'Paystack'
    FLUTTERWAVE = 'flutterwave', 'Flutterwave'


class GradingScaleType(models.TextChoices):
    BRITISH_NIGERIAN = 'british_nigerian', 'British/Nigerian (A=70+, 5.0 scale)'
    AMERICAN = 'american', 'American (A=90+, 4.0 scale)'
    CUSTOM = 'custom', 'Custom'


class EmailProvider(models.TextChoices):
    SMTP = 'smtp', 'SMTP'
    SENDGRID = 'sendgrid', 'SendGrid'
    MAILGUN = 'mailgun', 'Mailgun'


class SMSProvider(models.TextChoices):
    SMS = 'sms', 'SMS'
    TWILIO = 'twilio', 'Twilio'


class Settings(models.Model):
    """Institution settings singleton."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    institution_name = models.CharField(max_length=200)
    motto = models.CharField(max_length=500, blank=True)
    logo_url = models.URLField(blank=True)
    primary_color = models.CharField(max_length=7, default='#1e3a8a')  # Blue
    secondary_color = models.CharField(max_length=7, default='#059669')  # Green
    
    # Grading defaults
    grading_scale_type = models.CharField(
        max_length=20,
        choices=GradingScaleType.choices,
        default=GradingScaleType.BRITISH_NIGERIAN
    )
    grading_boundaries = models.JSONField(
        default=list,
        help_text='Grade boundaries e.g. [{"grade": "A", "min": 70, "point": 5.0}]'
    )
    
    # Academic calendar
    academic_year_start = models.DateField()
    semester_structure = models.JSONField(
        default=list,
        help_text='e.g. [{"name": "First Semester", "duration_weeks": 16}]'
    )
    
    # Payment gateway
    payment_gateway = models.CharField(
        max_length=20,
        choices=PaymentGateway.choices,
        default=PaymentGateway.PAYSTACK
    )
    paystack_secret_key = models.CharField(max_length=200, blank=True)
    paystack_public_key = models.CharField(max_length=200, blank=True)
    flutterwave_secret_key = models.CharField(max_length=200, blank=True)
    flutterwave_public_key = models.CharField(max_length=200, blank=True)
    
    # Communication
    email_provider = models.CharField(
        max_length=20,
        choices=EmailProvider.choices,
        default=EmailProvider.SMTP
    )
    email_host = models.CharField(max_length=200, blank=True)
    email_port = models.IntegerField(default=587)
    email_username = models.CharField(max_length=200, blank=True)
    email_password = models.CharField(max_length=200, blank=True)
    email_from = models.EmailField(blank=True)
    
    sms_provider = models.CharField(
        max_length=20,
        choices=SMSProvider.choices,
        default=SMSProvider.SMS
    )
    sms_api_key = models.CharField(max_length=200, blank=True)
    
    # Setup wizard state
    setup_completed = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='created_settings'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'settings'
        verbose_name_plural = 'Settings'

    def save(self, *args, **kwargs):
        # Set default grading boundaries based on scale type
        if not self.grading_boundaries:
            if self.grading_scale_type == GradingScaleType.BRITISH_NIGERIAN:
                self.grading_boundaries = [
                    {'grade': 'A', 'min': 70, 'point': 5.0},
                    {'grade': 'B', 'min': 60, 'point': 4.0},
                    {'grade': 'C', 'min': 50, 'point': 3.0},
                    {'grade': 'D', 'min': 45, 'point': 2.0},
                    {'grade': 'E', 'min': 40, 'point': 1.0},
                    {'grade': 'F', 'min': 0, 'point': 0.0},
                ]
            elif self.grading_scale_type == GradingScaleType.AMERICAN:
                self.grading_boundaries = [
                    {'grade': 'A', 'min': 90, 'point': 4.0},
                    {'grade': 'B', 'min': 80, 'point': 3.0},
                    {'grade': 'C', 'min': 70, 'point': 2.0},
                    {'grade': 'D', 'min': 60, 'point': 1.0},
                    {'grade': 'F', 'min': 0, 'point': 0.0},
                ]
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.institution_name

    @classmethod
    def get_instance(cls):
        """Get or create settings instance."""
        instance, _ = cls.objects.get_or_create(
            id=cls.objects.first().id if cls.objects.exists() else uuid.uuid4()
        )
        return instance