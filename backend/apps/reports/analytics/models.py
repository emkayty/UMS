"""
AI/ML Analytics & Predictive Features
Student success prediction, at-risk detection, recommendation engines
"""

from django.db import models
import uuid


class StudentSuccessModel(models.Model):
    """ML model for student success prediction."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    MODEL_TYPES = [
        ('logistic_regression', 'Logistic Regression'),
        ('random_forest', 'Random Forest'),
        ('gradient_boosting', 'Gradient Boosting'),
        ('neural_network', 'Neural Network'),
    ]
    
    model_type = models.CharField(max_length=30, choices=MODEL_TYPES, default='random_forest')
    features = models.JSONField(default=list)
    
    TARGETS = [
        ('graduation', 'Graduation'),
        ('good_standing', 'Good Academic Standing'),
        ('dropout', 'Dropout Risk'),
        ('first_class', 'First Class'),
    ]
    
    target = models.CharField(max_length=30, choices=TARGETS)
    
    accuracy = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    precision = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    recall = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    f1_score = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    
    training_samples = models.IntegerField(default=0)
    is_production = models.BooleanField(default=False)
    last_trained = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class StudentRiskScore(models.Model):
    """Predicted risk scores for students."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey('student.StudentProfile', on_delete=models.CASCADE, related_name='risk_scores')
    session = models.ForeignKey('academic.AcademicSession', on_delete=models.CASCADE)
    
    dropout_risk = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    academic_probation_risk = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    financial_risk = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    
    factors = models.JSONField(default=dict)
    
    RISK_LEVELS = [('low', 'Low Risk'), ('medium', 'Medium Risk'), ('high', 'High Risk'), ('critical', 'Critical')]
    risk_level = models.CharField(max_length=20, choices=RISK_LEVELS, default='low')
    
    intervention_recommended = models.JSONField(default=list)
    model = models.ForeignKey(StudentSuccessModel, on_delete=models.SET_NULL, null=True, blank=True)
    predicted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'session']


class CourseRecommendationEngine(models.Model):
    """AI course recommendation system."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=100)
    RECOMMENDATION_TYPES = [
        ('prerequisite', 'Prerequisite-chain'),
        ('career_path', 'Career Path'),
        ('similar_students', 'Similar Students'),
    ]
    
    recommendation_type = models.CharField(max_length=30, choices=RECOMMENDATION_TYPES)
    weight_features = models.JSONField(default=dict)
    top_n = models.IntegerField(default=5)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class PredictiveEnrollment(models.Model):
    """Enrollment forecasting."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    session = models.ForeignKey('academic.AcademicSession', on_delete=models.CASCADE)
    predictions = models.JSONField(default=dict)
    model_accuracy = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    predicted_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['session']


class SmartGradePrediction(models.Model):
    """AI-predicted final grade."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey('student.StudentProfile', on_delete=models.CASCADE)
    course = models.ForeignKey('academic.Course', on_delete=models.CASCADE)
    session = models.ForeignKey('academic.AcademicSession', on_delete=models.CASCADE)
    
    predicted_score = models.DecimalField(max_digits=5, decimal_places=2)
    confidence_interval = models.JSONField(default=dict)
    score_needed_for_grade = models.JSONField(default=dict)
    
    actual_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    predicted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'course', 'session']


class GraduateOutcomePrediction(models.Model):
    """Predicted career outcomes."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey('student.StudentProfile', on_delete=models.CASCADE, related_name='outcome_predictions')
    predicted_jobs = models.JSONField(default=list)
    predicted_salary_range = models.JSONField(default=dict)
    required_skills = models.JSONField(default=list)
    current_skills = models.JSONField(default=list)
    predicted_at = models.DateTimeField(auto_now_add=True)


class AnalyticsDashboard(models.Model):
    """Pre-built analytics dashboards."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    DASHBOARD_TYPES = [
        ('executive', 'Executive Summary'),
        ('enrollment', 'Enrollment Analytics'),
        ('academic', 'Academic Performance'),
        ('financial', 'Financial Analytics'),
        ('predictive', 'Predictive Analytics'),
    ]
    
    dashboard_type = models.CharField(max_length=30, choices=DASHBOARD_TYPES)
    widgets = models.JSONField(default=list)
    roles = models.JSONField(default=list)
    refresh_schedule = models.CharField(max_length=20, default='daily')
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)