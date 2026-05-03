"""
Core App Configuration
"""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Core app configuration."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
    verbose_name = 'Core'
    label = 'core'
    
    def ready(self):
        """Initialize app."""
        # Import signals
        from . import signals  # noqa
        from . import audit    # noqa