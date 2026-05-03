"""
Abstract Serializers
Standardized, Professional API Serializers
"""

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.utils import timezone


# ============================================================
# BASE SERIALIZERS
# ============================================================

class BaseSerializer(serializers.ModelSerializer):
    """Abstract base serializer with common functionality."""
    
    class Meta:
        abstract = True
    
    # UUID field
    uuid = serializers.UUIDField(read_only=True)
    
    # Timestamp fields
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    # Common fields
    is_active = serializers.BooleanField(default=True)
    status = serializers.CharField(read_only=True)
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context['request'].user
        return super().update(instance, validated_data)


class ReadOnlySerializer(serializers.ModelSerializer):
    """Serializer with all fields read-only."""
    
    class Meta:
        abstract = True
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].read_only = True


class NestedSerializer(serializers.ModelSerializer):
    """Serializer with nested objects."""
    
    class Meta:
        abstract = True
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # Convert UUID to string
        if 'uuid' in rep:
            rep['uuid'] = str(rep['uuid'])
        return rep


# ============================================================
# CHOICE SERIALIZERS
# ============================================================

class ChoiceField(serializers.ChoiceField):
    """Enhanced choice field."""
    
    def __init__(self, choices, **kwargs):
        self.choice_names = {c[0]: c[1] for c in choices}
        super().__init__(choices=choices, **kwargs)


# ============================================================
# VALIDATION SERIALIZERS
# ============================================================

class ValidateOnCreateSerializer(BaseSerializer):
    """Serializer that validates on create only."""
    
    class Meta:
        abstract = True
    
    def validate(self, attrs):
        # Skip validation on update
        if self.instance:
            return attrs
        return super().validate(attrs)


class ValidateOnUpdateSerializer(BaseSerializer):
    """Serializer that validates on update only."""
    
    class Meta:
        abstract = True
    
    def validate(self, attrs):
        # Skip validation on create
        if not self.instance:
            return attrs
        return super().validate(attrs)


# ============================================================
# FILTERS
# ============================================================

class BaseFilterSerializer(serializers.Serializer):
    """Base filter serializer."""
    
    search = serializers.CharField(required=False)
    status = serializers.ChoiceField(
        choices=['draft', 'pending', 'active', 'inactive', 'archived'],
        required=False
    )
    is_active = serializers.BooleanField(required=False)
    
    # Pagination
    page = serializers.IntegerField(default=1, min_value=1)
    page_size = serializers.IntegerField(default=20, min_value=1, max_value=100)
    
    # Ordering
    ordering = serializers.CharField(default='-created_at')


# ============================================================
# RESPONSE SERIALIZERS
# ============================================================

class PaginatedResponseSerializer(serializers.Serializer):
    """Standard paginated response."""
    
    def __init__(self, data=None, status_code=200, **kwargs):
        self.status_code = status_code
        super().__init__(data=data, **kwargs)
    
    def to_representation(self, data):
        return {
            'status_code': self.status_code,
            'results': data.get('results', []),
            'pagination': {
                'page': data.get('page', 1),
                'page_size': data.get('page_size', 20),
                'total_pages': data.get('total_pages', 1),
                'total_count': data.get('total_count', 0),
                'has_next': data.get('has_next', False),
                'has_prev': data.get('has_prev', False),
            }
        }


class ErrorResponseSerializer(serializers.Serializer):
    """Standard error response."""
    
    code = serializers.CharField()
    message = serializers.CharField()
    details = serializers.DictField(required=False)
    timestamp = serializers.DateTimeField(default=timezone.now)


class SuccessResponseSerializer(serializers.Serializer):
    """Standard success response."""
    
    message = serializers.CharField()
    data = serializers.DictField(required=False)


# ============================================================
# HELPER MIXINS
# ============================================================

class TimestampMixin:
    """Add timestamp functionality."""
    
    def get_timestamp(self, obj):
        return timezone.now().isoformat()


class StatusMixin:
    """Add status functionality."""
    
    def get_status_display(self, obj):
        return obj.get_status_display()


class UserMixin:
    """Add user info functionality."""
    
    def get_created_by(self, obj):
        if obj.created_by:
            return {
                'uuid': str(obj.created_by.uuid),
                'email': obj.created_by.email,
                'name': obj.created_by.get_full_name() or obj.created_by.username
            }
        return None
    
    def get_updated_by(self, obj):
        if obj.updated_by:
            return {
                'uuid': str(obj.updated_by.uuid),
                'email': obj.updated_by.email,
                'name': obj.updated_by.get_full_name() or obj.updated_by.username
            }
        return None


# ============================================================
# COMMON SERIALIZERS
# ============================================================

class UserBasicSerializer(serializers.ModelSerializer):
    """Basic user info serializer."""
    
    class Meta:
        from apps.accounts.models import User
        model = User
        fields = ['uuid', 'email', 'first_name', 'last_name', 'is_active']
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['uuid'] = str(rep['uuid'])
        return rep


class UserFullSerializer(UserBasicSerializer):
    """Full user info serializer."""
    
    class Meta(UserBasicSerializer.Meta):
        fields = ['uuid', 'email', 'first_name', 'last_name', 'phone', 
                 'is_active', 'is_staff', 'date_joined']


# ============================================================
# EXPORT SERIALIZERS
# ============================================================

class ExportSerializer(serializers.Serializer):
    """Export data serializer."""
    
    format = serializers.ChoiceField(
        choices=['csv', 'excel', 'json', 'pdf'],
        default='csv'
    )
    fields = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    include_headers = serializers.BooleanField(default=True)


# ============================================================
# ID SERIALIZER
# ============================================================

class UUIDSerializer(serializers.Serializer):
    """Serializer for UUID input."""
    
    uuid = serializers.UUIDField()
    
    def validate_uuid(self, value):
        return str(value)

# ============================================================
# AUTO-GENERATED MODULE SERIALIZERS
# ============================================================
# Generated to fix missing serializers for new modules

from apps.student.admission import (
    OnlineApplication, OLevelResult, PostUtmeResult, AdmissionLetter
)
from apps.student.transcript import TranscriptRequest, TranscriptRecord
from apps.student.guardian import Guardian, NextOfKin
from apps.student.parent_portal import ParentAccount, ParentNotification, ParentLoginRequest
from apps.institution.hostel import Hostel, Floor, Room, Bed, HostelApplication, HostelAllotment, HostelFee
from apps.institution.clearance import StudentClearance, ClearanceItem, ClearanceSetup, ClearanceOfficer
from apps.institution.siwes import ITCompany, ITPlacement, ITLogbook, ITAssessment, ITLetter
from apps.institution.alumni import AlumniProfile, EmploymentRecord, FurtherStudy
from apps.institution.calendar import AcademicCalendar, CalendarEvent, Timetable, TimetableSlot
from apps.institution.id_card import IDCard, IDCardRequest
from apps.institution.biometric import Biometric, BiometricLog, AttendanceDevice
from apps.finance.payments import PaymentGatewayConfig, PaymentTransaction, Invoice, Refund, BankAccount, ManualPayment
from apps.communication.notifications import EmailTemplate, EmailNotification, SMSNotification
from apps.learning.library import Library, LibrarySection, Book, BookCopy, BookBorrow
from apps.staff.leave import LeaveEntitlement, LeaveApplication


class OLevelResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = OLevelResult
        fields = ['id', 'exam_type', 'exam_year', 'exam_number', 'subjects']


class OnlineApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlineApplication
        fields = ['id', 'application_number', 'session', 'first_name', 'last_name', 'email', 'phone', 'status', 'payment_status']


class PostUtmeResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostUtmeResult
        fields = ['id', 'application', 'score', 'percentile', 'exam_date']


class AdmissionLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdmissionLetter
        fields = ['id', 'application', 'admission_number', 'is_accepted', 'acceptance_fee_paid']


class TranscriptRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranscriptRecord
        fields = ['id', 'session', 'total_units', 'gpa', 'cgpa']


class TranscriptRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranscriptRequest
        fields = ['id', 'student', 'transcript_type', 'status', 'amount', 'payment_status']


class GuardianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guardian
        fields = ['id', 'relation', 'first_name', 'last_name', 'phone', 'email']


class NextOfKinSerializer(serializers.ModelSerializer):
    class Meta:
        model = NextOfKin
        fields = ['id', 'first_name', 'last_name', 'relation', 'phone']


class ParentAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentAccount
        fields = ['id', 'user', 'relation', 'can_view_results', 'status']


class ParentNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentNotification
        fields = ['id', 'student', 'title', 'message', 'is_read', 'sent_at']


class ParentLoginRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentLoginRequest
        fields = ['id', 'student', 'parent_name', 'parent_email', 'request_token']


class HostelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hostel
        fields = ['id', 'name', 'code', 'hostel_type', 'gender', 'total_beds', 'available_beds']


class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = ['id', 'floor_number', 'hostel', 'total_rooms']


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'room_number', 'floor', 'room_type', 'capacity', 'occupied']


class BedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bed
        fields = ['id', 'bed_number', 'room', 'is_occupied']


class HostelApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostelApplication
        fields = ['id', 'student', 'hostel', 'session', 'status', 'applied_at']


class HostelAllotmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostelAllotment
        fields = ['id', 'application', 'bed', 'check_in_date', 'status']


class HostelFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostelFee
        fields = ['id', 'session', 'hostel_type', 'amount', 'due_date']


class StudentClearanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentClearance
        fields = ['id', 'student', 'session', 'status', 'completed_at']


class ClearanceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClearanceItem
        fields = ['id', 'item_name', 'department', 'status', 'approved_by']


class ClearanceSetupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClearanceSetup
        fields = ['id', 'department', 'item_name', 'is_required']


class ClearanceOfficerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClearanceOfficer
        fields = ['id', 'user', 'department', 'can_approve']


class GraduationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentClearance
        fields = ['id', 'session', 'generated_at']


class ITCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = ITCompany
        fields = ['id', 'name', 'address', 'city', 'industry', 'is_verified']


class ITPlacementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ITPlacement
        fields = ['id', 'student', 'company', 'session', 'start_date', 'end_date', 'status']


class ITLogbookSerializer(serializers.ModelSerializer):
    class Meta:
        model = ITLogbook
        fields = ['id', 'placement', 'week_number', 'description', 'status']


class ITAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ITAssessment
        fields = ['id', 'placement', 'company_score', 'school_score', 'total_score', 'grade']


class ITLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ITLetter
        fields = ['id', 'placement', 'letter_type', 'issued_date']


class AlumniProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlumniProfile
        fields = ['id', 'student', 'graduation_year', 'degree_class', 'is_active']


class EmploymentRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentRecord
        fields = ['id', 'company', 'position', 'start_date', 'is_current']


class FurtherStudySerializer(serializers.ModelSerializer):
    class Meta:
        model = FurtherStudy
        fields = ['id', 'institution', 'course', 'level', 'status']


class AlumniEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlumniEvent
        fields = ['id', 'title', 'event_date', 'venue', 'registration_deadline']


class AlumniDuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlumniDues
        fields = ['id', 'session', 'amount', 'due_date']


class JobPostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPosting
        fields = ['id', 'title', 'company', 'location', 'salary', 'apply_deadline']


class AcademicCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicCalendar
        fields = ['id', 'session', 'name', 'is_active']


class CalendarEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarEvent
        fields = ['id', 'title', 'event_type', 'start_date', 'end_date', 'venue', 'status']


class TimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timetable
        fields = ['id', 'session', 'programme', 'level', 'semester', 'is_active']


class TimetableSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimetableSlot
        fields = ['id', 'timetable', 'day_of_week', 'start_time', 'course', 'venue']


class IDCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = IDCard
        fields = ['id', 'student', 'card_number', 'status', 'expiry_date']


class IDCardRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = IDCardRequest
        fields = ['id', 'student', 'request_type', 'status', 'fee']


class BiometricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Biometric
        fields = ['id', 'student', 'biometric_type', 'status', 'is_active']


class BiometricLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BiometricLog
        fields = ['id', 'biometric', 'is_successful', 'verified_at']


class AttendanceDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceDevice
        fields = ['id', 'name', 'device_id', 'location', 'is_active']


class PaymentGatewayConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentGatewayConfig
        fields = ['id', 'gateway', 'merchant_email', 'is_active']


class PaymentTransactionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTransaction
        fields = ['id', 'user', 'amount', 'payment_type', 'gateway', 'status', 'transaction_ref']


class InvoiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id', 'student', 'invoice_number', 'total', 'status', 'due_date']


class RefundListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refund
        fields = ['id', 'transaction', 'amount', 'status']


class BankAccountListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ['id', 'bank_name', 'account_number', 'is_active', 'is_default']


class ManualPaymentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManualPayment
        fields = ['id', 'student', 'amount', 'sender_name', 'status']


class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = ['id', 'name', 'subject', 'is_active']


class EmailNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailNotification
        fields = ['id', 'recipient', 'subject', 'sent_at', 'status']


class SMSNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSNotification
        fields = ['id', 'recipient', 'message', 'sent_at', 'status']


class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ['id', 'name', 'code', 'location', 'is_active']


class LibrarySectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibrarySection
        fields = ['id', 'library', 'name', 'code', 'max_borrow_days']


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'isbn', 'title', 'author', 'category', 'total_copies', 'available_copies']


class BookCopySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCopy
        fields = ['id', 'book', 'copy_number', 'barcode', 'status']


class BookBorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookBorrow
        fields = ['id', 'book_copy', 'student', 'due_date', 'status']


class LeaveEntitlementSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveEntitlement
        fields = ['id', 'staff', 'leave_type', 'total_days', 'used_days']


class LeaveApplicationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveApplication
        fields = ['id', 'staff', 'leave_type', 'start_date', 'end_date', 'status']
