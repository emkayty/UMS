"""
URL Routing for new API endpoints
COMPLETE API - All endpoints registered
Django Ninja primary, DRF for compatibility
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Django Ninja import
from apps.core.api import router as ninja_router
from apps.institution.views import HostelViewSet, HostelApplicationViewSet
from apps.student.views import StudentProfileViewSet, OnlineApplicationViewSet, TranscriptRequestViewSet
from apps.finance.views import PaymentViewSet, InvoiceViewSet, FeeTypeViewSet, BankAccountViewSet
from apps.core.viewsets_extra import (
    # Clearance
    ClearanceViewSet,
    # SIWES
    ITPlacementViewSet, ITAssessmentViewSet, ITLetterViewSet,
    # Alumni
    AlumniProfileViewSet, AlumniEventViewSet,
    # Library
    BookViewSet, BookBorrowViewSet, LibraryCardViewSet,
    # Calendar
    CalendarEventViewSet, TimetableViewSet,
    # Leave
    LeaveApplicationViewSet, LeaveEntitlementViewSet,
    # ID Cards
    IDCardRequestViewSet, IDCardViewSet,
    # Notifications
    NotificationViewSet,
    # Parent Portal
    ParentPortalViewSet,
    # Biometrics
    BiometricViewSet, AttendanceLogViewSet,
    # Guardian
    GuardianViewSet, NextOfKinViewSet,
)

# Create router
router = DefaultRouter()

# ========== INSTITUTION ==========
router.register(r'hostels', HostelViewSet, basename='hostel')
router.register(r'hostel-applications', HostelApplicationViewSet, basename='hostel-application')
router.register(r'clearance', ClearanceViewSet, basename='clearance')

# ========== STUDENT ==========
router.register(r'students', StudentProfileViewSet, basename='student')
router.register(r'applications', OnlineApplicationViewSet, basename='application')
router.register(r'transcripts', TranscriptRequestViewSet, basename='transcript')

# ========== FINANCE ==========
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'invoices', InvoiceViewSet, basename='invoice')
router.register(r'fee-types', FeeTypeViewSet, basename='fee-type')
router.register(r'bank-accounts', BankAccountViewSet, basename='bank-account')

# ========== SIWES ==========
router.register(r'siwes-placements', ITPlacementViewSet, basename='siwes-placement')
router.register(r'siwes-assessments', ITAssessmentViewSet, basename='siwes-assessment')
router.register(r'siwes-letters', ITLetterViewSet, basename='siwes-letter')

# ========== ALUMNI ==========
router.register(r'alumni-profile', AlumniProfileViewSet, basename='alumni-profile')
router.register(r'alumni-events', AlumniEventViewSet, basename='alumni-event')

# ========== LIBRARY ==========
router.register(r'library-books', BookViewSet, basename='library-book')
router.register(r'library-borrow', BookBorrowViewSet, basename='library-borrow')
router.register(r'library-cards', LibraryCardViewSet, basename='library-card')

# ========== CALENDAR ==========
router.register(r'calendar-events', CalendarEventViewSet, basename='calendar-event')
router.register(r'timetable', TimetableViewSet, basename='timetable')

# ========== LEAVE ==========
router.register(r'leave-applications', LeaveApplicationViewSet, basename='leave-application')
router.register(r'leave-entitlements', LeaveEntitlementViewSet, basename='leave-entitlement')

# ========== ID CARDS ==========
router.register(r'id-card-requests', IDCardRequestViewSet, basename='id-card-request')
router.register(r'id-cards', IDCardViewSet, basename='id-card')

# ========== NOTIFICATIONS ==========
router.register(r'notifications', NotificationViewSet, basename='notification')

# ========== PARENT PORTAL ==========
router.register(r'parent-portal', ParentPortalViewSet, basename='parent-portal')

# ========== BIOMETRICS ==========
router.register(r'biometrics', BiometricViewSet, basename='biometric')
router.register(r'attendance-logs', AttendanceLogViewSet, basename='attendance-log')

# ========== GUARDIAN ==========
router.register(r'guardians', GuardianViewSet, basename='guardian')
router.register(r'next-of-kin', NextOfKinViewSet, basename='next-of-kin')

# Django Ninja API routes
from django.urls import path
from apps.core.api import router as ninja_router

urlpatterns = [
    # Django Ninja (PRIMARY API)
    path('api/v1/', include(ninja_router.urls)),
    # DRF (compatibility)
    path('', include(router.urls)),
]