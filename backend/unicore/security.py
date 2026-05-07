"""
Security Utilities for UMS

Security helpers and protections.
"""
import hashlib
import hmac
import secrets
import re
from typing import Optional
from django.conf import settings


def generate_token(length: int = 32) -> str:
    """Generate secure token"""
    return secrets.token_urlsafe(length)


def hash_password(password: str) -> str:
    """Hash password (using Django's hasher)"""
    from django.contrib.auth.hashers import make_password
    return make_password(password)


def verify_password(password: str, hashed: str) -> bool:
    """Verify password"""
    from django.contrib.auth.hashers import check_password
    return check_password(password, hashed)


def hash_string(text: str, salt: str = "") -> str:
    """Hash string with salt"""
    combined = f"{text}{salt}"
    return hashlib.sha256(combined.encode()).hexdigest()


def verify_signature(data: str, signature: str, secret: str) -> bool:
    """Verify HMAC signature"""
    expected = hmac.new(
        secret.encode(),
        data.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(signature, expected)


def sanitize_html(text: str) -> str:
    """Sanitize HTML"""
    # Remove script tags
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    # Remove on* event handlers
    text = re.sub(r' on\w+="[^"]*"', '', text, flags=re.IGNORECASE)
    return text


def sanitize_sql(text: str) -> str:
    """Sanitize for SQL (parameterize instead!)"""
    return text.replace("'", "''")


def generate_api_key() -> str:
    """Generate API key"""
    return f"sk_{secrets.token_urlsafe(32)}"


def mask_sensitive_data(data: str, visible: int = 4) -> str:
    """Mask sensitive data"""
    if len(data) <= visible:
        return "*" * len(data)
    return "*" * (len(data) - visible) + data[-visible:]


def check_password_strength(password: str) -> tuple:
    """Check password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain uppercase"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain lowercase"
    if not re.search(r'\d', password):
        return False, "Password must contain digit"
    return True, "Password is strong"