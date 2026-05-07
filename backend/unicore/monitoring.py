"""
Monitoring Utilities for UMS

Health checks and monitoring helpers.
"""
from typing import Dict, Any
from django.core.cache import cache
from django.db import connection
import psutil
import os


def get_system_health() -> Dict[str, Any]:
    """Get system health status"""
    return {
        "status": "healthy",
        "cpu": psutil.cpu_percent(interval=0.1),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
    }


def get_database_health() -> Dict[str, str]:
    """Get database health"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return {"status": "healthy", "vendor": connection.vendor}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


def get_cache_health() -> Dict[str, str]:
    """Get cache health"""
    try:
        cache.set("health_check", "ok", 10)
        if cache.get("health_check") == "ok":
            return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
    return {"status": "unhealthy", "error": "unknown"}


def get_api_health() -> Dict[str, Any]:
    """Get comprehensive API health"""
    return {
        "system": get_system_health(),
        "database": get_database_health(),
        "cache": get_cache_health(),
    }


class HealthChecker:
    """Health checker"""
    
    @staticmethod
    def check_all() -> Dict[str, Any]:
        """Check all components"""
        return get_api_health()
    
    @staticmethod
    def is_healthy() -> bool:
        """Check if system is healthy"""
        health = get_api_health()
        return health["database"]["status"] == "healthy"