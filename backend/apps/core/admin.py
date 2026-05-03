"""
Django Admin Configuration
Register models in Django admin
"""

from django.contrib import admin
from django.apps import apps

# Import all models
from apps.academic.models import (
   AcademicSession, Semester, Programme, Department, Course
)
from apps.student.models import StudentProfile
from apps.staff.models import StaffProfile
from apps.finance.models import FeeType, StudentFee
from apps.institution.models import Settings
from apps.lifecycle.models import Hostel, HostelApplication
from apps.student.admission import OnlineApplication, AdmissionLetter
from apps.student.transcript import TranscriptRequest
from apps.finance.payments import PaymentTransaction, Invoice, BankAccount


# ============================================================
# ACADEMIC ADMIN
# ============================================================

@admin.register(AcademicSession)
class AcademicSessionAdmin(admin.ModelAdmin):
    list_display = ['name', 'session', 'is_active']
    list_filter = ['is_active']


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ['name', 'session', 'start_date', 'end_date']


@admin.register(Programme)
class ProgrammeAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'programme_type', 'department']
    list_filter = ['programme_type', 'department']
    search_fields = ['code', 'name']


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'faculty']
    list_filter = ['faculty']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'department', 'level', 'semester']
    list_filter = ['department', 'level', 'semester']
    search_fields = ['code', 'name']


# ============================================================
# STUDENT ADMIN
# ============================================================

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['matric_number', 'surname', 'first_name', 'programme', 'level']
    list_filter = ['programme', 'level', 'status']
    search_fields = ['matric_number', 'surname', 'first_name']
    date_hierarchy = 'admission_year'


# ============================================================
# STAFF ADMIN
# ============================================================

@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ['staff_id', 'surname', 'first_name', 'department', 'staff_type']
    list_filter = ['department', 'staff_type', 'status']
    search_fields = ['staff_id', 'surname', 'first_name']


# ============================================================
# FINANCE ADMIN
# ============================================================

@admin.register(FeeType)
class FeeTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'fee_type', 'amount', 'is_active']
    list_filter = ['fee_type', 'is_active']
    search_fields = ['code', 'name']


@admin.register(StudentFee)
class StudentFeeAdmin(admin.ModelAdmin):
    list_display = ['student', 'fee_type', 'session', 'amount', 'status']
    list_filter = ['fee_type', 'session', 'status']
    search_fields = ['student__matric_number']


# ============================================================
# INSTITUTION ADMIN  
# ============================================================

@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'hostel_type', 'gender', 'available_beds']
    list_filter = ['hostel_type', 'gender', 'is_active']
    search_fields = ['code', 'name']


@admin.register(HostelApplication)
class HostelApplicationAdmin(admin.ModelAdmin):
    list_display = ['student', 'hostel', 'session', 'status']
    list_filter = ['session', 'status']
    search_fields = ['student__matric_number']


# ============================================================
# ADMISSION ADMIN
# ============================================================

@admin.register(OnlineApplication)
class OnlineApplicationAdmin(admin.ModelAdmin):
    list_display = ['application_number', 'last_name', 'first_name', 'status']
    list_filter = ['session', 'status', 'payment_status']
    search_fields = ['application_number', 'last_name', 'email']
    date_hierarchy = 'created_at'


@admin.register(AdmissionLetter)
class AdmissionLetterAdmin(admin.ModelAdmin):
    list_display = ['application', 'admission_number', 'is_accepted']
    list_filter = ['is_accepted', 'acceptance_fee_paid']
    search_fields = ['admission_number']


# ============================================================
# TRANSCRIPT ADMIN
# ============================================================

@admin.register(TranscriptRequest)
class TranscriptRequestAdmin(admin.ModelAdmin):
    list_display = ['student', 'transcript_type', 'status', 'amount']
    list_filter = ['status', 'transcript_type']
    search_fields = ['student__matric_number']


# ============================================================
# FINANCE ADMIN
# ============================================================

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ['bank_name', 'account_number', 'is_active', 'is_default']
    list_filter = ['is_active']


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_ref', 'user', 'amount', 'status', 'gateway']
    list_filter = ['status', 'gateway']
    search_fields = ['transaction_ref', 'user__email']
    date_hierarchy = 'initiated_at'


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'student', 'total', 'status', 'due_date']
    list_filter = ['session', 'status']
    search_fields = ['invoice_number', 'student__matric_number']