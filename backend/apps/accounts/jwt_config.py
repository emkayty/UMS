"""
JWT Authentication Configuration for Django Ninja
Production-ready JWT settings without DRF dependencies.
"""
from datetime import timedelta

# JWT Settings for Django Ninja
JWT_SECRET_KEY = 'jwt-secret-key-change-in-production'
JWT_ALGORITHM = 'HS256'
JWT_ACCESS_TOKEN_LIFETIME = timedelta(minutes=15)
JWT_REFRESH_TOKEN_LIFETIME = timedelta(days=7)
JWT_CLOCK_SKEW = timedelta(seconds=10)

# Token Blacklist Settings
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

# Authentication scheme - Django Ninja uses function-based auth
AUTHENTICATION_CLASSES = [
    'apps.accounts.authentication.JWTAuthentication',
]

# Permission classes - Django Ninja style (callable classes)
PERMISSION_CLASSES = [
    'apps.accounts.permissions.IsAuthenticated',
]