from ninja import Router, Schema
from typing import List, Optional

from apps.communication.models import Announcement, Notification, Message

router = Router(tags=['Communication'])


# === Announcements ===
class AnnouncementSchema(Schema):
    id: str
    title: str
    body: str
    scope: str
    faculty_id: Optional[str]
    department_id: Optional[str]
    posted_by: str
    posted_at: str


@router.get('/announcements', response=List[AnnouncementSchema])
def list_announcements(request, scope: str = None):
    """List active announcements."""
    qs = Announcement.objects.filter(is_active=True)
    if scope:
        qs = qs.filter(scope=scope)
    return qs[:20]


@router.post('/announcements', response=AnnouncementSchema)
def create_announcement(request, data: dict):
    """Create announcement."""
    announcement = Announcement.objects.create(
        title=data.get('title'),
        body=data.get('body'),
        scope=data.get('scope', 'global'),
        faculty_id=data.get('faculty_id'),
        department_id=data.get('department_id'),
        posted_by=request.auth[0]
    )
    return announcement


@router.get('/announcements/{id}', response=AnnouncementSchema)
def get_announcement(request, id: str):
    """Get announcement by ID."""
    return get_object_or_404(Announcement, id=id)


@router.patch('/announcements/{id}', response=AnnouncementSchema)
def update_announcement(request, id: str, data: dict):
    """Update announcement."""
    announcement = get_object_or_404(Announcement, id=id)
    for field in ['title', 'body', 'scope', 'faculty_id', 'department_id']:
        if field in data and data[field] is not None:
            setattr(announcement, field, data[field])
    announcement.save()
    return announcement


@router.delete('/announcements/{id}')
def delete_announcement(request, id: str):
    """Soft delete announcement."""
    announcement = get_object_or_404(Announcement, id=id)
    announcement.is_active = False
    announcement.save()
    return {'success': True, 'message': 'Announcement deactivated'}


# === Notifications ===
@router.get('/notifications')
def list_notifications(request, unread_only: bool = False):
    """List user notifications."""
    qs = Notification.objects.filter(user=request.auth[0])
    if unread_only:
        qs = qs.filter(is_read=False)
    
    return [
        {
            'id': str(n.id),
            'title': n.title,
            'message': n.message,
            'is_read': n.is_read,
            'created_at': n.created_at.isoformat()
        }
        for n in qs[:50]
    ]


@router.post('/notifications/{id}/read')
def mark_notification_read(request, id: str):
    """Mark notification as read."""
    notification = Notification.objects.get(id=id)
    notification.is_read = True
    notification.save()
    return {'success': True}


@router.post('/notifications/read-all')
def mark_all_read(request):
    """Mark all notifications as read."""
    Notification.objects.filter(user=request.auth[0], is_read=False).update(is_read=True)
    return {'success': True}


# === Messages ===
@router.get('/messages')
def list_messages(request):
    """List user's messages."""
    messages = Message.objects.filter(
        sender=request.auth[0]
    ) | Message.objects.filter(receiver=request.auth[0])
    
    return [
        {
            'id': str(m.id),
            'sender': m.sender.email,
            'receiver': m.receiver.email,
            'subject': m.subject,
            'body': m.body[:100],
            'is_read': m.is_read,
            'sent_at': m.sent_at.isoformat()
        }
        for m in messages[:50]
    ]


@router.post('/messages/send')
def send_message(request, data: dict):
    """Send internal message."""
    message = Message.objects.create(
        sender=request.auth[0],
        receiver_id=data.get('receiver_id'),
        subject=data.get('subject'),
        body=data.get('body')
    )
    
    # Create notification for receiver
    Notification.objects.create(
        user=message.receiver,
        title=f"New message: {message.subject}",
        message=f"You have a new message from {message.sender.email}",
        action_url=f"/messages/{message.id}"
    )
    
    return {'success': True}


# === Broadcast ===
@router.post('/broadcast')
def broadcast_message(request, data: dict):
    """Send announcement to all users."""
    announcement = Announcement.objects.create(
        title=data.get('title'),
        body=data.get('body'),
        scope='global',
        posted_by=request.auth[0]
    )
    
    # Create notifications for all users
    from apps.accounts.models import User
    for user in User.objects.filter(is_active=True):
        Notification.objects.create(
            user=user,
            title=data.get('title'),
            message=data.get('body')[:200],
            action_url=f"/announcements/{announcement.id}"
        )
    
    return {'success': True, 'recipients': User.objects.filter(is_active=True).count()}