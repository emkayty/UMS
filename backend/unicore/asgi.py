"""
ASGI config for UniCore project.
Supports HTTP and WebSocket via Django Channels.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unicore.settings')

# Initialize Django ASGI application first
django_asgi_app = get_asgi_application()

# Try to import channels for WebSocket support
try:
    from channels.auth import AuthMiddlewareStack
    from channels.routing import ProtocolTypeRouter, URLRouter
    from channels.security.websocket import AllowedOriginOriginValidator
    
    # Import WebSocket URL patterns if they exist
    # from apps.core.routing import websocket_urlpatterns
    
    application = ProtocolTypeRouter({
        'http': django_asgi_app,
        'websocket': AuthMiddlewareStack(
            URLRouter([])
        ),
    })
    
except ImportError:
    # Fallback to basic Django ASGI if channels not available
    application = django_asgi_app
