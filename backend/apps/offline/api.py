from ninja import Router
from datetime import datetime

router = Router(tags=['Offline Sync'])


# === Offline Attendance Sync ===
@router.post('/offline/attendance-batch')
def sync_attendance_batch(request, data: dict):
    """Sync attendance records from offline."""
    records = data.get('records', [])
    synced = 0
    conflicts = []
    
    for record in records:
        session_id = record.get('attendance_session_id')
        student_id = record.get('student_id')
        timestamp = record.get('timestamp')
        
        # Check for existing record
        from apps.learning.models import AttendanceRecord, AttendanceSession
        
        session = AttendanceSession.objects.filter(id=session_id).first()
        if not session:
            conflicts.append({
                'session_id': session_id,
                'error': 'Session not found'
            })
            continue
        
        # Validate timestamp against session date
        try:
            record_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except ValueError:
            record_time = datetime.now()
        
        # Check if late (more than 30 mins after start time)
        is_late = (record_time - datetime.combine(session.date, datetime.min.time())).seconds > 1800
        
        # Create/update record
        from apps.student.models import StudentProfile
        
        student = StudentProfile.objects.filter(id=student_id).first()
        if not student:
            conflicts.append({
                'student_id': student_id,
                'error': 'Student not found'
            })
            continue
        
        # Check for duplicates
        existing = AttendanceRecord.objects.filter(
            session=session, student=student
        ).first()
        
        if existing:
            conflicts.append({
                'student_id': student_id,
                'session_id': session_id,
                'error': 'Already recorded'
            })
            continue
        
        AttendanceRecord.objects.create(
            session=session,
            student=student,
            timestamp=record_time,
            method='qr',
            is_valid=not is_late
        )
        synced += 1
    
    return {
        'success': True,
        'synced': synced,
        'conflicts': conflicts
    }


# === Offline Assignment Sync ===
@router.post('/offline/assignment-submit')
def sync_assignment_submit(request, data: dict):
    """Sync assignment submission from offline."""
    assignment_id = data.get('assignment_id')
    student_id = data.get('student_id')
    text_answer = data.get('text_answer', '')
    
    from apps.learning.models import AssignmentSubmission, Assignment
    from apps.student.models import StudentProfile
    
    assignment = Assignment.objects.filter(id=assignment_id).first()
    if not assignment:
        return {'success': False, 'error': 'Assignment not found'}
    
    student = StudentProfile.objects.filter(id=student_id).first()
    if not student:
        return {'success': False, 'error': 'Student not found'}
    
    submission, created = AssignmentSubmission.objects.get_or_create(
        assignment=assignment,
        student=student,
        defaults={
            'text_answer': text_answer,
            'submitted_at': datetime.now(),
            'status': 'submitted'
        }
    )
    
    if not created:
        submission.text_answer = text_answer
        submission.submitted_at = datetime.now()
        submission.status = 'submitted'
        submission.save()
    
    # Check if late
    if assignment.due_date < datetime.now():
        submission.status = 'late'
        submission.save()
    
    return {
        'success': True,
        'submission_id': str(submission.id),
        'status': submission.status
    }


# === Sync Status ===
@router.get('/offline/sync-status')
def get_sync_status(request):
    """Get last sync time for user."""
    # In production, store last sync time per user
    return {
        'last_sync': datetime.now().isoformat(),
        'pending': 0
    }


# === Queue Status ===
@router.get('/offline/queue-status')
def get_queue_status(request):
    """Check pending offline operations."""
    # In production, count pending items in queue
    return {
        'pending_count': 0,
        'last_error': None
    }


# === Batch Results Sync ===
@router.post('/offline/results-batch')
def sync_results_batch(request, data: dict):
    """Sync quiz results from offline."""
    results = data.get('results', [])
    synced = 0
    
    for result in results:
        quiz_id = result.get('quiz_id')
        student_id = result.get('student_id')
        answers = result.get('answers', {})
        
        from apps.learning.models import QuizAttempt, Quiz
        from apps.student.models import StudentProfile
        
        quiz = Quiz.objects.filter(id=quiz_id).first()
        if not quiz:
            continue
        
        student = StudentProfile.objects.filter(id=student_id).first()
        if not student:
            continue
        
        attempt, created = QuizAttempt.objects.get_or_create(
            quiz=quiz,
            student=student,
            defaults={
                'answers': answers,
                'submitted_at': datetime.now()
            }
        )
        
        if created:
            # Auto-grade
            correct = 0
            total = len(quiz.questions)
            
            for i, question in enumerate(quiz.questions):
                if answers.get(str(i)) == question.get('correct_answer'):
                    correct += 1
            
            if total > 0:
                attempt.score_total = (correct / total) * 100
                attempt.is_passed = float(attempt.score_total) >= 50
            attempt.save()
            synced += 1
    
    return {'success': True, 'synced': synced}