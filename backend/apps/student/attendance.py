"""
Student Attendance System
Tracks student attendance in lectures and exams
"""

from django.db import models
import uuid
from django.utils import timezone


class StudentAttendance(models.Model):
    """Student lecture attendance."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey(
        'student.StudentProfile',
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )
    
    session = models.ForeignKey('academic.AcademicSession', on_delete=models.CASCADE)
    semester = models.ForeignKey('academic.Semester', on_delete=models.CASCADE)
    
    # Course/Class
    course = models.ForeignKey('academic.Course', on_delete=models.CASCADE)
    
    # Attendance details
    date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('present', 'Present'),
            ('absent', 'Absent'),
            ('late', 'Late (>15min)'),
            ('excused', 'Excused'),
        ],
        default='absent'
    )
    
    minutes_late = models.IntegerField(default=0)
    remark = models.CharField(max_length=100, blank=True)
    
    marked_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True
    )
    
    marked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'course', 'date']
        indexes = [
            models.Index(fields=['student', 'session', 'semester']),
            models.Index(fields=['course', 'date']),
        ]


class AttendanceSession(models.Model):
    """QR code attendance session."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    course = models.ForeignKey('academic.Course', on_delete=models.CASCADE)
    session = models.ForeignKey('academic.AcademicSession', on_delete=models.CASCADE)
    semester = models.ForeignKey('academic.Semester', on_delete=models.CASCADE)
    
    # QR Code
    qr_code = models.CharField(max_length=50, unique=True)
    expires_at = models.DateTimeField()
    
    # Status
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['course', 'session', 'semester']


class AttendanceSummary(models.Model):
    """Aggregated attendance per student per course."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, edible=False)
    
    student = models.ForeignKey(
        'student.StudentProfile',
        on_delete=models.CASCADE,
        related_name='attendance_summaries'
    )
    
    session = models.ForeignKey('academic.AcademicSession', on_delete=models.CASCADE)
    semester = models.ForeignKey('academic.Semester', on_delete=models.CASCADE)
    course = models.ForeignKey('academic.Course', on_delete=models.CASCADE)
    
    # Counts
    total_sessions = models.IntegerField(default=0)
    present_count = models.IntegerField(default=0)
    absent_count = models.IntegerField(default=0)
    late_count = models.IntegerField(default=0)
    excused_count = models.IntegerField(default=0)
    
    # Percentage
    attendance_percentage = models.DecimalField(
        max_digits=4, decimal_places=2, default=0
    )
    
    # Status
    ATTENDANCE_STATUS = [
        ('good', 'Good (>75%)'),
        ('warning', 'Warning (60-75%)'),
        ('critical', 'Critical (<60%)'),
    ]
    status = models.CharField(max_length=20, choices=ATTENDANCE_STATUS, default='good')
    
    class Meta:
        unique_together = ['student', 'course', 'semester']


class Invigilation(models.Model):
    """Lecturer invigilation assignments."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    invigilator = models.ForeignKey(
        'staff.StaffProfile',
        on_delete=models.CASCADE,
        related_name='invigilation_duties'
    )
    
    # Exam details
    exam = models.ForeignKey('learning.Exam', on_delete=models.CASCADE)
    
    # Assignment
    is_principal = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=[
            ('assigned', 'Assigned'),
            ('accepted', 'Accepted'),
            ('completed', 'Completed'),
            ('reported', 'Reported'),
        ],
        default='assigned'
    )
    
    # Report
    students_present = models.IntegerField(default=0)
    students_absent = models.IntegerField(default=0)
    incidents = models.TextField(blank=True)
    
    assigned_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['invigilator', 'exam']


class Publication(models.Model):
    """Lecturer research publications."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    author = models.ForeignKey(
        'staff.StaffProfile',
        on_delete=models.CASCADE,
        related_name='publications'
    )
    
    title = models.CharField(max_length=500)
    journal = models.CharField(max_length=200)
    
    TYPE = [
        ('journal', 'Journal Article'),
        ('conference', 'Conference Paper'),
        ('book', 'Book Chapter'),
        ('book_chapter', 'Book'),
        ('technical', 'Technical Report'),
    ]
    publication_type = models.CharField(max_length=20, choices=TYPE)
    
    # Details
    year = models.IntegerField()
    volume = models.CharField(max_length=20, blank=True)
    pages = models.CharField(max_length=20, blank=True)
    doi = models.CharField(max_length=100, blank=True)
    
    # Indexing
    is_indexed = models.BooleanField(default=False)
    indexing_bodies = models.JSONField(default=list)
    # ['SCIE', 'SSCI', 'AHCI', 'COPERNICUS']
    
    citation_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class ResearchGrant(models.Model):
    """Research grants/funding."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    researcher = models.ForeignKey(
        'staff.StaffProfile',
        on_delete=models.CASCADE,
        related_name='grants'
    )
    
    title = models.CharField(max_length=500)
    funding_body = models.CharField(max_length=200)
    
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    currency = models.CharField(max_length=3, default='NGN')
    
    start_date = models.DateField()
    end_date = models.DateField()
    
    STATUS = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('terminated', 'Terminated'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)


class DepartmentBudget(models.Model):
    """Department budget management."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    department = models.ForeignKey(
        'academic.Department',
        on_delete=models.CASCADE,
        related_name='budgets'
    )
    
    session = models.ForeignKey('academic.AcademicSession', on_delete=models.CASCADE)
    
    # Budget
    allocated = models.DecimalField(max_digits=14, decimal_places=2)
    spent = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    
    # Allocation breakdown
    allocation_detail = models.JSONField(default=dict)
    # {'personnel': 500000, 'equipment': 200000, 'research': 300000}
    
    approved_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='+'
    )
    
    approved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['department', 'session']


class FeeDebtCollection(models.Model):
    """Fee debt recovery tracking."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey(
        'student.StudentProfile',
        on_delete=models.CASCADE,
        related_name='debt_collections'
    )
    
    # Debt details
    total_debt = models.DecimalField(max_digits=14, decimal_places=2)
    payments = models.JSONField(default=list)
    # [{'amount': 10000, 'date': '2024-01-15'}]
    
    # Collection
    STATUS = [
        ('active', 'Active'),
        ('payment_plan', 'Payment Plan'),
        ('collected', 'Fully Collected'),
        ('written_off', 'Written Off'),
        ('sent_legal', 'Sent to Legal'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='active')
    
    contact_attempts = models.IntegerField(default=0)
    last_contact = models.DateField(null=True, blank=True)
    
    payment_plan_amount = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True
    )
    payment_plan_due = models.DateField(null=True, blank=True)
    
    assigned_to = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='+'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)