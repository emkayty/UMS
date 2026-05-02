"""
Grading Policy Resolution and CGPA Calculation Engine
"""
from apps.academic.grading import GradingPolicy


def resolve_grading_policy(course_id, programme_id, faculty_id):
    """Resolve effective grading policy with inheritance.
    
    Priority: course > programme > faculty > institution default
    """
    return GradingPolicy.resolve_policy(course_id, programme_id, faculty_id)


def calculate_grade(score, policy):
    """Calculate grade for a score."""
    return policy.get_grade(score)


def calculate_grade_point(score, policy):
    """Calculate grade point for a score."""
    return policy.calculate_grade_point(score)


def calculate_cgpa(student, session_id=None, semester_id=None):
    """Calculate student's CGPA.
    
    Args:
        student: StudentProfile instance
        session_id: Optional session filter
        semester_id: Optional semester filter
    
    Returns:
        dict with gpa, cumulative_gpa, and breakdown
    """
    from apps.student.models import CourseRegistration
    from apps.student.results import Result
    
    regs = CourseRegistration.objects.filter(
        student=student, status='active'
    )
    
    results = Result.objects.filter(
        registration__in=regs,
        status__in=['approved_hod', 'approved_dean', 'approved_senate']
    )
    
    if session_id:
        results = results.filter(session_id=session_id)
    if semester_id:
        results = results.filter(semester_id=semester_id)
    
    total_grade_points = 0
    total_credit_units = 0
    
    breakdown = []
    
    for result in results:
        course = result.registration.course
        policy = resolve_grading_policy(
            course_id=course.id,
            programme_id=course.programme_id,
            faculty_id=course.department.faculty_id
        )
        
        grade_point = calculate_grade_point(float(result.score), policy)
        credit_units = course.credit_units
        
        total_grade_points += grade_point * credit_units
        total_credit_units += credit_units
        
        breakdown.append({
            'course': course.code,
            'score': float(result.score),
            'grade': result.grade,
            'grade_point': grade_point,
            'credit_units': credit_units
        })
    
    gpa = round(total_grade_points / total_credit_units, 2) if total_credit_units > 0 else 0
    
    return {
        'gpa': gpa,
        'cumulative_gpa': gpa,  # Same as GPA for now
        'total_credit_units': total_credit_units,
        'breakdown': breakdown
    }


def calculate_what_if_cgpa(student, changes):
    """Calculate what-if CGPA with hypothetical changes.
    
    Args:
        student: StudentProfile instance
        changes: list of {course_id, hypothetical_score}
    
    Returns:
        dict with hypothetical CGPA
    """
    from apps.student.models import CourseRegistration
    from apps.student.results import Result
    from apps.academic.models import Course
    
    # Get current results
    regs = CourseRegistration.objects.filter(
        student=student, status='active'
    )
    
    results = Result.objects.filter(
        registration__in=regs,
        status__in=['approved_hod', 'approved_dean', 'approved_senate']
    )
    
    total_grade_points = 0
    total_credit_units = 0
    
    # Apply changes
    change_map = {c['course_id']: c['score'] for c in changes}
    
    for result in results:
        course = result.registration.course
        policy = resolve_grading_policy(
            course_id=course.id,
            programme_id=course.programme_id,
            faculty_id=course.department.faculty_id
        )
        
        # Use hypothetical or actual score
        score = change_map.get(str(course.id), float(result.score))
        
        grade_point = calculate_grade_point(score, policy)
        credit_units = course.credit_units
        
        total_grade_points += grade_point * credit_units
        total_credit_units += credit_units
    
    cgpa = round(total_grade_points / total_credit_units, 2) if total_credit_units > 0 else 0
    
    return {'hypothetical_cgpa': cgpa}


def check_graduation_eligibility(student):
    """Check if student is eligible to graduate.
    
    Returns:
        dict with eligibility status and requirements
    """
    from apps.student.models import CourseRegistration
    from apps.student.results import Result, GraduationClearance
    
    regs = CourseRegistration.objects.filter(
        student=student, status='active'
    )
    
    # Check all required results
    total_required = regs.count()
    total_approved = Result.objects.filter(
        registration__in=regs,
        status__in=['approved_hod', 'approved_dean', 'approved_senate']
    ).count()
    
    # Check clearance
    clearance = GraduationClearance.objects.filter(student=student).first()
    
    requirements = {
        'results_complete': total_required > 0 and total_approved >= total_required,
        'results_approved': total_approved,
        'total_results': total_required,
        'library': clearance.cleared_by_library if clearance else False,
        'hostel': clearance.cleared_by_hostel if clearance else False,
        'bursary': clearance.cleared_by_bursary if clearance else False,
        'department': clearance.cleared_by_department if clearance else False
    }
    
    all_cleared = all([
        requirements['results_complete'],
        requirements['library'],
        requirements['hostel'],
        requirements['bursary'],
        requirements['department']
    ])
    
    return {
        'eligible': all_cleared,
        'requirements': requirements
    }