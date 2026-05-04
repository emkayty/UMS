from ninja import Router, Schema
from typing import Optional, List
from django.shortcuts import get_object_or_404
from django.utils import timezone

from apps.staff.models import (
    StaffProfile, LeaveRequest, LeaveBalance, LeaveType,
    LeaveRequestStatus, PromotionRecord
)
from apps.staff.leave_accrual import LeaveAccrualService

router = Router(tags=['Staff'])


# === Staff Schemas ===
class StaffProfileSchema(Schema):
    id: str
    user_id: str
    first_name: str
    last_name: str
    staff_id: str
    faculty_id: Optional[str]
    department_id: Optional[str]
    rank: str
    is_active: bool


class StaffProfileCreateSchema(Schema):
    user_id: str  # email
    first_name: str
    last_name: str
    staff_id: str
    faculty_id: Optional[str] = None
    department_id: Optional[str] = None
    rank: str
    employment_date: str


class LeaveRequestCreateSchema(Schema):
    leave_type: str
    start_date: str
    end_date: str
    reason: str


class LeaveRequestUpdateSchema(Schema):
    status: Optional[str] = None
    approval_comment: Optional[str] = None
    rejection_reason: Optional[str] = None


class LeaveRequestSchema(Schema):
    id: str
    staff_id: str
    leave_type: str
    start_date: str
    end_date: str
    status: str
    reason: str


class LeaveBalanceSchema(Schema):
    id: str
    leave_type: str
    year: int
    total_days: int
    used_days: int
    remaining_days: int


# === Staff CRUD ===
@router.get('/staff', response=List[StaffProfileSchema])
def list_staff(request, department_id: str = None, faculty_id: str = None, is_active: bool = None):
    """List staff with filters."""
    qs = StaffProfile.objects.all()
    if department_id:
        qs = qs.filter(department_id=department_id)
    if faculty_id:
        qs = qs.filter(faculty_id=faculty_id)
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs[:100]


@router.post('/staff', response=StaffProfileSchema)
def create_staff(request, data: StaffProfileCreateSchema):
    """Create new staff member."""
    from apps.accounts.models import User
    from datetime import datetime
    
    # Get or create user account
    try:
        user = User.objects.get(email=data.user_id)
    except User.DoesNotExist:
        user = User.objects.create_user(
            email=data.user_id,
            password=f"{data.staff_id}2024",  # Default password
            role='lecturer'
        )
    
    staff = StaffProfile.objects.create(
        user=user,
        first_name=data.first_name,
        last_name=data.last_name,
        staff_id=data.staff_id,
        faculty_id=data.faculty_id,
        department_id=data.department_id,
        rank=data.rank,
        employment_date=datetime.strptime(data.employment_date, '%Y-%m-%d').date()
    )
    
    # Initialize leave balances
    LeaveAccrualService.initialize_leave_balances(staff)
    
    return staff


@router.get('/staff/{id}', response=StaffProfileSchema)
def get_staff(request, id: str):
    return get_object_or_404(StaffProfile, id=id)


@router.patch('/staff/{id}', response=StaffProfileSchema)
def update_staff(request, id: str, data: dict):
    """Update staff profile."""
    staff = get_object_or_404(StaffProfile, id=id)
    for field in ['first_name', 'last_name', 'rank', 'grade', 'step', 'phone']:
        if field in data and data[field] is not None:
            setattr(staff, field, data[field])
    staff.save()
    return staff


@router.delete('/staff/{id}')
def delete_staff(request, id: str):
    """Soft delete staff (deactivate)."""
    staff = get_object_or_404(StaffProfile, id=id)
    staff.is_active = False
    staff.termination_date = timezone.now().date()
    staff.save()
    return {'success': True, 'message': 'Staff deactivated'}


@router.get('/staff/{id}/profile')
def get_staff_profile(request, id: str):
    """Get staff full profile with computed fields."""
    staff = get_object_or_404(StaffProfile, id=id)
    return {
        'id': str(staff.id),
        'name': staff.full_name,
        'staff_id': staff.staff_id,
        'department': staff.department.name if staff.department else None,
        'faculty': staff.faculty.name if staff.faculty else None,
        'rank': staff.rank,
        'grade': staff.grade,
        'step': staff.step,
        'is_confirmed': staff.is_confirmed,
        'years_of_service': staff.years_of_service,
        'is_active': staff.is_active,
        'employment_date': staff.employment_date.isoformat()
    }


# === Leave Request CRUD ===
@router.get('/leave', response=List[LeaveRequestSchema])
def list_leave_requests(request, staff_id: str = None, status: str = None):
    """List leave requests."""
    qs = LeaveRequest.objects.all()
    if staff_id:
        qs = qs.filter(staff_id=staff_id)
    if status:
        qs = qs.filter(status=status)
    return qs[:100]


@router.post('/leave', response=LeaveRequestSchema)
def create_leave_request(request, data: LeaveRequestCreateSchema):
    """Create leave request."""
    from apps.accounts.models import User
    
    # Get staff profile from user
    staff = get_object_or_404(StaffProfile, user=request.auth[0])
    
    leave_request = LeaveRequest.objects.create(
        staff=staff,
        leave_type=data.leave_type,
        start_date=data.start_date,
        end_date=data.end_date,
        reason=data.reason
    )
    return leave_request


@router.get('/leave/{id}', response=LeaveRequestSchema)
def get_leave_request(request, id: str):
    return get_object_or_404(LeaveRequest, id=id)


@router.patch('/leave/{id}/approve', response=LeaveRequestSchema)
def approve_leave(request, id: str, data: LeaveRequestUpdateSchema):
    """Approve leave request."""
    leave = get_object_or_404(LeaveRequest, id=id)
    
    if leave.status != LeaveRequestStatus.PENDING:
        return {'error': 'Can only approve pending requests'}
    
    leave.status = LeaveRequestStatus.APPROVED
    leave.approved_by = request.auth[0]
    leave.approval_comment = data.approval_comment or ''
    leave.save()
    
    # Update leave balance
    LeaveAccrualService.record_leave_taken(leave)
    
    return leave


@router.patch('/leave/{id}/reject', response=LeaveRequestSchema)
def reject_leave(request, id: str, data: LeaveRequestUpdateSchema):
    """Reject leave request."""
    leave = get_object_or_404(LeaveRequest, id=id)
    
    if leave.status != LeaveRequestStatus.PENDING:
        return {'error': 'Can only reject pending requests'}
    
    leave.status = LeaveRequestStatus.REJECTED
    leave.approved_by = request.auth[0]
    leave.rejection_reason = data.rejection_reason or ''
    leave.save()
    
    return leave


# === Leave Balance ===
@router.get('/leave-balances/{staff_id}', response=List[LeaveBalanceSchema])
def get_leave_balances(request, staff_id: str):
    """Get staff leave balances."""
    balances = LeaveBalance.objects.filter(staff_id=staff_id)
    return [
        {
            'id': str(b.id),
            'leave_type': b.leave_type,
            'year': b.year,
            'total_days': b.total_days,
            'used_days': b.used_days,
            'remaining_days': b.remaining_days
        }
        for b in balances
    ]


# === Leave APIs ===
@router.post('/staff/{id}/leave', response=dict)
def request_leave(request, id: str, data: LeaveRequestSchema):
    """Submit leave request."""
    staff = get_object_or_404(StaffProfile, id=id)
    
    leave = LeaveRequest.objects.create(
        staff=staff,
        leave_type=data.leave_type,
        start_date=data.start_date,
        end_date=data.end_date,
        reason=data.reason
    )
    
    return {'success': True, 'leave_id': str(leave.id)}


@router.get('/staff/{id}/leaves')
def get_leave_history(request, id: str):
    """Get staff leave history."""
    staff = get_object_or_404(StaffProfile, id=id)
    leaves = LeaveRequest.objects.filter(staff=staff)
    
    return [
        {
            'id': str(l.id),
            'leave_type': l.leave_type,
            'start_date': l.start_date.isoformat(),
            'end_date': l.end_date.isoformat(),
            'status': l.status,
            'created_at': l.created_at.isoformat()
        }
        for l in leaves
    ]


@router.get('/leaves', response=List[LeaveRequestSchema])
def list_leave_requests(request, status: str = 'pending', department_id: str = None):
    """List pending leave requests (for HOD/admin)."""
    qs = LeaveRequest.objects.filter(status=status)
    if department_id:
        qs = qs.filter(staff__department_id=department_id)
    return qs


@router.patch('/leaves/{id}')
def process_leave(request, id: str, data: dict):
    """Approve/reject leave."""
    leave = get_object_or_404(LeaveRequest, id=id)
    action = data.get('action')
    
    if action == 'approve':
        leave.status = 'approved'
    elif action == 'reject':
        leave.status = 'rejected'
    
    leave.approved_by = request.auth[0]
    leave.approval_comment = data.get('comment', '')
    leave.save()
    
    return {'success': True}


# === Promotion APIs ===
@router.post('/staff/{id}/promotion')
def record_promotion(request, id: str, data: dict):
    """Record staff promotion."""
    staff = get_object_or_404(StaffProfile, id=id)
    
    promotion = PromotionRecord.objects.create(
        staff=staff,
        from_rank=data.get('from_rank'),
        to_rank=data.get('to_rank'),
        effective_date=data.get('effective_date'),
        approved_by=request.auth[0]
    )
    
    # Update staff rank
    staff.rank = data.get('to_rank')
    staff.save()
    
    return {'success': True}


# === Appraisals ===
@router.get('/staff/{id}/appraisals')
def get_appraisals(request, id: str):
    """Get staff appraisals."""
    staff = get_object_or_404(StaffProfile, id=id)
    appraisals = staff.appraisals.all()
    
    return [
        {
            'session': a.session.name,
            'score': float(a.score),
            'comment': a.comment
        }
        for a in appraisals
    ]


# === Payroll (for Bursar) ===
@router.get('/payroll')
def get_payroll(request, department_id: str = None, month: str = None):
    """Get payroll data."""
    from apps.finance.models import PayrollRecord
    
    qs = PayrollRecord.objects.all()
    if department_id:
        qs = qs.filter(staff__department_id=department_id)
    if month:
        qs = qs.filter(month=month)
    
    return [
        {
            'staff_id': str(p.staff.id),
            'name': f"{p.staff.first_name} {p.staff.last_name}",
            'basic_salary': float(p.basic_salary),
            'allowances': float(p.allowances),
            'deductions': float(p.deductions),
            'net_pay': float(p.net_pay)
        }
        for p in qs
    ]