from .settings import *  # Inherit all settings

# ============================================================
# PRODUCTION CONFIGURATION OVERRIDES
# ============================================================

# Override DEBUG - ALWAYS False in production
DEBUG = False

# Security settings
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Session security
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HTTPS settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# ============================================================
# EMAIL BACKEND (SMTP)
# ============================================================

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@unicore.edu')
EMAIL_SUBJECT_PREFIX = '[UniCore] '

# Alternative: Useconsole for development
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ============================================================
# RATE LIMITING
# ============================================================

RATELIMIT_USE_CACHE = 'default'
RATELIMIT_DEFAULT = '100/m'  # 100 requests per minute
RATELIMIT_AUTHENTICATED = '200/m'
RATELIMIT_VIEW = '200/m'

# ============================================================
# CORS (Production)
# ============================================================

CORS_ALLOWED_ORIGINS = os.environ.get(
    'CORS_ALLOWED_ORIGINS', 
    'https://yourdomain.com'
).split(',')

# ============================================================
# STATIC & MEDIA FILES (S3)
# ============================================================

# AWS S3 Configuration
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')
AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_S3_CUSTOM_DOMAIN')
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = 'public-read'

# Static files
STATIC_FILES_STORAGE = 'storages.backends.StaticFileStorage'
if AWS_STORAGE_BUCKET_NAME:
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'

# Media files
MEDIA_FILES_STORAGE = 'storages.backends.MediaFileStorage'
if AWS_STORAGE_BUCKET_NAME:
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

# ============================================================
# MONITORING (Sentry)
# ============================================================

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

SENTRY_DSN = os.environ.get('SENTRY_DSN')

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.1,
        send_default_pii=False,
        environment='production',
    )

# ============================================================
# CACHING (Redis - Production)
# ============================================================

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL', 'redis://localhost:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'ums',
        'TIMEOUT': 300,
    }
}

# ============================================================
# DATABASE (PostgreSQL - Production)
# ============================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'ums_prod'),
        'USER': os.environ.get('POSTGRES_USER', 'ums_user'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
        'CONN_MAX_AGE': 60,
        'OPTIONS': {
            'sslmode': os.environ.get('POSTGRES_SSL_MODE', 'require'),
            'connect_timeout': 10,
        },
    }
}

# ============================================================
# CELERY (Production)
# ============================================================

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/1')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/2')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Africa/Lagos'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes

# ============================================================
# LOGGING (Production)
# ============================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'json': {
            'format': '{"time": "%(asctime)s", "level": "%(levelname)s", "module": "%(module)s", "message": "%(message)s"}',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'ums.log'),
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'WARNING',
            'propagate': False,
        },
        'apps': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Ensure logs directory exists
LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

# ============================================================
# ADMIN (Production)
# ============================================================

ADMINS = [
    ('Admin', os.environ.get('ADMIN_EMAIL', 'admin@unicore.edu')),
]

MANAGERS = ADMINS

# ============================================================
# 2FA (Two-Factor Authentication)
# ============================================================

# Enable 2FA for staff and admin
TWO_FACTOR_ENABLED = os.environ.get('TWO_FACTOR_ENABLED', 'True') == 'True'

if TWO_FACTOR_ENABLED:
    # Add to installed apps
    INSTALLED_APPS += ['django_otp', 'django_otp.plugins.otp_static', 'django_otp.plugins.otp_totp']
    
    # Add to middleware
    MIDDLEWARE = [
        'django_otp.middleware.OTPMiddleware',
    ] + MIDDLEWARE

# ============================================================
# AUDIT LOGGING
# ============================================================

AUDIT_LOG_ENABLED = True
AUDIT_LOG_MAX_ENTRIES = 10000
AUDIT_LOG_PER_SAVE = 50  # Bulk save every 50 entries

# ============================================================
# PAGINATION
# ============================================================

REST_FRAMEWORK['PAGE_SIZE'] = 20