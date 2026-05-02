"""
CORE API - Unified, Optimized API Endpoints
Consolidated from all apps for efficiency
"""

from ninja import Router, Schema
from typing import List, Optional
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q, Count, Avg, Sum
from django.conf import settings

router = Router(tags=['Core'])


# ============================================================
# CORE SCHEMAS
# ============================================================

class FacultySchema(Schema):
    id: str
    name: str
    code: str
    is_active: bool


class DepartmentSchema(Schema):
    id: str
    name: str
    code: str
    faculty_id: str


class ProgrammeSchema(Schema):
    id: str
    name: str
    code: str
    degree_type: str
    duration_years: int


class CourseSchema(Schema):
    id: str
    code: str
    name: str
    credit_units: int
    level: str
    semester: str
    is_compulsory: bool


class StudentSchema(Schema):
    id: str
    student_id: str
    name: str
    email: str
    programme: Optional[str]
    level: str
    cgpa: float
    status: str


class ResultSchema(Schema):
    id: str
    course_code: str
    course_name: str
    score: float
    grade: str
    grade_point: float
    session: str
    semester: str


class FeeSchema(Schema):
    id: str
    description: str
    amount: float
    status: str


# ============================================================
# CORE ACADEMIC ENDPOINTS
# ============================================================

@router.get('/faculties', response=List[FacultySchema])
def list_faculties(request):
    """List all faculties."""
    from apps.core.models import Faculty
    return Faculty.objects.filter(is_active=True)


@router.get('/faculties/{id}', response=FacultySchema)
def get_faculty(request, id: str):
    """Get faculty details."""
    from apps.core.models import Faculty
    return get_object_or_404(Faculty, id=id)


@router.get('/departments', response=List[DepartmentSchema])
def list_departments(request, faculty_id: str = None):
    """List departments."""
    from apps.core.models import Department
    
    query = Department.objects.filter(is_active=True)
    if faculty_id:
        query = query.filter(faculty_id=faculty_id)
    
    return query


@router.get('/departments/{id}', response=DepartmentSchema)
def get_department(request, id: str):
    """Get department details."""
    from apps.core.models import Department
    return get_object_or_404(Department, id=id)


@router.get('/programmes', response=List[ProgrammeSchema])
def list_programmes(request, department_id: str = None):
    """List programmes."""
    from apps.core.models import Programme
    
    query = Programme.objects.filter(is_active=True)
    if department_id:
        query = query.filter(department_id=department_id)
    
    return query


@router.get('/courses', response=List[CourseSchema])
def list_courses(request, programme_id: str = None, level: str = None):
    """List courses."""
    from apps.core.models import Course
    
    query = Course.objects.filter(is_active=True)
    if programme_id:
        query = query.filter(programme_id=programme_id)
    if level:
        query = query.filter(level=level)
    
    return query[:50]


@router.get('/sessions')
def list_sessions(request):
    """List academic sessions."""
    from apps.core.models import AcademicSession
    
    sessions = AcademicSession.objects.all().order_by('-start_date')
    return [
        {
            'id': str(s.id),
            'name': s.name,
            'is_current': s.is_current,
            'start': str(s.start_date),
            'end': str(s.end_date)
        }
        for s in sessions
    ]


@router.get('/current')
def get_current_academic(request):
    """Get current session and semester."""
    from apps.core.models import AcademicSession, Semester
    
    session = AcademicSession.objects.filter(is_current=True).first()
    semester = Semester.objects.filter(is_current=True).first()
    
    return {
        'session': {
            'id': str(session.id),
            'name': session.name
        } if session else None,
        'semester': {
            'id': str(semester.id),
            'name': semester.semester
        } if semester else None
    }


# ============================================================
# CORE STUDENT ENDPOINTS
# ============================================================

@router.get('/students', response=List[StudentSchema])
def list_students(request, programme_id: str = None, level: str = None, status: str = None):
    """List students with filters."""
    from apps.core.models import StudentProfile
    
    query = StudentProfile.objects.select_related('user', 'programme')
    
    if programme_id:
        query = query.filter(programme_id=programme_id)
    if level:
        query = query.filter(current_level=level)
    if status:
        query = query.filter(status=status)
    
    return query[:100]


@router.get('/students/{student_id}', response=StudentSchema)
def get_student(request, student_id: str):
    """Get student details."""
    from apps.core.models import StudentProfile
    
    student = get_object_or_404(StudentProfile, student_id=student_id)
    return {
        'id': str(student.id),
        'student_id': student.student_id,
        'name': student.user.get_full_name() if student.user else '',
        'email': student.user.email if student.user else '',
        'programme': student.programme.name if student.programme else None,
        'level': student.current_level,
        'cgpa': float(student.cgpa),
        'status': student.status
    }


@router.get('/students/{student_id}/results', response=List[ResultSchema])
def get_student_results(request, student_id: str, session_id: str = None, semester: str = None):
    """Get student results."""
    from apps.core.models import StudentProfile, Result
    
    student = get_object_or_404(StudentProfile, student_id=student_id)
    query = Result.objects.filter(student=student)
    
    if session_id:
        query = query.filter(session_id=session_id)
    if semester:
        query = query.filter(semester__semester=semester)
    
    return [
        {
            'id': str(r.id),
            'course_code': r.course.code,
            'course_name': r.course.name,
            'score': float(r.score),
            'grade': r.grade,
            'grade_point': float(r.grade_point),
            'session': r.session.name,
            'semester': r.semester.semester
        }
        for r in query
    ]


@router.get('/students/{student_id}/gpa')
def calculate_student_gpa(request, student_id: str, session_id: str = None, semester: str = None):
    """Calculate student GPA."""
    from apps.core.models import StudentProfile, Result
    
    student = get_object_or_404(StudentProfile, student_id=student_id)
    query = Result.objects.filter(student=student, approved=True)
    
    if session_id:
        query = query.filter(session_id=session_id)
    if semester:
        query = query.filter(semester__semester=semester)
    
    results = query
    return {
        'cgpa': apps.core.models.calculate_gpa(results),
        'results_count': results.count()
    }


# ============================================================
# CORE FINANCE ENDPOINTS
# ============================================================

@router.get('/students/{student_id}/invoices')
def get_student_invoices(request, student_id: str):
    """Get student invoices."""
    from apps.core.models import StudentProfile, Invoice
    
    student = get_object_or_404(StudentProfile, student_id=student_id)
    invoices = Invoice.objects.filter(student=student)
    
    return [
        {
            'id': str(i.id),
            'description': i.description,
            'amount': float(i.amount),
            'status': i.status,
            'due': str(i.due_date) if i.due_date else None
        }
        for i in invoices
    ]


@router.get('/students/{student_id}/payments')
def get_student_payments(request, student_id: str):
    """Get student payments."""
    from apps.core.models import StudentProfile, Payment
    
    student = get_object_or_404(StudentProfile, student_id=student_id)
    payments = Payment.objects.filter(student=student, status='success')
    
    return [
        {
            'id': str(p.id),
            'amount': float(p.amount),
            'ref': p.payment_ref,
            'date': str(p.paid_at) if p.paid_at else None
        }
        for p in payments
    ]


# ============================================================
# CORE LEARNING ENDPOINTS
# ============================================================

@router.get('/courses/{course_id}/materials')
def get_course_materials(request, course_id: str):
    """Get course materials."""
    from apps.core.models import CourseMaterial
    
    materials = CourseMaterial.objects.filter(
        course_id=course_id,
        is_published=True
    )
    
    return [
        {
            'id': str(m.id),
            'title': m.title,
            'type': m.material_type,
            'url': m.file_url,
            'created': str(m.created_at)
        }
        for m in materials
    ]


@router.get('/courses/{course_id}/exams')
def get_course_exams(request, course_id: str):
    """Get course exams."""
    from apps.core.models import Exam
    
    exams = Exam.objects.filter(course_id=course_id)
    
    return [
        {
            'id': str(e.id),
            'title': e.title,
            'type': e.exam_type,
            'date': str(e.date),
            'duration': e.duration_minutes,
            'total_marks': e.total_marks
        }
        for e in exams
    ]


# ============================================================
# CORE STATISTICS
# ============================================================

@router.get('/stats')
def get_statistics(request):
    """Get system statistics."""
    from apps.core.models import (
        StudentProfile, Programme, Course, 
        AcademicSession, StaffProfile, Invoice, Payment
    )
    
    active_students = StudentProfile.objects.filter(status='active').count()
    active_staff = StaffProfile.objects.filter(is_active=True).count()
    programmes = Programme.objects.filter(is_active=True).count()
    
    # Finance stats
    total_invoiced = Invoice.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    total_collected = Payment.objects.filter(status='success').aggregate(Sum('amount'))['amount__sum'] or 0
    
    return {
        'students': {
            'active': active_students,
            'programmes': programmes
        },
        'staff': {
            'active': active_staff
        },
        'finance': {
            'invoiced': float(total_invoiced),
            'collected': float(total_collected),
            'collection_rate': round(float(total_collected) / float(total_invoiced) * 100, 1) if total_invoiced > 0 else 0
        }
    }


# ============================================================
# CORE SEARCH
# ============================================================

@router.get('/search')
def global_search(request, q: str, type: str = 'all'):
    """Global search across system."""
    from apps.core.models import StudentProfile, Programme, Course, Department
    
    results = {'students': [], 'courses': [], 'departments': []}
    
    if type in ['all', 'students']:
        students = StudentProfile.objects.filter(
            Q(student_id__icontains=q) |
            Q(user__first_name__icontains=q) |
            Q(user__last_name__icontains=q)
        )[:10]
        results['students'] = [
            {'id': str(s.id), 'student_id': s.student_id, 'name': s.user.get_full_name()}
            for s in students
        ]
    
    if type in ['all', 'courses']:
        courses = Course.objects.filter(
            Q(code__icontains=q) |
            Q(name__icontains=q)
        )[:10]
        results['courses'] = [
            {'id': str(c.id), 'code': c.code, 'name': c.name}
            for c in courses
        ]
    
    if type in ['all', 'departments']:
        departments = Department.objects.filter(
            Q(code__icontains=q) |
            Q(name__icontains=q)
        )[:10]
        results['departments'] = [
            {'id': str(d.id), 'code': d.code, 'name': d.name}
            for d in departments
        ]
    
    return results