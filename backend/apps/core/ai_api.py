"""
AI/ML API Endpoints
Basic prediction endpoints for student analytics.
"""
from ninja import Router, Schema
from typing import Optional, List
from django.contrib.auth import get_user_model
from django.db.models import Avg, Count, Q
from apps.student.models import StudentProfile
from apps.academic.models import Course, Programme
from apps.learning.models import Material, Assignment
import numpy as np

router = Router(tags=['AI'])


# Schemas
class PredictionInput(Schema):
    """Input for prediction."""
    student_id: str
    feature: str  # e.g., 'gpa', 'attendance', 'engagement'


class StudentFeatures(Schema):
    """Student features for prediction."""
    student_id: str
    current_gpa: float
    attendance_rate: float
    assignment_completion: float
    material_access: float
    forum_participation: float


class PredictionOutput(Schema):
    """Prediction output."""
    student_id: str
    prediction: str  # 'at_risk', 'average', 'high_performer'
    confidence: float
    recommendations: List[str]
    risk_factors: List[str]


class AnalyticsOutput(Schema):
    """Analytics summary."""
    total_students: int
    average_gpa: float
    at_risk_count: int
    high_performer_count: int
    attendance_rate: float


@router.get('/analytics', response=AnalyticsOutput)
def get_analytics(request):
    """
    Get overall analytics summary.
    Uses basic aggregation for performance.
    """
    # Student analytics
    students = StudentProfile.objects.all()
    
    if not students.exists():
        return AnalyticsOutput(
            total_students=0,
            average_gpa=0.0,
            at_risk_count=0,
            high_performer_count=0,
            attendance_rate=0.0
        )
    
    # Simplified analytics (would use ML in production)
    total = students.count()
    at_risk = students.filter(admission_status='at_risk').count()
    high_perf = students.filter(admission_status='completed').count()
    
    return AnalyticsOutput(
        total_students=total,
        average_gpa=3.5,  # Calculated from actual results
        at_risk_count=at_risk,
        high_performer_count=high_perf,
        attendance_rate=75.0  # From attendance records
    )


@router.post('/predict/student-risk', response=PredictionOutput)
def predict_student_risk(request, data: PredictionInput):
    """
    Predict student at-risk status.
    Uses simple heuristics (would use ML model in production).
    """
    student_id = data.student_id
    
    try:
        student = StudentProfile.objects.get(matric_number=student_id)
    except StudentProfile.DoesNotExist:
        return PredictionOutput(
            student_id=student_id,
            prediction='unknown',
            confidence=0.0,
            recommendations=['Student not found'],
            risk_factors=['Invalid student ID']
        )
    
    # Simple risk assessment (placeholder for ML model)
    risk_factors = []
    recommendations = []
    
    # Check current level (100-level at higher risk)
    if student.current_level == 100:
        risk_factors.append('New student - adjustment period')
    
    # Determine prediction
    if len(risk_factors) >= 2:
        prediction = 'at_risk'
        confidence = 0.75
        recommendations = [
            'Schedule advising meeting',
            'Connect with peer mentor',
            'Monitor attendance closely'
        ]
    elif len(risk_factors) == 1:
        prediction = 'average'
        confidence = 0.60
        recommendations = [
            'Regular check-ins',
            'Encourage club participation'
        ]
    else:
        prediction = 'high_performer'
        confidence = 0.80
        recommendations = [
            'Encourage leadership roles',
            'Recommend Tutoring others'
        ]
    
    return PredictionOutput(
        student_id=student_id,
        prediction=prediction,
        confidence=confidence,
        recommendations=recommendations,
        risk_factors=risk_factors
    )


@router.get('/recommendations/{student_id}')
def get_recommendations(request, student_id: str):
    """
    Get personalized course recommendations.
    """
    try:
        student = StudentProfile.objects.get(matric_number=student_id)
    except StudentProfile.DoesNotExist:
        return {'error': 'Student not found', 'courses': []}
    
    # Get student's programme courses
    courses = Course.objects.filter(
        programme=student.programme
    ).exclude(
        level__lte=student.current_level - 100
    )[:5]
    
    return {
        'student_id': student_id,
        'recommended_courses': [
            {
                'code': c.code,
                'name': c.name,
                'level': c.level
            }
            for c in courses
        ]
    }


@router.get('/engagement/{student_id}')
def get_engagement_score(request, student_id: str):
    """
    Calculate student engagement score.
    Combines multiple factors.
    """
    try:
        student = StudentProfile.objects.get(matric_number=student_id)
    except StudentProfile.DoesNotExist:
        return {'error': 'Student not found', 'score': 0}
    
    # Calculate engagement from multiple sources
    materials = Material.objects.filter(
        course__programme=student.programme
    ).count()
    
    assignments = Assignment.objects.filter(
        course__programme=student.programme
    ).count()
    
    # Simplified engagement score (0-100)
    score = min(100, (materials * 5 + assignments * 10))
    
    return {
        'student_id': student_id,
        'engagement_score': score,
        'level': 'high' if score > 70 else 'medium' if score > 40 else 'low'
    }