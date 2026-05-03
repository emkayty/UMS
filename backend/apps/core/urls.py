"""
URL Routing for new API endpoints
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.institution.views import HostelViewSet, HostelApplicationViewSet
from apps.student.views import StudentProfileViewSet, OnlineApplicationViewSet, TranscriptRequestViewSet
from apps.finance.views import PaymentViewSet, InvoiceViewSet, FeeTypeViewSet, BankAccountViewSet

# Create router
router = DefaultRouter()

# Institution endpoints
router.register(r'hostels', HostelViewSet, basename='hostel')
router.register(r'hostel-applications', HostelApplicationViewSet, basename='hostel-application')

# Student endpoints
router.register(r'students', StudentProfileViewSet, basename='student')
router.register(r'applications', OnlineApplicationViewSet, basename='application')
router.register(r'transcripts', TranscriptRequestViewSet, basename='transcript')

# Finance endpoints
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'invoices', InvoiceViewSet, basename='invoice')
router.register(r'fee-types', FeeTypeViewSet, basename='fee-type')
router.register(r'bank-accounts', BankAccountViewSet, basename='bank-account')

urlpatterns = [
    path('', include(router.urls)),
]