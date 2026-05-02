"""
LLM Integration & AI Services
Chatbot, document processing, smart search, automation
"""

from django.db import models


class AIChatbot(models.Model):
    """AI-powered student assistant."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=100, default='UniCore Assistant')
    llm_provider = models.CharField(
        max_length=30,
        choices=[
            ('openai', 'OpenAI'),
            ('anthropic', 'Anthropic Claude'),
            ('google', 'Google Gemini'),
            ('local', 'Local Model'),
        ],
        default='openai'
    )
    model_name = models.CharField(max_length=50, default='gpt-4')
    api_key = models.CharField(max_length=200, blank=True)
    
    system_prompt = models.TextField(default="You are a helpful university assistant.")
    can_answer_admission = models.BooleanField(default=True)
    can_answer_academic = models.BooleanField(default=True)
    can_answer_financial = models.BooleanField(default=True)
    can_escalate = models.BooleanField(default=True)
    
    max_tokens = models.IntegerField(default=1000)
    temperature = models.DecimalField(max_digits=2, decimal_places=1, default=0.7)
    
    allowed_roles = models.JSONField(default=['student', 'lecturer'])
    is_active = models.BooleanField(default=True)
    total_conversations = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ChatConversation(models.Model):
    """Chat conversation tracking."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    chatbot = models.ForeignKey(AIChatbot, on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True)
    session_id = models.CharField(max_length=100)
    messages = models.JSONField(default=list)
    turn_count = models.IntegerField(default=0)
    
    RESOLUTION_STATUS = [
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
        ('escalated', 'Escalated'),
    ]
    resolution_status = models.CharField(max_length=20, choices=RESOLUTION_STATUS, default='pending')
    escalated_to = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='+')
    
    user_feedback = models.CharField(max_length=20, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)


class DocumentAIProcessor(models.Model):
    """AI document processing."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=100)
    DOCUMENT_TYPES = [
        ('transcript', 'Transcript'),
        ('certificate', 'Certificate'),
        ('id_card', 'ID Card'),
        ('application', 'Application Form'),
    ]
    
    document_type = models.CharField(max_length=30, choices=DOCUMENT_TYPES)
    ocr_model = models.CharField(max_length=50, default='tesseract')
    extraction_fields = models.JSONField(default=list)
    
    auto_validate = models.BooleanField(default=True)
    accuracy_rate = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    processed_count = models.IntegerField(default=0)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class SmartSearch(models.Model):
    """AI-powered semantic search."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=100)
    SEARCH_TARGETS = [
        ('courses', 'Courses'),
        ('programmes', 'Programmes'),
        ('handbook', 'Student Handbook'),
    ]
    
    search_targets = models.JSONField(default=list)
    embedding_model = models.CharField(max_length=50, default='text-embedding')
    similarity_threshold = models.DecimalField(max_digits=3, decimal_places=2, default=0.7)
    
    enable_spell_check = models.BooleanField(default=True)
    enable_autocomplete = models.BooleanField(default=True)
    max_results = models.IntegerField(default=10)
    
    search_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class IntelligentAutomation(models.Model):
    """AI automation workflows."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    TRIGGER_TYPES = [
        ('enrollment', 'Enrollment Milestone'),
        ('attendance', 'Low Attendance Alert'),
        ('grade', 'Low Grade Alert'),
        ('payment', 'Payment Default'),
    ]
    
    trigger = models.CharField(max_length=30, choices=TRIGGER_TYPES)
    
    ACTIONS = [
        ('notify', 'Send Notification'),
        ('email', 'Send Email'),
        ('alert', 'Alert Admin'),
        ('hold', 'Place Hold'),
    ]
    
    actions = models.JSONField(default=list)
    conditions = models.JSONField(default=dict)
    
    is_active = models.BooleanField(default=True)
    last_triggered = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class AnomalyDetection(models.Model):
    """Anomaly detection for academic fraud."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=100)
    ANOMALY_TYPES = [
        ('enrollment_spike', 'Enrollment Spike'),
        ('grade_inflation', 'Grade Inflation'),
        ('attendance_anomaly', 'Attendance Anomaly'),
    ]
    
    anomaly_type = models.CharField(max_length=30, choices=ANOMALY_TYPES)
    algorithm = models.CharField(max_length=30, choices=[
        ('z_score', 'Z-Score'),
        ('isolation_forest', 'Isolation Forest'),
    ])
    
    sensitivity = models.DecimalField(max_digits=3, decimal_places=2, default=0.05)
    detected_count = models.IntegerField(default=0)
    alert_admins = models.JSONField(default=list)
    
    is_active = models.BooleanField(default=True)
    last_run = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)