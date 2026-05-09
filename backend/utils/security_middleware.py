"""
Session Security Middleware
Enforces session expiry and security
"""

import time
from django.utils import timezone
from django.http import HttpRequest
from django.conf import settings


class SessionExpiryMiddleware:
    """
    Middleware to enforce session expiry
    - Max session duration
    - Idle timeout
    - Absolute session timeout
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # Config from settings
        self.max_session_duration = getattr(
            settings, 
            'SESSION_MAX_DURATION', 
            8 * 60 * 60  # 8 hours default
        )
        self.idle_timeout = getattr(
            settings,
            'SESSION_IDLE_TIMEOUT', 
            30 * 60  # 30 minutes
        )
    
    def __call__(self, request: HttpRequest):
        # Skip for unauthenticated users
        if not request.user.is_authenticated:
            return self.get_response(request)
        
        # Get session
        session = getattr(request, 'session', None)
        if not session:
            return self.get_response(request)
        
        # Check session creation time
        created = session.get('_session_created_at')
        if not created:
            session['_session_created_at'] = time.time()
            created = time.time()
        
        # Check absolute timeout (max session duration)
        elapsed = time.time() - created
        if elapsed > self.max_session_duration:
            # Session expired - force re-login
            from django.contrib.auth import logout
            logout(request)
            return self._session_expired_response(
                request,
                'Session expired. Please login again.'
            )
        
        # Check idle timeout
        last_activity = session.get('_last_activity_at', created)
        idle_elapsed = time.time() - last_activity
        
        if idle_elapsed > self.idle_timeout:
            # Idle timeout - force re-login
            from django.contrib.auth import logout
            logout(request)
            return self._session_expired_response(
                request,
                'You have been idle too long. Please login again.'
            )
        
        # Update last activity
        session['_last_activity_at'] = time.time()
        
        return self.get_response(request)
    
    def _session_expired_response(self, request, message):
        """Return appropriate response for session expiry"""
        from django.http import JsonResponse
        
        # Check if API request
        if request.path.startswith('/api/') or request.headers.get('Accept') == 'application/json':
            return JsonResponse({
                'error': 'session_expired',
                'message': message,
                'code': 'SESSION_EXPIRED',
            }, status=401)
        
        # Redirect to login for web
        from django.shortcuts import redirect
        from django.urls import reverse
        login_url = reverse('login') + f'?next={request.path}'
        return redirect(login_url)


class TenantContextMiddleware:
    """
    Middleware to set tenant context from request
    Extracts tenant_id and sets it in Django settings
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request: HttpRequest):
        # Extract tenant from request
        tenant_id = None
        
        # 1. X-Tenant-ID header (API)
        tenant_id = request.headers.get('X-Tenant-ID')
        
        # 2. Subdomain
        if not tenant_id:
            host = request.get_host().split(':')[0]  # Remove port
            parts = host.split('.')
            if len(parts) >= 3 and parts[0] not in ['www', 'api', 'localhost']:
                tenant_id = parts[0]
        
        # 3. From authenticated user
        if not tenant_id and request.user.is_authenticated:
            if hasattr(request.user, 'institution_id'):
                tenant_id = str(request.user.institution_id)
            elif hasattr(request.user, 'tenant_id'):
                tenant_id = str(request.user.tenant_id)
        
        # Set in settings for TenantManager
        if tenant_id:
            settings.CURRENT_TENANT_ID = tenant_id
        else:
            # Check if superuser (can see all)
            if not (request.user.is_authenticated and request.user.is_superuser):
                settings.CURRENT_TENANT_ID = None
        
        settings.CURRENT_USER = request.user if request.user.is_authenticated else None
        
        try:
            response = self.get_response(request)
        finally:
            # Clear after request
            if hasattr(settings, 'CURRENT_TENANT_ID'):
                delattr(settings, 'CURRENT_TENANT_ID')
            if hasattr(settings, 'CURRENT_USER'):
                delattr(settings, 'CURRENT_USER')
        
        return response


class JWTTokenExpiryMiddleware:
    """
    Middleware to check JWT token expiry
    Enforces token expiration on API requests
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request: HttpRequest):
        # Only check for API requests
        if not request.path.startswith('/api/'):
            return self.get_response(request)
        
        # Skip auth endpoints
        if request.path.startswith('/api/auth/') and request.path != '/api/auth/me/':
            return self.get_response(request)
        
        # Check for JWT token
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]  # Remove 'Bearer '
            
            # Verify token (simple check - full verification is in auth endpoint)
            # This is just to catch expired tokens earlier
            try:
                from apps.accounts.jwt_config import decode_token
                payload = decode_token(token)
                
                if payload:
                    # Check expiration
                    exp = payload.get('exp', 0)
                    if exp and time.time() > exp:
                        from django.http import JsonResponse
                        return JsonResponse({
                            'error': 'token_expired',
                            'message': 'JWT token has expired',
                        }, status=401)
                        
            except Exception:
                pass  # Let the auth endpoint handle it
        
        return self.get_response(request)


# Export
__all__ = [
    'SessionExpiryMiddleware',
    'TenantContextMiddleware',
    'JWTTokenExpiryMiddleware',
]