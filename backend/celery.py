"""
CELERY CONFIGURATION
Task queue for background processing
"""

from celery import Celery
from celery.schedules import crontab

# Redis as message broker
REDIS_URL = 'redis://localhost:6379/0'

app = Celery('ums')

# Load config from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()

# Celery beat schedule for periodic tasks
app.conf.beat_schedule = {
    # Sync results every 5 minutes
    'sync-results': {
        'task': 'apps.ai.tasks.sync_results',
        'schedule': 300.0,
    },
    # Send daily reminders at 8am
    'daily-reminders': {
        'task': 'apps.communication.tasks.send_daily_reminders',
        'schedule': crontab(hour=8, minute=0),
    },
    # Weekly report every Monday at 9am
    'weekly-report': {
        'task': 'apps.reports.tasks.weekly_report',
        'schedule': crontab(hour=9, minute=0, day_of_week=1),
    },
    # Monthly analytics at 1st of month
    'monthly-analytics': {
        'task': 'apps.reports.tasks.monthly_analytics',
        'schedule': crontab(hour=10, minute=0, day_of_month=1),
    },
    # Cleanup old sessions (daily at 2am)
    'cleanup': {
        'task': 'apps.core.tasks.cleanup_old_sessions',
        'schedule': crontab(hour=2, minute=0),
    },
}

# Task settings
app.conf.task_serializer = 'json'
app.conf.accept_content = ['json']
app.conf.result_serializer = 'json'
app.conf.timezone = 'Africa/Lagos'
app.conf.enable_utc = True

# Task routing
app.conf.task_routes = {
    'apps.ai.tasks.*': {'queue': 'ai'},
    'apps.communication.tasks.*': {'queue': 'notifications'},
    'apps.reports.tasks.*': {'queue': 'reports'},
}

# Rate limiting
app.conf.task_default_rate_limit = '100/m'

# Task result expiry (7 days)
app.conf.task_result_expires = 604800

# Worker settings
app.conf.worker_prefetch_multiplier = 4
app.conf.worker_max_tasks_per_child = 1000

# Broker settings
app.conf.broker_connection_retry_on_startup = True
app.conf.broker_connection_max_retries = 10