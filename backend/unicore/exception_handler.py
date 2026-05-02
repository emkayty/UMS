"""
Custom exception handler with securityfocused error responses.
Does not expose internal details in production.
"""
import sys
import logging
import traceback

from django.conf import settings
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """Custom exception handler for consistent API responses.
    
    Security features:
    - Never expose stack traces in production
    - Never expose sensitive data (settings, paths, etc.)
    - Log full details server-side for debugging
    """
    response = exception_handler(exc, context)
    
    # Get exception details for logging (not for client)
    request = context.get('request')
    exc_info = sys.exc_info()
    
    if response is not None:
        if response.status_code == 401:
            response.data = {
                'success': False,
                'error': 'Authentication required',
                'code': 'AUTH_REQUIRED'
            }
        elif response.status_code == 403:
            response.data = {
                'success': False,
                'error': 'Permission denied',
                'code': 'PERMISSION_DENIED'
            }
        elif response.status_code == 404:
            response.data = {
                'success': False,
                'error': 'Resource not found',
                'code': 'NOT_FOUND'
            }
        elif response.status_code == 400:
            # Validation error - include details but sanitize
            error_detail = _sanitize_error_detail(
                getattr(exc, 'detail', None)
            )
            response.data = {
                'success': False,
                'error': error_detail,
                'code': 'VALIDATION_ERROR'
            }
        else:
            response.data = {
                'success': False,
                'error': 'An error occurred',
                'code': 'SERVER_ERROR'
            }
    else:
        # Unhandled exception - log full details
        _log_exception(request, exc, exc_info)
        
        response = Response(
            {
                'success': False,
                'error': 'Internal server error',
                'code': 'INTERNAL_ERROR'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Add security headers
    response['X-Content-Type-Options'] = 'nosniff'
    response['X-Frame-Options'] = 'DENY'
    response['X-XSS-Protection'] = '1; mode=block'
    
    return response


def _sanitize_error_detail(detail):
    """Sanitize error details to prevent information leakage."""
    if detail is None:
        return 'An error occurred'
    
    if isinstance(detail, dict):
        # Remove any keys that might contain sensitive data
        sensitive_keys = {'password', 'token', 'secret', 'key', 'auth', 'credential'}
        sanitized = {}
        for k, v in detail.items():
            if k.lower() not in sensitive_keys:
                sanitized[k] = v
        return sanitized
    
    return str(detail)


def _log_exception(request, exc, exc_info):
    """Log exception with full details for debugging."""
    # Log to server logs
    logger.exception(
        'Unhandled exception: %s\nRequest: %s\nTraceback: %s',
        exc,
        getattr(request, 'path', 'unknown'),
        ''.join(traceback.format_exception(*exc_info))
    )
    
    # Also log to audit if enabled
    if getattr(settings, 'AUDIT_LOG_ENABLED', False):
        audit_logger = logging.getLogger('audit')
        audit_logger.error(
            'EXCEPTION: %s path=%s method=%s user=%s',
            exc,
            getattr(request, 'path', 'unknown'),
            getattr(request, 'method', 'unknown'),
            getattr(request, 'user', 'anonymous')
        )