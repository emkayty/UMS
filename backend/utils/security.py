"""
SECURITY HARDENING MODULE
Enterprise-grade security utilities
"""

import hashlib
import hmac
import re
import secrets
import string
from datetime import datetime, timedelta
from typing import Optional, Tuple
from django.conf import settings
from django.utils import timezone


class SecurityUtils:
    """
    Enterprise Security Utilities
    Implements bank-grade security practices
    """
    
    # Secure password generation
    @staticmethod
    def generate_secure_password(
        length: int = 16,
        include_special: bool = True
    ) -> str:
        """Generate cryptographically secure password"""
        chars = string.ascii_letters + string.digits
        if include_special:
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        while True:
            password = ''.join(secrets.choice(chars) for _ in range(length))
            if re.search(r'[A-Z]', password) and \
               re.search(r'[a-z]', password) and \
               re.search(r'\d', password):
                if include_special:
                    if re.search(r'[!@#$%^&*()_+\-=[\]{}|;:,.<>?]', password):
                        return password
                else:
                    return password
    
    # Token generation
    @staticmethod
    def generate_token(length: int = 32) -> str:
        """Generate secure random token"""
        return secrets.token_urlsafe(length)
    
    # Password hashing (Argon2-like using PBKDF2)
    @staticmethod
    def hash_password(password: str, salt: Optional[str] = None) -> Tuple[str, str]:
        """Hash password with salt"""
        if salt is None:
            salt = secrets.token_hex(16)
        
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode(),
            salt.encode(),
            100000  # iterations
        )
        return key.hex(), salt
    
    @staticmethod
    def verify_password(
        password: str, 
        hashed: str, 
        salt: str
    ) -> bool:
        """Verify hashed password"""
        key, _ = SecurityUtils.hash_password(password, salt)
        return hmac.compare_digest(key, hashed)
    
    # API Key generation
    @staticmethod
    def generate_api_key(prefix: str = "ums") -> str:
        """Generate API key with prefix"""
        return f"{prefix}_{secrets.token_hex(24)}"
    
    # Session security
    @staticmethod
    def generate_session_token() -> str:
        """Generate secure session token"""
        return secrets.token_urlsafe(32)
    
    # Password strength validation
    @staticmethod
    def validate_password_strength(password: str) -> dict:
        """Validate password strength"""
        result = {
            'valid': True,
            'score': 0,
            'feedback': []
        }
        
        if len(password) < 8:
            result['valid'] = False
            result['feedback'].append('Password must be at least 8 characters')
        else:
            result['score'] += 1
        
        if not re.search(r'[A-Z]', password):
            result['feedback'].append('Add uppercase letter')
        else:
            result['score'] += 1
        
        if not re.search(r'[a-z]', password):
            result['feedback'].append('Add lowercase letter')
        else:
            result['score'] += 1
        
        if not re.search(r'\d', password):
            result['feedback'].append('Add number')
        else:
            result['score'] += 1
        
        if not re.search(r'[!@#$%^&*()_+\-=[\]{}|;:,.<>?]', password):
            result['feedback'].append('Add special character')
        else:
            result['score'] += 1
        
        if password.lower() in ['password', '12345678', 'qwerty']:
            result['valid'] = False
            result['feedback'].append('Common password detected')
        
        return result
    
    # Rate limiting helper
    @staticmethod
    def get_client_ip(request) -> str:
        """Get client IP with proxy support"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '')


class AuditLogger:
    """
    Enterprise Audit Logging
    Security event logging for compliance
    """
    
    # Audit event types
    LOGIN_SUCCESS = 'login_success'
    LOGIN_FAILED = 'login_failed'
    LOGOUT = 'logout'
    PASSWORD_CHANGE = 'password_change'
    PASSWORD_RESET = 'password_reset'
    PERMISSION_DENIED = 'permission_denied'
    DATA_ACCESS = 'data_access'
    DATA_EXPORT = 'data_export'
    API_ACCESS = 'api_access'
    BLOCKED_IP = 'blocked_ip'
    
    @classmethod
    def log_event(
        cls,
        event_type: str,
        user: Optional[str] = None,
        ip_address: Optional[str] = None,
        details: Optional[dict] = None,
        tenant_id: Optional[str] = None
    ) -> dict:
        """Log security event"""
        event = {
            'timestamp': timezone.now().isoformat(),
            'type': event_type,
            'user': user,
            'ip_address': ip_address,
            'details': details or {},
            'tenant_id': tenant_id,
        }
        
        # In production, this would write to a secure audit log
        # For now, return the event
        return event
    
    @classmethod
    def log_login_success(cls, request, user, **kwargs):
        """Log successful login"""
        ip = SecurityUtils.get_client_ip(request)
        return cls.log_event(cls.LOGIN_SUCCESS, str(user), ip, **kwargs)
    
    @classmethod
    def log_login_failed(cls, request, email, reason='', **kwargs):
        """Log failed login"""
        ip = SecurityUtils.get_client_ip(request)
        return cls.log_event(cls.LOGIN_FAILED, email, ip, {'reason': reason}, **kwargs)
    
    @classmethod
    def log_permission_denied(cls, request, user, resource, **kwargs):
        """Log permission denied"""
        ip = SecurityUtils.get_client_ip(request)
        return cls.log_event(
            cls.PERMISSION_DENIED, 
            str(user), 
            ip, 
            {'resource': resource},
            **kwargs
        )


class InputSanitizer:
    """
    Input Sanitization
    Prevents XSS, SQL injection, and other attacks
    """
    
    # HTML dangerous patterns
    HTML_PATTERNS = [
        r'<script[^>]*>.*?</script>',
        r'javascript:',
        r'on\w+\s*=',
        r'<iframe[^>]*>',
        r'<object[^>]*>',
        r'<embed[^>]*>',
    ]
    
    # SQL injection patterns
    SQL_PATTERNS = [
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|ALTER|CREATE|TRUNCATE)\b)",
        r"(--|#|/\*|\*/)",
        r"(\bOR\b\s+\d+\s*=\s*\d+)",
        r"(\bAND\b\s+\d+\s*=\s*\d+)",
    ]
    
    @classmethod
    def sanitize_html(cls, value: str) -> str:
        """Remove dangerous HTML"""
        if not value:
            return value
        
        result = value
        for pattern in cls.HTML_PATTERNS:
            result = re.sub(pattern, '', result, flags=re.IGNORECASE)
        
        return result
    
    @classmethod
    def sanitize_sql(cls, value: str) -> str:
        """Detect SQL injection attempts"""
        if not value:
            return value
        
        for pattern in cls.SQL_PATTERNS:
            if re.search(pattern, value, re.IGNORECASE):
                # Log and reject
                raise ValueError("Potentially dangerous input detected")
        
        return value
    
    @classmethod
    def sanitize_filename(cls, filename: str) -> str:
        """Sanitize file upload names"""
        # Remove path separators
        filename = filename.replace('/', '').replace('\\', '')
        # Remove non-alphanumeric except . - _
        filename = re.sub(r'[^a-zA-Z0-9.\-_]', '', filename)
        # Limit length
        return filename[:255]
    
    @classmethod
    def validate_email(cls, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))


class TenantSecurity:
    """
    Multi-tenant Security
    Ensures data isolation between tenants
    """
    
    @classmethod
    def filter_by_tenant(cls, queryset, tenant_id: str, user):
        """Filter queryset by tenant"""
        # If user is superuser, skip tenant filter
        if user.is_superuser:
            return queryset
        
        # Check if tenant_id matches
        if hasattr(queryset.model, 'tenant_id'):
            return queryset.filter(tenant_id=tenant_id)
        
        # Check institution foreign key
        if hasattr(queryset.model, 'institution'):
            return queryset.filter(institution_id=tenant_id)
        
        return queryset
    
    @classmethod
    def validate_tenant_access(cls, user, tenant_id: str) -> bool:
        """Validate user has access to tenant"""
        if user.is_superuser:
            return True
        
        # Check user's tenant assignments
        if hasattr(user, 'tenants'):
            return user.tenants.filter(id=tenant_id).exists()
        
        return False


# Export utilities
__all__ = [
    'SecurityUtils',
    'AuditLogger',
    'InputSanitizer',
    'TenantSecurity',
]