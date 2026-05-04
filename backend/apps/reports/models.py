import uuid
from django.db import models
from apps.accounts.models import User


class AuditLog(models.Model):
    """Immutable audit log."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='audit_logs_dup'
    )
    action_type = models.CharField(max_length=50)
    model_name = models.CharField(max_length=50)
    object_id = models.CharField(max_length=50, blank=True)
    changes = models.JSONField(default=dict)
    ip_address = models.GenericIPAddressField(null=True)
    user_agent = models.CharField(max_length=500, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'audit_logs'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'action_type']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"{self.user} - {self.action_type} on {self.model_name}"

    def save(self, *args, **kwargs):
        # Make immutable - prevent updates
        if self.pk is not None:
            raise ValueError("Audit logs cannot be modified")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValueError("Audit logs cannot be deleted")


class AuditLogMixin:
    """Mixin to automatically create audit logs."""
    
    @property
    def audit_log_user(self):
        return getattr(self, '_audit_user', None)
    
    @audit_log_user.setter
    def audit_log_user(self, value):
        self._audit_user = value
    
    def log_create(self, user):
        self._audit_log_action('create', user)
    
    def log_update(self, user, old_data, new_data):
        self._audit_log_action('update', user, old_data, new_data)
    
    def log_delete(self, user):
        self._audit_log_action('delete', user)
    
    def _audit_log_action(self, action, user, changes=None):
        AuditLog.objects.create(
            user=user,
            action_type=action,
            model_name=self.__class__.__name__,
            object_id=str(self.pk) if hasattr(self, 'pk') else str(self.id),
            changes=changes or {}
        )