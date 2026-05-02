import uuid
import hashlib
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserRole(models.TextChoices):
    STUDENT = 'student', 'Student'
    LECTURER = 'lecturer', 'Lecturer'
    HOD = 'hod', 'Head of Department'
    DEAN = 'dean', 'Dean'
    REGISTRAR = 'registrar', 'Registrar'
    BURSAR = 'bursar', 'Bursar'
    INSTITUTION_ADMIN = 'institution_admin', 'Institution Admin'
    PARENT = 'parent', 'Parent'
    GUARDIAN = 'guardian', 'Guardian'


class UserManager(BaseUserManager):
    """Custom user manager with secure password handling."""
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', UserRole.INSTITUTION_ADMIN)
        if password:
            extra_fields['password_changed_at'] = timezone.now()
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Production-ready custom user model with roles and security features."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, db_index=True)
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.STUDENT)
    
    # Account status
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    # Security fields
    password_changed_at = models.DateTimeField(null=True, blank=True)
    last_password_reset = models.DateTimeField(null=True, blank=True)
    failed_login_attempts = models.IntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True, help_text='Account locked until')
    must_change_password = models.BooleanField(default=False)
    
    # Two-factor authentication
    totp_secret = models.CharField(max_length=32, blank=True, help_text='TOTP secret for 2FA')
    totp_enabled = models.BooleanField(default=False)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    
    # Preferences
    preferences = models.JSONField(default=dict, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role']

    class Meta:
        db_table = 'users'
        ordering = ['email']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role', 'is_active']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.email

    def has_role(self, *roles):
        """Check if user has any of the specified roles."""
        return self.role in roles

    @property
    def is_locked(self) -> bool:
        """Check if account is temporarily locked."""
        if self.locked_until and self.locked_until > timezone.now():
            return True
        return False

    def lock(self, duration_minutes: int = 15):
        """Lock account for specified duration."""
        self.locked_until = timezone.now() + timezone.timedelta(minutes=duration_minutes)
        self.save(update_fields=['locked_until'])

    def unlock(self):
        """Unlock account."""
        self.locked_until = None
        self.failed_login_attempts = 0
        self.save(update_fields=['locked_until', 'failed_login_attempts'])

    def record_failed_login(self):
        """Record failed login attempt and lock if necessary."""
        self.failed_login_attempts += 1
        max_attempts = 5  # Lock after 5 failed attempts
        if self.failed_login_attempts >= max_attempts:
            self.lock()
        self.save(update_fields=['failed_login_attempts', 'locked_until'])

    def reset_failed_logins(self):
        """Reset failed login counter."""
        self.failed_login_attempts = 0
        self.save(update_fields=['failed_login_attempts'])

    def set_password(self, password, record_history=True):
        """Set password with history tracking."""
        super().set_password(password)
        self.password_changed_at = timezone.now()
        
        if record_history and self.id:
            # Save to password history
            PasswordHistory.objects.create(
                user=self,
                password_hash=self.password
            )
            
            # Keep only last N passwords
            history_count = getattr(__import__('django.conf', fromlist=['settings']).settings, 
                                 'PASSWORD_HISTORY_COUNT', 5)
            old_passwords = PasswordHistory.objects.filter(
                user=self
            ).order_by('-created_at')[history_count:]
            old_passwords.delete()
        
        self.save(update_fields=['password', 'password_changed_at', 'updated_at'])

    def check_password(self, password, enforce_history=True):
        """Check password with history validation."""
        if self.is_locked:
            return False
        
        result = super().check_password(password)
        
        if result and enforce_history and self.id:
            # Clear failed attempts on successful login
            if self.failed_login_attempts > 0:
                self.reset_failed_logins()
        
        return result


class PasswordHistory(models.Model):
    """Track password history for reuse prevention."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='password_history'
    )
    password_hash = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'password_history'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.created_at}"


class UserSession(models.Model):
    """Track active user sessions."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sessions'
    )
    token_jti = models.CharField(max_length=64, unique=True)
    device_info = models.CharField(max_length=255, blank=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'user_sessions'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.device_info}"

    def is_expired(self) -> bool:
        return self.expires_at < timezone.now()

    def deactivate(self):
        self.is_active = False
        self.save(update_fields=['is_active'])