"""
Disciplinary & Course Registration APIs
Disciplinary cases, hearings, course overrides
"""

from ninja import Router, Schema
from typing import List, Optional
from django.shortcuts import get_object_or_404
from django.utils import timezone

router = Router(tags=['Disciplinary'])


# === Schemas ===
class DisciplinaryCaseSchema(Schema):
    id: str
    student_id: str
    category: str
    incident_date: str
    status: str


class DisciplinaryCreateSchema(Schema):
    student_id: str
    incident_date: str
    incident_location: str
    category: str
    description: str


class DisciplinaryHearingSchema(Schema):
    case_id: str
    hearing_date: str
    hearing_time: str
    venue: str


class HearingDecisionSchema(Schema):
    decision: str
    sanction_details: Optional[str] = ''


class CourseOverrideSchema(Schema):
    student_id: str
    course_id: str
    session_id: str
    semester_id: str
    reason: str


class WarningSchema(Schema):
    id: str
    student_id: str
    warning_type: str
    reason: str
    is_resolved: bool


# === Disciplinary APIs ===
@router.get('/cases')
def list_cases(request):
    """List all disciplinary cases."""
    from apps.student.disciplinary import DisciplinaryCase
    
    cases = DisciplinaryCase.objects.all().order_by('-created_at')
    
    return [
        {
            'id': str(c.id),
            'student': c.student.user.get_full_name() if c.student and c.student.user else None,
            'category': c.category,
            'status': c.status,
            'date': str(c.incident_date)
        }
        for c in cases
    ]


@router.get('/cases/{id}')
def get_case(request, id: str):
    """Get case details."""
    from apps.student.disciplinary import DisciplinaryCase
    
    case = get_object_or_404(DisciplinaryCase, id=id)
    
    return {
        'id': str(case.id),
        'student': case.student.user.get_full_name() if case.student and case.student.user else None,
        'category': case.category,
        'description': case.description,
        'status': case.status,
        'witnesses': case.witnesses
    }


@router.post('/cases')
def create_case(request, data: DisciplinaryCreateSchema):
    """Create disciplinary case."""
    from apps.student.disciplinary import DisciplinaryCase
    
    case = DisciplinaryCase.objects.create(
        student_id=data.student_id,
        incident_date=data.incident_date,
        incident_location=data.incident_location,
        category=data.category,
        description=data.description,
        reported_by=request.user
    )
    
    return {'success': True, 'id': str(case.id)}


@router.post('/cases/{id}/hearing')
def schedule_hearing(request, id: str, data: DisciplinaryHearingSchema):
    """Schedule disciplinary hearing."""
    from apps.student.disciplinary import DisciplinaryCase, DisciplinaryHearing
    
    case = get_object_or_404(DisciplinaryCase, id=id)
    
    hearing = DisciplinaryHearing.objects.create(
        case=case,
        hearing_date=data.hearing_date,
        hearing_time=data.hearing_time,
        venue=data.venue
    )
    
    case.status = 'hearing_scheduled'
    case.save()
    
    return {'success': True, 'id': str(hearing.id)}


@router.post('/hearing/{id}/decide')
def decide_case(request, id: str, data: HearingDecisionSchema):
    """Give case decision."""
    from apps.student.disciplinary import DisciplinaryCase, DisciplinaryHearing
    
    hearing = get_object_or_404(DisciplinaryHearing, id=id)
    
    hearing.decision = data.decision
    hearing.save()
    
    case = hearing.case
    case.status = 'decided'
    case.save()
    
    return {'success': True, 'decision': data.decision}


@router.get('/cases/student/{student_id}')
def get_student_cases(request, student_id: str):
    """Get student disciplinary history."""
    from apps.student.disciplinary import DisciplinaryCase
    
    cases = DisciplinaryCase.objects.filter(student_id=student_id)
    
    return [
        {
            'id': str(c.id),
            'category': c.category,
            'status': c.status,
            'decided': c.status == 'decided',
            'date': str(c.incident_date)
        }
        for c in cases
    ]


@router.post('/cases/{id}/appeal')
def appeal_case(request, id: str, grounds: str):
    """Appeal disciplinary decision."""
    from apps.student.disciplinary import DisciplinaryCase, DisciplinaryAppeal
    
    case = get_object_or_404(DisciplinaryCase, id=id)
    
    appeal = DisciplinaryAppeal.objects.create(
        case=case,
        grounds=grounds
    )
    
    case.status = 'appealed'
    case.save()
    
    return {'success': True, 'id': str(appeal.id)}


# === Warnings ===
@router.get('/warnings')
def list_warnings(request):
    """List all warnings."""
    from apps.student.disciplinary import StudentWarning
    
    warnings = StudentWarning.objects.all().order_by('-created_at')
    
    return [
        {
            'id': str(w.id),
            'student': w.student.user.get_full_name() if w.student and w.student.user else None,
            'type': w.warning_type,
            'reason': w.reason,
            'resolved': w.is_resolved
        }
        for w in warnings
    ]


@router.post('/warnings')
def create_warning(request, data: WarningSchema):
    """Issue warning."""
    from apps.student.disciplinary import StudentWarning
    
    warning = StudentWarning.objects.create(
        student_id=data.student_id,
        warning_type=data.warning_type,
        reason=data.reason,
        issued_by=request.user
    )
    
    return {'success': True, 'id': str(warning.id)}


@router.post('/warnings/{id}/resolve')
def resolve_warning(request, id: str):
    """Mark warning as resolved."""
    from apps.student.disciplinary import StudentWarning
    
    warning = get_object_or_404(StudentWarning, id=id)
    warning.is_resolved = True
    warning.resolved_at = timezone.now()
    warning.save()
    
    return {'success': True}


# === Course Overrides ===
@router.get('/overrides')
def list_overrides(request):
    """List course registration overrides."""
    from apps.student.disciplinary import CourseRegistrationOverride
    
    overrides = CourseRegistrationOverride.objects.all().order_by('-created_at')
    
    return [
        {
            'id': str(o.id),
            'student': o.student.user.get_full_name() if o.student and o.student.user else None,
            'course': o.course.code if o.course else None,
            'reason': o.reason,
            'approved': o.is_approved
        }
        for o in overrides
    ]


@router.post('/overrides')
def create_override(request, data: CourseOverrideSchema):
    """Request course override."""
    from apps.student.disciplinary import CourseRegistrationOverride
    
    override = CourseRegistrationOverride.objects.create(
        student_id=data.student_id,
        course_id=data.course_id,
        session_id=data.session_id,
        semester_id=data.semester_id,
        reason=data.reason
    )
    
    return {'success': True, 'id': str(override.id)}


@router.post('/overrides/{id}/approve')
def approve_override(request, id: str):
    """Approve course override."""
    from apps.student.disciplinary import CourseRegistrationOverride
    
    override = get_object_or_404(CourseRegistrationOverride, id=id)
    override.is_approved = True
    override.approved_by = request.user
    override.approved_at = timezone.now()
    override.save()
    
    return {'success': True}


@router.post('/overrides/{id}/reject')
def reject_override(request, id: str):
    """Reject course override."""
    from apps.student.disciplinary import CourseRegistrationOverride
    
    override = get_object_or_404(CourseRegistrationOverride, id=id)
    override.is_approved = False
    override.approved_by = request.user
    override.approved_at = timezone.now()
    override.save()
    
    return {'success': True}


# === Prerequisites ===
@router.get('/prerequisites')
def list_prerequisites(request):
    """List course prerequisites."""
    from apps.student.disciplinary import CoursePrerequisite
    
    prereqs = CoursePrerequisite.objects.all()
    
    return [
        {
            'course': p.course.code,
            'prerequisite': p.prerequisite.code,
            'type': p.prereq_type,
            'min_grade': p.min_grade
        }
        for p in prereqs
    ]


@router.get('/prerequisites/{course_id}')
def get_course_prerequisites(request, course_id: str):
    """Get prerequisites for a course."""
    from apps.student.disciplinary import CoursePrerequisite
    
    prereqs = CoursePrerequisite.objects.filter(course_id=course_id)
    
    return [
        {
            'prerequisite': p.prerequisite.code,
            'name': p.prerequisite.name,
            'type': p.prereq_type,
            'min_grade': p.min_grade
        }
        for p in prereqs
    ]