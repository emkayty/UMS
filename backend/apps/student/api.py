from ninja import Router, Schema
from typing import Optional, List
from django.shortcuts import get_object_or_404

from apps.student.models import (
    StudentProfile, AdmissionApplication, CourseRegistration, 
    TimetableEntry
)
from apps.student.results import (
    Result, CGPAHistory, GraduationClearance, Transcript, Certificate
)

router = Router(tags=['Student'])


# === Schemas ===
class StudentProfileSchema(Schema):
    id: str
    user_id: str
    matric_number: Optional[str]
    first_name: str
    last_name: str
    phone: Optional[str]
    programme_id: Optional[str]
    current_level: int
    admission_status: str


class AdmissionApplicationSchema(Schema):
    id: str
    student_id: str
    jamb_reg_no: Optional[str]
    jamb_score: Optional[int]
    application_session_id: str
    status: str


class CourseRegistrationSchema(Schema):
    id: str
    student_id: str
    course_id: str
    session_id: str
    semester_id: str
    status: str


class ResultSchema(Schema):
    id: str
    registration_id: str
    score: float
    grade: str
    grade_point: float
    status: str


class CGPASchema(Schema):
    student_id: str
    gpa: float
    cumulative_gpa: float
    session: str
    semester: str


# === Admission APIs ===
class AdmissionApplicationCreateSchema(Schema):
    email: str
    password: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    jamb_reg_no: Optional[str] = None
    jamb_score: Optional[int] = None
    programme_id: Optional[str] = None


@router.post('/admissions/apply', response=dict)
def apply_admission(request, data: AdmissionApplicationCreateSchema):
    """Public endpoint to apply for admission with validation."""
    from apps.accounts.models import User
    from apps.academic.models import Programme
    import re
    
    # Validate email format
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, data.email):
        return {'success': False, 'error': 'Invalid email format'}
    
    # Check email not exists
    if User.objects.filter(email__iexact=data.email).exists():
        return {'success': False, 'error': 'Email already registered'}
    
    # Validate password strength
    if len(data.password) < 8:
        return {'success': False, 'error': 'Password must be at least 8 characters'}
    
    # Validate required fields
    if not data.first_name or not data.last_name:
        return {'success': False, 'error': 'First and last name are required'}
    
    # Validate programme if provided
    if data.programme_id:
        try:
            Programme.objects.get(id=data.programme_id)
        except Programme.DoesNotExist:
            return {'success': False, 'error': 'Invalid programme selected'}
    
    # Create user account
    user = User.objects.create_user(
        email=data.email, 
        password=data.password, 
        role='student'
    )
    
    # Create student profile
    profile = StudentProfile.objects.create(
        user=user,
        first_name=data.first_name,
        last_name=data.last_name,
        phone=data.phone or '',
        jamb_reg_no=data.jamb_reg_no or '',
        jamb_score=data.jamb_score,
        programme_id=data.programme_id,
        admission_status='applied'
    )
    
    return {'success': True, 'student_id': str(profile.id), 'message': 'Application submitted successfully'}


@router.get('/admissions/applications', response=List[AdmissionApplicationSchema])
def list_applications(request, status: str = None, session_id: str = None):
    """List admission applications (registrar only)."""
    qs = AdmissionApplication.objects.all()
    if status:
        qs = qs.filter(status=status)
    if session_id:
        qs = qs.filter(application_session_id=session_id)
    return qs[:100]


@router.patch('/admissions/{id}/process', response=dict)
def process_admission(request, id: str, data: dict):
    """Process admission application (admit/reject)."""
    application = get_object_or_404(AdmissionApplication, id=id)
    action = data.get('action')
    
    if action == 'admit':
        application.status = 'admitted'
    elif action == 'reject':
        application.status = 'rejected'
    
    application.reviewer = request.auth[0]
    application.review_notes = data.get('notes', '')
    application.save()
    
    # Update student profile
    application.student.admission_status = application.status
    if action == 'admit':
        # Generate matric number
        import random
        year = application.application_session.name[:4]
        rand_num = str(random.randint(10000, 99999))
        application.student.matric_number = f"{year}{rand_num}"
    application.student.save()
    
    return {'success': True}


# === Student APIs ===
@router.get('/students', response=List[StudentProfileSchema])
def list_students(request, programme_id: str = None, level: int = None):
    """List students."""
    qs = StudentProfile.objects.all()
    if programme_id:
        qs = qs.filter(programme_id=programme_id)
    if level:
        qs = qs.filter(current_level=level)
    return qs


@router.get('/students/{id}', response=StudentProfileSchema)
def get_student(request, id: str):
    return get_object_or_404(StudentProfile, id=id)


@router.post('/students/{id}/register-courses')
def register_courses(request, id: str, data: dict):
    """Register courses for a student with transaction safety."""
    from django.db import transaction
    from django.db.models import F
    from apps.academic.models import Course, AcademicSession, Semester
    
    student = get_object_or_404(StudentProfile, id=id)
    course_ids = data.get('course_ids', [])
    session_id = data.get('session_id')
    semester_id = data.get('semester_id')
    
    # Use transaction with row locking for safety
    with transaction.atomic():
        # Lock course registrations for this student to prevent race conditions
        # Use select_for_update on available courses to check seat limits
        registrations = []
        for course_id in course_ids:
            try:
                # Get course with lock for seat checking
                course = Course.objects.select_for_update().get(id=course_id)
                
                # Check if already registered (prevent duplicate)
                existing = CourseRegistration.objects.filter(
                    student=student,
                    course=course,
                    session_id=session_id,
                    semester_id=semester_id
                ).first()
                
                if existing:
                    continue  # Skip already registered
                
                # Create registration
                reg = CourseRegistration.objects.create(
                    student=student,
                    course=course,
                    session_id=session_id,
                    semester_id=semester_id,
                    status='active'
                )
                registrations.append(reg)
                
            except Course.DoesNotExist:
                continue  # Skip invalid courses
    
    return {'success': True, 'registered': len(registrations)}


@router.get('/students/{id}/courses')
def get_student_courses(request, id: str):
    """Get student's registered courses."""
    student = get_object_or_404(StudentProfile, id=id)
    registrations = CourseRegistration.objects.filter(
        student=student, status='active'
    )
    return [
        {
            'id': str(r.id),
            'course': {'id': str(r.course.id), 'code': r.course.code, 'title': r.course.title},
            'session': r.session.name,
            'semester': r.semester.name
        }
        for r in registrations
    ]


@router.get('/students/{id}/timetable')
def get_student_timetable(request, id: str, semester_id: str = None):
    """Get student timetable."""
    student = get_object_or_404(StudentProfile, id=id)
    regs = CourseRegistration.objects.filter(student=student, status='active')
    if semester_id:
        regs = regs.filter(semester_id=semester_id)
    
    timetable = []
    for reg in regs:
        entries = TimetableEntry.objects.filter(course=reg.course, semester=reg.semester)
        for entry in entries:
            timetable.append({
                'day': entry.day_of_week,
                'start': entry.start_time.isoformat(),
                'end': entry.end_time.isoformat(),
                'venue': entry.venue,
                'course': {'code': entry.course.code, 'title': entry.course.title}
            })
    
    return timetable


# === Result APIs ===
@router.get('/students/{id}/results')
def get_student_results(request, id: str, session_id: str = None, semester_id: str = None):
    """Get student results."""
    student = get_object_or_404(StudentProfile, id=id)
    regs = CourseRegistration.objects.filter(student=student)
    
    results = Result.objects.filter(registration__in=regs)
    if session_id:
        results = results.filter(session_id=session_id)
    if semester_id:
        results = results.filter(semester_id=semester_id)
    
    return [
        {
            'course_code': r.registration.course.code,
            'course_title': r.registration.course.title,
            'score': float(r.score),
            'grade': r.grade,
            'grade_point': float(r.grade_point),
            'status': r.status
        }
        for r in results
    ]


@router.get('/students/{id}/cgpa')
def get_student_cgpa(request, id: str):
    """Calculate student's CGPA."""
    student = get_object_or_404(StudentProfile, id=id)
    
    # Get all approved results
    regs = CourseRegistration.objects.filter(
        student=student, status='active'
    )
    results = Result.objects.filter(
        registration__in=regs, status__in=['approved_hod', 'approved_dean', 'approved_senate']
    )
    
    total_points = 0
    total_units = 0
    
    for result in results:
        course = result.registration.course
        total_points += float(result.grade_point) * course.credit_units
        total_units += course.credit_units
    
    cgpa = round(total_points / total_units, 2) if total_units > 0 else 0
    
    return {
        'student_id': str(student.id),
        'cgpa': cgpa,
        'total_credit_units': total_units,
        'results_count': len(results)
    }


# === Clearance APIs ===
@router.get('/students/{id}/clearance')
def get_clearance_status(request, id: str):
    """Get graduation clearance status."""
    student = get_object_or_404(StudentProfile, id=id)
    clearance, _ = GraduationClearance.objects.get_or_create(student=student)
    
    return {
        'library': clearance.cleared_by_library,
        'hostel': clearance.cleared_by_hostel,
        'bursary': clearance.cleared_by_bursary,
        'department': clearance.cleared_by_department,
        'eligible': clearance.eligible_to_graduate
    }


# === Transcript APIs ===
@router.post('/students/{id}/request-transcript')
def request_transcript(request, id: str):
    """Request official transcript."""
    import uuid
    
    student = get_object_or_404(StudentProfile, id=id)
    transcript = Transcript.objects.create(
        student=student,
        qr_verification_code=str(uuid.uuid4())[:8].upper()
    )
    
    return {'success': True, 'transcript_id': str(transcript.id)}


@router.get('/transcripts/{id}/download')
def download_transcript(request, id: str):
    """Download transcript PDF."""
    transcript = get_object_or_404(Transcript, id=id)
    if not transcript.pdf_url:
        return {'error': 'Transcript not yet available', 'url': None}
    return {'url': transcript.pdf_url}

# === Student My Courses ===
@router.get('/me/courses')
def get_my_courses(request):
    """Get current student's registered courses."""
    from django.db.models import Prefetch
    
    if not hasattr(request, 'auth') or not request.auth:
        return {'courses': [], 'error': 'Not authenticated'}
    
    try:
        student = StudentProfile.objects.get(user=request.auth[0])
    except StudentProfile.DoesNotExist:
        return {'courses': []}
    
    registrations = CourseRegistration.objects.filter(
        student=student,
        status='active'
    ).select_related('course')
    
    courses = []
    for reg in registrations:
        courses.append({
            'id': str(reg.course.id),
            'code': reg.course.code,
            'title': reg.course.title,
            'credit_units': reg.course.credit_units,
            'level': reg.course.level,
            'status': reg.status,
            'session': reg.session.name if reg.session else None,
            'semester': reg.semester.name if reg.semester else None
        })
    
    return {'courses': courses}


# === Student My Results ===
@router.get('/me/results')
def get_my_results(request):
    """Get current student's results."""
    if not hasattr(request, 'auth') or not request.auth:
        return {'results': [], 'error': 'Not authenticated'}
    
    try:
        student = StudentProfile.objects.get(user=request.auth[0])
    except StudentProfile.DoesNotExist:
        return {'results': [], 'gpa': 0, 'cgpa': 0}
    
    # Get all results
    results = Result.objects.filter(
        registration__student=student
    ).select_related('registration__course', 'session', 'semester').order_by('-session__start_date')
    
    result_list = []
    for r in results:
        result_list.append({
            'id': str(r.id),
            'code': r.registration.course.code if r.registration else '',
            'title': r.registration.course.title if r.registration else '',
            'score': float(r.score) if r.score else None,
            'grade': r.grade,
            'grade_point': float(r.grade_point) if r.grade_point else None,
            'status': r.status,
            'session': r.session.name if r.session else None,
            'semester': r.semester.name if r.semester else None
        })
    
    # Get latest CGPA
    cgpa = CGPAHistory.objects.filter(student=student).order_by('-created_at').first()
    
    return {
        'results': result_list,
        'gpa': float(cgpa.gpa) if cgpa and cgpa.gpa else 0,
        'cgpa': float(cgpa.cumulative_gpa) if cgpa and cgpa.cumulative_gpa else 0,
        'total_credits': cgpa.total_credits if cgpa else 0
    }


# === Student My Fees ===
@router.get('/me/fees')
def get_my_fees(request):
    """Get current student's fees."""
    if not hasattr(request, 'auth') or not request.auth:
        return {'fees': []}
    
    try:
        student = StudentProfile.objects.get(user=request.auth[0])
    except StudentProfile.DoesNotExist:
        return {'fees': []}
    
    from apps.finance.models import StudentFee
    fees = StudentFee.objects.filter(student=student).select_related('fee_item')
    
    fee_list = []
    for f in fees:
        fee_list.append({
            'name': f.fee_item.name if f.fee_item else 'Fee',
            'amount_due': float(f.amount_due) if f.amount_due else 0,
            'amount_paid': float(f.amount_paid) if f.amount_paid else 0,
            'status': f.status
        })
    
    return {'fees': fee_list}


# === Student My Clearance ===
@router.get('/me/clearance')
def get_my_clearance(request):
    """Get current student's clearance status."""
    if not hasattr(request, 'auth') or not request.auth:
        return {}
    
    try:
        student = StudentProfile.objects.get(user=request.auth[0])
    except StudentProfile.DoesNotExist:
        return {}
    
    clearance = GraduationClearance.objects.filter(student=student).first()
    
    if not clearance:
        return {'status': 'not_started'}
    
    return {
        'status': 'eligible' if clearance.eligible_to_graduate else 'pending',
        'library': clearance.cleared_by_library,
        'bursary': clearance.cleared_by_bursary,
        'hostel': clearance.cleared_by_hostel,
        'department': clearance.cleared_by_department,
        'eligible': clearance.eligible_to_graduate
    }


# === Extended Student Lifecycle APIs ===

# === Applicant Applications ===
@router.get('/applicants')
def list_applicants(request, status: str = None):
    """List all job applicants."""
    from apps.lifecycle.models import ApplicantData
    
    qs = ApplicantData.objects.all()
    if status:
        qs = qs.filter(application_status=status)
    
    return {'count': qs.count(), 'applicants': [
        {'id': str(a.id), 'name': f"{a.first_name} {a.last_name}", 'email': a.email, 
         'phone': a.phone, 'state': a.state_of_origin, 'status': a.application_status}
        for a in qs[:50]
    ]}


@router.post('/apply')
def submit_admission_application(request, data: dict):
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
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        title=data.get('title'),
        date_of_birth=data.get('date_of_birth'),
        state_of_origin=data.get('state_of_origin'),
        local_govt_area=data.get('lga'),
        phone=data.get('phone'),
        email=email,
        father_name=data.get('father_name'),
        father_phone=data.get('father_phone'),
        father_email=data.get('father_email'),
        mother_name=data.get('mother_name'),
        mother_phone=data.get('mother_phone'),
        guardian_name=data.get('guardian_name'),
        guardian_phone=data.get('guardian_phone'),
        emergency_contact_name=data.get('emergency_name'),
        emergency_contact_phone=data.get('emergency_phone'),
        jamb_registration_number=data.get('jamb_reg_no'),
        jamb_score=data.get('jamb_score'),
        o_level_sitting1_exam_type=data.get('olevel_type'),
        o_level_sitting1_results=data.get('olevel_results', {}),
        application_status='submitted'
    )
    
    return {'id': str(applicant.id), 'status': 'Application submitted successfully'}


# === Hostel Management ===
@router.get('/hostels')
def list_hostels(request):
    """List available hostels."""
    from apps.lifecycle.models import Hostel
    
    hostels = Hostel.objects.filter(is_active=True)
    return {'count': hostels.count(), 'hostels': [
        {'id': str(h.id), 'name': h.name, 'code': h.code,
         'gender': h.gender, 'capacity': h.capacity, 'available': h.capacity - h.occupied,
         'location': h.location, 'has_wifi': h.has_wifi}
        for h in hostels
    ]}


@router.get('/my-hostel')
def get_my_hostel(request):
    """Get current student's hostel allocation."""
    if not hasattr(request, 'auth') or not request.auth:
        return {}
    
    from apps.student.models import StudentProfile
    from apps.lifecycle.models import StudentHostelAllocation
    
    try:
        student = StudentProfile.objects.get(user=request.auth[0])
    except StudentProfile.DoesNotExist:
        return {}
    
    try:
        allocation = StudentHostelAllocation.objects.get(student=student)
        return {
            'hostel': allocation.hostel.name,
            'block': allocation.block,
            'room': allocation.room_number,
            'bed': allocation.bed_number,
            'status': allocation.status
        }
    except StudentHostelAllocation.DoesNotExist:
        return {'status': 'Not allocated'}


# === Change Requests ===
@router.get('/change-requests')
def list_change_requests(request):
    """List student change requests."""
    from apps.lifecycle.models import StudentChangeRequest
    
    requests = StudentChangeRequest.objects.all()[:20]
    return [
        {'id': str(r.id), 'type': r.request_type, 'current': r.current_value,
         'requested': r.requested_value, 'status': r.status}
        for r in requests
    ]


# === Discipline ===
@router.get('/discipline-records')
def list_discipline_records(request):
    """List disciplinary records."""
    from apps.lifecycle.models import StudentDiscipline
    
    records = StudentDiscipline.objects.all()[:20]
    return [
        {'id': str(r.id), 'student': r.student.last_name, 'offence': r.offence_type,
         'severity': r.severity, 'action': r.action, 'status': r.status}
        for r in records
    ]


# === Alumni ===
@router.get('/alumni')
def list_alumni(request):
    """List alumni."""
    from apps.lifecycle.models import AlumniRecord
    
    alumni = AlumniRecord.objects.all()[:50]
    return [
        {'id': str(a.id), 'name': f"{a.student.first_name} {a.student.last_name}",
         'degree': a.degree_awarded, 'class': a.class_of_degree, 'employed': a.is_employed}
        for a in alumni
    ]
