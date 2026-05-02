"""
Academic Workflow Models
HOD/Dean approval workflows and budget management
"""

from django.db import models
import uuid


class ApprovalWorkflow(models.Model):
    """Generic approval workflow."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Request details
    request_type = models.CharField(max_length=50)
    request_id = models.UUIDField()
    
    # Current approver
    current_level = models.CharField(
        max_length=20,
        choices=[
            ('hod', 'HOD'),
            ('dean', 'Dean'),
            ('registrar', 'Registrar'),
            ('bursar', 'Bursar'),
            ('vc', 'Vice Chancellor'),
            ('senate', 'Senate'),
        ],
        default='hod'
    )
    
    # Workflow definition
    workflow_sequence = models.JSONField(default=list)
    # ['hod', 'dean', 'senate']
    
    STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)


class ApprovalAction(models.Model):
    """Individual approval actions."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    workflow = models.ForeignKey(
        ApprovalWorkflow,
        on_delete=models.CASCADE,
        related_name='actions'
    )
    
    approver = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True)
    
    level = models.CharField(max_length=20)
    
    action = models.CharField(
        max_length=20,
        choices=[
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('requested_changes', 'Requested Changes'),
        ]
    )
    
    comment = models.TextField(blank=True)
    
    acted_at = models.DateTimeField(auto_now_add=True)


class ResultModeration(models.Model):
    """Result moderation workflow."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Course
    course = models.ForeignKey('academic.Course', on_delete=models.CASCADE)
    session = models.ForeignKey('academic.AcademicSession', on_delete=models.CASCADE)
    semester = models.ForeignKey('academic.Semester', on_delete=models.CASCADE)
    
    # Moderation status
    submitted_by = models.ForeignKey(
        'staff.StaffProfile',
        on_delete=models.SET_NULL,
        null=True,
        related_name='+'
    )
    
    MODERATION_STATUS = [
        ('pending', 'Pending HOD'),
        ('hod_approved', 'Approved by HOD'),
        ('pending_dean', 'Pending Dean'),
        ('dean_approved', 'Approved by Dean'),
        ('senate_approved', ' Approved by Senate'),
        ('published', 'Published'),
    ]
    status = models.CharField(max_length=30, choices=MODERATION_STATUS, default='pending')
    
    # Statistics before moderation
    total_students = models.IntegerField(default=0)
    pass_count = models.IntegerField(default=0)
    fail_count = models.IntegerField(default=0)
    mean_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    standard_deviation = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # HOD approval
    hod_approved = models.BooleanField(default=False)
    hod = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='+'
    )
    hod_approved_at = models.DateTimeField(null=True, blank=True)
    
    # Dean approval
    dean_approved = models.BooleanField(default=False)
    dean = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='+'
    )
    dean_approved_at = models.DateTimeField(null=True, blank=True)
    
    # Senate approval
    senate_approved = models.BooleanField(default=False)
    senate_approved_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['course', 'session', 'semester']


class CourseAllocation(models.Model):
    """Course allocation to lecturers."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    course = models.ForeignKey('academic.Course', on_delete=models.CASCADE)
    session = models.ForeignKey('academic.AcademicSession', on_delete=models.CASCADE)
    semester = models.ForeignKey('academic.Semester', on_delete=models.CASCADE)
    
    # Lecturer
    lecturer = models.ForeignKey(
        'staff.StaffProfile',
        on_delete=models.CASCADE,
        related_name='allocated_courses'
    )
    
    # Allocation
    is_coordinator = models.BooleanField(default=False)
    allocated_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='+'
    )
    
    approved_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='+'
    )
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )
    
    class Meta:
        unique_together = ['course', 'session', 'semester', 'lecturer']


class ClearanceItem(models.Model):
    """Graduation clearance items."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=100)
    department = models.ForeignKey(
        'academic.Department',
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    
    description = models.TextField()
    is_required = models.BooleanField(default=True)
    
    # Approval
    required_role = models.CharField(
        max_length=20,
        choices=[
            ('library', 'Library'),
            ('sports', 'Sports'),
            ('hostel', 'Hostel'),
            ('ict', 'ICT'),
            ('accounts', 'Accounts'),
            ('registry', 'Registry'),
        ],
        default='registry'
    )
    
    order = models.IntegerField(default=0)


class StudentClearance(models.Model):
    """Student graduation clearance."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey(
        'student.StudentProfile',
        on_delete=models.CASCADE,
        related_name='clearances'
    )
    
    session = models.ForeignKey('academic.AcademicSession', on_delete=models.CASCADE)
    
    # Overall status
    STATUS = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('released', 'Released'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    
    # Completion
    completed_at = models.DateTimeField(null=True, blank=True)
    released_at = models.DateTimeField(null=True, blank=True)
    released_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='+'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)


class ClearanceStatus(models.Model):
    """Individual clearance item status."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    clearance = models.ForeignKey(
        StudentClearance,
        on_delete=models.CASCADE,
        related_name='items'
    )
    
    item = models.ForeignKey(ClearanceItem, on_delete=models.CASCADE)
    
    STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    
    comment = models.CharField(max_length=200, blank=True)
    approved_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='+'
    )
    
    approved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['clearance', 'item']