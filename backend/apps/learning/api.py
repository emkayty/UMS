from ninja import Router, Schema
from typing import Optional, List
from django.shortcuts import get_object_or_404
import uuid

from apps.learning.models import (
    Material, Assignment, AssignmentSubmission, Quiz, QuizAttempt,
    AttendanceSession, AttendanceRecord
)
from apps.academic.models import Course

router = Router(tags=['Learning'])


# === Material Schemas ===
class MaterialSchema(Schema):
    id: str
    course_id: str
    title: str
    file_url: str
    file_type: str
    description: str
    is_offline_available: bool


class AssignmentSchema(Schema):
    id: str
    course_id: str
    title: str
    description: str
    due_date: str
    max_score: float
    status: str


class SubmissionSchema(Schema):
    id: str
    assignment_id: str
    student_id: str
    file_url: str
    text_answer: str
    score: Optional[float]
    status: str


class QuizSchema(Schema):
    id: str
    course_id: str
    title: str
    duration_minutes: int
    is_published: bool


class AttendanceSessionSchema(Schema):
    id: str
    course_id: str
    date: str
    qr_code_token: str
    is_active: bool


# === Material APIs ===
@router.get('/courses/{course_id}/materials', response=List[MaterialSchema])
def list_materials(request, course_id: str):
    """List materials for a course."""
    qs = Material.objects.filter(course_id=course_id)
    return qs[:50]


@router.post('/courses/{course_id}/materials', response=MaterialSchema)
def upload_material(request, course_id: str, data: MaterialSchema):
    """Upload learning material."""
    course = get_object_or_404(Course, id=course_id)
    material = Material.objects.create(
        course=course,
        lecturer=request.auth[0],
        title=data.title,
        file_url=data.file_url,
        file_type=data.file_type,
        description=data.description,
        is_offline_available=data.is_offline_available
    )
    return material


@router.get('/materials/{id}', response=MaterialSchema)
def get_material(request, id: str):
    """Get material by ID."""
    return get_object_or_404(Material, id=id)


@router.put('/materials/{id}', response=MaterialSchema)
def update_material(request, id: str, data: MaterialSchema):
    """Update material."""
    material = get_object_or_404(Material, id=id)
    for field in ['title', 'file_url', 'file_type', 'description', 'is_offline_available']:
        value = getattr(data, field, None)
        if value is not None:
            setattr(material, field, value)
    material.save()
    return material


@router.delete('/materials/{id}')
def delete_material(request, id: str):
    """Delete material."""
    material = get_object_or_404(Material, id=id)
    material.delete()
    return {'success': True, 'message': 'Material deleted'}


# === Assignment APIs ===
@router.get('/courses/{course_id}/assignments', response=List[AssignmentSchema])
def list_assignments(request, course_id: str, status: str = None):
    """List assignments for a course."""
    qs = Assignment.objects.filter(course_id=course_id)
    if status:
        qs = qs.filter(status=status)
    return qs[:50]


@router.post('/courses/{course_id}/assignments', response=AssignmentSchema)
def create_assignment(request, course_id: str, data: AssignmentSchema):
    """Create assignment."""
    course = get_object_or_404(Course, id=course_id)
    assignment = Assignment.objects.create(
        course=course,
        lecturer=request.auth[0],
        title=data.title,
        description=data.description,
        due_date=data.due_date,
        max_score=data.max_score,
        grading_rubric={},
        status=data.status or 'draft'
    )
    return assignment


@router.get('/assignments/{id}', response=AssignmentSchema)
def get_assignment(request, id: str):
    """Get assignment by ID."""
    return get_object_or_404(Assignment, id=id)


@router.patch('/assignments/{id}', response=AssignmentSchema)
def update_assignment(request, id: str, data: dict):
    """Update assignment."""
    assignment = get_object_or_404(Assignment, id=id)
    for field in ['title', 'description', 'due_date', 'max_score', 'status']:
        if field in data and data[field] is not None:
            setattr(assignment, field, data[field])
    assignment.save()
    return assignment


@router.delete('/assignments/{id}')
def delete_assignment(request, id: str):
    """Delete assignment."""
    assignment = get_object_or_404(Assignment, id=id)
    assignment.delete()
    return {'success': True, 'message': 'Assignment deleted'}


@router.post('/assignments/{id}/publish', response=AssignmentSchema)
def publish_assignment(request, id: str):
    """Publish assignment."""
    assignment = get_object_or_404(Assignment, id=id)
    assignment.status = 'published'
    assignment.save()
    return assignment


@router.get('/assignments/{id}/submissions')
def list_submissions(request, id: str):
    """List assignment submissions (for lecturer)."""
    assignment = get_object_or_404(Assignment, id=id)
    submissions = assignment.submissions.all()
    
    return [
        {
            'id': str(s.id),
            'student': s.student.matric_number or str(s.student.id),
            'file_url': s.file_url,
            'text_answer': s.text_answer[:200] if s.text_answer else '',
            'submitted_at': s.submitted_at.isoformat() if s.submitted_at else None,
            'score': float(s.score) if s.score else None,
            'status': s.status
        }
        for s in submissions[:50]
    ]


@router.patch('/assignments/{id}/grade')
def grade_submission(request, id: str, data: dict):
    """Grade a submission."""
    submission = get_object_or_404(AssignmentSubmission, id=id)
    submission.score = data.get('score')
    submission.feedback = data.get('feedback', '')
    submission.status = 'graded'
    submission.save()
    
    return {'success': True}


# === Quiz APIs ===
@router.get('/courses/{course_id}/quizzes', response=List[QuizSchema])
def list_quizzes(request, course_id: str):
    return Quiz.objects.filter(course_id=course_id)


@router.post('/courses/{course_id}/quizzes', response=QuizSchema)
def create_quiz(request, course_id: str, data: QuizSchema):
    course = get_object_or_404(Course, id=course_id)
    quiz = Quiz.objects.create(
        course=course,
        lecturer=request.auth[0],
        title=data.title,
        duration_minutes=data.duration_minutes,
        start_time=data.start_time,
        end_time=data.end_time,
        questions=data.questions or []
    )
    return quiz


@router.post('/quizzes/{id}/attempts')
def start_quiz_attempt(request, id: str):
    """Start a quiz attempt."""
    from apps.student.models import StudentProfile
    
    quiz = get_object_or_404(Quiz, id=id)
    student = request.auth[0].student_profile
    
    attempt, created = QuizAttempt.objects.get_or_create(
        quiz=quiz,
        student=student,
        defaults={}
    )
    
    return {'success': True, 'attempt_id': str(attempt.id)}


@router.post('/quizzes/{attempt_id}/submit')
def submit_quiz_attempt(request, attempt_id: str, data: dict):
    """Submit quiz answers."""
    attempt = get_object_or_404(QuizAttempt, id=attempt_id)
    attempt.answers = data.get('answers', {})
    attempt.submitted_at = datetime.now()
    
    # Auto-grade
    quiz = attempt.quiz
    correct = 0
    total = len(quiz.questions)
    
    for i, question in enumerate(quiz.questions):
        if attempt.answers.get(str(i)) == question.get('correct_answer'):
            correct += 1
    
    if total > 0:
        attempt.score_total = (correct / total) * 100
    
    attempt.save()
    
    return {'success': True, 'score': float(attempt.score_total) if attempt.score_total else 0}


# === Attendance APIs ===
@router.post('/courses/{course_id}/attendance-sessions', response=AttendanceSessionSchema)
def create_attendance_session(request, course_id: str):
    """Create attendance session with QR code."""
    course = get_object_or_404(Course, id=course_id)
    token = uuid.uuid4().hex
    
    session = AttendanceSession.objects.create(
        course=course,
        lecturer=request.auth[0],
        date=data.get('date'),
        qr_code_token=token
    )
    return session


@router.get('/attendance-sessions/{id}/records')
def list_attendance_records(request, id: str):
    """List attendance records."""
    session = get_object_or_404(AttendanceSession, id=id)
    records = session.records.all()
    
    return [
        {
            'student': r.student.matric_number or str(r.student.id),
            'timestamp': r.timestamp.isoformat(),
            'method': r.method
        }
        for r in records
    ]


@router.post('/attendance-sessions/{id}/record')
def record_attendance(request, id: str, data: dict):
    """Record attendance (QR scan or manual)."""
    session = get_object_or_404(AttendanceSession, id=id)
    
    # Verify QR token
    if data.get('method') == 'qr':
        if data.get('token') != session.qr_code_token:
            return {'success': False, 'error': 'Invalid QR code'}
    
    student_id = data.get('student_id')
    from apps.student.models import StudentProfile
    student = get_object_or_404(StudentProfile, id=student_id)
    
    record, created = AttendanceRecord.objects.get_or_create(
        session=session,
        student=student,
        defaults={
            'method': data.get('method', 'qr')
        }
    )
    
    return {'success': created}


# === Grade Sheet APIs ===
@router.post('/lecturer/grade-sheet')
def submit_grade_sheet(request, data: dict):
    """Submit grades for approval."""
    from apps.student.results import Result
    from apps.academic.grading import GradingPolicy
    
    course_id = data.get('course_id')
    semester_id = data.get('semester_id')
    results = data.get('results', [])
    
    for item in results:
        registration_id = item.get('registration_id')
        score = item.get('score')
        
        # Get grading policy
        reg = CourseRegistration.objects.get(id=registration_id)
        policy = GradingPolicy.resolve_policy(
            course_id=reg.course_id,
            programme_id=reg.course.programme_id,
            faculty_id=reg.course.department.faculty_id
        )
        
        grade = policy.get_grade(score)
        grade_point = policy.calculate_grade_point(score)
        
        result, _ = Result.objects.get_or_create(
            registration_id=registration_id,
            session_id=data.get('session_id'),
            semester_id=semester_id,
            defaults={
                'score': score,
                'grade': grade.get('grade'),
                'grade_point': grade_point,
                'lecturer': request.auth[0]
            }
        )
        
        if result.status == 'pending':
            result.status = 'pending'
            result.lecturer = request.auth[0]
            result.save()
    
    return {'success': True}


@router.get('/lecturer/grade-sheets')
def list_grade_sheets(request, status: str = None):
    """List submitted grade sheets."""
    from apps.student.results import Result
    
    qs = Result.objects.filter(lecturer=request.auth[0])
    if status:
        qs = qs.filter(status=status)
    
    return [
        {
            'id': str(r.id),
            'course': r.registration.course.code,
            'semester': r.semester.name,
            'status': r.status
        }
        for r in qs
    ]


from datetime import datetime
from apps.student.models import CourseRegistration