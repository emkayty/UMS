"""
Academic Workflow APIs
Result moderation, approval workflows, clearance
"""

from ninja import Router, Schema
from typing import List, Optional
from django.shortcuts import get_object_or_404
from django.utils import timezone

router = Router(tags=['Workflow'])


# === Schemas ===
class ResultModerationSchema(Schema):
    id: str
    course_id: str
    status: str
    total_students: int
    pass_count: int
    fail_count: int
    mean_score: float


class ApprovalActionSchema(Schema):
    id: str
    request_type: str
    current_level: str
    status: str
    created_at: str


class ClearanceItemSchema(Schema):
    id: str
    name: str
    department_id: Optional[str]
    is_required: bool
    required_role: str
    order: int


class StudentClearanceSchema(Schema):
    id: str
    student_id: str
    session_id: str
    status: str
    completed_at: Optional[str]


class ClearanceActionSchema(Schema):
    item_id: str
    status: str
    comment: Optional[str] = ''


class CourseAllocationSchema(Schema):
    id: str
    course_id: str
    lecturer_id: str
    is_coordinator: bool
    status: str


# === Result Moderation ===
@router.get('/moderation')
def list_moderation(request):
    """List result moderation records."""
    from apps.student.workflow import ResultModeration
    
    mods = ResultModeration.objects.all().order_by('-created_at')
    
    return [
        {
            'id': str(m.id),
            'course': m.course.code if m.course else None,
            'status': m.status,
            'total': m.total_students,
            'mean': float(m.mean_score)
        }
        for m in mods
    ]


@router.get('/moderation/{course_id}/{session_id}/{semester_id}')
def get_moderation(request, course_id: str, session_id: str, semester_id: str):
    """Get moderation for specific course."""
    from apps.student.workflow import ResultModeration
    
    mod = ResultModeration.objects.filter(
        course_id=course_id,
        session_id=session_id,
        semester_id=semester_id
    ).first()
    
    if not mod:
        return {
            'id': None,
            'status': 'pending',
            'hod_approved': False,
            'dean_approved': False,
            'senate_approved': False
        }
    
    return {
        'id': str(mod.id),
        'status': mod.status,
        'total_students': mod.total_students,
        'pass_count': mod.pass_count,
        'fail_count': mod.fail_count,
        'mean': float(mod.mean_score),
        'hod_approved': mod.hod_approved,
        'dean_approved': mod.dean_approved,
        'senate_approved': mod.senate_approved
    }


@router.post('/moderation/{id}/hod-approve')
def hod_approve_moderation(request, id: str):
    """HOD approves results."""
    from apps.student.workflow import ResultModeration
    
    mod = get_object_or_404(ResultModeration, id=id)
    mod.hod_approved = True
    mod.hod = request.auth[0]
    mod.hod_approved_at = timezone.now()
    
    # Update status
    if mod.hod_approved and not mod.status.startswith('hod'):
        mod.status = 'hod_approved'
    
    mod.save()
    
    return {'success': True, 'status': mod.status}


@router.post('/moderation/{id}/dean-approve')
def dean_approve_moderation(request, id: str):
    """Dean approves results."""
    from apps.student.workflow import ResultModeration
    
    mod = get_object_or_404(ResultModeration, id=id)
    mod.dean_approved = True
    mod.dean = request.auth[0]
    mod.dean_approved_at = timezone.now()
    
    if mod.dean_approved:
        mod.status = 'dean_approved'
    
    mod.save()
    
    return {'success': True, 'status': mod.status}


@router.post('/moderation/{id}/senate-approve')
def senate_approve_moderation(request, id: str):
    """Senate approves and publishes results."""
    from apps.student.workflow import ResultModeration
    
    mod = get_object_or_404(ResultModeration, id=id)
    mod.senate_approved = True
    mod.senate_approved_at = timezone.now()
    mod.status = 'published'
    mod.save()
    
    return {'success': True, 'status': mod.status}


# === Approval Workflow ===
@router.get('/approvals')
def list_approvals(request):
    """List pending approvals for user."""
    from apps.student.workflow import ApprovalWorkflow
    from apps.accounts.models import User
    
    # Get pending for current user's role
    role = request.auth[0].role
    
    pending = ApprovalWorkflow.objects.filter(
        current_level=role,
        status='pending'
    ).order_by('-created_at')
    
    return [
        {
            'id': str(a.id),
            'request_type': a.request_type,
            'current_level': a.current_level,
            'created_at': str(a.created_at)
        }
        for a in pending
    ]


@router.post('/approvals/{id}/approve')
def approve_request(request, id: str, comment: str = ''):
    """Approve a request."""
    from apps.student.workflow import ApprovalWorkflow, ApprovalAction
    
    workflow = get_object_or_404(ApprovalWorkflow, id=id)
    
    # Record action
    ApprovalAction.objects.create(
        workflow=workflow,
        approver=request.auth[0],
        level=workflow.current_level,
        action='approved',
        comment=comment
    )
    
    # Move to next level
    current_idx = workflow.workflow_sequence.index(workflow.current_level) if workflow.current_level in workflow.workflow_sequence else -1
    
    if current_idx + 1 < len(workflow.workflow_sequence):
        workflow.current_level = workflow.workflow_sequence[current_idx + 1]
    else:
        workflow.status = 'approved'
        workflow.completed_at = timezone.now()
    
    workflow.save()
    
    return {'success': True, 'current_level': workflow.current_level}


@router.post('/approvals/{id}/reject')
def reject_request(request, id: str, reason: str):
    """Reject a request."""
    from apps.student.workflow import ApprovalWorkflow, ApprovalAction
    
    workflow = get_object_or_404(ApprovalWorkflow, id=id)
    
    # Record rejection
    ApprovalAction.objects.create(
        workflow=workflow,
        approver=request.auth[0],
        level=workflow.current_level,
        action='rejected',
        comment=reason
    )
    
    workflow.status = 'rejected'
    workflow.completed_at = timezone.now()
    workflow.save()
    
    return {'success': True, 'status': 'rejected'}


# === Course Allocation ===
@router.get('/allocation')
def list_allocations(request):
    """List course allocations."""
    from apps.student.workflow import CourseAllocation
    
    allocations = CourseAllocation.objects.all()
    
    return [
        {
            'id': str(a.id),
            'course': a.course.code if a.course else None,
            'lecturer': a.lecturer.user.get_full_name() if a.lecturer and a.lecturer.user else None,
            'is_coordinator': a.is_coordinator,
            'status': a.status
        }
        for a in allocations
    ]


@router.post('/allocation')
def create_allocation(request, data: CourseAllocationSchema):
    """Create course allocation."""
    from apps.student.workflow import CourseAllocation
    from apps.academic.models import Course
    from apps.staff.models import StaffProfile
    
    allocation = CourseAllocation.objects.create(
        course_id=data.course_id,
        lecturer_id=data.lecturer_id,
        is_coordinator=data.is_coordinator,
        status='pending',
        allocated_by=request.auth[0]
    )
    
    return {'success': True, 'id': str(allocation.id)}


@router.post('/allocation/{id}/approve')
def approve_allocation(request, id: str):
    """Approve course allocation."""
    from apps.student.workflow import CourseAllocation
    
    allocation = get_object_or_404(CourseAllocation, id=id)
    allocation.status = 'approved'
    allocation.approved_by = request.auth[0]
    allocation.save()
    
    return {'success': True}


# === Clearance ===
@router.get('/clearance/items')
def list_clearance_items(request):
    """List all clearance items."""
    from apps.student.workflow import ClearanceItem
    
    items = ClearanceItem.objects.all().order_by('order')
    
    return [
        {
            'id': str(i.id),
            'name': i.name,
            'required_role': i.required_role,
            'is_required': i.is_required
        }
        for i in items
    ]


@router.post('/clearance/items')
def create_clearance_item(request, data: ClearanceItemSchema):
    """Create clearance item."""
    from apps.student.workflow import ClearanceItem
    
    item = ClearanceItem.objects.create(
        name=data.name,
        department_id=data.department_id,
        is_required=data.is_required,
        required_role=data.required_role,
        order=data.order
    )
    
    return {'success': True, 'id': str(item.id)}


@router.get('/clearance/student/{student_id}')
def get_student_clearance(request, student_id: str):
    """Get student clearance status."""
    from apps.student.workflow import StudentClearance, ClearanceStatus
    
    clearance = StudentClearance.objects.filter(
        student_id=student_id
    ).order_by('-created_at').first()
    
    if not clearance:
        return {'status': 'none'}
    
    items = ClearanceStatus.objects.filter(clearance=clearance)
    
    return {
        'id': str(clearance.id),
        'status': clearance.status,
        'items': [
            {
                'item': item.item.name,
                'status': item.status,
                'comment': item.comment
            }
            for item in items
        ]
    }


@router.post('/clearance/student/{clearance_id}/action')
def clearance_action(request, clearance_id: str, data: ClearanceActionSchema):
    """Process clearance item."""
    from apps.student.workflow import StudentClearance, ClearanceStatus
    
    clearance = get_object_or_404(StudentClearance, id=clearance_id)
    
    status = ClearanceStatus.objects.filter(
        clearance=clearance,
        item_id=data.item_id
    ).first()
    
    if status:
        status.status = data.status
        status.comment = data.comment
        status.approved_by = request.auth[0]
        status.approved_at = timezone.now()
        status.save()
        
        # Check if all required items approved
        pending = clearance.items.filter(status='pending', item__is_required=True).count()
        if pending == 0:
            clearance.status = 'completed'
            clearance.completed_at = timezone.now()
            clearance.save()
    
    return {'success': True}