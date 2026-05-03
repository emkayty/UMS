"""
Django Admin Configuration
Register models in Django admin
"""

from django.contrib import admin
from django.apps import apps

# Import only necessary models
from apps.academic.models import AcademicSession, Semester, Programme, Department, Course
from apps.student.models import StudentProfile
from apps.staff.models import StaffProfile
from apps.finance.models import FeeType, StudentFee

# ============================================================
# ACADEMIC ADMIN
# ============================================================

@admin.register(AcademicSession)
class AcademicSessionAdmin(admin.ModelAdmin):
    list_display = ('session', 'is_current', 'start_date', 'end_date')
    list_filter = ('is_current',)

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('semester', 'session', 'is_current', 'start_date', 'end_date')
    list_filter = ('is_current', 'session')

@admin.register(Programme)
class ProgrammeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'department', 'duration_years')
    search_fields = ('name', 'code')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'faculty')
    search_fields = ('name', 'code')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'credits', 'department')
    search_fields = ('code', 'title')

# ============================================================
# STUDENT ADMIN
# ============================================================

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'matric_number', 'programme', 'level')
    list_filter = ('level', 'programme')
    search_fields = ('matric_number', 'user__first_name', 'user__last_name')

# ============================================================
# STAFF ADMIN
# ============================================================

@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'staff_number', 'department', 'position')
    search_fields = ('staff_number', 'user__first_name')

# ============================================================
# FINANCE ADMIN
# ============================================================

@admin.register(FeeType)
class FeeTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'level', 'session')

@admin.register(StudentFee)
class StudentFeeAdmin(admin.ModelAdmin):
    list_display = ('student', 'fee_type', 'amount', 'status', 'created_at')
    list_filter = ('status',)
