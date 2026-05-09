"""
Django Prometheus Metrics API
Provides /metrics endpoint for Prometheus monitoring
"""

import os
import time
import psutil
from datetime import datetime
from django.http import JsonResponse
from django.views import View
from django.db import connection
from django.conf import settings


class MetricsView(View):
    """
    Prometheus metrics endpoint
    Returns system, application, and database metrics
    """
    
    def get(self, request):
        # Check auth for production
        if not settings.DEBUG:
            auth_header = request.headers.get('Authorization')
            expected = f"Bearer {os.environ.get('METRICS_AUTH_TOKEN', 'ums-metrics-token')}"
            if auth_header != expected:
                return JsonResponse({'error': 'Unauthorized'}, status=401)
        
        metrics = self._collect_metrics()
        return JsonResponse(metrics, status=200)
    
    def _collect_metrics(self):
        """Collect all metrics"""
        return {
            # System metrics
            'system': self._get_system_metrics(),
            # Application metrics
            'application': self._get_application_metrics(),
            # Database metrics
            'database': self._get_database_metrics(),
            # Cache metrics
            'cache': self._get_cache_metrics(),
            # Timestamp
            'timestamp': datetime.now().isoformat(),
        }
    
    def _get_system_metrics(self):
        """Get system-level metrics"""
        return {
            # CPU
            'cpu_percent': psutil.cpu_percent(interval=0.1),
            'cpu_count': psutil.cpu_count(),
            'cpu_count_logical': psutil.cpu_count(logical=True),
            
            # Memory
            'memory_total': psutil.virtual_memory().total,
            'memory_available': psutil.virtual_memory().available,
            'memory_percent': psutil.virtual_memory().percent,
            'memory_used': psutil.virtual_memory().used,
            
            # Disk
            'disk_total': psutil.disk_usage('/').total,
            'disk_used': psutil.disk_usage('/').used,
            'disk_free': psutil.disk_usage('/').free,
            'disk_percent': psutil.disk_usage('/').percent,
            
            # Load average (if available)
            'load_average': getattr(os, 'getloadavg', lambda: (0, 0, 0))(),
        }
    
    def _get_application_metrics(self):
        """Get application-level metrics"""
        return {
            # Django settings
            'debug': settings.DEBUG,
            'app_name': 'ums',
            'version': os.environ.get('APP_VERSION', '1.0.0'),
            
            # Installed apps count
            'installed_apps': len(settings.INSTALLED_APPS),
            
            # Middleware count
            'middleware_count': len(settings.MIDDLEWARE),
            
            # Database connections
            'db_connections': self._get_db_connection_count(),
        }
    
    def _get_database_metrics(self):
        """Get database metrics"""
        try:
            with connection.cursor() as cursor:
                # Get database size (PostgreSQL)
                try:
                    cursor.execute("""
                        SELECT pg_size_pretty(pg_database_size(current_database()))
                    """)
                    db_size = cursor.fetchone()[0]
                except:
                    db_size = 'unknown'
                
                # Get table counts
                try:
                    cursor.execute("""
                        SELECT COUNT(*) FROM information_schema.tables 
                        WHERE table_schema = 'public'
                    """)
                    table_count = cursor.fetchone()[0]
                except:
                    table_count = 0
                
                return {
                    'engine': 'postgresql',
                    'size': db_size,
                    'tables': table_count,
                    'connections': self._get_db_connection_count(),
                }
        except Exception as e:
            return {'error': str(e)}
    
    def _get_cache_metrics(self):
        """Get cache metrics"""
        try:
            from django.core.cache import caches
            cache = caches['default']
            
            return {
                'backend': getattr(cache, 'class', 'unknown'),
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _get_db_connection_count(self):
        """Get database connection count"""
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT COUNT(*) FROM pg_stat_activity 
                    WHERE datname = current_database()
                """)
                return cursor.fetchone()[0]
        except:
            return 0


def prometheus_metrics(request):
    """
    Simple function-based view for /metrics endpoint
    Usage: Add to urls.py: path('metrics/', views.prometheus_metrics)
    """
    # Check auth for production
    if not settings.DEBUG:
        auth_header = request.headers.get('Authorization')
        expected = f"Bearer {os.environ.get('METRICS_AUTH_TOKEN', 'ums-metrics-token')}"
        if auth_header != expected:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    # CPU and memory
    cpu_percent = psutil.cpu_percent(interval=0.1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    # Build Prometheus format output
    lines = [
        f"# HELP ums_cpu_percent CPU usage percentage",
        f"# TYPE ums_cpu_percent gauge",
        f"ums_cpu_percent {cpu_percent}",
        f"",
        f"# HELP ums_memory_percent Memory usage percentage",
        f"# TYPE ums_memory_percent gauge",
        f"ums_memory_percent {memory.percent}",
        f"",
        f"# HELP ums_memory_available Available memory in bytes",
        f"# TYPE ums_memory_available gauge",
        f"ums_memory_available {memory.available}",
        f"",
        f"# HELP ums_disk_free Free disk space in bytes",
        f"# TYPE ums_disk_free gauge",
        f"ums_disk_free {disk.free}",
        f"",
        f"# HELP ums_disk_percent Disk usage percentage",
        f"# TYPE ums_disk_percent gauge",
        f"ums_disk_percent {disk.percent}",
        f"",
        f"# HELP ums_uptime_seconds Application uptime",
        f"# TYPE ums_uptime_seconds gauge",
        f"ums_uptime_seconds {time.time() - psutil.boot_time()}",
    ]
    
    # Build response
    output = '\n'.join(lines) + '\n'
    
    from django.http import HttpResponse
    return HttpResponse(output, content_type='text/plain; charset=utf-8')


# Export views
__all__ = ['MetricsView', 'prometheus_metrics']