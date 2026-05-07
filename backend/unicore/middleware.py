"""
UMS Middleware - Request/Response Logging and Performance
"""
import time
import logging
import json
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(MiddlewareMixin):
    """Log all requests and responses"""
    
    def process_request(self, request):
        request.start_time = time.time()
        logger.info(f"REQUEST: {request.method} {request.path}")
        return None
    
    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            logger.info(
                f"RESPONSE: {request.method} {request.path} "
                f"status={response.status_code} duration={duration:.3f}s"
            )
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