"""
Maintenance Mode for UMS

Provides system-wide maintenance mode for during
upgrades and maintenance windows.
"""
import os
import logging
from datetime import datetime
from typing import Optional
from django.core.cache import cache

logger = logging.getLogger(__name__)


# Cache keys
MAINTENANCE_MODE_KEY = "ums_maintenance_mode"
MAINTENANCE_MESSAGE_KEY = "ums_maintenance_message"


class MaintenanceMode:
    """Manage maintenance mode"""
    
    @staticmethod
    def is_enabled() -> bool:
        """Check if maintenance mode is enabled"""
        return cache.get(MAINTENANCE_MODE_KEY, False)
    
    @staticmethod
    def enable(message: str = "System under maintenance"):
        """
        Enable maintenance mode
        
        Args:
            message: Message to display to users
        """
        cache.set(MAINTENANCE_MODE_KEY, True, timeout=None)  # No timeout
        cache.set(MAINTENANCE_MESSAGE_KEY, message)
        logger.warning(f"Maintenance mode enabled: {message}")
    
    @staticmethod
    def disable():
        """Disable maintenance mode"""
        cache.delete(MAINTENANCE_MODE_KEY)
        cache.delete(MAINTENANCE_MESSAGE_KEY)
        logger.warning("Maintenance mode disabled")
    
    @staticmethod
    def get_message() -> str:
        """Get maintenance message"""
        return cache.get(MAINTENANCE_MESSAGE_KEY, "System under maintenance")


def is_maintenance_mode() -> bool:
    """Check if maintenance mode is active"""
    return MaintenanceMode.is_enabled()


def enable_maintenance_mode(message: str = "System under maintenance"):
    """Enable maintenance mode"""
    MaintenanceMode.enable(message)


def disable_maintenance_mode():
    """Disable maintenance mode"""
    MaintenanceMode.disable()