"""
Extended Student Services APIs
Applications, Hostel, Transcripts, Complaints, Alumni
"""

from ninja import Router, Schema
from typing import List, Optional
from django.shortcuts import get_object_or_404
from django.utils import timezone
import uuid

router = Router(tags=['Services'])


# === Applicant Schemas ===
class ApplicantSchema(Schema):
    id: str
    application_number: str
    first_name: str
    last_name: str
    email: str
    programme_id: str
    jamb_score: Optional[int]
    status: str


class ApplicantCreateSchema(Schema):
    first_name: str
    last_name: str
    email: str
    phone: str
    date_of_birth: str
    gender: str
    programme_id: str
    jamb_number: Optional[str] = ''
    jamb_score: Optional[int] = None
    olevel_results: Optional[List[dict]] = []


# === Hostel Schemas ===
class HostelSchema(Schema):
    id: str
    name: str
    type: str
    total_beds: int
    available_beds: int
    amenities: List[str]


class HostelRoomSchema(Schema):
    id: str
    hostel_id: str
    room_number: str
    floor: int
    capacity: int
    occupied: int
    room_type: str
    status: str


class HostelApplicationSchema(Schema):
    hostel_id: Optional[str]
    room_type: str


# === Transcript Schemas ===
class TranscriptRequestSchema(Schema):
    id: str
    recipient_name: str
    recipient_institution: str
    purpose: str
    status: str
    fee_paid: bool


class TranscriptRequestCreateSchema(Schema):
    recipient_name: str
    recipient_institution: str
    recipient_address: str
    recipient_email: str
    purpose: str
    delivery_method: str


# === Complaint Schemas ===
class ComplaintSchema(Schema):
    id: str
    category: str
    subject: str
    status: str
    assigned_to: Optional[str]
    created_at: str


class ComplaintCreateSchema(Schema):
    category: str
    subject: str
    description: str
    is_anonymous: bool = False


class ComplaintResponseSchema(Schema):
    response: str


# === Alumni Schemas ===
class AlumniSchema(Schema):
    id: str
    student_id: str
    status: str
    employer: Optional[str]
    job_title: Optional[str]
    is_donated: bool


class AlumniUpdateSchema(Schema):
    status: str
    employer: Optional[str] = ''
    job_title: Optional[str] = ''
    institution: Optional[str] = ''
    program: Optional[str] = ''
    willing_to_mentor: bool = True


# === Applicant APIs ===
@router.get('/applications')
def list_applications(request):
    """List all applications."""
    from apps.student.extended_services import Applicant
    
    apps = Applicant.objects.all().order_by('-applied_at')
    
    return [
        {
            'id': str(a.id),
            'application_number': a.application_number,
            'name': f"{a.first_name} {a.last_name}",
            'email': a.email,
            'programme': a.programme.name if a.programme else None,
            'status': a.status
        }
        for a in apps
    ]


@router.get('/applications/{id}', response=ApplicantSchema)
def get_application(request, id: str):
    """Get application details."""
    from apps.student.extended_services import Applicant
    
    return get_object_or_404(Applicant, id=id)


@router.post('/applications', response=ApplicantSchema)
def create_application(request, data: ApplicantCreateSchema):
    """Submit new application."""
    from apps.student.extended_services import Applicant
    
    # Generate application number
    app_number = f"APP{uuid.uuid4().hex[:8].upper()}"
    
    applicant = Applicant.objects.create(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        phone=data.phone,
        date_of_birth=data.date_of_birth,
        gender=data.gender,
        application_number=app_number,
        programme_id=data.programme_id,
        jamb_number=data.jamb_number,
        jamb_score=data.jamb_score,
        olevel_results=data.olevel_results or []
    )
    
    return applicant


@router.post('/applications/{id}/screen')
def screen_application(request, id: str):
    """Score and process application."""
    from apps.student.extended_services import Applicant, ScreeningScore
    
    applicant = get_object_or_404(Applicant, id=id)
    
    # Calculate screening score
    total_points = 0
    
    for result in applicant.olevel_results:
        grade = result.get('grade', '')
        points = ScreeningScore.POINTS.get(grade, 0)
        total_points += points
    
    applicant.screening_score = total_points
    applicant.status = 'screening'
    applicant.screening_date = timezone.now().date()
    applicant.save()
    
    return {'success': True, 'score': total_points}


@router.post('/applications/{id}/admit')
def admit_applicant(request, id: str):
    """Admit applicant."""
    from apps.student.extended_services import Applicant
    
    applicant = get_object_or_404(Applicant, id=id)
    
    # Generate student ID
    student_id = f"ST{uuid.uuid4().hex[:6].upper()}"
    
    applicant.status = 'admitted'
    applicant.admission_date = timezone.now().date()
    applicant.student_id = student_id
    applicant.save()
    
    # Note: In production, would also create user account and student profile
    
    return {'success': True, 'student_id': student_id}


# === Hostel APIs ===
@router.get('/hostels')
def list_hostels(request):
    """List available hostels."""
    from apps.student.extended_services import Hostel
    
    hostels = Hostel.objects.filter(is_active=True)
    
    return [
        {
            'id': str(h.id),
            'name': h.name,
            'type': h.type,
            'available': h.available_beds,
            'amenities': h.amenities
        }
        for h in hostels
    ]


@router.get('/hostels/{id}/rooms')
def list_hostel_rooms(request, id: str):
    """List rooms in hostel."""
    from apps.student.extended_services import HostelRoom
    
    rooms = HostelRoom.objects.filter(hostel_id=id, status='available')
    
    return [
        {
            'id': str(r.id),
            'room_number': r.room_number,
            'floor': r.floor,
            'capacity': r.capacity,
            'occupied': r.occupied,
            'room_type': r.room_type
        }
        for r in rooms
    ]


@router.post('/hostel/apply')
def apply_for_hostel(request, data: HostelApplicationSchema):
    """Apply for hostel."""
    from apps.student.extended_services import HostelApplication
    from apps.student.models import StudentProfile
    from apps.academic.models import AcademicSession
    
    student = StudentProfile.objects.filter(user=request.auth[0]).first()
    
    if not student:
        return {'error': 'Student profile not found'}
    
    session = AcademicSession.objects.filter(is_current=True).first()
    
    application = HostelApplication.objects.create(
        student=student,
        hostel_id=data.hostel_id,
        room_type=data.room_type,
        session=session,
        status='pending'
    )
    
    return {'success': True, 'id': str(application.id)}


@router.get('/hostel/applications')
def list_hostel_applications(request):
    """List hostel applications."""
    from apps.student.extended_services import HostelApplication
    
    apps = HostelApplication.objects.all().order_by('-applied_at')
    
    return [
        {
            'id': str(a.id),
            'student': a.student.user.get_full_name() if a.student and a.student.user else None,
            'status': a.status,
            'hostel': a.hostel.name if a.hostel else None
        }
        for a in apps
    ]


@router.post('/hostel/applications/{id}/approve')
def approve_hostel_application(request, id: str):
    """Approve hostel application."""
    from apps.student.extended_services import HostelApplication, HostelRoom
    
    app = get_object_or_404(HostelApplication, id=id)
    
    # Find available room
    room = HostelRoom.objects.filter(
        hostel=app.hostel,
        status='available',
        occupied__lt=models.F('capacity')
    ).first()
    
    if room:
        app.allocated_room = room
        app.status = 'allocated'
        room.occupied += 1
        if room.occupied >= room.capacity:
            room.status = 'full'
        room.save()
    else:
        app.status = 'rejected'
    
    app.save()
    
    return {'success': True, 'room': room.room_number if room else None}


# === Transcript APIs ===
@router.post('/transcripts/request')
def request_transcript(request, data: TranscriptRequestCreateSchema):
    """Request transcript."""
    from apps.student.extended_services import TranscriptRequest
    from apps.student.models import StudentProfile
    
    student = StudentProfile.objects.filter(user=request.auth[0]).first()
    
    if not student:
        return {'error': 'Student profile not found'}
    
    transcript = TranscriptRequest.objects.create(
        student=student,
        recipient_name=data.recipient_name,
        recipient_institution=data.recipient_institution,
        recipient_address=data.recipient_address,
        recipient_email=data.recipient_email,
        purpose=data.purpose,
        delivery_method=data.delivery_method
    )
    
    return {'success': True, 'id': str(transcript.id), 'fee': float(transcript.fee_amount)}


@router.get('/transcripts')
def list_transcripts(request):
    """List transcript requests."""
    from apps.student.extended_services import TranscriptRequest
    
    trans = TranscriptRequest.objects.all().order_by('-created_at')
    
    return [
        {
            'id': str(t.id),
            'student': t.student.user.email if t.student and t.student.user else None,
            'recipient': t.recipient_institution,
            'purpose': t.purpose,
            'status': t.status,
            'fee_paid': t.fee_paid
        }
        for t in trans
    ]


@router.post('/transcripts/{id}/process')
def process_transcript(request, id: str):
    """Process transcript request."""
    from apps.student.extended_services import TranscriptRequest
    
    transcript = get_object_or_404(TranscriptRequest, id=id)
    transcript.status = 'ready'
    transcript.processed_by = request.auth[0]
    transcript.processed_at = timezone.now()
    transcript.save()
    
    return {'success': True}


# === Complaint APIs ===
@router.post('/complaints')
def create_complaint(request, data: ComplaintCreateSchema):
    """Submit complaint."""
    from apps.student.extended_services import Complaint
    from apps.student.models import StudentProfile
    
    student = None
    if not data.is_anonymous:
        student = StudentProfile.objects.filter(user=request.auth[0]).first()
    
    complaint = Complaint.objects.create(
        student=student,
        category=data.category,
        subject=data.subject,
        description=data.description,
        is_anonymous=data.is_anonymous
    )
    
    return {'success': True, 'id': str(complaint.id)}


@router.get('/complaints')
def list_complaints(request):
    """List complaints."""
    from apps.student.extended_services import Complaint
    
    complaints = Complaint.objects.all().order_by('-created_at')
    
    return [
        {
            'id': str(c.id),
            'category': c.category,
            'subject': c.subject,
            'status': c.status,
            'created_at': str(c.created_at)
        }
        for c in complaints
    ]


@router.post('/complaints/{id}/respond')
def respond_complaint(request, id: str, data: ComplaintResponseSchema):
    """Respond to complaint."""
    from apps.student.extended_services import Complaint
    
    complaint = get_object_or_404(Complaint, id=id)
    complaint.response = data.response
    complaint.status = 'resolved'
    complaint.resolved_at = timezone.now()
    complaint.save()
    
    return {'success': True}


@router.post('/complaints/{id}/rate')
def rate_complaint(request, id: str, rating: int):
    """Rate complaint resolution."""
    from apps.student.extended_services import Complaint
    
    complaint = get_object_or_404(Complaint, id=id)
    complaint.satisfaction_rating = rating
    complaint.save()
    
    return {'success': True}


# === Alumni APIs ===
@router.get('/alumni')
def list_alumni(request):
    """List alumni."""
    from apps.student.extended_services import Alumni
    
    alumni = Alumni.objects.all().order_by('-updated_at')
    
    return [
        {
            'id': str(a.id),
            'student': a.student.user.email if a.student and a.student.user else None,
            'status': a.status,
            'employer': a.employer,
            'is_donated': a.is_donated
        }
        for a in alumni
    ]


@router.post('/alumni/update')
def update_alumni(request, data: AlumniUpdateSchema):
    """Update alumni profile."""
    from apps.student.extended_services import Alumni
    from apps.student.models import StudentProfile
    
    student = StudentProfile.objects.filter(user=request.auth[0]).first()
    
    if not student:
        return {'error': 'Student profile not found'}
    
    alumni, _ = Alumni.objects.get_or_create(
        student=student,
        defaults={
            'graduation_session_id': student.current_session_id,
            'degree': 'Bachelor',
            'cgpa': 0.0
        }
    )
    
    alumni.status = data.status
    alumni.employer = data.employer
    alumni.job_title = data.job_title
    alumni.institution = data.institution
    alumni.program = data.program
    alumni.willing_to_mentor = data.willing_to_mentor
    alumni.save()
    
    return {'success': True}


@router.post('/alumni/donate')
def alumni_donate(request, amount: float):
    """Record alumni donation."""
    from apps.student.extended_services import Alumni
    from apps.student.models import StudentProfile
    
    student = StudentProfile.objects.filter(user=request.auth[0]).first()
    
    if not student:
        return {'error': 'Student profile not found'}
    
    alumni = Alumni.objects.filter(student=student).first()
    
    if alumni:
        alumni.is_donated = True
        alumni.donation_amount = amount
        alumni.save()
    
    return {'success': True}