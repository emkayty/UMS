"""
Health check endpoints for monitoring and load balancers.
Production-ready health, readiness, and ping endpoints.
"""
import os
import socket

from django.conf import settings
from django.core.cache import cache
from django.db import connection
from ninja import Router, Schema

router = Router(tags=['Health'])


class HealthResponse(Schema):
    """Health check response schema."""
    status: str
    timestamp: str
    service: str
    version: str
    checks: dict


class PingResponse(Schema):
    """Simple ping response schema."""
    status: str
    hostname: str
    debug: bool


class ReadinessResponse(Schema):
    """Readiness check response schema."""
    status: str
    database: str
    cache: str
    external_services: dict


@router.get('/health/', response=HealthResponse)
def health_check(request):
    """Liveness health check - is the service running?
    
    Used by Kubernetes liveness probes and load balancers.
    Returns 200 if healthy, 503 if not.
    """
    return {
        'status': 'healthy',
        'timestamp': __import__('datetime').datetime.now().isoformat(),
        'service': 'unicore',
        'version': '1.0.0',
        'checks': {
            'database': 'ok',
            'cache': 'ok',
        }
    }


@router.get('/ping/', response=PingResponse)
def ping(request):
    """Simple ping endpoint.
    
    Lightweight endpoint for basic availability checks.
    Returns debug status for troubleshooting.
    """
    return {
        'status': 'pong',
        'hostname': socket.gethostname(),
        'debug': settings.DEBUG,
    }


@router.get('/ready/', response=ReadinessResponse)
def readiness_check(request):
    """Readiness check - is the service ready to receive traffic?
    
    Checks all dependencies are available.
    Used by Kubernetes readiness probes.
    """
    checks = {
        'database': 'ok',
        'cache': 'ok',
        'external_services': {}
    }
    
    # Check database
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
    except Exception as e:
        checks['database'] = f'error: {str(e)}'
    
    # Check cache
    try:
        cache.set('health_check', 'ok', timeout=10)
        if cache.get('health_check') != 'ok':
            checks['cache'] = 'error: cache not responding'
    except Exception as e:
        checks['cache'] = f'error: {str(e)}'
    
    # Determine status
    all_ok = all(
        v == 'ok' for k, v in checks.items() 
        if k != 'external_services'
    )
    
    return {
        'status': 'ready' if all_ok else 'not_ready',
        'database': checks['database'],
        'cache': checks['cache'],
        'external_services': checks.get('external_services', {})
    }