"""
Audit Logging
UMS Comprehensive Audit Trail
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import json
import logging

User = get_user_model()
logger = logging.getLogger('audit')


class AuditLog(models.Model):
    """Model for audit log entries."""
    
    class ActionType(models.TextChoices):
        CREATE = 'create', 'Created'
        READ = 'read', 'Viewed'
        UPDATE = 'Updated', 'update'
        DELETE = 'delete', 'Deleted'
        LOGIN = 'login', 'Login'
        LOGOUT = 'logout', 'Logout'
        LOGIN_FAILED = 'login_failed', 'Login Failed'
        PASSWORD_CHANGE = 'password_change', 'Password Changed'
        PERMISSION_CHANGE = 'permission_change', 'Permission Changed'
        EXPORT = 'export', 'Exported'
        IMPORT = 'import', 'Imported'
    
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='audit_logs'
    )
    
    action = models.CharField(max_length=30, choices=ActionType.choices)
    content_type = models.ForeignKey(
        'contenttypes.ContentType',
        on_delete=models.SET_NULL,
        null=True
    )
    object_id = models.CharField(max_length=255, null=True)
    object_repr = models.TextField(blank=True)
    
    # Change tracking
    changes = models.TextField(blank=True)  # JSON
    old_values = models.TextField(blank=True)
    new_values = models.TextField(blank=True)
    
    # Request info
    ip_address = models.GenericIPAddressField(null=True)
    user_agent = models.TextField(blank())
    request_method = models.CharField(max_length=10)
    request_path = models.TextField()
    
    # Timestamp
    timestamp = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['action', 'timestamp']),
        ]
    
    def __str__(self):
        return f'{self.action} by {self.user} at {self.timestamp}'


class AuditLogger:
    """Central audit logging class."""
    
    @staticmethod
    def log(action, user=None, content_type=None, object_id=None,
           changes=None, old_values=None, new_values=None,
           request=None, **extra):
        """Log an audit entry."""
        try:
            entry = AuditLog.objects.create(
                user=user,
                action=action,
                content_type=content_type,
                object_id=str(object_id) if object_id else None,
                changes=json.dumps(changes) if changes else None,
                old_values=json.dumps(old_values) if old_values else None,
                new_values=json.dumps(new_values) if new_values else None,
                ip_address=AuditLogger.get_ip(request),
                user_agent=AuditLogger.get_user_agent(request),
                request_method=getattr(request, 'method', ''),
                request_path=getattr(request, 'path', ''),
            )
            
            # Also log to file
            logger.info(
                f'AUDIT: {action} by {user} '
                f'({content_type}:{object_id}) '
                f'from {AuditLogger.get_ip(request)}'
            )
            
            return entry
        except Exception as e:
            logger.error(f'Audit logging error: {e}')
            return None
    
    @staticmethod
    def get_ip(request):
        """Get client IP."""
        if not request:
            return None
        
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')
    
    @staticmethod
    def get_user_agent(request):
        """Get user agent."""
        if not request:
            return ''
        return request.META.get('HTTP_USER_AGENT', '')[:500]
    
    # Convenience methods
    @classmethod
    def log_create(cls, user, instance, request=None):
        """Log model creation."""
        from django.contrib.contenttypes.models import ContentType
        return cls.log(
            action=AuditLog.ActionType.CREATE,
            user=user,
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.pk,
            new_values=cls.get_model_values(instance),
            request=request,
        )
    
    @classmethod
    def log_update(cls, user, instance, old_data, new_data, request=None):
        """Log model update."""
        from django.contrib.contenttypes.models import ContentType
        changes = cls.get_changes(old_data, new_data)
        return cls.log(
            action=AuditLog.ActionType.UPDATE,
            user=user,
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.pk,
            changes=changes,
            old_values=old_data,
            new_values=new_data,
            request=request,
        )
    
    @classmethod
    def log_delete(cls, user, instance, request=None):
        """Log model deletion."""
        from django.contrib.contenttypes.models import ContentType
        return cls.log(
            action=AuditLog.ActionType.DELETE,
            user=user,
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.pk,
            old_values=cls.get_model_values(instance),
            request=request,
        )
    
    @classmethod
    def log_login(cls, user, success, request=None):
        """Log login attempt."""
        action = AuditLog.ActionType.LOGIN if success else AuditLog.ActionType.LOGIN_FAILED
        return cls.log(
            action=action,
            user=user if success else None,
            request=request,
            metadata={'success': success}
        )
    
    @classmethod
    def log_view(cls, user, instance, request=None):
        """Log model view."""
        from django.contrib.contenttypes.models import ContentType
        return cls.log(
            action=AuditLog.ActionType.READ,
            user=user,
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.pk,
            request=request,
        )
    
    @staticmethod
    def get_model_values(instance):
        """Get model values as dict."""
        from django.forms.models import model_to_dict
        try:
            return model_to_dict(instance, fields=[f.name for f in instance._meta.fields])
        except:
            return {'id': instance.pk}
    
    @staticmethod
    def get_changes(old_data, new_data):
        """Get changes between old and new data."""
        if not old_data or not new_data:
            return None
        
        changes = {}
        for key in set(list(old_data.keys()) + list(new_data.keys())):
            old = old_data.get(key)
            new = new_data.get(key)
            if old != new:
                changes[key] = {'from': old, 'to': new}
        
        return changes if changes else None


# Signal handlers for automatic logging
def audit_signal_handler(sender, instance, old_data=None, **kwargs):
    """Signal handler for automatic audit logging."""
    # This would be connected to post_save signals
    pass


# Helper decorator for views
def audit(action):
    """Decorator to auto-audit a view."""
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            # Call view
            response = view_func(request, *args, **kwargs)
            
            # Log based on response
            if hasattr(request, 'user') and request.user.is_authenticated:
                if response.status_code < 400:
                    AuditLogger.log(
                        action=action,
                        user=request.user,
                        request=request,
                    )
            
            return response
        return wrapper
    return decorator


# QuerySet enhancement
class AuditableManager(models.Manager):
    """Manager with audit capabilities."""
    
    def get_queryset(self):
        return super().get_queryset()
    
    def create_with_audit(self, user, **kwargs):
        """Create with audit logging."""
        instance = self.create(**kwargs)
        AuditLogger.log_create(user, instance)
        return instance


# Context manager for manual auditing
class audit_context:
    """Context manager for manual auditing."""
    
    def __init__(self, action, user, request=None):
        self.action = action
        self.user = user
        self.request = request
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            AuditLogger.log(
                action='error',
                user=self.user,
                request=self.request,
                metadata={'error': str(exc_val)}
            )
        return False


# Usage examples:
"""
# 1. Automatic in views
from apps.core.audit import AuditLogger

def update_student(request, student_id):
    student = Student.objects.get(id=student_id)
    old_data = {...student data...}
    
    # Update
    student.save()
    
    # Audit
    AuditLogger.log_update(request.user, student, old_data, new_data, request)

# 2. Decorator
from apps.core.audit import audit

@audit(AuditLog.ActionType.EXPORT)
def export_data(request):
    ...

# 3. Context manager
with audit_context('create', request.user, request) as ctx:
    Student.objects.create(...)
"""