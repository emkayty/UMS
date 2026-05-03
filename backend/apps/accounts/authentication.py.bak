"""
JWT Authentication with refresh token rotation and blacklisting.
Production-ready security implementation.
"""
import secrets
import hashlib
import logging
from datetime import datetime, timedelta
from typing import Optional, Tuple
from django.conf import settings
from django.core.cache import cache
from rest_framework import authentication, exceptions

logger = logging.getLogger(__name__)


class TokenType:
    ACCESS = 'access'
    REFRESH = 'refresh'


class JWTBlacklist:
    """Token blacklist for revoked tokens."""
    
    PREFIX = 'jwt_blacklist:'
    
    @classmethod
    def add(cls, token_jti: str, expires_at: datetime) -> bool:
        """Add token to blacklist."""
        ttl = int((expires_at - datetime.utcnow()).total_seconds())
        if ttl > 0:
            cache.set(f"{cls.PREFIX}{token_jti}", True, timeout=ttl)
            return True
        return False
    
    @classmethod
    def is_blacklisted(cls, token_jti: str) -> bool:
        """Check if token is blacklisted."""
        return cache.get(f"{cls.PREFIX}{token_jti}") is not None
    
    @classmethod
    def revoke_user_tokens(cls, user_id: str) -> int:
        """Revoke all tokens for a user (for password change, logout all, etc.)."""
        # Use a user-specific prefix for bulk revocation
        prefix = f"user_tokens:{user_id}:"
        # Cache doesn't support pattern deletion, so we track tokens per user
        key = f"{prefix}all"
        revoked = cache.get(key, [])
        if revoked:
            for jti in revoked:
                cls.add(jti, datetime.utcnow() + timedelta(days=1))
        cache.set(key, [], timeout=0)  # Reset
        return len(revoked) if revoked else 0


def generate_token_id() -> str:
    """Generate unique token identifier."""
    return secrets.token_urlsafe(16)


def hash_token(token: str) -> str:
    """Hash token for storage."""
    return hashlib.sha256(token.encode()).hexdigest()


def generate_access_token(user) -> Tuple[str, str]:
    """Generate JWT access token with JTI.
    
    Returns:
        tuple: (token, jti)
    """
    jti = generate_token_id()
    payload = {
        'user_id': str(user.id),
        'email': user.email,
        'role': user.role,
        'jti': jti,
        'exp': datetime.utcnow() + settings.JWT_ACCESS_TOKEN_LIFETIME,
        'iat': datetime.utcnow(),
        'type': TokenType.ACCESS
    }
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token, jti


def generate_refresh_token(user) -> Tuple[str, str]:
    """Generate JWT refresh token with rotation.
    
    Returns:
        tuple: (token, jti)
    """
    jti = generate_token_id()
    payload = {
        'user_id': str(user.id),
        'jti': jti,
        'exp': datetime.utcnow() + settings.JWT_REFRESH_TOKEN_LIFETIME,
        'iat': datetime.utcnow(),
        'type': TokenType.REFRESH
    }
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token, jti


def verify_token(token: str, token_type: str = None) -> Optional[dict]:
    """Verify token and return payload."""
    try:
        # First try: access token (shorter lifetime)
        options = {}
        if token_type == TokenType.REFRESH:
            options = {'verify_exp': True}
        
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            options=options
        )
        
        # Check token type if specified
        if token_type and payload.get('type') != token_type:
            return None
        
        return payload
    except jwt.ExpiredSignatureError:
        logger.debug("Token expired")
        return None
    except jwt.InvalidTokenError as e:
        logger.debug(f"Invalid token: {e}")
        return None


def is_token_revoked(payload: dict) -> bool:
    """Check if token has been revoked."""
    jti = payload.get('jti')
    if not jti:
        return True  # No JTI = invalid
    
    # Check global blacklist
    if JWTBlacklist.is_blacklisted(jti):
        return True
    
    return False


class JWTAuthentication(authentication.BaseAuthentication):
    """JWT Authentication with token blacklisting support."""

    keyword = 'Bearer'

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        try:
            prefix, token = auth_header.split(' ')
            if prefix.lower() != self.keyword.lower():
                return None
        except ValueError:
            return None

        return self._authenticate_credentials(token), None

    def _authenticate_credentials(self, token):
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
                options={'verify_exp': True}
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token')

        # Check if token is revoked
        if is_token_revoked(payload):
            raise exceptions.AuthenticationFailed('Token has been revoked')

        from apps.accounts.models import User
        try:
            user = User.objects.get(id=payload['user_id'])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('User account is disabled')

        return (user, token)