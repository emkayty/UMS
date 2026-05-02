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
    
    # Model configuration
    MODEL_TYPES = [
        ('logistic_regression', 'Logistic Regression'),
        ('random_forest', 'Random Forest'),
        ('gradient_boosting', 'Gradient Boosting'),
        ('neural_network', 'Neural Network'),
        ('ensemble', 'Ensemble'),
    ]
    
    model_type = models.CharField(max_length=30, choices=MODEL_TYPES, default='random_forest')
    
    # Feature configuration
    features = models.JSONField(default=list)
    # Features used: ['gpa', 'attendance', 'assignment_score', 'engagement', 'demographics']
    
    # Target
    TARGETS = [
        ('graduation', 'Graduation'),
        ('good_standing', 'Good Academic Standing'),
        ('dropout', 'Dropout Risk'),
        ('first_class', 'First Class'),
    ]
    
    target = models.CharField(max_length=30, choices=TARGETS)
    
    # Performance
    accuracy = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    precision = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    recall = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    f1_score = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    auc_roc = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    
    # Training data
    training_start_date = models.DateField()
    training_end_date = models.DateField()
    training_samples = models.IntegerField(default=0)
    
    # Model persistence
    model_file = models.CharField(max_length=200, blank=True)
    is_production = models.BooleanField(default=False)
    
    last_trained = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class StudentRiskScore(models.Model):
    """Predicted risk scores for students."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey(
        'student.StudentProfile', on_delete=models.CASCADE,
        related_name='risk_scores'
    )
    
    session = models.ForeignKey(
        'academic.AcademicSession', on_delete=models.CASCADE
    )
    
    # Risk categories
    dropout_risk = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    academic_probation_risk = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    financial_risk = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    completion_risk = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    
    # Contributing factors
    factors = models.JSONField(default=dict)
    # {'low_gpa': 0.7, 'low_attendance': 0.5, 'payment_issues': 0.3}
    
    # Risk level
    RISK_LEVELS = [
        ('low', 'Low Risk'),
        ('medium', 'Medium Risk'),
        ('high', 'High Risk'),
        ('critical', 'Critical'),
    ]
    
    risk_level = models.CharField(max_length=20, choices=RISK_LEVELS, default='low')
    
    # Early warning
    early_warning_sent = models.BooleanField(default=False)
    intervention_recommended = models.JSONField(default=list)
    
    model = models.ForeignKey(
        StudentSuccessModel, on_delete=models.SET_NULL,
        null=True, blank=True
    )
    
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
        ('skill_gap', 'Skill Gap'),
        ('difficulty', 'Difficulty Level'),
        ('engagement', 'Engagement-based'),
    ]
    
    recommendation_type = models.CharField(max_length=30, choices=RECOMMENDATION_TYPES)
    
    # Configuration
    weight_features = models.JSONField(default=dict)
    # {'gpa': 0.3, 'interest': 0.2, 'career': 0.2, 'prereq': 0.3}
    
    # Number of recommendations
    top_n = models.IntegerField(default=5)
    
    min_similarity_score = models.DecimalField(
        max_digits=4, decimal_places=2, default=0.5
    )
    
    is_active = models.BooleanField(default=True)
    
    # Feedback tracking
    click_through_rate = models.DecimalField(
        max_digits=4, decimal_places=2, default=0
    )
    conversion_rate = models.DecimalField(
        max_digits=4, decimal_places=2, default=0
    )
    
    created_at = models.DateTimeField(auto_now_add=True)


class PersonalizedLearningPath(models.Model):
    """AI-generated personalized learning paths."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey(
        'student.StudentProfile', on_delete=models.CASCADE,
        related_name='learning_paths'
    )
    
    course = models.ForeignKey(
        'academic.Course', on_delete=models.CASCADE
    )
    
    # Learning path details
    topics = models.JSONField(default=list)
    # [{topic: 'Introduction', order: 1, estimated_time: 60, mastered: true}]
    
    current_position = models.IntegerField(default=0)
    completion_percentage = models.DecimalField(
        max_digits=4, decimal_places=2, default=0
    )
    
    # Adaptive difficulty
    difficulty_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
        ],
        default='intermediate'
    )
    
    # Performance-based adjustments
    mastered_topics = models.JSONField(default=list)
    weak_topics = models.JSONField(default=list)
    recommended_resources = models.JSONField(default=list)
    
    estimated_completion_hours = models.IntegerField(default=0)
    actual_completion_hours = models.IntegerField(default=0)
    
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class PredictiveEnrollment(models.Model):
    """Enrollment forecasting."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    session = models.ForeignKey(
        'academic.AcademicSession', on_delete=models.CASCADE
    )
    
    # Predictions by programme
    predictions = models.JSONField(default=dict)
    # {programme_id: {predicted: 150, confidence: 0.85, range: [130, 170]}}
    
    # Model performance
    model_accuracy = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True
    )
    
    # Actual vs predicted
    actual_enrollment = models.IntegerField(null=True, blank=True)
    variance = models.IntegerField(default=0)
    
    predicted_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['session']


class GraduateOutcomePrediction(models.Model):
    """Predicted career outcomes for students."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey(
        'student.StudentProfile', on_delete=models.CASCADE,
        related_name='outcome_predictions'
    )
    
    # Predicted outcomes
    predicted_jobs = models.JSONField(default=list)
    # [{job_title: 'Software Engineer', probability: 0.7, sector: 'Tech'}]
    
    # Salary prediction
    predicted_salary_range = models.JSONField(default=dict)
    # {min: 150000, max: 250000, currency: 'NGN'}
    
    # Skills gap analysis
    required_skills = models.JSONField(default=list)
    current_skills = models.JSONField(default=list)
    gap_analysis = models.JSONField(default=list)
    
    # Further education recommendations
    recommended_programs = models.JSONField(default=list)
    
    model = models.ForeignKey(
        StudentSuccessModel, on_delete=models.SET_NULL,
        null=True, blank=True
    )
    
    predicted_at = models.DateTimeField(auto_now=True)


class SmartGradePrediction(models.Model):
    """AI-predicted final grade based on current performance."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey(
        'student.StudentProfile', on_delete=models.CASCADE
    )
    course = models.ForeignKey(
        'academic.Course', on_delete=models.CASCADE
    )
    session = models.ForeignKey(
        'academic.AcademicSession', on_delete=models.CASCADE
    )
    
    # Input features
    current_ca_scores = models.JSONField(default=list)
    current_exam_scores = models.JSONField(default=list)
    attendance_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    assignment_completion = models.DecimalField(max_digits=5, decimal_places=2)
    
    # Prediction
    predicted_score = models.DecimalField(max_digits=5, decimal_places=2)
    confidence_interval = models.JSONField(default=dict)
    # {lower: 65, upper: 75, confidence: 0.90}
    
    # What-if analysis
    score_needed_for_grade = models.JSONField(default=dict)
    # {A: 85, B: 75, C: 65}
    
    actual_score = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    prediction_error = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    
    predicted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'course', 'session']


class DataWarehouse(models.Model):
    """Data warehouse for analytics."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    # Data tables
    tables = models.JSONField(default=list)
    # ['fact_enrollment', 'dim_student', 'dim_course', 'fact_grade']
    
    # Last sync
    last_ETL_date = models.DateTimeField(null=True, blank=True)
    row_count = models.IntegerField(default=0)
    
    # Connection
    warehouse_type = models.CharField(
        max_length=20,
        choices=[
            ('snowflake', 'Snowflake'),
            ('bigquery', 'BigQuery'),
            ('redshift', 'Redshift'),
            ('local', 'Local PostgreSQL'),
        ]
    )
    connection_string = models.CharField(max_length=500, blank=True)
    
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)


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
        ('hr', 'Human Resources'),
        ('predictive', 'Predictive Analytics'),
        ('nuc', 'NUC Accreditation'),
    ]
    
    dashboard_type = models.CharField(max_length=30, choices=DASHBOARD_TYPES)
    
    # Widgets
    widgets = models.JSONField(default=list)
    # [{type: 'line_chart', title: 'Enrollment Trend', data: 'fact_enrollment'}]
    
    # Access
    roles = models.JSONField(default=list)
    # ['institution_admin', 'dean', 'registrar']
    
    # Refresh schedule
    REFRESH_OPTIONS = [
        ('realtime', 'Real-time'),
        ('hourly', 'Hourly'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
    ]
    
    refresh_schedule = models.CharField(max_length=20, choices=REFRESH_OPTIONS, default='daily')
    
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)