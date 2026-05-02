"""
UniCore URL Configuration
Production-ready with health check endpoints.
"""
from django.urls import path
from django.contrib import admin
from django.http import HttpResponse
from django.conf import settings
from django.views.static import serve
from ninja import NinjaAPI

# Import all API routers
from apps.accounts.api import router as auth_router
from apps.accounts.health import router as health_router
from apps.institution.api import router as settings_router
from apps.academic.api import router as academic_router
from apps.student.api import router as student_router
from apps.staff.api import router as staff_router
from apps.learning.api import router as learning_router
from apps.finance.api import router as finance_router
from apps.communication.api import router as communication_router
from apps.reports.api import router as reports_router
from apps.reports.analytics.api import router as analytics_router
from apps.offline.api import router as offline_router
from apps.lifecycle.api import router as lifecycle_router

# New routers (v2)
from apps.student.attendance_api import router as attendance_router
from apps.student.workflow_api import router as workflow_router
from apps.student.extended_services_api import router as services_router
from apps.student.disciplinary_api import router as disciplinary_router

# Learning routers
from apps.learning.library_exam_api import router as library_exam_router

api = NinjaAPI(title='UniCore API', version='1.0.0')

# Add all route groups
api.add_router('/health/', health_router)
api.add_router('/auth/', auth_router)
api.add_router('/settings/', settings_router)
api.add_router('/academic/', academic_router)
api.add_router('/students/', student_router)
api.add_router('/staff/', staff_router)
api.add_router('/learning/', learning_router)
api.add_router('/fees/', finance_router)
api.add_router('/announcements/', communication_router)
api.add_router('/reports/', reports_router)
api.add_router('/ai/', analytics_router)
api.add_router('/offline/', offline_router)
api.add_router('/lifecycle/', lifecycle_router)

# New v2 routers
api.add_router('/attendance/', attendance_router)
api.add_router('/workflow/', workflow_router)
api.add_router('/services/', services_router)
api.add_router('/disciplinary/', disciplinary_router)

# Learning v2
api.add_router('/library/', library_exam_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', api.urls),
    
    # Health check endpoints (no auth required)
    path('health/', lambda r: HttpResponse('OK'), name='health_root'),
    path('health/ping/', lambda r: HttpResponse('pong'), name='ping'),
    
    # Static and media files in debug mode
] if settings.DEBUG else []

# Static files
if settings.DEBUG:
    urlpatterns += [
        path('static/<path:path>', serve, {'document_root': settings.STATIC_ROOT}),
        path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
    ]

# Root endpoint
urlpatterns += [
    path('', lambda r: HttpResponse(
        '<h1>UniCore Running</h1>'
        '<pre>API: <a href="/api/v1/">/api/v1/</a></pre>'
        '<pre>Health: <a href="/api/v1/health/">/api/v1/health/</a></pre>'
    )),
]
