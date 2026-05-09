"""
Type hints definitions for UMS
Comprehensive type definitions for all utility functions
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel


# ========================================================
# SECURITY TYPES
# ========================================================

class SecurityConfig(BaseModel):
    """Security configuration"""
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    session_timeout_minutes: int = 60
    max_login_attempts: int = 5
    lockout_duration_minutes: int = 15


class AuditEvent(BaseModel):
    """Audit event for security logging"""
    event_type: str
    user_id: str
    timestamp: str
    ip_address: Optional[str] = None
    resource: Optional[str] = None
    action: Optional[str] = None


# ========================================================
# TENANT TYPES
# ========================================================

class TenantConfig(BaseModel):
    """Tenant configuration"""
    tenant_id: str
    institution_name: str
    domain: str
    features: Dict[str, bool]
    limits: Dict[str, int]


class TenantMetrics(BaseModel):
    """Tenant usage metrics"""
    tenant_id: str
    total_users: int = 0
    total_requests: int = 0
    total_storage_mb: float = 0.0
    api_calls_remaining: int = 0


# ========================================================
# STUDENT TYPES
# ========================================================

class StudentProfile(BaseModel):
    """Student profile data"""
    student_id: str
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    mat_number: Optional[str] = None
    department: str
    level: int


class CourseRegistration(BaseModel):
    """Course registration"""
    registration_id: str
    student_id: str
    course_id: str
    semester: str
    session: str
    status: str = "pending"


class GradeRecord(BaseModel):
    """Grade record"""
    student_id: str
    course_id: str
    score: float
    grade: str
    gpa: float
    year: int
    semester: str


# ========================================================
# PAYMENT TYPES  
# ========================================================

class PaymentRequest(BaseModel):
    """Payment request"""
    amount: float
    payment_type: str
    student_id: str
    description: Optional[str] = None


class PaymentConfirmation(BaseModel):
    """Payment confirmation"""
    transaction_id: str
    status: str
    amount: float
    timestamp: str
    channel: str


# ========================================================
# CONCURRENCY TYPES
# ========================================================

class IdempotencyRecord(BaseModel):
    """Idempotency record"""
    key: str
    operation: str
    status: str
    result: Optional[Dict[str, Any]] = None
    created_at: str
    completed_at: Optional[str] = None


class TransactionResult(BaseModel):
    """Transaction result"""
    success: bool
    transaction_id: Optional[str] = None
    message: str
    data: Optional[Dict[str, Any]] = None


# ========================================================
# OPTIMIZATION TYPES
# ========================================================

class FieldSelectionRequest(BaseModel):
    """Request for field selection"""
    fields: Optional[str] = None
    limit: int = 20
    offset: int = 0


class OptimizedResponse(BaseModel):
    """Optimized API response"""
    data: List[Dict[str, Any]]
    meta: Dict[str, Any]


# ========================================================
# OBSERVABILITY TYPES
# ========================================================

class HealthStatus(BaseModel):
    """Health status"""
    status: str
    checks: Dict[str, str]
    timestamp: str


class MetricsRequest(BaseModel):
    """Metrics request"""
    metric_names: List[str]
    time_range_minutes: int = 60


# ========================================================
# COURSE TYPES
# ========================================================

class Course(BaseModel):
    """Course data"""
    course_id: str
    code: str
    title: str
    department: str
    units: int
    level: int
    semester: str


class CoursePrerequisite(BaseModel):
    """Course prerequisite"""
    course_id: str
    prerequisite_id: str
    is_mandatory: bool = False


# ========================================================
# TYPE EXPORTS
# ========================================================

__all__ = [
    'SecurityConfig',
    'AuditEvent', 
    'TenantConfig',
    'TenantMetrics',
    'StudentProfile',
    'CourseRegistration',
    'GradeRecord',
    'PaymentRequest',
    'PaymentConfirmation',
    'IdempotencyRecord',
    'TransactionResult',
    'FieldSelectionRequest',
    'OptimizedResponse',
    'HealthStatus',
    'MetricsRequest',
    'Course',
    'CoursePrerequisite',
]