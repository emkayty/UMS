"""
Additional Academic APIs
Awards, Assessments, Documents
"""

from ninja import Router, Schema
from typing import List, Optional
from django.shortcuts import get_object_or_404
from django.utils import timezone

router = Router(tags=['Additional'])


# === Awards ===
class AwardSchema(Schema):
    id: str
    name: str
    award_type: str
    amount: float


class AssessmentSchema(Schema):
    id: str
    title: str
    course_id: str
    start_date: str
    duration_minutes: int


# === Awards APIs ===
@router.get('/awards')
def list_awards(request):
    """List all awards."""
    from apps.student.additional import StudentAward
    
    awards = StudentAward.objects.filter(is_active=True)
    
    return [
        {
            'id': str(a.id),
            'name': a.name,
            'type': a.award_type,
            'amount': float(a.amount),
            'deadline': str(a.application_deadline) if a.application_deadline else None
        }
        for a in awards
    ]


@router.post('/awards/{id}/apply')
def apply_award(request, id: str):
    """Apply for award."""
    from apps.student.additional import StudentAward, AwardRecipient
    from apps.student.models import StudentProfile
    
    award = get_object_or_404(StudentAward, id=id)
    student = StudentProfile.objects.filter(user=request.user).first()
    
    if not student:
        return {'error': 'Student profile not found'}
    
    recipient = AwardRecipient.objects.create(
        award=award,
        student=student,
        amount=award.amount
    )
    
    return {'success': True, 'id': str(recipient.id)}


@router.get('/awards/recipients')
def list_recipients(request):
    """List award recipients."""
    from apps.student.additional import AwardRecipient
    
    recipients = AwardRecipient.objects.all().order_by('-selection_date')
    
    return [
        {
            'id': str(r.id),
            'student': r.student.user.get_full_name() if r.student and r.student.user else None,
            'award': r.award.name,
            'amount': float(r.amount),
            'status': r.status
        }
        for r in recipients
    ]


@router.post('/awards/recipients/{id}/approve')
def approve_award(request, id: str):
    """Approve award recipient."""
    from apps.student.additional import AwardRecipient
    
    recipient = get_object_or_404(AwardRecipient, id=id)
    recipient.status = 'approved'
    recipient.awarded_by = request.user
    recipient.save()
    
    return {'success': True}


# === Partnerships ===
@router.get('/partnerships')
def list_partnerships(request):
    """List partnerships."""
    from apps.student.additional import Partnership
    
    partnerships = Partnership.objects.all()
    
    return [
        {
            'id': str(p.id),
            'name': p.institution_name,
            'country': p.country,
            'type': p.partner_type,
            'status': p.status
        }
        for p in partnerships
    ]


# === Assessments ===
@router.get('/assessments')
def list_assessments(request):
    """List online assessments."""
    from apps.student.additional import OnlineAssessment
    
    assessments = OnlineAssessment.objects.filter(is_published=True)
    
    return [
        {
            'id': str(a.id),
            'title': a.title,
            'course': a.course.code if a.course else None,
            'duration': a.duration_minutes,
            'start': str(a.start_date)
        }
        for a in assessments
    ]


@router.get('/assessments/{id}')
def get_assessment(request, id: str):
    """Get assessment details."""
    from apps.student.additional import OnlineAssessment, AssessmentQuestion
    
    assessment = get_object_or_404(OnlineAssessment, id=id)
    questions = AssessmentQuestion.objects.filter(assessment=assessment)
    
    return {
        'id': str(assessment.id),
        'title': assessment.title,
        'instructions': assessment.instructions,
        'duration': assessment.duration_minutes,
        'total_marks': assessment.total_marks,
        'pass_mark': assessment.pass_mark,
        'questions': [
            {
                'id': str(q.id),
                'text': q.question_text,
                'type': q.question_type,
                'marks': q.marks
            }
            for q in questions
        ]
    }


@router.post('/assessments/{id}/start')
def start_assessment(request, id: str):
    """Start assessment attempt."""
    from apps.student.additional import OnlineAssessment, AssessmentAttempt
    from apps.student.models import StudentProfile
    
    assessment = get_object_or_404(OnlineAssessment, id=id)
    student = StudentProfile.objects.filter(user=request.user).first()
    
    if not student:
        return {'error': 'Student not found'}
    
    # Check attempts
    attempts = AssessmentAttempt.objects.filter(
        assessment=assessment,
        student=student
    ).count()
    
    if attempts >= assessment.max_attempts:
        return {'error': 'Max attempts reached'}
    
    attempt = AssessmentAttempt.objects.create(
        assessment=assessment,
        student=student,
        attempt_number=attempts + 1,
        started_at=timezone.now()
    )
    
    return {'success': True, 'id': str(attempt.id)}


@router.post('/assessments/attempts/{id}/submit')
def submit_assessment(request, id: str, answers: dict):
    """Submit assessment."""
    from apps.student.additional import AssessmentAttempt
    
    attempt = get_object_or_404(AssessmentAttempt, id=id)
    attempt.answers = answers
    attempt.submitted_at = timezone.now()
    
    # Calculate score (simplified)
    from apps.student.additional import AssessmentQuestion
    questions = AssessmentQuestion.objects.filter(assessment=attempt.assessment)
    
    score = 0
    for q in questions:
        if answers.get(str(q.id)) == q.correct_answer:
            score += q.marks
    
    total = sum(q.marks for q in questions)
    attempt.score = (score / total * 100) if total > 0 else 0
    attempt.passed = attempt.score >= attempt.assessment.pass_mark
    attempt.save()
    
    return {'success': True, 'score': float(attempt.score), 'passed': attempt.passed}


@router.get('/assessments/attempts/{id}')
def get_attempt_result(request, id: str):
    """Get attempt result."""
    from apps.student.additional import AssessmentAttempt
    
    attempt = get_object_or_404(AssessmentAttempt, id=id)
    
    return {
        'id': str(attempt.id),
        'score': float(attempt.score),
        'passed': attempt.passed,
        'submitted': str(attempt.submitted_at)
    }


# === Convocation ===
@router.get('/convocation')
def list_convocations(request):
    """List convocation ceremonies."""
    from apps.student.additional import Convocation
    
    convocations = Convocation.objects.all().order_by('-year')
    
    return [
        {
            'id': str(c.id),
            'number': c.ceremony_number,
            'year': c.year,
            'type': c.convocation_type,
            'date': str(c.ceremony_date),
            'status': c.status
        }
        for c in convocations
    ]


@router.post('/convocation/{id}/register')
def register_convocation(request, id: str):
    """Register for convocation."""
    from apps.student.additional import Convocation, ConvocationGraduate
    from apps.student.models import StudentProfile
    
    convocation = get_object_or_404(Convocation, id=id)
    student = StudentProfile.objects.filter(user=request.user).first()
    
    if not student:
        return {'error': 'Student profile not found'}
    
    # Check clearance
    if not student.clearance_complete:
        return {'error': 'Clearance not complete'}
    
    graduate, _ = ConvocationGraduate.objects.get_or_create(
        convocation=convocation,
        student=student,
        defaults={
            'degree': student.current_level,
            'cgpa': student.cgpa
        }
    )
    
    return {'success': True, 'id': str(graduate.id)}


# === Documents ===
@router.get('/documents/templates')
def list_templates(request):
    """List document templates."""
    from apps.student.additional import DocumentTemplate
    
    templates = DocumentTemplate.objects.filter(is_active=True)
    
    return [
        {
            'id': str(t.id),
            'name': t.name,
            'type': t.document_type
        }
        for t in templates
    ]


@router.post('/documents/generate')
def generate_document(request, data: dict):
    """Generate document from template."""
    from apps.student.additional import DocumentTemplate, GeneratedDocument
    from apps.student.models import StudentProfile
    import uuid
    
    template = get_object_or_404(DocumentTemplate, id=data.get('template_id'))
    student = StudentProfile.objects.filter(user=request.user).first()
    
    if not student:
        return {'error': 'Student not found'}
    
    doc = GeneratedDocument.objects.create(
        template=template,
        student=student,
        content=template.template_content,
        verification_code=str(uuid.uuid4())
    )
    
    return {'success': True, 'id': str(doc.id), 'code': doc.verification_code}


@router.get('/documents/verify/{code}')
def verify_document(request, code: str):
    """Verify document."""
    from apps.student.additional import GeneratedDocument
    
    doc = GeneratedDocument.objects.filter(verification_code=code).first()
    
    if not doc:
        return {'valid': False}
    
    return {
        'valid': True,
        'template': doc.template.name,
        'student': doc.student.user.get_full_name() if doc.student and doc.student.user else None,
        'created': str(doc.created_at)
    }


# === Audit Log ===
@router.get('/audit')
def list_audit(request):
    """List audit log."""
    from apps.student.additional import AuditLog
    
    logs = AuditLog.objects.all().order_by('-created_at')[:100]
    
    return [
        {
            'id': str(l.id),
            'user': l.user.email if l.user else None,
            'action': l.action,
            'model': l.model_name,
            'created': str(l.created_at)
        }
        for l in logs
    ]