"""
MONITORING & METRICS MODULE
Enterprise monitoring and observability
"""

import time
import psutil
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from functools import wraps
from django.conf import settings

logger = logging.getLogger(__name__)


class MetricsCollector:
    """
    System Metrics Collection
    For monitoring application health
    """
    
    @staticmethod
    def get_system_metrics() -> dict:
        """Collect system metrics"""
        return {
            'cpu_percent': psutil.cpu_percent(interval=0.1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent,
            'timestamp': datetime.now().isoformat(),
        }
    
    @staticmethod
    def get_database_metrics() -> dict:
        """Get database connection metrics"""
        # Placeholder for actual DB metrics
        return {
            'connections': 0,
            'max_connections': 100,
            'timestamp': datetime.now().isoformat(),
        }
    
    @staticmethod
    def get_cache_metrics() -> dict:
        """Get cache metrics"""
        return {
            'hits': 0,
            'misses': 0,
            'timestamp': datetime.now().isoformat(),
        }
    
    @classmethod
    def get_all_metrics(cls) -> dict:
        """Get all system metrics"""
        return {
            'system': cls.get_system_metrics(),
            'database': cls.get_database_metrics(),
            'cache': cls.get_cache_metrics(),
        }


class PerformanceMonitor:
    """
    Request Performance Monitoring
    Track endpoint performance
    """
    
    # In-memory storage for request metrics
    REQUEST_METRICS = {}
    
    @classmethod
    def track_request(
        cls,
        endpoint: str,
        method: str,
        duration_ms: float,
        status_code: int
    ):
        """Track request metrics"""
        key = f"{method}:{endpoint}"
        
        if key not in cls.REQUEST_METRICS:
            cls.REQUEST_METRICS[key] = {
                'requests': 0,
                'total_duration': 0,
                'min_duration': float('inf'),
                'max_duration': 0,
                'errors': 0,
            }
        
        metrics = cls.REQUEST_METRICS[key]
        metrics['requests'] += 1
        metrics['total_duration'] += duration_ms
        metrics['min_duration'] = min(metrics['min_duration'], duration_ms)
        metrics['max_duration'] = max(metrics['max_duration'], duration_ms)
        
        if status_code >= 400:
            metrics['errors'] += 1
    
    @classmethod
    def get_endpoint_metrics(cls, endpoint: str = None) -> dict:
        """Get metrics for specific endpoint or all"""
        if endpoint:
            return cls.REQUEST_METRICS.get(endpoint, {})
        return cls.REQUEST_METRICS
    
    @classmethod
    def get_average_duration(cls, endpoint: str) -> float:
        """Get average response time for endpoint"""
        metrics = cls.REQUEST_METRICS.get(endpoint, {})
        if metrics.get('requests', 0) == 0:
            return 0
        return metrics['total_duration'] / metrics['requests']


def monitor_performance(endpoint_name: str = None):
    """
    Decorator to monitor function performance
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                duration_ms = (time.time() - start_time) * 1000
                endpoint = endpoint_name or f"{func.__module__}.{func.__name__}"
                status_code = 200  # Default, would need actual status
                PerformanceMonitor.track_request(
                    endpoint,
                    'CALL',
                    duration_ms,
                    status_code
                )
        return wrapper
    return decorator


class HealthChecker:
    """
    Application Health Checks
    For container orchestration and monitoring
    """
    
    # Health check components
    COMPONENTS = {}
    
    @classmethod
    def register_component(cls, name: str, check_func):
        """Register health check component"""
        cls.COMPONENTS[name] = check_func
    
    @classmethod
    def check_component(cls, name: str) -> dict:
        """Check individual component"""
        check_func = cls.COMPONENTS.get(name)
        if not check_func:
            return {'status': 'unknown', 'message': 'No check function'}
        
        try:
            result = check_func()
            return {'status': 'healthy', 'result': result}
        except Exception as e:
            return {'status': 'unhealthy', 'error': str(e)}
    
    @classmethod
    def check_all(cls) -> dict:
        """Check all components"""
        results = {}
        overall_healthy = True
        
        for name in cls.COMPONENTS:
            result = cls.check_component(name)
            results[name] = result
            if result['status'] != 'healthy':
                overall_healthy = False
        
        return {
            'healthy': overall_healthy,
            'components': results,
            'timestamp': datetime.now().isoformat(),
        }
    
    @classmethod
    def liveness_check(cls) -> dict:
        """Kubernetes liveness probe"""
        return {'status': 'alive'}
    
    @classmethod
    def readiness_check(cls) -> dict:
        """Kubernetes readiness probe"""
        return cls.check_all()


# Register default health checks
def database_health_check():
    """Check database connectivity"""
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute('SELECT 1')
    return True

HealthChecker.register_component('database', database_health_check)


class AlertManager:
    """
    Alert Management
    For threshold-based alerting
    """
    
    # Alert thresholds
    THRESHOLDS = {
        'cpu_percent': 80,
        'memory_percent': 85,
        'disk_percent': 90,
        'response_time_ms': 1000,
    }
    
    @classmethod
    def check_thresholds(cls, metrics: dict) -> list:
        """Check metrics against thresholds"""
        alerts = []
        
        cpu = metrics.get('system', {}).get('cpu_percent', 0)
        if cpu > cls.THRESHOLDS['cpu_percent']:
            alerts.append({
                'severity': 'warning',
                'message': f'CPU usage high: {cpu}%',
            })
        
        memory = metrics.get('system', {}).get('memory_percent', 0)
        if memory > cls.THRESHOLDS['memory_percent']:
            alerts.append({
                'severity': 'warning',
                'message': f'Memory usage high: {memory}%',
            })
        
        return alerts
    
    @classmethod
    def send_alert(cls, alert: dict):
        """Send alert (placeholder)"""
        logger.warning(f"ALERT: {alert}")


# Export utilities
__all__ = [
    'MetricsCollector',
    'PerformanceMonitor',
    'HealthChecker',
    'AlertManager',
    'monitor_performance',
]