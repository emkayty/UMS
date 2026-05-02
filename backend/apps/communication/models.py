import uuid
from django.db import models
from apps.accounts.models import User
from apps.academic.models import Faculty, Department


class AnnouncementScope(models.TextChoices):
    GLOBAL = 'global', 'Global'
    FACULTY = 'faculty', 'Faculty'
    DEPARTMENT = 'department', 'Department'


class Announcement(models.Model):
    """Announcements."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    body = models.TextField()
    scope = models.CharField(
        max_length=20, choices=AnnouncementScope.choices,
        default=AnnouncementScope.GLOBAL
    )
    faculty = models.ForeignKey(
        Faculty, on_delete=models.CASCADE, null=True, blank=True,
        related_name='announcements'
    )
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, null=True, blank=True,
        related_name='announcements'
    )
    posted_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='announcements'
    )
    posted_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'announcements'
        ordering = ['-posted_at']

    def __str__(self):
        return self.title


class Notification(models.Model):
    """User notifications."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notifications'
    )
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    action_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.title}"


class Message(models.Model):
    """Internal messages."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_messages'
    )
    subject = models.CharField(max_length=200)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'messages'
        ordering = ['-sent_at']

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.subject}"