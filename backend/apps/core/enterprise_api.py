"""
ENTERPRISE APIs
Advanced enterprise features
"""

from ninja import Router, Schema
from typing import List, Optional
from django.shortcuts import get_object_or_404
from django.utils import timezone

router = Router(tags=['Enterprise'])


# ============================================================
# ENTERPRISE SCHEMAS
# ============================================================

class CustomFieldSchema(Schema):
    id: str
    name: str
    field_type: str
    model: str
    required: bool


class DataExportSchema(Schema):
    id: str
    name: str
    export_type: str
    model: str
    status: str


class WebhookSchema(Schema):
    id: str
    name: str
    url: str
    events: List[str]
    is_active: bool


class ScheduledTaskSchema(Schema):
    id: str
    name: str
    task_name: str
    schedule_type: str
    status: str
    next_run: Optional[str]


# ============================================================
# CUSTOM FIELDS
# ============================================================

@router.get('/custom-fields')
def list_custom_fields(request, model: str = None):
    """List custom fields."""
    from apps.core.enterprise import CustomField
    
    query = CustomField.objects.filter(is_active=True)
    if model:
        query = query.filter(model=model)
    
    return [
        {
            'id': str(f.id),
            'name': f.name,
            'field_type': f.field_type,
            'model': f.model,
            'required': f.required,
            'options': f.options
        }
        for f in query
    ]


@router.post('/custom-fields')
def create_custom_field(request, data: CustomFieldSchema):
    """Create custom field."""
    from apps.core.enterprise import CustomField
    
    field = CustomField.objects.create(
        name=data.name,
        field_type=data.field_type,
        model=data.model,
        required=data.required
    )
    
    return {'success': True, 'id': str(field.id)}


@router.get('/custom-fields/{id}/values')
def get_field_values(request, id: str):
    """Get custom field values."""
    from apps.core.enterprise import CustomField, CustomFieldValue
    
    field = get_object_or_404(CustomField, id=id)
    values = CustomFieldValue.objects.filter(field=field)
    
    return [
        {'object_id': v.object_id, 'value': v.value}
        for v in values
    ]


@router.post('/custom-fields/{id}/values')
def set_field_value(request, id: str, object_id: str, value):
    """Set custom field value."""
    from apps.core.enterprise import CustomField, CustomFieldValue
    
    field = get_object_or_404(CustomField, id=id)
    
    value_obj, _ = CustomFieldValue.objects.get_or_create(
        field=field,
        object_id=object_id,
        defaults={'value': value}
    )
    
    value_obj.value = value
    value_obj.save()
    
    return {'success': True}


# ============================================================
# DATA EXPORT
# ============================================================

@router.get('/exports')
def list_exports(request):
    """List data exports."""
    from apps.core.enterprise import DataExport
    
    exports = DataExport.objects.all().order_by('-created_at')
    
    return [
        {
            'id': str(e.id),
            'name': e.name,
            'type': e.export_type,
            'status': e.status,
            'rows': e.row_count,
            'created': str(e.created_at)
        }
        for e in exports
    ]


@router.post('/exports')
def create_export(request, data: dict):
    """Create data export."""
    from apps.core.enterprise import DataExport
    
    export = DataExport.objects.create(
        name=data.get('name'),
        export_type=data.get('type'),
        model=data.get('model'),
        fields=data.get('fields', []),
        filters=data.get('filters', {}),
        requested_by=request.user
    )
    
    # Would trigger celery task here
    # export_task.delay(str(export.id))
    
    return {'success': True, 'id': str(export.id)}


@router.get('/exports/{id}/download')
def download_export(request, id: str):
    """Download export file."""
    from apps.core.enterprise import DataExport
    
    export = get_object_or_404(DataExport, id=id)
    
    if export.status != 'completed':
        return {'error': 'Export not ready'}
    
    if export.file:
        return {'url': export.file.url}
    
    return {'error': 'File not found'}


# ============================================================
# WEBHOOKS
# ============================================================

@router.get('/webhooks')
def list_webhooks(request):
    """List webhooks."""
    from apps.core.enterprise import Webhook
    
    webhooks = Webhook.objects.all()
    
    return [
        {
            'id': str(w.id),
            'name': w.name,
            'url': w.url,
            'events': w.events,
            'is_active': w.is_active
        }
        for w in webhooks
    ]


@router.post('/webhooks')
def create_webhook(request, data: dict):
    """Create webhook."""
    from apps.core.enterprise import Webhook
    
    webhook = Webhook.objects.create(
        name=data.get('name'),
        url=data.get('url'),
        events=data.get('events', []),
        auth_type=data.get('auth_type', 'none'),
        auth_secret=data.get('auth_secret', '')
    )
    
    return {'success': True, 'id': str(webhook.id)}


@router.post('/webhooks/{id}/test')
def test_webhook(request, id: str):
    """Test webhook delivery."""
    from apps.core.enterprise import Webhook, WebhookDelivery
    
    webhook = get_object_or_404(Webhook, id=id)
    
    # Create test delivery
    delivery = WebhookDelivery.objects.create(
        webhook=webhook,
        event='test',
        payload={'test': True}
    )
    
    # Would trigger task here
    # deliver_webhook.delay(str(delivery.id))
    
    return {'success': True, 'id': str(delivery.id)}


@router.get('/webhooks/deliveries')
def list_deliveries(request, webhook_id: str = None):
    """List webhook deliveries."""
    from apps.core.enterprise import WebhookDelivery
    
    query = WebhookDelivery.objects.all()
    if webhook_id:
        query = query.filter(webhook_id=webhook_id)
    
    return [
        {
            'id': str(d.id),
            'event': d.event,
            'status': d.status,
            'attempts': d.attempts,
            'created': str(d.created_at)
        }
        for d in query[:50]
    ]


# ============================================================
# SCHEDULED TASKS
# ============================================================

@router.get('/tasks')
def list_tasks(request):
    """List scheduled tasks."""
    from apps.core.enterprise import ScheduledTask
    
    tasks = ScheduledTask.objects.all()
    
    return [
        {
            'id': str(t.id),
            'name': t.name,
            'task': t.task_name,
            'schedule': t.schedule_type,
            'status': t.status,
            'next': str(t.next_run) if t.next_run else None
        }
        for t in tasks
    ]


@router.post('/tasks')
def create_task(request, data: dict):
    """Create scheduled task."""
    from apps.core.enterprise import ScheduledTask
    
    task = ScheduledTask.objects.create(
        name=data.get('name'),
        task_name=data.get('task_name'),
        task_params=data.get('params', {}),
        schedule_type=data.get('schedule_type'),
        time=data.get('time'),
        run_at=data.get('run_at')
    )
    
    return {'success': True, 'id': str(task.id)}


@router.post('/tasks/{id}/run')
def run_task(request, id: str):
    """Run task manually."""
    from apps.core.enterprise import ScheduledTask, TaskExecution
    
    task = get_object_or_404(ScheduledTask, id=id)
    
    execution = TaskExecution.objects.create(
        task=task,
        status='running',
        started_at=timezone.now()
    )
    
    # Would trigger task here
    # run_task.delay(str(execution.id))
    
    return {'success': True, 'id': str(execution.id)}


@router.get('/tasks/{id}/executions')
def list_task_executions(request, id: str):
    """List task executions."""
    from apps.core.enterprise import TaskExecution
    
    executions = TaskExecution.objects.filter(task_id=id).order_by('-created_at')
    
    return [
        {
            'id': str(e.id),
            'status': e.status,
            'output': e.output[:100] if e.output else None,
            'duration': e.duration_seconds,
            'created': str(e.created_at)
        }
        for e in executions[:20]
    ]


# ============================================================
# NOTIFICATIONS
# ============================================================

@router.get('/notifications/templates')
def list_notification_templates(request):
    """List notification templates."""
    from apps.core.enterprise import NotificationTemplate
    
    templates = NotificationTemplate.objects.filter(is_active=True)
    
    return [
        {
            'id': str(t.id),
            'name': t.name,
            'channel': t.channel,
            'subject': t.subject,
            'variables': t.variables
        }
        for t in templates
    ]


@router.post('/notifications/templates')
def create_notification_template(request, data: dict):
    """Create notification template."""
    from apps.core.enterprise import NotificationTemplate
    
    template = NotificationTemplate.objects.create(
        name=data.get('name'),
        channel=data.get('channel'),
        subject=data.get('subject', ''),
        body=data.get('body'),
        variables=data.get('variables', [])
    )
    
    return {'success': True, 'id': str(template.id)}


@router.post('/notifications/send')
def send_notification(request, data: dict):
    """Send notification."""
    from apps.core.enterprise import NotificationLog
    
    log = NotificationLog.objects.create(
        recipient=data.get('recipient'),
        channel=data.get('channel'),
        subject=data.get('subject', ''),
        body=data.get('body'),
        status='pending'
    )
    
    # Would send via appropriate channel
    # send_notification.delay(str(log.id))
    
    return {'success': True, 'id': str(log.id)}


@router.get('/notifications/logs')
def list_notification_logs(request, status: str = None):
    """List notification logs."""
    from apps.core.enterprise import NotificationLog
    
    query = NotificationLog.objects.all()
    if status:
        query = query.filter(status=status)
    
    return [
        {
            'id': str(l.id),
            'recipient': l.recipient,
            'channel': l.channel,
            'status': l.status,
            'sent': str(l.sent_at) if l.sent_at else None
        }
        for l in query[:50]
    ]


# ============================================================
# AUDIT
# ============================================================

@router.get('/audit')
def list_audit(request, model: str = None, user_id: str = None):
    """List audit entries."""
    from apps.core.enterprise import AuditEntry
    
    query = AuditEntry.objects.all()
    if model:
        query = query.filter(model=model)
    if user_id:
        query = query.filter(user_id=user_id)
    
    return [
        {
            'id': str(a.id),
            'user': a.user.email if a.user else None,
            'action': a.action,
            'model': a.model,
            'status': a.status,
            'created': str(a.created_at)
        }
        for a in query[:50]
    ]


# ============================================================
# API KEYS
# ============================================================

@router.get('/api-keys')
def list_api_keys(request):
    """List API keys."""
    from apps.core.enterprise import APIKey
    
    keys = APIKey.objects.filter(user=request.user)
    
    return [
        {
            'id': str(k.id),
            'name': k.name,
            'key': k.key[:10] + '...',
            'is_active': k.is_active,
            'last_used': str(k.last_used) if k.last_used else None
        }
        for k in keys
    ]


@router.post('/api-keys')
def create_api_key(request, data: dict):
    """Create API key."""
    from apps.core.enterprise import APIKey
    import secrets
    
    key = secrets.token_hex(32)
    
    api_key = APIKey.objects.create(
        name=data.get('name'),
        key=key,
        user=request.user,
        permissions=data.get('permissions', []),
        rate_limit=data.get('rate_limit', 1000)
    )
    
    return {'success': True, 'key': key}


@router.delete('/api-keys/{id}')
def delete_api_key(request, id: str):
    """Delete API key."""
    from apps.core.enterprise import APIKey
    
    api_key = get_object_or_404(APIKey, id=id, user=request.user)
    api_key.delete()
    
    return {'success': True}


# ============================================================
# INSTITUTION
# ============================================================

@router.get('/institution')
def get_institution(request):
    """Get institution."""
    from apps.core.enterprise import Institution
    
    institution = Institution.objects.first()
    
    if not institution:
        return {'error': 'Not configured'}
    
    return {
        'id': str(institution.id),
        'name': institution.name,
        'short_name': institution.short_name,
        'email': institution.email,
        'timezone': institution.timezone,
        'currency': institution.currency
    }


@router.get('/institution/settings')
def get_institution_settings(request):
    """Get institution settings."""
    from apps.core.enterprise import InstitutionSettings
    
    settings = InstitutionSettings.objects.first()
    
    if not settings:
        return {'error': 'Not configured'}
    
    return {
        'late_fee_percentage': float(settings.late_fee_percentage),
        'late_fee_grace_days': settings.late_fee_grace_days,
        'min_course_units': settings.min_course_units,
        'max_course_units': settings.max_course_units,
        'attendance_threshold': float(settings.attendance_threshold)
    }