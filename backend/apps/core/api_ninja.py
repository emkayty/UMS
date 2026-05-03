"""
UMS API - Django Ninja (STRICT - NO DRF)
All endpoints using Django Ninja framework only
"""

from ninja import Router, Schema
from typing import List, Optional
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count, Sum, Avg
from django.utils import timezone

from apps.academic.models import Faculty, Department, Programme, Course, AcademicSession, Semester
from apps.student.models import StudentProfile, AdmissionApplication, TranscriptRequest
from apps.finance.models import Payment, Invoice, FeeType, FeeStructure
from apps.institution.models import Hostel, HostelApplication
from apps.staff.models import StaffProfile, LeaveApplication, LeaveEntitlement
from apps.learning.models import CourseMaterial, Exam
from apps.communication.models import Notification

router = Router(tags=['UMS'])

# ============================================================
# SCHEMAS
# ============================================================

class FacultySchema(Schema):
    id: int
    name: str
    code: str
    is_active: bool

class DepartmentSchema(Schema):
    id: int
    name: str
    code: str
    faculty_id: int

class ProgrammeSchema(Schema):
    id: int
    name: str
    code: str
    qualification: str
    department_id: int

class CourseSchema(Schema):
    id: int
    code: str
    name: str
    credits: int
    department_id: int

class StudentSchema(Schema):
    id: int
    student_id: str
    first_name: str
    last_name: str
    email: str
    programme_id: int
    level: str

class HostelSchema(Schema):
    id: int
    name: str
    gender: str
    total_beds: int
    available_beds: int

class PaymentSchema(Schema):
    id: int
    amount: float
    payment_date: str
    student_id: int
    status: str

class InvoiceSchema(Schema):
    id: int
    amount: float
    due_date: str
    student_id: int
    status: str

class NotificationSchema(Schema):
    id: int
    title: str
    message: str
    created_at: str
    is_read: bool

# ============================================================
# FACULTY ENDPOINTS
# ============================================================

@router.get('/faculties', response=List[FacultySchema])
def list_faculties(request):
    return Faculty.objects.filter(is_active=True)

@router.get('/faculties/{int:faculty_id}', response=FacultySchema)
def get_faculty(request, faculty_id: int):
    return get_object_or_404(Faculty, id=faculty_id)

@router.post('/faculties')
def create_faculty(request, data: FacultySchema):
    faculty = Faculty.objects.create(
        name=data.name,
        code=data.code,
        is_active=data.is_active
    )
    return faculty

@router.put('/faculties/{int:faculty_id}')
def update_faculty(request, faculty_id: int, data: FacultySchema):
    faculty = get_object_or_404(Faculty, id=faculty_id)
    faculty.name = data.name
    faculty.code = data.code
    faculty.is_active = data.is_active
    faculty.save()
    return faculty

@router.delete('/faculties/{int:faculty_id}')
def delete_faculty(request, faculty_id: int):
    faculty = get_object_or_404(Faculty, id=faculty_id)
    faculty.delete()
    return {'deleted': True}

# ============================================================
# DEPARTMENT ENDPOINTS
# ============================================================

@router.get('/departments', response=List[DepartmentSchema])
def list_departments(request):
    return Department.objects.all()

@router.get('/departments/{int:dept_id}', response=DepartmentSchema)
def get_department(request, dept_id: int):
    return get_object_or_404(Department, id=dept_id)

# ============================================================
# PROGRAMME ENDPOINTS
# ============================================================

@router.get('/programmes', response=List[ProgrammeSchema])
def list_programmes(request):
    return Programme.objects.all()

@router.get('/programmes/{int:prog_id}', response=ProgrammeSchema)
def get_programme(request, prog_id: int):
    return get_object_or_404(Programme, id=prog_id)

# ============================================================
# COURSE ENDPOINTS
# ============================================================

@router.get('/courses', response=List[CourseSchema])
def list_courses(request):
    return Course.objects.all()[:100]

@router.get('/courses/{int:course_id}', response=CourseSchema)
def get_course(request, course_id: int):
    return get_object_or_404(Course, id=course_id)

# ============================================================
# STUDENT ENDPOINTS
# ============================================================

@router.get('/students', response=List[StudentSchema])
def list_students(request):
    return StudentProfile.objects.all()[:100]

@router.get('/students/{str:student_id}', response=StudentSchema)
def get_student(request, student_id: str):
    return get_object_or_404(StudentProfile, student_id=student_id)

@router.post('/students')
def create_student(request, data: StudentSchema):
    return {'message': 'Create student'}

@router.get('/students/{str:student_id}/results')
def get_student_results(request, student_id: str):
    return {'student_id': student_id, 'results': []}

@router.get('/students/{str:student_id}/gpa')
def get_student_gpa(request, student_id: str):
    return {'student_id': student_id, 'gpa': 0.0}

@router.get('/students/{str:student_id}/invoices')
def get_student_invoices(request, student_id: str):
    return {'student_id': student_id, 'invoices': []}

@router.get('/students/{str:student_id}/payments')
def get_student_payments(request, student_id: str):
    return {'student_id': student_id, 'payments': []}

# ============================================================
# HOSTEL ENDPOINTS
# ============================================================

@router.get('/hostels', response=List[HostelSchema])
def list_hostels(request):
    return Hostel.objects.all()

@router.get('/hostels/{int:hostel_id}', response=HostelSchema)
def get_hostel(request, hostel_id: int):
    return get_object_or_404(Hostel, id=hostel_id)

@router.post('/hostels')
def create_hostel(request, data: HostelSchema):
    hostel = Hostel.objects.create(
        name=data.name,
        gender=data.gender,
        total_beds=data.total_beds,
        available_beds=data.available_beds
    )
    return hostel

# ============================================================
# PAYMENT ENDPOINTS
# ============================================================

@router.get('/payments', response=List[PaymentSchema])
def list_payments(request):
    return Payment.objects.all()[:100]

@router.get('/payments/{int:payment_id}', response=PaymentSchema)
def get_payment(request, payment_id: int):
    return get_object_or_404(Payment, id=payment_id)

@router.post('/payments')
def create_payment(request):
    return {'message': 'Create payment'}

# ============================================================
# INVOICE ENDPOINTS
# ============================================================

@router.get('/invoices', response=List[InvoiceSchema])
def list_invoices(request):
    return Invoice.objects.all()[:100]

@router.get('/invoices/{int:invoice_id}', response=InvoiceSchema)
def get_invoice(request, invoice_id: int):
    return get_object_or_404(Invoice, id=invoice_id)

# ============================================================
# NOTIFICATION ENDPOINTS
# ============================================================

@router.get('/notifications', response=List[NotificationSchema])
def list_notifications(request):
    return Notification.objects.all()[:50]

@router.post('/notifications/{int:notification_id}/read')
def mark_notification_read(request, notification_id: int):
    notif = get_object_or_404(Notification, id=notification_id)
    notif.is_read = True
    notif.save()
    return notif

# ============================================================
# CLEARANCE ENDPOINTS
# ============================================================

@router.get('/clearance')
def get_clearance(request):
    return {'clearances': []}

@router.post('/clearance')
def create_clearance(request):
    return {'message': 'Create clearance'}

# ============================================================
# SIWES ENDPOINTS
# ============================================================

@router.get('/siwes-placements')
def list_siwes_placements(request):
    return {'placements': []}

@router.post('/siwes-placements')
def create_siwes_placement(request):
    return {'message': 'Create placement'}

# ============================================================
# ALUMNI ENDPOINTS
# ============================================================

@router.get('/alumni-profile')
def list_alumni(request):
    return {'alumni': []}

@router.post('/alumni-profile')
def create_alumni(request):
    return {'message': 'Create alumni'}

# ============================================================
# LIBRARY ENDPOINTS
# ============================================================

@router.get('/library-books')
def list_books(request):
    return {'books': []}

@router.post('/library-books')
def create_book(request):
    return {'message': 'Create book'}

# ============================================================
# CALENDAR ENDPOINTS
# ============================================================

@router.get('/calendar-events')
def list_events(request):
    return {'events': []}

@router.post('/calendar-events')
def create_event(request):
    return {'message': 'Create event'}

# ============================================================
# LEAVE ENDPOINTS
# ============================================================

@router.get('/leave-applications')
def list_leaves(request):
    return {'leaves': []}

@router.post('/leave-applications')
def create_leave(request):
    return {'message': 'Create leave'}

# ============================================================
# ID CARD ENDPOINTS
# ============================================================

@router.get('/id-card-requests')
def list_id_requests(request):
    return {'requests': []}

@router.post('/id-card-requests')
def create_id_request(request):
    return {'message': 'Create ID request'}

# ============================================================
# STATS ENDPOINTS
# ============================================================

@router.get('/stats')
def get_stats(request):
    return {
        'total_students': StudentProfile.objects.count(),
        'total_faculties': Faculty.objects.count(),
        'total_departments': Department.objects.count(),
        'total_programmes': Programme.objects.count(),
    }

@router.get('/search')
def search(request, q: str = '', type: str = 'all'):
    results = {}
    if type in ['all', 'students']:
        students = StudentProfile.objects.filter(
            Q(student_id__icontains=q) |
            Q(user__first_name__icontains=q) |
            Q(user__last_name__icontains=q)
        )[:10]
        results['students'] = [{'id': s.id, 'student_id': s.student_id} for s in students]
    
    if type in ['all', 'courses']:
        courses = Course.objects.filter(
            Q(code__icontains=q) |
            Q(name__icontains=q)
        )[:10]
        results['courses'] = [{'id': c.id, 'code': c.code, 'name': c.name} for c in courses]
    
    return results

# ============================================================
# SESSION ENDPOINTS
# ============================================================

@router.get('/sessions')
def list_sessions(request):
    return AcademicSession.objects.all()

@router.get('/current')
def get_current_session(request):
    current = AcademicSession.objects.filter(is_current=True).first()
    if current:
        return {'id': current.id, 'year': current.year, 'name': current.name}
    return {'message': 'No current session'}