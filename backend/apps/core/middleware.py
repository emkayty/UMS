"""
Middleware for UMS
Request/Response Processing
"""

from django.http import JsonResponse
from django.utils import timezone
from django.conf import settings
import time
import logging
import json

logger = logging.getLogger(__name__)


# ============================================================
# TIMING MIDDLEWARE
# ============================================================

class TimingMiddleware:
    """Measure request processing time."""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        start_time = time.time()
        
        response = self.get_response(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Add timing header
        response['X-Process-Time'] = str(process_time)
        
        # Log slow requests
        if process_time > 1.0:
            logger.warning(
                f'Slow request: {request.path} took {process_time:.2f}s'
            )
        
        return response


# ============================================================
# CORS MIDDLEWARE (Enhanced)
# ============================================================

class CorsMiddleware:
    """Enhanced CORS handling."""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Allow all origins in development
        if settings.DEBUG:
            response['Access-Control-Allow-Origin'] = '*'
        
        # Allow credentials
        response['Access-Control-Allow-Credentials'] = 'true'
        
        # Allow methods
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        
        # Allow headers
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        
        # Cache preflight
        response['Access-Control-Max-Age'] = '3600'
        
        return response


# ============================================================
# SECURITY MIDDLEWARE
# ============================================================

class SecurityHeadersMiddleware:
    """Add security headers."""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Prevent clickjacking
        response['X-Frame-Options'] = 'DENY'
        
        # XSS protection
        response['X-XSS-Protection'] = '1; mode=block'
        
        # Content type sniffing
        response['X-Content-Type-Options'] = 'nosniff'
        
        # Referrer policy
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Permissions policy
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        return response


# ============================================================
# RATE LIMITING MIDDLEWARE
# ============================================================

class RateLimitMiddleware:
    """Simple rate limiting."""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests = {}  # Use Redis in production
    
    def __call__(self, request):
        # Skip for DEBUG
        if settings.DEBUG:
            return self.get_response(request)
        
        # Get client IP
        ip = self.get_client_ip(request)
        
        # Check rate limit
        if self.is_rate_limited(ip):
            return JsonResponse(
                {'error': 'Rate limit exceeded'},
                status=429
            )
        
        return self.get_response(request)
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', 'unknown')
    
    def is_rate_limited(self, ip):
        import time
        now = time.time()
        
        # Clean old requests
        self.requests = {k: v for k, v in self.requests.items() if now - v < 60}
        
        # Check limit (100 per minute)
        if ip in self.requests and self.requests[ip] >= 100:
            return True
        
        # Increment
        self.requests[ip] = self.requests.get(ip, 0) + 1
        return False


# ============================================================
# REQUEST LOGGING MIDDLEWARE
# ============================================================

class RequestLoggingMiddleware:
    """Log all requests."""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Log request
        logger.info(
            f'Request: {request.method} {request.path} '
            f'from {self.get_client_ip(request)}'
        )
        
        response = self.get_response(request)
        
        # Log response
        logger.info(
            f'Response: {request.method} {request.path} '
            f'status={response.status_code}'
        )
        
        return response
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', 'unknown')


# ============================================================
# JSON RESPONSE MIDDLEWARE
# ============================================================

class JsonResponseMiddleware:
    """Ensure JSON responses."""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # For API requests, ensure JSON
        if request.path.startswith('/api/'):
            response['Content-Type'] = 'application/json'
        
        return response


# ============================================================
# AUTH MIDDLEWARE
# ============================================================

class AuthMiddleware:
    """Handle authentication."""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Skip for public endpoints
        public_paths = [
            '/api/v1/auth/login',
            '/api/v1/auth/register',
            '/health',
            '/api/v1/public',
        ]
        
        if request.path in public_paths:
            return self.get_response(request)
        
        # Check authentication
        if not request.user.is_authenticated:
            return JsonResponse(
                {'error': 'Authentication required'},
                status=401
            )
        
        return self.get_response(request)