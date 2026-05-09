"""
Course Registration Validation Service
Validates course registration rules:
- Prerequisite completion
- Credit load limits
- Add/drop period enforcement
- Carryover rules
"""

from typing import List, Dict, Optional, Tuple
from django.utils import timezone
from django.db.models import Sum


class RegistrationValidationError(Exception):
    """Custom exception for registration validation errors"""
    def __init__(self, message: str, code: str = "VALIDATION_ERROR"):
        self.message = message
        self.code = code
        super().__init__(message)


class CourseRegistrationValidator:
    """
    Validates course registration according to university rules
    """
    
    # Default credit limits (configurable per institution)
    DEFAULT_MIN_CREDITS = 15
    DEFAULT_MAX_CREDITS = 24
    DEFAULT_CARRYOVER_LIMIT = 2
    
    def __init__(self, student, session, semester):
        self.student = student
        self.session = session
        self.semester = semester
    
    def validate_registration(
        self, 
        courses: List['Course']
    ) -> Tuple[bool, List[str]]:
        """
        Validate course registration
        
        Returns: (is_valid, error_messages)
        """
        errors = []
        
        # 1. Check add/drop period
        if not self.is_within_registration_period():
            errors.append("Registration is closed. Please check the academic calendar.")
        
        # 2. Check credit load
        credit_errors = self.validate_credit_load(courses)
        if credit_errors:
            errors.extend(credit_errors)
        
        # 3. Check prerequisites
        prereq_errors = self.validate_prerequisites(courses)
        if prereq_errors:
            errors.extend(prereq_errors)
        
        # 4. Check carryover limit
        carryover_errors = self.validate_carryover_limit(courses)
        if carryover_errors:
            errors.extend(carryover_errors)
        
        # 5. Check for duplicates
        duplicate_errors = self.check_duplicates(courses)
        if duplicate_errors:
            errors.extend(duplicate_errors)
        
        return len(errors) == 0, errors
    
    def is_within_registration_period(self) -> bool:
        """Check if current date is within registration period"""
        from apps.academic.models import AcademicSession
        
        try:
            session = AcademicSession.objects.get(
                id=self.session.id,
                is_registration_open=True
            )
            
            now = timezone.now()
            
            # Check if within registration period
            if session.registration_start and session.registration_end:
                return session.registration_start <= now <= session.registration_end
            
            # Check add/drop period
            if session.add_drop_start and session.add_drop_end:
                return session.add_drop_start <= now <= session.add_drop_end
            
            return True  # No period defined, allow
            
        except AcademicSession.DoesNotExist:
            return True  # No restriction if session not found
    
    def validate_credit_load(self, courses: List['Course']) -> List[str]:
        """Validate credit load is within limits"""
        errors = []
        
        total_credits = sum(c.credit_units for c in courses)
        
        # Get student profile for custom limits
        max_credits = getattr(self.student, 'max_credit_load', self.DEFAULT_MAX_CREDITS)
        min_credits = getattr(self.student, 'min_credit_load', self.DEFAULT_MIN_CREDITS)
        
        if total_credits < min_credits:
            errors.append(
                f"Credit load ({total_credits}) is below minimum required ({min_credits})"
            )
        
        if total_credits > max_credits:
            errors.append(
                f"Credit load ({total_credits}) exceeds maximum allowed ({max_credits})"
            )
        
        return errors
    
    def validate_prerequisites(self, courses: List['Course']) -> List[str]:
        """Check that prerequisites are completed"""
        errors = []
        
        # Get completed courses
        from apps.student.models import CourseRegistration
        from apps.core.models import Result
        
        completed_results = Result.objects.filter(
            student=self.student,
            grade_point__gt=0  # Passed
        ).select_related('course')
        
        completed_course_ids = set(r.course.id for r in completed_results)
        
        # Check each course's prerequisites
        for course in courses:
            prerequisites = course.prerequisites.all()
            
            for prereq in prerequisites:
                if prereq.id not in completed_course_ids:
                    errors.append(
                        f"Prerequisite not met: {prereq.code} - {prereq.name} "
                        f"must be completed before registering for {course.code}"
                    )
        
        return errors
    
    def validate_carryover_limit(self, courses: List['Course']) -> List[str]:
        """Check carryover (failed courses) limit"""
        errors = []
        
        # Get failed courses
        from apps.core.models import Result
        
        failed_results = Result.objects.filter(
            student=self.student,
            grade_point=0  # Failed
        ).select_related('course')
        
        failed_course_ids = set(r.course.id for r in failed_results)
        
        # Count how many failed courses are being repeated
        repeated_failures = sum(
            1 for c in courses 
            if c.id in failed_course_ids
        )
        
        new_failures = len(failed_course_ids) - repeated_failures
        
        # Total outstanding failures
        outstanding_failures = new_failures + repeated_failures
        
        if outstanding_failures > self.DEFAULT_CARRYOVER_LIMIT:
            errors.append(
                f"Carryover limit exceeded. You have {outstanding_failures} outstanding "
                f"failed courses (max allowed: {self.DEFAULT_CARRYOVER_LIMIT}). "
                f"Please repeat and pass some courses first."
            )
        
        return errors
    
    def check_duplicates(self, courses: List['Course']) -> List[str]:
        """Check for duplicate course registration"""
        errors = []
        
        # Get current semester registrations
        from apps.student.models import CourseRegistration
        
        existing = CourseRegistration.objects.filter(
            student=self.student,
            session=self.session,
            semester=self.semester,
            status__in=['registered', 'completed']
        ).select_related('course')
        
        registered_course_ids = set(r.course.id for r in existing)
        
        for course in courses:
            if course.id in registered_course_ids:
                errors.append(
                    f"Already registered for {course.code} - {course.name}"
                )
        
        # Also check for duplicates within the request
        course_ids = [c.id for c in courses]
        if len(course_ids) != len(set(course_ids)):
            errors.append("Duplicate courses in registration request")
        
        return errors
    
    def get_registration_summary(self, courses: List['Course']) -> Dict:
        """Get summary of registration"""
        return {
            'total_courses': len(courses),
            'total_credits': sum(c.credit_units for c in courses),
            'student': str(self.student),
            'session': str(self.session),
            'semester': str(self.semester),
            'within_period': self.is_within_registration_period(),
        }


# Helper functions

def validate_course_registration(student, session, semester, courses) -> Tuple[bool, List[str]]:
    """
    Convenience function to validate course registration
    
    Usage:
        is_valid, errors = validate_course_registration(
            student=student,
            session=session,
            semester=semester,
            courses=[course1, course2, course3]
        )
    """
    validator = CourseRegistrationValidator(student, session, semester)
    return validator.validate_registration(courses)


def get_available_courses(student, session, semester) -> List['Course']:
    """
    Get courses available for registration
    Filters out courses student cannot take
    """
    from apps.academic.models import Programme
    
    # Get student's programme
    try:
        profile = student.student_profile
        programme = profile.programme
    except:
        return []
    
    # Get courses for programme and semester
    from apps.academic.models import Course
    
    courses = Course.objects.filter(
        programme=programme,
        semester=semester,
        session=session,
        is_active=True
    ).select_related('programme')
    
    # Get completed courses
    from apps.core.models import Result
    completed = Result.objects.filter(
        student=student,
        grade_point__gt=0
    ).values_list('course_id', flat=True)
    
    # Filter available
    available = []
    for course in courses:
        # Check if already registered
        from apps.student.models import CourseRegistration
        registered = CourseRegistration.objects.filter(
            student=student,
            course=course,
            status__in=['registered', 'completed']
        ).exists()
        
        if not registered:
            available.append(course)
    
    return available


# Export
__all__ = [
    'CourseRegistrationValidator',
    'RegistrationValidationError',
    'validate_course_registration',
    'get_available_courses',
]