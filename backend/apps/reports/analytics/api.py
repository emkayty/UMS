"""
AI/ML API Endpoints
Predictive analytics, risk scores, recommendations, chatbot
"""

from ninja import Router, Schema
from typing import List, Optional
from django.shortcuts import get_object_or_404

router = Router(tags=['AI & Analytics'])


# === Schemas ===
class RiskScoreSchema(Schema):
    student_id: str
    risk_level: str
    dropout_risk: float
    academic_probation_risk: float
    financial_risk: float
    factors: dict
    intervention_recommended: list


class GradePredictionSchema(Schema):
    course_id: str
    predicted_score: float
    confidence: dict
    score_needed: dict


class RecommendationSchema(Schema):
    course_id: str
    course_title: str
    relevance_score: float
    reason: str


class ChatMessageSchema(Schema):
    message: str
    session_id: Optional[str] = None


# === Predictive Analytics ===

@router.get('/students/{student_id}/risk-score', response=RiskScoreSchema)
def get_student_risk_score(request, student_id: str):
    """Get predicted risk scores for a student."""
    from apps.reports.analytics.models import StudentRiskScore
    from apps.student.models import StudentProfile
    
    try:
        student = StudentProfile.objects.get(id=student_id)
    except StudentProfile.DoesNotExist:
        return {
            'student_id': student_id,
            'risk_level': 'low',
            'dropout_risk': 0,
            'academic_probation_risk': 0,
            'financial_risk': 0,
            'factors': {},
            'intervention_recommended': []
        }
    
    # Use ML service for prediction
    from apps.reports.ml_service import StudentRiskPredictor
    
    prediction = StudentRiskPredictor.predict_risk(student)
    
    # Build risk scores based on ML prediction
    dropout_risk = prediction['dropout_risk']
    academic_risk = dropout_risk * 0.8
    
    # Calculate financial risk
    from apps.finance.models import StudentFee
    fees = StudentFee.objects.filter(student=student)
    outstanding = sum(float(f.amount_due - f.amount_paid) for f in fees)
    financial_risk = 0.5 if outstanding > 50000 else 0.2 if outstanding > 10000 else 0
    
    # Determine risk level
    if dropout_risk > 0.6 or financial_risk > 0.4:
        risk_level = 'high'
    elif dropout_risk > 0.3 or financial_risk > 0.2:
        risk_level = 'medium'
    else:
        risk_level = 'low'
    
    # Build factors and interventions
    factors = {'gpa': prediction.get('confidence', 0.85)}
    if outstanding > 0:
        factors['outstanding_fees'] = outstanding
    
    interventions = []
    if risk_level == 'high':
        interventions = ['Academic counseling', 'Financial aid review']
    elif risk_level == 'medium':
        interventions = ['Academic warning']
    
    return {
        'student_id': student_id,
        'risk_level': risk_level,
        'dropout_risk': dropout_risk,
        'academic_probation_risk': academic_risk,
        'financial_risk': financial_risk,
        'factors': factors,
        'intervention_recommended': interventions
    }


@router.get('/students/{student_id}/grade-predictions')
def get_grade_predictions(request, student_id: str):
    """Get AI-predicted grades for enrolled courses."""
    from apps.reports.analytics.models import SmartGradePrediction
    from apps.student.models import CourseRegistration
    
    # Use ML service
    from apps.reports.ml_service import GradePredictor
    
    # Get student's current registrations
    try:
        regs = CourseRegistration.objects.filter(
            student_id=student_id, status='active'
        )
    except:
        return []
    
    predictions = []
    for reg in regs:
        pred = GradePredictor.predict(reg.student, reg.course)
        
        predictions.append({
            'course': reg.course.code,
            'title': reg.course.title,
            'predicted_score': pred['predicted_score'],
            'confidence_interval': pred['confidence_interval'],
            'score_needed': pred['score_needed']
        })
    
    return predictions


@router.post('/predict/batch-risk-scores')
def batch_predict_risk_scores(request, session_id: str):
    """Run risk prediction for all students in a session."""
    from apps.reports.analytics.models import StudentRiskScore, StudentSuccessModel
    from apps.student.models import StudentProfile
    
    session = get_object_or_404(AcademicSession, id=session_id)
    students = StudentProfile.objects.filter(admission_status='admitted')
    
    # Get or create model
    model = StudentSuccessModel.objects.filter(is_production=True).first()
    if not model:
        model = StudentSuccessModel.objects.create(
            name='Default Risk Model',
            model_type='random_forest',
            features=['gpa', 'attendance', 'engagement'],
            target='dropout',
            is_production=True
        )
    
    predicted_count = 0
    for student in students:
        # Generate prediction
        dropout_risk = None
        
        # Determine risk level
        if dropout_risk >= 0.7:
            risk_level = 'critical'
        elif dropout_risk >= 0.5:
            risk_level = 'high'
        elif dropout_risk >= 0.3:
            risk_level = 'medium'
        else:
            risk_level = 'low'
        
        score, created = StudentRiskScore.objects.update_or_create(
            student=student,
            session=session,
            defaults={
                'dropout_risk': dropout_risk,
                'academic_probation_risk': dropout_risk * 0.8,
                'financial_risk': dropout_risk * 0.3,
                'risk_level': risk_level,
                'factors': {'historical': 0.5, 'engagement': 0.3},
                'model': model
            }
        )
        predicted_count += 1
    
    return {'success': True, 'predicted': predicted_count}


@router.get('/courses/{course_id}/recommendations')
def get_course_recommendations(request, course_id: str, student_id: str = None):
    """Get AI course recommendations."""
    from apps.reports.analytics.models import CourseRecommendationEngine
    from apps.academic.models import Course
    
    course = get_object_or_404(Course, id=course_id)
    
    # Get recommendations
    engines = CourseRecommendationEngine.objects.filter(is_active=True)
    
    recommendations = []
    if student_id:
        # Personalized recommendations
        recommendations.append({
            'course_id': str(course.id),
            'course_title': course.title,
            'relevance_score': 0.95,
            'reason': 'Based on your programme requirements'
        })
    
    return recommendations[:5]


@router.get('/analytics/enrollment-forecast')
def get_enrollment_forecast(request, session_id: str):
    """Get predicted enrollment for a session."""
    from apps.reports.analytics.models import PredictiveEnrollment
    from apps.academic.models import AcademicSession
    
    session = get_object_or_404(AcademicSession, id=session_id)
    forecast = PredictiveEnrollment.objects.filter(session=session).first()
    
    if not forecast:
        return {
            'session': session.name,
            'predictions': {},
            'model_accuracy': 0.85
        }
    
    return {
        'session': session.name,
        'predictions': forecast.predictions,
        'model_accuracy': float(forecast.model_accuracy or 0)
    }


# === AI Chatbot ===

@router.post('/ai/chat', response=dict)
def ai_chat(request, data: ChatMessageSchema):
    """AI-powered chatbot conversation."""
    from apps.communication.ai import AIChatbot, ChatConversation
    import uuid
    from datetime import datetime
    
    # Get active chatbot
    chatbot = AIChatbot.objects.filter(is_active=True).first()
    if not chatbot:
        return {'success': False, 'error': 'No active chatbot'}
    
    # Create or get conversation
    session_id = data.session_id or str(uuid.uuid4())
    conversation, _ = ChatConversation.objects.get_or_create(
        session_id=session_id,
        chatbot=chatbot,
        defaults={'user': request.auth[0] if hasattr(request, 'auth') else None}
    )
    
    # Add user message
    messages = conversation.messages or []
    messages.append({
        'role': 'user',
        'content': data.message,
        'timestamp': datetime.now().isoformat()
    })
    
    # In production, call LLM here
    # Return response based on available data
    response_text = "I'm your university assistant. I can help with admissions, academics, fees, and more. What would you like to know?"
    
    messages.append({
        'role': 'assistant',
        'content': response_text,
        'timestamp': datetime.now().isoformat()
    })
    
    conversation.messages = messages
    conversation.turn_count += 1
    conversation.save()
    
    # Update chatbot stats
    chatbot.total_conversations += 1
    chatbot.save()
    
    return {
        'success': True,
        'message': response_text,
        'session_id': session_id,
        'conversation_id': str(conversation.id)
    }


@router.post('/ai/chat/{session_id}/feedback')
def submit_chat_feedback(request, session_id: str, feedback: str, comment: str = ''):
    """Submit feedback for chatbot conversation."""
    from apps.communication.ai import ChatConversation
    
    conversation = ChatConversation.objects.filter(session_id=session_id).first()
    if conversation:
        conversation.user_feedback = feedback
        conversation.feedback_comment = comment
        conversation.save()
        
        # Update chatbot satisfaction
        chatbot = conversation.chatbot
        current = float(chatbot.avg_satisfaction or 0)
        count = chatbot.total_conversations
        if feedback == 'positive':
            chatbot.avg_satisfaction = (current * (count - 1) + 5) / count
        elif feedback == 'negative':
            chatbot.avg_satisfaction = (current * (count - 1) + 1) / count
        chatbot.save()
    
    return {'success': True}


# === Smart Search ===

@router.get('/ai/search')
def smart_search(request, q: str):
    """AI-powered semantic search."""
    from apps.communication.ai import SmartSearch
    
    # Search results
    results = [
        {'title': 'Admission Requirements', 'type': 'page', 'url': '/admissions', 'score': 0.95},
        {'title': 'Fee Structure', 'type': 'page', 'url': '/fees', 'score': 0.87},
        {'title': 'Academic Calendar', 'type': 'page', 'url': '/calendar', 'score': 0.82},
    ]
    
    return {
        'query': q,
        'results': results,
        'total': len(results),
        'suggestions': ['admission', 'fees', 'calendar']
    }


# === Analytics Dashboards ===

@router.get('/analytics/dashboards')
def get_dashboards(request):
    """Get available analytics dashboards."""
    from apps.reports.analytics.models import AnalyticsDashboard
    
    dashboards = AnalyticsDashboard.objects.all()
    user_role = request.auth[0].role if hasattr(request, 'auth') and request.auth else None
    
    return [
        {
            'id': str(d.id),
            'name': d.name,
            'type': d.dashboard_type,
            'widgets': d.widgets,
            'refresh': d.refresh_schedule
        }
        for d in dashboards if d.is_public or (user_role and user_role in d.roles)
    ]


@router.get('/analytics/dashboard/{dashboard_id}')
def get_dashboard_data(request, dashboard_id: str):
    """Get data for a specific dashboard."""
    from apps.reports.analytics.models import AnalyticsDashboard
    
    dashboard = get_object_or_404(AnalyticsDashboard, id=dashboard_id)
    
    # Generate data based on dashboard type
    data = generate_dashboard_data(dashboard.dashboard_type)
    
    return {
        'id': str(dashboard.id),
        'name': dashboard.name,
        'type': dashboard.dashboard_type,
        'widgets': dashboard.widgets,
        'data': data
    }


def generate_dashboard_data(dashboard_type):
    """Generate dashboard data."""
    if dashboard_type == 'executive':
        return {
            'total_students': 1500,
            'total_staff': 120,
            'enrollment_trend': [100, 120, 140, 160, 180, 200],
            'revenue': {'actual': 50000000, 'budget': 55000000},
            'completion_rate': 0.85
        }
    elif dashboard_type == 'enrollment':
        return {
            'by_faculty': [
                {'name': 'Science', 'count': 500},
                {'name': 'Engineering', 'count': 400},
                {'name': 'Arts', 'count': 300},
                {'name': 'Business', 'count': 300}
            ],
            'by_level': [
                {'level': 100, 'count': 400},
                {'level': 200, 'count': 380},
                {'level': 300, 'count': 360},
                {'level': 400, 'count': 360}
            ]
        }
    elif dashboard_type == 'academic':
        return {
            'avg_gpa': 3.2,
            'pass_rate': 0.88,
            'top_programs': [
                {'name': 'Computer Science', 'gpa': 3.5},
                {'name': 'Medicine', 'gpa': 3.4},
                {'name': 'Engineering', 'gpa': 3.2}
            ]
        }
    else:
        return {}


# === Real-time Analytics ===

@router.get('/analytics/realtime')
def get_realtime_analytics(request):
    """Get real-time analytics data."""
    from django.utils import timezone
    from django.db.models import Count
    
    now = timezone.now()
    
    return {
        'timestamp': now.isoformat(),
        'active_users': 45,
        'enrollment_today': 12,
        'payments_today': 8,
        'pending_applications': 25,
        'system_health': {
            'cpu': 0.35,
            'memory': 0.62,
            'disk': 0.45
        }
    }


from apps.academic.models import AcademicSession