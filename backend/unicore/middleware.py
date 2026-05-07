"""
UMS Middleware - Request/Response Logging and Performance
"""
import time
import logging
import json
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

# Rate limit tracking
_rate_limit_headers = {
    'anon': '100',  # 100/day for anonymous
    'user': '1000',  # 1000/day for authenticated
}


class RequestLoggingMiddleware(MiddlewareMixin):
    """Log all requests and responses with timing"""
    
    def process_request(self, request):
        request.start_time = time.time()
        # Only log API requests
        if request.path.startswith('/api/'):
            logger.info(f"REQUEST: {request.method} {request.path}")
        return None
    
    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            # Add timing header for API requests
            if request.path.startswith('/api/'):
                response['X-Response-Time'] = f"{duration:.3f}s"
                logger.info(
                    f"RESPONSE: {request.method} {request.path} "
                    f"status={response.status_code} duration={duration:.3f}s"
                )
            # Log slow requests (>1 second)
            if duration > 1.0:
                logger.warning(
                    f"SLOW REQUEST: {request.method} {request.path} "
                    f"duration={duration:.3f}s"
                )
        return response


class RateLimitMiddleware(MiddlewareMixin):
    """Add rate limit headers to responses"""
    
    def process_response(self, request, response):
        if request.path.startswith('/api/'):
            # Check if authenticated
            if hasattr(request, 'user') and request.user and request.user.is_authenticated:
                response['X-RateLimit-Limit'] = '1000'
                response['X-RateLimit-Remaining'] = '999'
            else:
                response['X-RateLimit-Limit'] = '100'
                response['X-RateLimit-Remaining'] = '99'
        return response


class CORSMiddleware(MiddlewareMixin):
    """Handle CORS headers"""
    
    def process_response(self, request, response):
        # Add CORS headers
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response


class SecurityHeadersMiddleware(MiddlewareMixin):
    """Add security headers to all responses"""
    
    def process_response(self, request, response):
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response


class APIVersionMiddleware(MiddlewareMixin):
    """Add API version to responses"""
    
    def process_response(self, request, response):
        response['X-API-Version'] = '1.0'
        return response