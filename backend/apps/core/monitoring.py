"""
MONITORING & METRICS
Application performance monitoring
"""

from django.http import JsonResponse
from django.db import connection
from django.utils import timezone
from functools import wraps
import time
import logging

logger = logging.getLogger(__name__)


class PerformanceMiddleware:
    """Track request performance."""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        start_time = time.time()
        
        response = self.get_response(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Add header
        response['X-Response-Time'] = f'{duration:.3f}s'
        
        # Log slow requests
        if duration > 1.0:
            logger.warning(
                f'Slow request: {request.method} {request.path} took {duration:.3f}s'
            )
        
        return response


class RequestLoggingMiddleware:
    """Log all requests."""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Log request
        logger.info(f'{request.method} {request.path}')
        
        response = self.get_response(request)
        
        # Log response
        logger.info(
            f'{request.method} {request.path} returned {response.status_code}'
        )
        
        return response


def track_metrics(view_func):
    """Decorator to track view metrics."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        start_time = time.time()
        
        try:
            response = view_func(request, *args, **kwargs)
            status = 'success'
        except Exception as e:
            status = 'error'
            raise
        finally:
            duration = time.time() - start_time
            
            # Log metrics
            logger.info(
                f'metrics: {view_func.__name__} '
                f'status={status} '
                f'duration={duration:.3f}s'
            )
        
        return response
    
    return wrapper


def get_metrics(request):
    """Return application metrics."""
    
    metrics = {
        'timestamp': timezone.now().isoformat(),
        'requests': {
            'total': 0,  # Would use Redis for actual counts
        },
        'database': {
            'connected': True,
        },
        'cache': {
            'enabled': True,
        },
    }
    
    return JsonResponse(metrics)


def get_stats(request):
    """Return system statistics."""
    
    import os
    import shutil
    
    # Get disk usage
    total, used, free = shutil.disk_usage('/')
    
    stats = {
        'system': {
            'disk': {
                'total': total,
                'used': used,
                'free': free,
                'percent': (used / total) * 100,
            },
            'memory': {
                'total': os.sysconf('SC_PHYS_PAGES') * os.sysconf('SC_PAGESIZE'),
            },
        },
        'timestamp': timezone.now().isoformat(),
    }
    
    return JsonResponse(stats)