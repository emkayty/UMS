import os
import re
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    SECRET_KEY = 'dev-secret-key-not-for-production-2024'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() in ('true', '1', 'yes')

ALLOWED_HOSTS_ENV = os.environ.get('ALLOWED_HOSTS', '')
ALLOWED_HOSTS = ALLOWED_HOSTS_ENV.split(',') if ALLOWED_HOSTS_ENV else ['*']

# Trust proxy headers for production deployments behind proxy
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Security settings - force HTTPS in production
SECURE_SSL_REDIRECT = not DEBUG
SECURE_REDIRECT_EXEMPT = [] if not DEBUG else ['^health/$']
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG
SECURE_CONTENT_TYPE_NOSNIFF = not DEBUG
SECURE_BROWSER_XSS_FILTER = not DEBUG
X_FRAME_OPTIONS = 'DENY'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third party
    # 'rest_framework',
    'corsheaders',
    # Local apps
    'apps.accounts',
    'apps.institution',
    'apps.academic',
    'apps.student',
    'apps.staff',
    'apps.learning',
    'apps.finance',
    'apps.communication',
    'apps.core',
    'apps.reports',
    'apps.reports.analytics',
    'apps.offline',
    'apps.lifecycle',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'unicore.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'unicore.wsgi.application'

# Database
# Production requires PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'unicore_db'),
        'USER': os.environ.get('POSTGRES_USER', 'postgres'),
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

# Cache configuration - Redis for production, LocMemCache for development
# Production: Use Redis for caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL', 'redis://localhost:6379/1'),
        'TIMEOUT': 300,
    }
}

# Fallback to LocMemCache in debug mode without Redis
if DEBUG and not os.environ.get('REDIS_URL'):
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }

# Session backend
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# Fallback to SQLite only in DEBUG mode (development only)
if DEBUG and not os.environ.get('POSTGRES_DB'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Lagos'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = []  # No custom static dir needed

# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Ensure media directory exists
(BASE_DIR / 'media').mkdir(exist_ok=True)

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User model
AUTH_USER_MODEL = 'accounts.User'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'apps.accounts.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.IsAuthenticated',
    ],
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'EXCEPTION_HANDLER': 'unicore.exceptions.custom_exception_handler',
}

# OpenAPI / Swagger Configuration (drf-spectacular)
SPECTACULAR_SETTINGS = {
    'TITLE': 'UMS API',
    'DESCRIPTION': '''
University Management System REST API

## Features
- Authentication (JWT)
- Academic Management
- Student Management
- Staff Management
- Finance & Fees
- Learning & Exams
- AI/ML Services
- Analytics

## Authentication
Use JWT token in Authorization header:
```
Authorization: Bearer <token>
```
''',
    'VERSION': '2.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'TAGS': [
        {'name': 'Authentication', 'description': 'Login, logout'},
        {'name': 'Academic', 'description': 'Faculties, departments'},
        {'name': 'Students', 'description': 'Students'},
        {'name': 'Finance', 'description': 'Fees, payments'},
    ]
}

# CORS
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',') if not DEBUG else []
CORS_ALLOW_CREDENTIALS = True

# Ninja settings
NINJA_SERIALIZER_CLASS = 'django_ninja.serializers.ModelSerializer'

# JWT Settings
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
if not JWT_SECRET_KEY:
    JWT_SECRET_KEY = 'dev-jwt-secret-not-for-production-2024'

JWT_ALGORITHM = 'HS256'
JWT_ACCESS_TOKEN_LIFETIME = timedelta(minutes=15)  # Short-lived access tokens
JWT_REFRESH_TOKEN_LIFETIME = timedelta(days=7)
JWT_CLOCK_SKEW = timedelta(seconds=10)

# Rate limiting
RATELIMIT_ENABLED = not DEBUG
RATELIMIT_USE_CACHE = 'default'
RATELIMIT_DEFAULT = '100/hour'  # Default rate limit
RATELIMIT_AUTH = '10/minute'   # Stricter limit for auth endpoints
RATELIMIT_LOGIN = '5/minute'   # Very strict for login

# Password policy
PASSWORD_MIN_LENGTH = 12
PASSWORD_REQUIRE_UPPERCASE = True
PASSWORD_REQUIRE_LOWERCASE = True
PASSWORD_REQUIRE_DIGITS = True
PASSWORD_REQUIRE_SPECIAL = True
PASSWORD_SPECIAL_CHARS = r'!@#$%^&*()_+-=[]{}|;:,.<>?'
PASSWORD_HISTORY_COUNT = 5  # Don't allow reusing last 5 passwords
PASSWORD_MAX_AGE_DAYS = 90  # Force password change after 90 days

# Session security
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_NAME = 'unicore_sessionid'
SESSION_COOKIE_AGE = 60 * 60 * 2  # 2 hours
SESSION_SAVE_EVERY_REQUEST = True

# CSRF settings
CSRF_USE_SESSIONS = True
CSRF_COOKIE_NAME = 'unicore_csrf'
CSRF_HEADER_NAME = 'HTTP_X_CSRFTOKEN'
CSRF_EXEMPT_PATTERNS = [
    r'^api/v1/auth/refresh$',
    r'^api/v1/payments/webhook$',
    r'^health/$',
]

# CORS - restrictive in production
CORS_ALLOW_ALL_ORIGINS = DEBUG  # Only allow all in debug mode
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',') if not DEBUG else []
CORS_ALLOW_CREDENTIALS = True
CORS_EXPOSE_HEADERS = ['Content-Type', 'X-CSRFToken']
CORS_PREFLIGHT_MAX_AGE = 3600

# Audit logging
AUDIT_LOG_ENABLED = not DEBUG
AUDIT_LOG_RETENTION_DAYS = 365
AUDIT_LOG_EVENTS = [
    'LOGIN',
    'LOGOUT',
    'PASSWORD_CHANGE',
    'PASSWORD_RESET',
    'ROLE_CHANGE',
    'PERMISSION_DENIED',
    'DATA_EXPORT',
]

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
# Django Ninja defaults
NINJA_PAGINATION_CLASS = 'django_ninja.pagination.PageNumberPagination'
NINJA_PAGINATION_DEFAULT_ORDERING = ('id',)
NINJA_PAGINATION_MAX_OFFSET = 1000
NINJA_PAGINATION_PER_PAGE = 25
NINJA_PAGINATION_MAX_PER_PAGE_SIZE = 100
NINJA_PAGINATION_MAX_LIMIT = 100
NINJA_NUM_PROXIES = 0
NINJA_DEFAULT_THROTTLE_RATES = {
    'anon': '1000/hour',
    'user': '10000/hour'
}
NINJA_FIX_REQUEST_FILES_METHODS = ['POST', 'PATCH', 'PUT']
