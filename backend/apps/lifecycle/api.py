from ninja import Router, Schema
from typing import Optional
from django.db.models import Count, Sum

router = Router(tags=['Lifecycle'])


# === Applicant APIs ===
@router.get('/applicants')
def list_applicants(request, status: str = None):
    """List all applicants."""
    from apps.lifecycle.models import ApplicantData
    
    qs = ApplicantData.objects.all()
    if status:
        qs = qs.filter(application_status=status)
    
    return {
        'count': qs.count(),
        'applicants': [
            {
                'id': str(a.id),
                'name': f"{a.first_name} {a.last_name}",
                'email': a.email,
                'phone': a.phone,
                'state': a.state_of_origin,
                'jamb_score': a.jamb_score,
                'status': a.application_status
            }
            for a in qs[:50]
        ]
    }


@router.post('/apply')
def submit_application(request, data: dict):
    """Submit new admission application."""
    from apps.lifecycle.models import ApplicantData
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    email = data.get('email')
    
    user, _ = User.objects.get_or_create(
        email=email,
        defaults={'role': 'student', 'is_active': False}
    )
    if data.get('password'):
        user.set_password(data.get('password'))
        user.save()
    
    applicant = ApplicantData.objects.create(
        user=user,
        title=data.get('title', ''),
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        date_of_birth=data.get('date_of_birth'),
        state_of_origin=data.get('state_of_origin', ''),
        local_govt_area=data.get('lga', ''),
        phone=data.get('phone', ''),
        email=email,
        father_name=data.get('father_name', ''),
        father_phone=data.get('father_phone', ''),
        father_email=data.get('father_email', ''),
        mother_name=data.get('mother_name', ''),
        mother_phone=data.get('mother_phone', ''),
        guardian_name=data.get('guardian_name', ''),
        guardian_phone=data.get('guardian_phone', ''),
        emergency_contact_name=data.get('emergency_name', ''),
        emergency_contact_phone=data.get('emergency_phone', ''),
        jamb_registration_number=data.get('jamb_reg_no', ''),
        jamb_score=data.get('jamb_score'),
        application_status='submitted'
    )
    
    return {'id': str(applicant.id), 'status': 'Application submitted successfully'}


# === Hostel APIs ===
@router.get('/hostels')
def list_hostels(request):
    """List all hostels."""
    from apps.lifecycle.models import Hostel
    
    hostels = Hostel.objects.filter(is_active=True)
    return {
        'count': hostels.count(),
        'hostels': [
            {
                'id': str(h.id),
                'name': h.name,
                'code': h.code,
                'gender': h.gender,
                'capacity': h.capacity,
                'available': h.capacity - h.occupied,
                'location': h.location,
                'has_wifi': h.has_wifi,
                'has_ac': h.has_ac
            }
            for h in hostels
        ]
    }


@router.post('/hostels/{hostel_id}/allocate')
def allocate_hostel(request, hostel_id: str, data: dict):
    """Allocate hostel to student."""
    from apps.lifecycle.models import Hostel, StudentHostelAllocation
    from apps.student.models import StudentProfile
    from apps.academic.models import AcademicSession
    
    try:
        hostel = Hostel.objects.get(id=hostel_id)
    except Hostel.DoesNotExist:
        return {'error': 'Hostel not found'}
    
    student = StudentProfile.objects.get(id=data.get('student_id'))
    session = AcademicSession.objects.filter(is_current=True).first()
    
    allocation = StudentHostelAllocation.objects.create(
        student=student,
        session=session,
        hostel=hostel,
        block=data.get('block', 'A'),
        floor=data.get('floor', 1),
        room_number=data.get('room_number', '001'),
        bed_number=data.get('bed_number', 1),
        room_type=data.get('room_type', 'double'),
        hostel_fee=data.get('fee', 50000),
    )
    
    hostel.occupied += 1
    hostel.save()
    
    return {'id': str(allocation.id), 'status': 'allocated'}


# === Student Hostel ===
@router.get('/students/{student_id}/hostel')
def get_student_hostel(request, student_id: str):
    """Get student's hostel allocation."""
    from apps.lifecycle.models import StudentHostelAllocation
    
    try:
        allocation = StudentHostelAllocation.objects.get(student_id=student_id)
        return {
            'id': str(allocation.id),
            'hostel': allocation.hostel.name,
            'block': allocation.block,
            'floor': allocation.floor,
            'room': allocation.room_number,
            'bed': allocation.bed_number,
            'status': allocation.status
        }
    except StudentHostelAllocation.DoesNotExist:
        return {'status': 'Not allocated'}


# === Change Requests ===
@router.get('/change-requests')
def list_change_requests(request, status: str = None):
    """List change requests."""
    from apps.lifecycle.models import StudentChangeRequest
    
    qs = StudentChangeRequest.objects.all()
    if status:
        qs = qs.filter(status=status)
    
    return {
        'count': qs.count(),
        'requests': [
            {
                'id': str(r.id),
                'student': f"{r.student.first_name} {r.student.last_name}",
                'type': r.request_type,
                'current': r.current_value,
                'requested': r.requested_value,
                'status': r.status
            }
            for r in qs[:20]
        ]
    }


# === Discipline ===
@router.get('/discipline')
def list_discipline(request, status: str = None):
    """List disciplinary cases."""
    from apps.lifecycle.models import StudentDiscipline
    
    qs = StudentDiscipline.objects.all()
    if status:
        qs = qs.filter(status=status)
    
    return {
        'count': qs.count(),
        'cases': [
            {
                'id': str(d.id),
                'student': f"{d.student.first_name} {d.student.last_name}",
                'offence': d.offence_type,
                'severity': d.severity,
                'action': d.action,
                'status': d.status,
                'date': d.incident_date.isoformat() if d.incident_date else None
            }
            for d in qs[:20]
        ]
    }


# === Surveys ===
@router.get('/surveys')
def list_surveys(request, survey_type: str = None):
    """List available surveys."""
    from apps.lifecycle.models import StudentSurvey
    
    qs = StudentSurvey.objects.filter(is_active=True)
    if survey_type:
        qs = qs.filter(survey_type=survey_type)
    
    return {
        'count': qs.count(),
        'surveys': [
            {
                'id': str(s.id),
                'title': s.title,
                'type': s.survey_type,
                'start': s.start_date.isoformat() if s.start_date else None,
                'end': s.end_date.isoformat() if s.end_date else None,
                'questions': len(s.questions or [])
            }
            for s in qs[:20]
        ]
    }


# === Alumni ===
@router.get('/alumni')
def list_alumni(request, graduation_year: int = None):
    """List alumni."""
    from apps.lifecycle.models import AlumniRecord
    
    qs = AlumniRecord.objects.all()
    if graduation_year:
        qs = qs.filter(graduation_year=graduation_year)
    
    return {
        'count': qs.count(),
        'alumni': [
            {
                'id': str(a.id),
                'name': f"{a.student.first_name} {a.student.last_name}",
                'matric': a.student.matric_number,
                'year': a.graduation_year,
                'degree': a.degree_awarded,
                'class': a.class_of_degree,
                'employed': a.is_employed
            }
            for a in qs[:50]
        ]
    }


# === Staff Recruitment ===
@router.get('/jobs')
def list_jobs(request, status: str = None):
    """List job postings."""
    from apps.lifecycle.models import JobPosting
    
    qs = JobPosting.objects.filter(is_active=True)
    if status:
        qs = qs.filter(status=status)
    
    return {
        'count': qs.count(),
        'jobs': [
            {
                'id': str(j.id),
                'title': j.title,
                'department': j.department.name if j.department else '',
                'level': j.level,
                'type': j.employment_type,
                'closing': j.closing_date.isoformat() if j.closing_date else None
            }
            for j in qs[:20]
        ]
    }


@router.post('/jobs')
def create_job(request, data: dict):
    """Create job posting."""
    from apps.lifecycle.models import JobPosting
    from apps.academic.models import Department
    
    job = JobPosting.objects.create(
        title=data.get('title'),
        department_id=data.get('department_id'),
        employment_type=data.get('type', 'permanent'),
        level=data.get('level', 'lecturer'),
        minimum_qualification=data.get('qualification', 'PhD'),
        job_description=data.get('description', ''),
        responsibilities=data.get('responsibilities', ''),
        benefits=data.get('benefits', ''),
        posting_date=data.get('posting_date'),
        closing_date=data.get('closing_date'),
        status='open'
    )
    
    return {'id': str(job.id), 'status': 'Job posted successfully'}


# === Staff Leave ===
@router.get('/leave-balances')
def list_leave_balances(request):
    """List staff leave balances."""
    from apps.lifecycle.models import LeaveBalance
    from apps.staff.models import StaffProfile
    
    balances = LeaveBalance.objects.all()[:50]
    return {
        'count': balances.count(),
        'balances': [
            {
                'id': str(b.id),
                'staff': f"{b.staff.first_name} {b.staff.last_name}",
                'annual_remaining': b.annual_remaining,
                'sick_remaining': b.sick_remaining,
                'casual_remaining': b.casual_remaining
            }
            for b in balances
        ]
    }


# === Parent Accounts ===
@router.get('/parents')
def list_parent_accounts(request):
    """List parent accounts."""
    from apps.lifecycle.models import ParentAccount
    
    accounts = ParentAccount.objects.all()[:50]
    return {
        'count': accounts.count(),
        'parents': [
            {
                'id': str(p.id),
                'name': f"{p.first_name} {p.last_name}",
                'email': p.email,
                'phone': p.phone,
                'relationship': p.relationship,
                'student': f"{p.student.first_name} {p.student.last_name}",
                'verified': p.is_verified
            }
            for p in accounts
        ]
    }