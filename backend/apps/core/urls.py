"""
URL Routing for UMS API
STRICT DJANGO NINJA - NO DRF
"""

from django.urls import path, include

# Django Ninja ONLY (new api_ninja.py)
from apps.core.api_ninja import router as ninja_router

# Django Ninja legacy (api.py) - also include
from apps.core.api import router as ninja_router_legacy

urlpatterns = [
    # Django Ninja STRICT
    path('api/v1/', include(ninja_router.urls)),
    # Legacy Ninja routes
    path('', include(ninja_router_legacy.urls)),
]