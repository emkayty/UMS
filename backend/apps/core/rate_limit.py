"""
Rate Limiting
UMS Rate Limiting Middleware
"""

from django.core.cache import cache
from django.http import JsonResponse
from django.conf import settings
from functools import wraps
import time


# Rate limit cache keys
RATE_LIMIT_KEY = 'rate_limit:{ip}:{view}'
RATE_LIMIT_BURST_KEY = 'rate_limit_burst:{ip}'


class RateLimitExceeded(Exception):
    """Exception raised when rate limit is exceeded."""
    
    def __init__(self, message='Rate limit exceeded', retry_after=60):
        self.message = message
        self.retry_after = retry_after
        super().__init__(message)


def get_client_ip(request):
    """Get client IP address from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', 'unknown')


def check_rate_limit(request, limit=100, window=60):
    """
    Check if request is within rate limit.
    
    Args:
        request: HTTP request
        limit: Number of requests allowed in window
        window: Time window in seconds
    
    Returns:
        bool: True if within limit
    
    Raises:
        RateLimitExceeded: If limit exceeded
    """
    ip = get_client_ip(request)
    key = RATE_LIMIT_KEY.format(ip=ip, view=request.path)
    
    # Get current count
    count = cache.get(key, 0)
    
    if count >= limit:
        # Get retry time
        ttl = cache.ttl(key)
        raise RateLimitExceeded(
            message=f'Rate limit exceeded. Try again in {ttl} seconds.',
            retry_after=ttl or window
        )
    
    return True


def rate_limit(limit=100, window=60, key_func=None):
    """
    Decorator to apply rate limiting to a view.
    
    Args:
        limit: Number of requests allowed
        window: Time window in seconds
        key_func: Function to generate custom key
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Skip if DEBUG
            if settings.DEBUG:
                return view_func(request, *args, **kwargs)
            
            # Determine key
            if key_func:
                key = key_func(request)
            else:
                ip = get_client_ip(request)
                key = RATE_LIMIT_KEY.format(ip=ip, view=request.path)
            
            # Check and increment
            try:
                check_rate_limit(request, limit, window)
            except RateLimitExceeded as e:
                return JsonResponse(
                    {'error': e.message, 'retry_after': e.retry_after},
                    status=429,
                    headers={'Retry-After': str(e.retry_after)}
                )
            
            # Increment counter
            count = cache.incr(key, 1)
            
            # Set expiry on first request
            if count == 1:
                cache.set(key, 1, window)
            
            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator


def per_ip_rate_limit(limit=100, window=60):
    """Rate limit by IP address."""
    return rate_limit(limit, window)


def per_user_rate_limit(limit=100, window=60):
    """Rate limit by user."""
    def key_func(request):
        user_id = request.user.id if request.user.is_authenticated else 'anonymous'
        return f'rate_limit:user:{user_id}:{request.path}'
    
    return rate_limit(limit, window, key_func)


# API-specific rate limiting
class APIRateLimitMiddleware:
    """Middleware for API rate limiting."""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Only limit API requests
        if request.path.startswith('/api/'):
            try:
                # Different limits for different endpoints
                if request.path.startswith('/api/v1/auth'):
                    # Stricter for auth endpoints
                    check_rate_limit(request, limit=10, window=60)
                elif request.path.startswith('/api/v1/ai'):
                    # Strictest for AI endpoints
                    check_rate_limit(request, limit=20, window=60)
                else:
                    # Default API limit
                    check_rate_limit(request, limit=100, window=60)
            except RateLimitExceeded as e:
                return JsonResponse(
                    {'error': e.message},
                    status=429
                )
        
        return self.get_response(request)


# IP-based rate limiting for public endpoints
class IPRateLimitMiddleware:
    """Simple IP-based rate limiting."""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests = {}  # In production, use Redis
    
    def __call__(self, request):
        ip = get_client_ip(request)
        now = time.time()
        
        # Clean old requests
        self.requests = {k: v for k, v in self.requests.items() if now - v < 60}
        
        # Check limit
        if ip in self.requests and self.requests[ip] >= 100:
            return JsonResponse(
                {'error': 'Rate limit exceeded'},
                status=429
            )
        
        # Increment
        self.requests[ip] = self.requests.get(ip, 0) + 1
        
        return self.get_response(request)


# View decorators for specific endpoints
def auth_rate_limit(view):
    """Rate limit for authentication endpoints."""
    return per_ip_rate_limit(limit=5, window=60)(view)


def upload_rate_limit(view):
    """Rate limit for file uploads."""
    return per_ip_rate_limit(limit=10, window=3600)(view)


def api_search_rate_limit(view):
    """Rate limit for search endpoints."""
    return per_user_rate_limit(limit=50, window=60)(view)


# Helper function to get rate limit status
def get_rate_limit_status(request):
    """Get current rate limit status."""
    ip = get_client_ip(request)
    key = RATE_LIMIT_KEY.format(ip=ip, view=request.path)
    
    count = cache.get(key, 0)
    ttl = cache.ttl(key)
    
    return {
        'ip': ip,
        'requests': count,
        'limit': 100,
        'remaining': max(0, 100 - count),
        'reset_in': ttl or 60,
    }


# Example usage in views:
"""
from apps.core.rate_limit import rate_limit, auth_rate_limit

@rate_limit(limit=10, window=60)
def login_view(request):
    # Only 10 requests per minute
    ...

@auth_rate_limit
def change_password_view(request):
    # Only 5 requests per minute
    ...
"""