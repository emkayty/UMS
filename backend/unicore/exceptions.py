"""
Custom Exception Handlers
UMS Global Error Handling
"""

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging
import traceback

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler for consistent API error responses.
    
    Format:
    {
        "error": {
            "code": "ERROR_CODE",
            "message": "Human readable message",
            "details": {} // Optional validation errors
        }
    }
    """
    response = exception_handler(exc, context)
    
    if response is not None:
        # Format DRF default errors
        error_data = {
            'code': 'error',
            'message': str(exc.detail) if hasattr(exc, 'detail') else str(exc),
        }
        
        if hasattr(exc, 'detail') and isinstance(exc.detail, dict):
            error_data['details'] = exc.detail
        
        response.data = {
            'error': error_data
        }
    
    return response


def global_exception_handler(request, exception):
    """
    Global exception handler for unhandled exceptions.
    """
    # Log the error
    logger.error(
        f'Unhandled exception: {exception}\n{traceback.format_exc()}'
    )
    
    # Return formatted error response
    return Response(
        {
            'error': {
                'code': 'internal_error',
                'message': 'An internal error occurred',
                'details': str(exception) if __import__('os').environ.get('DEBUG') == 'True' else None
            }
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


class APIError(Exception):
    """Base API error."""
    
    def __init__(self, message, code='error', status_code=status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(message)


class ValidationError(APIError):
    """Validation error."""
    
    def __init__(self, message, details=None):
        super().__init__(
            message=message,
            code='validation_error',
            status_code=status.HTTP_400_BAD_REQUEST
        )
        self.details = details


class AuthenticationError(APIError):
    """Authentication error."""
    
    def __init__(self, message='Authentication required'):
        super().__init__(
            message=message,
            code='authentication_failed',
            status_code=status.HTTP_401_UNAUTHORIZED
        )


class PermissionError(APIError):
    """Permission error."""
    
    def __init__(self, message='Permission denied'):
        super().__init__(
            message=message,
            code='permission_denied',
            status_code=status.HTTP_403_FORBIDDEN
        )


class NotFoundError(APIError):
    """Not found error."""
    
    def __init__(self, message='Resource not found'):
        super().__init__(
            message=message,
            code='not_found',
            status_code=status.HTTP_404_NOT_FOUND
        )


class ConflictError(APIError):
    """Conflict error."""
    
    def __init__(self, message='Resource conflict'):
        super().__init__(
            message=message,
            code='conflict',
            status_code=status.HTTP_409_CONFLICT
        )


# Error response helper
def format_error(message, code='error', status_code=400, details=None):
    """Format error response."""
    error = {
        'error': {
            'code': code,
            'message': message,
        }
    }
    
    if details:
        error['error']['details'] = details
    
    return Response(error, status=status_code)


def handle_404(request, exception):
    """Handle 404 errors."""
    return format_error(
        message='The requested resource was not found',
        code='not_found',
        status_code=404
    )


def handle_500(request, exception):
    """Handle 500 errors."""
    logger.error(f'500 Error: {exception}')
    
    return format_error(
        message='An internal server error occurred',
        code='internal_error',
        status_code=500
    )


def handle_403(request, exception):
    """Handle 403 errors."""
    return format_error(
        message='Permission denied',
        code='permission_denied',
        status_code=403
    )


def handle_400(request, exception):
    """Handle 400 errors."""
    return format_error(
        message=str(exception),
        code='bad_request',
        status_code=400
    )


def handle_401(request, exception):
    """Handle 401 errors."""
    return format_error(
        message='Authentication required',
        code='authentication_failed',
        status_code=401
    )