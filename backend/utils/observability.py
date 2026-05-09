"""
Observability Utilities
Monitoring, logging, and tracing utilities
"""

import uuid
import logging
import time
from typing import Optional, Dict, Any
from functools import wraps
from datetime import datetime
from django.utils import timezone


class ObservabilityLogger:
    """
    Structured logging for observability
    Includes correlation IDs and tenant context
    """
    
    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """Get a configured logger"""
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        return logger
    
    @staticmethod
    def log_request(
        logger: logging.Logger,
        method: str,
        path: str,
        status_code: int,
        correlation_id: str,
        tenant_id: Optional[str] = None,
        duration_ms: Optional[float] = None
    ):
        """Log HTTP request with context"""
        log_data = {
            'timestamp': timezone.now().isoformat(),
            'type': 'http_request',
            'method': method,
            'path': path,
            'status': status_code,
            'correlation_id': correlation_id,
        }
        
        if tenant_id:
            log_data['tenant_id'] = tenant_id
        
        if duration_ms:
            log_data['duration_ms'] = duration_ms
        
        logger.info(log_data)
    
    @staticmethod
    def log_audit(
        logger: logging.Logger,
        action: str,
        user_id: str,
        resource: str,
        correlation_id: str,
        tenant_id: Optional[str] = None,
        details: Optional[Dict] = None
    ):
        """Log audit event"""
        log_data = {
            'timestamp': timezone.now().isoformat(),
            'type': 'audit',
            'action': action,
            'user_id': user_id,
            'resource': resource,
            'correlation_id': correlation_id,
        }
        
        if tenant_id:
            log_data['tenant_id'] = tenant_id
        
        if details:
            log_data['details'] = details
        
        logger.info(log_data)


class CorrelationID:
    """
    Generate and manage correlation IDs for distributed tracing
    """
    
    @staticmethod
    def generate() -> str:
        """Generate new correlation ID"""
        return str(uuid.uuid4())
    
    @staticmethod
    def get_or_create(request) -> str:
        """Get from request or create new"""
        correlation_id = request.headers.get('X-Correlation-ID')
        if not correlation_id:
            correlation_id = CorrelationID.generate()
        return correlation_id


def trace_execution(logger: logging.Logger):
    """
    Decorator to trace function execution
    
    Usage:
        @trace_execution(logger)
        def my_function():
            pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            correlation_id = CorrelationID.generate()
            start_time = time.time()
            
            logger.info({
                'type': 'function_start',
                'function': func.__name__,
                'correlation_id': correlation_id,
            })
            
            try:
                result = func(*args, **kwargs)
                duration = (time.time() - start_time) * 1000
                
                logger.info({
                    'type': 'function_complete',
                    'function': func.__name__,
                    'correlation_id': correlation_id,
                    'duration_ms': duration,
                })
                
                return result
                
            except Exception as e:
                duration = (time.time() - start_time) * 1000
                
                logger.error({
                    'type': 'function_error',
                    'function': func.__name__,
                    'correlation_id': correlation_id,
                    'duration_ms': duration,
                    'error': str(e),
                })
                raise
        
        return wrapper
    return decorator


class MetricsCollector:
    """
    Collect application metrics
    """
    
    def __init__(self):
        self._counters: Dict[str, int] = {}
        self._gauges: Dict[str, float] = {}
        self._histograms: Dict[str, list] = {}
    
    def increment_counter(self, name: str, value: int = 1):
        """Increment a counter metric"""
        self._counters[name] = self._counters.get(name, 0) + value
    
    def set_gauge(self, name: str, value: float):
        """Set a gauge metric"""
        self._gauges[name] = value
    
    def record_histogram(self, name: str, value: float):
        """Record a histogram value"""
        if name not in self._histograms:
            self._histograms[name] = []
        self._histograms[name].append(value)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get all metrics"""
        return {
            'counters': self._counters.copy(),
            'gauges': self._gauges.copy(),
            'histograms': {
                k: {
                    'count': len(v),
                    'avg': sum(v) / len(v) if v else 0,
                    'min': min(v) if v else 0,
                    'max': max(v) if v else 0,
                }
                for k, v in self._histograms.items()
            }
        }


# Global metrics collector
_metrics = MetricsCollector()


def get_metrics_collector() -> MetricsCollector:
    """Get global metrics collector"""
    return _metrics


class HealthChecker:
    """
    Health check for various components
    """
    
    @staticmethod
    def check_database() -> Dict[str, Any]:
        """Check database health"""
        from django.db import connection
        
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1')
            return {'status': 'healthy', 'latency_ms': 0}
        except Exception as e:
            return {'status': 'unhealthy', 'error': str(e)}
    
    @staticmethod
    def check_cache() -> Dict[str, Any]:
        """Check cache health"""
        from django.core.cache import cache
        
        try:
            cache.set('health_check', 'ok', 10)
            value = cache.get('health_check')
            return {'status': 'healthy' if value == 'ok' else 'degraded'}
        except Exception as e:
            return {'status': 'unhealthy', 'error': str(e)}
    
    @staticmethod
    def check_all() -> Dict[str, Any]:
        """Check all components"""
        return {
            'timestamp': timezone.now().isoformat(),
            'database': HealthChecker.check_database(),
            'cache': HealthChecker.check_cache(),
        }


# Export
__all__ = [
    'ObservabilityLogger',
    'CorrelationID',
    'trace_execution',
    'MetricsCollector',
    'get_metrics_collector',
    'HealthChecker',
]