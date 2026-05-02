"""
HEALTH CHECK ENDPOINT
System health monitoring
"""

from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
from django.utils import timezone
import os


def health(request):
    """Health check endpoint for monitoring."""
    
    status = {
        'status': 'healthy',
        'timestamp': timezone.now().isoformat(),
        'version': '2.0.0',
        'checks': {}
    }
    
    # Database check
    try:
        connection.ensure_connection()
        status['checks']['database'] = 'healthy'
    except Exception as e:
        status['checks']['database'] = f'unhealthy: {str(e)}'
        status['status'] = 'degraded'
    
    # Cache check
    try:
        cache.set('health_check', 'ok', 10)
        if cache.get('health_check') == 'ok':
            status['checks']['cache'] = 'healthy'
        else:
            status['checks']['cache'] = 'unhealthy'
            status['status'] = 'degraded'
    except Exception as e:
        status['checks']['cache'] = f'unhealthy: {str(e)}'
    
    # Disk space check
    try:
        import shutil
        total, used, free = shutil.disk_usage('/')
        percent = (used / total) * 100
        status['checks']['disk'] = f'{percent:.1f}% used'
        
        if percent > 90:
            status['status'] = 'degraded'
    except Exception:
        pass
    
    # Memory check
    try:
        import resource
        usage = resource.getrusage(resource.RUSAGE_SELF)
        status['checks']['memory'] = f'{usage.ru_maxrss} KB'
    except Exception:
        pass
    
    # Environment info
    status['environment'] = {
        'debug': os.environ.get('DEBUG', 'False') == 'True',
        'python_version': os.environ.get('PYTHON_VERSION', 'N/A'),
    }
    
    return JsonResponse(status, status=200 if status['status'] == 'healthy' else 503)


def ready(request):
    """Readiness check - returns 200 if app can serve traffic."""
    
    # Quick DB check
    try:
        connection.ensure_connection()
        return JsonResponse({'ready': True})
    except Exception:
        return JsonResponse({'ready': False}, status=503)


def live(request):
    """Liveness check - returns 200 if app is running."""
    return JsonResponse({'alive': True})