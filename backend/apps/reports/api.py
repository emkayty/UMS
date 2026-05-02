from ninja import Router, Schema
from django.db.models import Count, Sum, Avg
from datetime import datetime

router = Router(tags=['Reports'])


# ===== Student List Report =====
@router.get('/student-list')
def get_student_list(request, programme_id: str = None, level: int = None):
    """Generate student list report with REAL data."""
    from apps.student.models import StudentProfile
    
    students = StudentProfile.objects.select_related('programme').all()
    
    if programme_id:
        students = students.filter(programme_id=programme_id)
    if level:
        students = students.filter(current_level=level)
    
    student_list = []
    for s in students[:100]:
        student_list.append({
            'id': str(s.id),
            'matric': s.matric_number,
            'name': f"{s.first_name} {s.last_name}",
            'programme': s.programme.name if s.programme else None,
            'level': s.current_level,
            'status': s.admission_status,
            'email': s.user.email if s.user else None
        })
    
    return {'count': students.count(), 'students': student_list}


# ===== Staff List Report =====
@router.get('/staff-list')
def get_staff_list(request, department_id: str = None):
    """Generate staff list report."""
    from apps.staff.models import StaffProfile
    
    staff = StaffProfile.objects.select_related('department').all()
    
    if department_id:
        staff = staff.filter(department_id=department_id)
    
    staff_list = []
    for s in staff[:100]:
        staff_list.append({
            'id': str(s.id),
            'staff_id': s.staff_id,
            'name': f"{s.first_name} {s.last_name}",
            'department': s.department.name if s.department else None,
            'rank': s.rank,
            'email': s.user.email if s.user else None
        })
    
    return {'count': staff.count(), 'staff': staff_list}


# ===== Course List Report =====
@router.get('/course-list')
def get_course_list(request, programme_id: str = None, level: int = None):
    """Generate course list report."""
    from apps.academic.models import Course
    
    courses = Course.objects.select_related('programme', 'department').all()
    
    if programme_id:
        courses = courses.filter(programme_id=programme_id)
    if level:
        courses = courses.filter(level=level)
    
    course_list = []
    for c in courses:
        course_list.append({
            'code': c.code,
            'title': c.title,
            'level': c.level,
            'credits': c.credit_units,
            'programme': c.programme.name if c.programme else None,
            'department': c.department.name if c.department else None
        })
    
    return {'count': courses.count(), 'courses': course_list}


# ===== Finance Summary =====
@router.get('/finance-summary')
def get_finance_summary(request, session_id: str = None):
    """Generate finance summary with REAL data."""
    from apps.finance.models import Payment, StudentFee
    
    total_collected = Payment.objects.filter(status='success').aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    fees = StudentFee.objects.all()
    total_expected = fees.aggregate(total=Sum('amount_due'))['total'] or 0
    total_paid = fees.aggregate(total=Sum('amount_paid'))['total'] or 0
    
    rate = 0
    if total_expected > 0:
        rate = round((float(total_collected) / float(total_expected)) * 100, 2)
    
    return {
        'total_collected': float(total_collected),
        'total_expected': float(total_expected),
        'total_outstanding': float(total_expected - total_paid),
        'collection_rate': rate,
        'student_count': fees.count(),
        'payment_count': Payment.objects.filter(status='success').count()
    }


# ===== Academic Stats =====
@router.get('/academic-stats')
def get_academic_stats(request):
    """Get academic statistics."""
    from apps.academic.models import Faculty, Department, Programme, Course, AcademicSession
    from apps.student.models import StudentProfile, CourseRegistration
    from apps.student.results import Result
    
    current_session = AcademicSession.objects.filter(is_current=True).first()
    
    return {
        'faculties': Faculty.objects.count(),
        'departments': Department.objects.count(),
        'programmes': Programme.objects.count(),
        'courses': Course.objects.count(),
        'current_session': current_session.name if current_session else None,
        'total_students': StudentProfile.objects.count(),
        'admitted_students': StudentProfile.objects.filter(admission_status='admitted').count(),
        'registered_students': CourseRegistration.objects.filter(status='active').count(),
        'results_uploaded': Result.objects.count()
    }


# ===== Clearance Status =====
@router.get('/clearance-status')
def get_clearance_report(request, session_id: str = None):
    """Generate clearance status report."""
    from apps.student.results import GraduationClearance
    
    clearances = GraduationClearance.objects.all()
    
    return {
        'total': clearances.count(),
        'eligible': clearances.filter(eligible_to_graduate=True).count(),
        'pending': clearances.filter(eligible_to_graduate=False).count(),
        'library_cleared': clearances.filter(cleared_by_library=True).count(),
        'bursary_cleared': clearances.filter(cleared_by_bursary=True).count()
    }
    comment = data.get('comment', '')
    role = data.get('role', 'hod')  # hod, dean, registrar
    
    if action == 'approve':
        if role == 'hod':
            result.status = 'approved_hod'
            result.approved_by_hod = request.auth[0]
            result.hod_comment = comment
        elif role == 'dean':
            result.status = 'approved_dean'
            result.approved_by_dean = request.auth[0]
            result.dean_comment = comment
        else:
            result.status = 'approved_senate'
            result.approved_by_senate = request.auth[0]
    else:  # reject
        result.status = 'rejected'
        if role == 'hod':
            result.hod_comment = comment
        else:
            result.dean_comment = comment
    
    result.save()
    return {'success': True}


@router.get('/approvals/history')
def get_approval_history(request, role: str = None):
    """Get approval history."""
    from apps.student.results import Result
    
    qs = Result.objects.exclude(status='pending')
    if role:
        if role == 'hod':
            qs = qs.filter(approved_by_hod=request.auth[0])
        elif role == 'dean':
            qs = qs.filter(approved_by_dean=request.auth[0])
    
    return [
        {
            'id': str(r.id),
            'course': r.registration.course.code,
            'status': r.status,
            'approved_by': r.approved_by_hod.email if r.approved_by_hod else (
                r.approved_by_dean.email if r.approved_by_dean else None
            ),
            'date': (
                r.updated_at.isoformat() if r.status != 'pending' 
                else r.created_at.isoformat()
            )
        }
        for r in qs[:50]
    ]


# === Dashboard Statistics ===
@router.get('/stats/dashboard')
def dashboard_stats(request):
    """Get dashboard statistics."""
    from apps.accounts.models import User
    from apps.student.models import StudentProfile, CourseRegistration
    from apps.academic.models import Course
    
    stats = {
        'total_students': User.objects.filter(role='student', is_active=True).count(),
        'total_lecturers': User.objects.filter(role='lecturer', is_active=True).count(),
        'total_courses': Course.objects.count(),
    }
    
    # Add student-specific stats
    if hasattr(request.auth[0], 'student_profile'):
        student = request.auth[0].student_profile
        regs = CourseRegistration.objects.filter(student=student, status='active')
        stats['registered_courses'] = regs.count()
    
    return stats


# === NYSC Export ===
@router.get('/export/nysc')
def export_nysc_list(request, session_id: str = None):
    """Export NYSC mobilization list."""
    from apps.student.models import StudentProfile
    from apps.student.results import Result
    from apps.academic.models import AcademicSession
    
    session = AcademicSession.objects.get(id=session_id) if session_id else (
        AcademicSession.objects.filter(is_current=True).first()
    )
    if not session:
        return {'success': False, 'error': 'No current session'}
    
    # Get final year students eligible for NYSC
    students = StudentProfile.objects.filter(
        admission_status='admitted',
        clearance__eligible_to_graduate=True
    ).select_related('programme', 'programme__department')
    
    nysc_list = []
    for student in students:
        # Calculate summary CGPA
        regs = CourseRegistration.objects.filter(student=student)
        results = Result.objects.filter(registration__in=regs)
        
        total_points = 0
        total_units = 0
        for result in results:
            course = result.registration.course
            total_points += float(result.grade_point) * course.credit_units
            total_units += course.credit_units
        
        cgpa = round(total_points / total_units, 2) if total_units > 0 else 0
        
        # Determine class of degree
        if cgpa >= 4.5:
            degree_class = 'First Class'
        elif cgpa >= 3.5:
            degree_class = 'Second Class Upper'
        elif cgpa >= 3.0:
            degree_class = 'Second Class Lower'
        elif cgpa >= 2.0:
            degree_class = 'Third Class'
        else:
            degree_class = 'Pass'
        
        nysc_list.append({
            'matric_no': student.matric_number,
            'surname': student.last_name,
            'other_names': student.first_name,
            'date_of_birth': student.date_of_birth.isoformat() if student.date_of_birth else '',
            'sex': student.gender,
            'state_of_origin': student.state_of_origin,
            'lga': student.lga,
            'phone': student.phone,
            'email': student.user.email,
            'programme': student.programme.name if student.programme else '',
            'class_of_degree': degree_class,
            'year_of_graduation': session.name.split('/')[0] if session else ''
        })
    
    return {
        'success': True,
        'students': nysc_list,
        'count': len(nysc_list)
    }


# === Analytics ===
@router.get('/analytics/enrollment')
def enrollment_analytics(request, session_id: str = None):
    """Get enrollment analytics."""
    from apps.student.models import StudentProfile
    from apps.academic.models import Programme
    
    programmes = Programme.objects.annotate(
        student_count=Count('students')
    )
    
    return [
        {
            'programme': p.name,
            'code': p.code,
            'students': p.student_count
        }
        for p in programmes
    ]


@router.get('/analytics/performance')
def performance_analytics(request):
    """Get performance analytics."""
    from apps.student.results import Result
    from apps.academic.models import Course
    
    # Average scores per course
    courses = Course.objects.annotate(
        avg_score=Avg('registrations__results__score')
    )
    
    return [
        {
            'course': c.code,
            'title': c.title,
            'level': c.level,
            'avg_score': float(c.avg_score or 0)
        }
        for c in courses if c.avg_score
    ]


# === Reports Generation ===
@router.get('/reports/accreditation')
def generate_accreditation_report(request, department_id: str):
    """Generate NUC accreditation report."""
    from apps.academic.models import Department, Course
    
    dept = Department.objects.get(id=department_id)
    
    staff_count = dept.staff.count()
    student_count = dept.students.count()
    courses = Course.objects.filter(department=dept)
    
    # Calculate student-staff ratio
    ratio = round(student_count / staff_count, 1) if staff_count > 0 else 0
    
    report = {
        'department': dept.name,
        'faculty': dept.faculty.name,
        'student_count': student_count,
        'staff_count': staff_count,
        'student_staff_ratio': ratio,
        'courses': [
            {
                'code': c.code,
                'title': c.title,
                'level': c.level,
                'credits': c.credit_units
            }
            for c in courses
        ]
    }
    
    return report


# === Audit Logs ===
@router.get('/audit-logs')
def list_audit_logs(request, user_id: str = None, action: str = None):
    """List audit logs."""
    from apps.reports.models import AuditLog
    
    qs = AuditLog.objects.all()
    if user_id:
        qs = qs.filter(user_id=user_id)
    if action:
        qs = qs.filter(action_type=action)
    
    return [
        {
            'user': log.user.email if log.user else 'System',
            'action': log.action_type,
            'model': log.model_name,
            'object_id': log.object_id,
            'timestamp': log.timestamp.isoformat()
        }
        for log in qs[:100]
    ]