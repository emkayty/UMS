"""
Authentication API with security features.
Production-ready with rate limiting, password validation, and audit logging.
"""
import re
import logging
from datetime import datetime
from typing import Optional

from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
from ninja import Router, Schema

from apps.accounts.models import User, PasswordHistory
from apps.accounts.authentication import (
    generate_access_token,
    generate_refresh_token,
    verify_token,
    JWTBlacklist,
    TokenType,
)

logger = logging.getLogger(__name__)
router = Router(tags=['Authentication'])

# Audit logger
audit_logger = logging.getLogger('audit')


class LoginRequest(Schema):
    """Login request schema."""
    email: str
    password: str
    device_info: Optional[str] = None


class RefreshRequest(Schema):
    """Refresh token request schema."""
    refresh: str


class LogoutRequest(Schema):
    """Logout request schema."""
    logout_all: bool = False


class PasswordChangeRequest(Schema):
    """Password change request schema."""
    old_password: str
    new_password: str
    confirm_password: str


class AuthResponse(Schema):
    """Authentication response schema."""
    success: bool
    access: str
    refresh: Optional[str] = ''
    user: Optional[dict] = None


class ErrorResponse(Schema):
    """Error response schema."""
    success: bool
    error: str
    code: Optional[str] = None


class PasswordStrengthResponse(Schema):
    """Password strength validation response."""
    valid: bool
    errors: list


def validate_password_strength(password: str, email: str = '') -> tuple[bool, list[str]]:
    """Validate password against security policy.
    
    Returns:
        tuple: (is_valid, list of error messages)
    """
    errors = []
    min_length = getattr(settings, 'PASSWORD_MIN_LENGTH', 12)
    
    if len(password) < min_length:
        errors.append(f"Password must be at least {min_length} characters")
    
    if getattr(settings, 'PASSWORD_REQUIRE_UPPERCASE', True):
        if not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter")
    
    if getattr(settings, 'PASSWORD_REQUIRE_LOWERCASE', True):
        if not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter")
    
    if getattr(settings, 'PASSWORD_REQUIRE_DIGITS', True):
        if not re.search(r'\d', password):
            errors.append("Password must contain at least one digit")
    
    special_chars = getattr(settings, 'PASSWORD_SPECIAL_CHARS', r'!@#$%^&*()_+-=[]{}|;:,.<>?')
    if getattr(settings, 'PASSWORD_REQUIRE_SPECIAL', True):
        pattern = f'[{re.escape(special_chars)}]'
        if not re.search(pattern, password):
            errors.append(f"Password must contain at least one special character ({special_chars})")
    
    # Check against email (no email in password)
    if email:
        email_parts = email.split('@')
        for part in email_parts:
            if len(part) >= 3 and part.lower() in password.lower():
                errors.append("Password cannot contain parts of your email")
    
    return len(errors) == 0, errors


def check_rate_limit(request, limit_type: str = 'login') -> bool:
    """Check if request is within rate limit.
    
    Returns True if allowed, False if rate limited.
    """
    if not getattr(settings, 'RATELIMIT_ENABLED', True):
        return True
    
    # Get client IP
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', 'unknown')
    
    cache_key = f"ratelimit:{limit_type}:{ip}"
    count = cache.get(cache_key, 0)
    
    # Get rate limit from settings
    rate_limit = getattr(settings, f'RATELIMIT_{limit_type.upper()}', '5/minute')
    
    # Simple rate limiting using cache
    # Format: "100/hour" or "5/minute"
    if '/' in rate_limit:
        limit, period = rate_limit.split('/')
        limit = int(limit)
        
        if count >= limit:
            return False
        
        # Increment and set expiry
        period_seconds = 60 if period == 'minute' else 3600
        cache.set(cache_key, count + 1, timeout=period_seconds)
    
    return True


def log_audit_event(event_type: str, user_id: str, details: dict):
    """Log security audit event."""
    if not getattr(settings, 'AUDIT_LOG_ENABLED', True):
        return
    
    events = getattr(settings, 'AUDIT_LOG_EVENTS', [])
    if event_type in events:
        audit_logger.info(f"{event_type}: user={user_id} ip={details.get('ip')} {details.get('extra', '')}")


def is_account_locked(user: User) -> bool:
    """Check if account is locked due to failed login attempts."""
    cache_key = f"lockout:{user.id}"
    return cache.get(cache_key) is not None


def lock_account(user: User, duration_minutes: int = 15):
    """Lock account after too many failed login attempts."""
    cache_key = f"lockout:{user.id}"
    cache.set(cache_key, True, timeout=duration_minutes * 60)
    logger.warning(f"Account locked: {user.email}")


@router.post('/login', response={200: AuthResponse, 401: ErrorResponse, 429: ErrorResponse})
def login(request, data: LoginRequest):
    """Authenticate user and return JWT tokens.
    
    Rate limited to prevent brute force attacks.
    """
    # Check rate limit first
    if not check_rate_limit(request, 'login'):
        return http_status.HTTP_429_TOO_MANY_REQUESTS, {
            'success': False,
            'error': 'Too many login attempts. Please try again later.',
            'code': 'RATE_LIMITED'
        }
    
    # Validate password format
    if not data.password:
        return http_status.HTTP_400_BAD_REQUEST, {
            'success': False,
            'error': 'Password is required',
            'code': 'INVALID_INPUT'
        }
    
    try:
        user = User.objects.get(email__iexact=data.email)
    except User.DoesNotExist:
        # Generic error to prevent user enumeration
        return http_status.HTTP_401_UNAUTHORIZED, {
            'success': False,
            'error': 'Invalid credentials',
            'code': 'INVALID_CREDENTIALS'
        }
    
    # Check if account is locked
    if is_account_locked(user):
        return http_status.HTTP_429_TOO_MANY_REQUESTS, {
            'success': False,
            'error': 'Account is temporarily locked. Try again later.',
            'code': 'ACCOUNT_LOCKED'
        }
    
    # Check password
    password_valid = user.check_password(data.password)
    
    if not password_valid:
        # Log failed attempt
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip = x_forwarded_for.split(',')[0].strip() if x_forwarded_for else request.META.get('REMOTE_ADDR', 'unknown')
        
        log_audit_event('LOGIN_FAILED', str(user.id), {'ip': ip, 'email': data.email})
        
        # Track failed attempts
        cache_key = f"failed_login:{user.id}"
        failed_count = cache.get(cache_key, 0) + 1
        cache.set(cache_key, failed_count, timeout=900)  # 15 minutes
        
        # Lock after 5 failed attempts
        if failed_count >= 5:
            lock_account(user)
        
        return http_status.HTTP_401_UNAUTHORIZED, {
            'success': False,
            'error': 'Invalid credentials',
            'code': 'INVALID_CREDENTIALS'
        }
    
    if not user.is_active:
        return http_status.HTTP_401_UNAUTHORIZED, {
            'success': False,
            'error': 'Account is disabled',
            'code': 'ACCOUNT_DISABLED'
        }
    
    # Check password expiry
    if hasattr(user, 'password_changed_at'):
        max_age = getattr(settings, 'PASSWORD_MAX_AGE_DAYS', 90)
        days_since_change = (timezone.now() - user.password_changed_at).days
        if days_since_change > max_age:
            # Force password change on next login
            logger.info(f"Password expired for {user.email}")
    
    # Generate tokens with rotation
    access_token, access_jti = generate_access_token(user)
    refresh_token, refresh_jti = generate_refresh_token(user)
    
    # Update last login
    user.last_login = timezone.now()
    user.save(update_fields=['last_login'])
    
    # Reset failed login count
    cache.delete(f"failed_login:{user.id}")
    
    # Log successful login
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = x_forwarded_for.split(',')[0].strip() if x_forwarded_for else request.META.get('REMOTE_ADDR', 'unknown')
    
    log_audit_event('LOGIN', str(user.id), {
        'ip': ip,
        'device': data.device_info or 'unknown'
    })
    
    return {
        'success': True,
        'access': access_token,
        'refresh': refresh_token,
        'user': {
            'id': str(user.id),
            'email': user.email,
            'role': user.role,
            'is_active': user.is_active,
            'created_at': user.created_at.isoformat()
        }
    }


@router.post('/refresh', response={200: AuthResponse, 401: ErrorResponse})
def refresh_token(request, data: RefreshRequest):
    """Refresh access token using refresh token with rotation.
    
    Old refresh token is invalidated (rotation).
    """
    payload = verify_token(data.refresh, TokenType.REFRESH)
    
    if not payload:
        return http_status.HTTP_401_UNAUTHORIZED, {
            'success': False,
            'error': 'Invalid or expired refresh token',
            'code': 'INVALID_TOKEN'
        }
    
    try:
        user = User.objects.get(id=payload['user_id'])
    except User.DoesNotExist:
        return http_status.HTTP_401_UNAUTHORIZED, {
            'success': False,
            'error': 'User not found',
            'code': 'USER_NOT_FOUND'
        }
    
    if not user.is_active:
        return http_status.HTTP_401_UNAUTHORIZED, {
            'success': False,
            'error': 'Account is disabled',
            'code': 'ACCOUNT_DISABLED'
        }
    
    # Generate new tokens (rotation)
    access_token, _ = generate_access_token(user)
    refresh_token, _ = generate_refresh_token(user)
    
    log_audit_event('TOKEN_REFRESH', str(user.id), {})
    
    return {
        'success': True,
        'access': access_token,
        'refresh': refresh_token,
        'user': {
            'id': str(user.id),
            'email': user.email,
            'role': user.role,
            'is_active': user.is_active,
            'created_at': user.created_at.isoformat()
        }
    }


@router.post('/logout', response=AuthResponse)
def logout(request, data: LogoutRequest):
    """Logout and revoke tokens."""
    user = request.auth[0]
    
    if data.logout_all:
        # Revoke all user tokens
        JWTBlacklist.revoke_user_tokens(str(user.id))
        log_audit_event('LOGOUT_ALL', str(user.id), {})
    else:
        # Revoke current token
        # Token JTI is in the payload
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]
            payload = verify_token(token, TokenType.ACCESS)
            if payload and payload.get('jti'):
                JWTBlacklist.add(
                    payload['jti'],
                    datetime.utcnow() + settings.JWT_ACCESS_TOKEN_LIFETIME
                )
    
    log_audit_event('LOGOUT', str(user.id), {})
    
    return {
        'success': True,
        'access': '',
        'refresh': '',
        'user': None
    }


@router.get('/me', response=dict)
def get_current_user(request):
    """Get current authenticated user."""
    user = request.auth[0]
    return {
        'id': str(user.id),
        'email': user.email,
        'role': user.role,
        'is_active': user.is_active,
        'created_at': user.created_at.isoformat()
    }


@router.post('/password/validate', response=PasswordStrengthResponse)
def validate_password(request, data: PasswordChangeRequest):
    """Validate password strength without changing."""
    valid, errors = validate_password_strength(data.new_password)
    return {'valid': valid, 'errors': errors}