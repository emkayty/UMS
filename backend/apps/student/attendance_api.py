"""
Attendance & Invigilation APIs
Complete CRUD for attendance, invigilation, publications
"""

from ninja import Router, Schema
from typing import List, Optional
from django.shortcuts import get_object_or_404
from django.utils import timezone
import uuid

router = Router(tags=['Attendance'])


# === Schemas ===
class StudentAttendanceSchema(Schema):
    id: str
    student_id: str
    course_id: str
    date: str
    status: str
    minutes_late: int
    remark: str


class AttendanceMarkSchema(Schema):
    student_id: str
    course_id: str
    date: str
    status: str
    minutes_late: Optional[int] = 0
    remark: Optional[str] = ''


class AttendanceSummarySchema(Schema):
    student_id: str
    course_id: str
    total_sessions: int
    present_count: int
    absent_count: int
    attendance_percentage: float
    status: str


class QRCodeSchema(Schema):
    course_id: str
    semester_id: str
    expires_at: str


class InvigilationSchema(Schema):
    id: str
    exam_id: str
    invigilator_id: str
    is_principal: bool
    status: str
    students_present: int
    students_absent: int


class InvigilationReportSchema(Schema):
    students_present: int
    students_absent: int
    incidents: str


class PublicationSchema(Schema):
    id: str
    author_id: str
    title: str
    journal: str
    publication_type: str
    year: int
    doi: str
    citation_count: int


class PublicationCreateSchema(Schema):
    title: str
    journal: str
    publication_type: str
    year: int
    volume: Optional[str] = ''
    pages: Optional[str] = ''
    doi: Optional[str] = ''


class ResearchGrantSchema(Schema):
    id: str
    researcher_id: str
    title: str
    funding_body: str
    amount: float
    start_date: str
    end_date: str
    status: str


class ResearchGrantCreateSchema(Schema):
    title: str
    funding_body: str
    amount: float
    start_date: str
    end_date: str


# === Attendance ===
@router.post('/attendance/mark')
def mark_attendance(request, data: AttendanceMarkSchema):
    """Mark student attendance."""
    from apps.student.attendance import StudentAttendance
    from apps.student.models import StudentProfile
    from apps.academic.models import Course
    
    student = get_object_or_404(StudentProfile, id=data.student_id)
    course = get_object_or_404(Course, id=data.course_id)
    
    attendance, created = StudentAttendance.objects.update_or_create(
        student=student,
        course=course,
        date=data.date,
        defaults={
            'status': data.status,
            'minutes_late': data.minutes_late,
            'remark': data.remark,
            'marked_by': request.auth[0]
        }
    )
    
    return {'success': True, 'id': str(attendance.id)}


@router.post('/attendance/bulk')
def bulk_mark_attendance(request, data: dict):
    """Bulk mark attendance."""
    from apps.student.attendance import StudentAttendance
    from apps.student.models import StudentProfile
    from apps.academic.models import Course
    
    records = data.get('records', [])
    created_count = 0
    
    for rec in records:
        try:
            student = StudentProfile.objects.get(id=rec.get('student_id'))
            course = Course.objects.get(id=rec.get('course_id'))
            
            StudentAttendance.objects.update_or_create(
                student=student,
                course=course,
                date=rec.get('date'),
                defaults={
                    'status': rec.get('status', 'present'),
                    'marked_by': request.auth[0]
                }
            )
            created_count += 1
        except:
            continue
    
    return {'success': True, 'marked': created_count}


@router.get('/attendance/{student_id}/courses/{course_id}')
def get_student_course_attendance(request, student_id: str, course_id: str):
    """Get attendance for student in specific course."""
    from apps.student.attendance import StudentAttendance
    
    records = StudentAttendance.objects.filter(
        student_id=student_id,
        course_id=course_id
    ).order_by('-date')
    
    return [
        {
            'date': str(a.date),
            'status': a.status,
            'minutes_late': a.minutes_late
        }
        for a in records
    ]


@router.get('/attendance/{student_id}/summary')
def get_attendance_summary(request, student_id: str):
    """Get all attendance summary for student."""
    from apps.student.attendance import AttendanceSummary
    
    summaries = AttendanceSummary.objects.filter(student_id=student_id)
    
    return [
        {
            'course': s.course.code,
            'total': s.total_sessions,
            'present': s.present_count,
            'percentage': float(s.attendance_percentage),
            'status': s.status
        }
        for s in summaries
    ]


@router.post('/attendance/qr/generate')
def generate_qr_session(request, data: QRCodeSchema):
    """Generate QR code session."""
    from apps.student.attendance import AttendanceSession
    from apps.academic.models import Course, Semester
    from django.utils import timezone
    
    course = get_object_or_404(Course, id=data.course_id)
    semester = get_object_or_404(Semester, id=data.semester_id)
    
    # Generate unique QR code
    qr_code = f"QR{uuid.uuid4().hex[:8].upper()}"
    
    session = AttendanceSession.objects.create(
        course=course,
        session=semester.session,
        semester=semester,
        qr_code=qr_code,
        expires_at=timezone.now() + timezone.timedelta(hours=2)
    )
    
    return {'success': True, 'qr_code': qr_code, 'expires_at': session.expires_at}


@router.post('/attendance/qr/verify')
def verify_qr_code(request, qr_code: str, student_id: str):
    """Verify QR code and mark attendance."""
    from apps.student.attendance import AttendanceSession, StudentAttendance
    from apps.student.models import StudentProfile
    from apps.academic.models import Course
    from django.utils import timezone
    
    session = AttendanceSession.objects.filter(
        qr_code=qr_code,
        is_active=True,
        expires_at__gt=timezone.now()
    ).first()
    
    if not session:
        return {'success': False, 'error': 'Invalid or expired QR code'}
    
    # Mark attendance
    student = get_object_or_404(StudentProfile, id=student_id)
    
    attendance = StudentAttendance.objects.create(
        student=student,
        course=session.course,
        session=session.session,
        semester=session.semester,
        date=timezone.now().date(),
        status='present',
        marked_by=request.auth[0]
    )
    
    return {'success': True, 'attendance_id': str(attendance.id)}


# === Invigilation ===
@router.get('/invigilation')
def list_invigilation(request):
    """List invigilation duties."""
    from apps.student.attendance import Invigilation
    from apps.accounts.models import User
    
    # Get lecturer's duties
    if request.auth[0].role == 'lecturer':
        duties = Invigilation.objects.filter(
            invigilator__user=request.auth[0]
        ).order_by('-assigned_at')
    else:
        duties = Invigilation.objects.all()
    
    return [
        {
            'id': str(i.id),
            'exam': i.exam.title if i.exam else None,
            'is_principal': i.is_principal,
            'status': i.status,
            'assigned_at': str(i.assigned_at)
        }
        for i in duties
    ]


@router.post('/invigilation/{id}/report')
def submit_invigilation_report(request, id: str, data: InvigilationReportSchema):
    """Submit invigilation report."""
    from apps.student.attendance import Invigilation
    
    invigilation = get_object_or_404(Invigilation, id=id)
    invigilation.students_present = data.students_present
    invigilation.students_absent = data.students_absent
    invigilation.incidents = data.incidents
    invigilation.status = 'reported'
    invigilation.completed_at = timezone.now()
    invigilation.save()
    
    return {'success': True}


# === Publications ===
@router.get('/publications')
def list_publications(request):
    """List publications."""
    from apps.student.attendance import Publication
    
    pubs = Publication.objects.all().order_by('-year')
    
    return [
        {
            'id': str(p.id),
            'author': p.author.user.get_full_name() if p.author and p.author.user else None,
            'title': p.title,
            'journal': p.journal,
            'type': p.publication_type,
            'year': p.year,
            'citations': p.citation_count
        }
        for p in pubs
    ]


@router.get('/publications/{staff_id}')
def get_staff_publications(request, staff_id: str):
    """Get staff publications."""
    from apps.student.attendance import Publication
    
    pubs = Publication.objects.filter(
        author_id=staff_id
    ).order_by('-year')
    
    return [
        {
            'id': str(p.id),
            'title': p.title,
            'journal': p.journal,
            'year': p.year,
            'citations': p.citation_count
        }
        for p in pubs
    ]


@router.post('/publications', response=PublicationSchema)
def create_publication(request, data: PublicationCreateSchema):
    """Create publication record."""
    from apps.student.attendance import Publication
    from apps.staff.models import StaffProfile
    
    # Get staff profile from user
    staff = StaffProfile.objects.filter(user=request.auth[0]).first()
    
    if not staff:
        return {'error': 'Staff profile not found'}
    
    publication = Publication.objects.create(
        author=staff,
        title=data.title,
        journal=data.journal,
        publication_type=data.publication_type,
        year=data.year,
        volume=data.volume,
        pages=data.pages,
        doi=data.doi
    )
    
    return publication


# === Research Grants ===
@router.get('/grants')
def list_grants(request):
    """List research grants."""
    from apps.student.attendance import ResearchGrant
    
    grants = ResearchGrant.objects.all().order_by('-start_date')
    
    return [
        {
            'id': str(g.id),
            'researcher': g.researcher.user.get_full_name() if g.researcher and g.researcher.user else None,
            'title': g.title,
            'funding_body': g.funding_body,
            'amount': float(g.amount),
            'status': g.status
        }
        for g in grants
    ]


@router.post('/grants', response=ResearchGrantSchema)
def create_grant(request, data: ResearchGrantCreateSchema):
    """Create research grant."""
    from apps.student.attendance import ResearchGrant
    from apps.staff.models import StaffProfile
    
    staff = StaffProfile.objects.filter(user=request.auth[0]).first()
    
    if not staff:
        return {'error': 'Staff profile not found'}
    
    grant = ResearchGrant.objects.create(
        researcher=staff,
        title=data.title,
        funding_body=data.funding_body,
        amount=data.amount,
        start_date=data.start_date,
        end_date=data.end_date
    )
    
    return grant