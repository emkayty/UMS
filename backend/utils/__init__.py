"""
UMS Backend Utilities Package
Enterprise-grade utilities for the University Management System
All modules are standardized and professionally organized.
"""

# Core Utilities Version
__version__ = "1.0.0"
__author__ = "UMS Engineering Team"
__status__ = "Production Ready"


# ========================================================
# EXPORTS - Public API
# ========================================================

# Security
from utils.tenant import TenantManager, TenantMixin, get_tenant_context
from utils.security import SecurityUtils, AuditLogger
from utils.security_middleware import SessionExpiryMiddleware
from utils.mfa import MFAService

# Domain
from apps.student.registration_validation import CourseRegistrationValidator
from utils.nigerian_payments import NigerianGradingSystem

# Concurrency
from utils.concurrency import IdempotencyManager, CourseCapacityManager

# Optimization
from utils.nigerian_optimization import FieldSelector, RetryOptimizer

# Performance
from utils.optimized_filters import apply_field_selection

# Observability
from utils.observability import HealthChecker, CorrelationID
from utils.monitoring import MetricsCollector

# Types
from utils.types import (
    SecurityConfig,
    TenantConfig,
    StudentProfile,
    CourseRegistration,
    GradeRecord,
    PaymentRequest,
)

# ML
from ml_service.drift_detector import ModelDriftDetector
from ml_service.tenant_isolation import TenantMLIsolationManager


# ========================================================
# VERSION INFO
# ========================================================

def get_version():
    return __version__


def get_system_info():
    return {
        "version": __version__,
        "status": __status__,
        "components": {
            "security": "TenantManager, MFA, AuditLogger",
            "domain": "CourseRegistration, GradingSystem",
            "concurrency": "IdempotencyManager, CourseCapacityManager",
            "optimization": "FieldSelector, RetryOptimizer",
            "observability": "HealthChecker, MetricsCollector",
            "ml": "ModelDriftDetector, TenantMLIsolation",
        },
    }


__all__ = [
    # Version
    "get_version",
    "get_system_info",
    
    # Security
    "TenantManager",
    "TenantMixin", 
    "get_tenant_context",
    "SecurityUtils",
    "AuditLogger",
    "SessionExpiryMiddleware",
    "MFAService",
    
    # Domain
    "CourseRegistrationValidator",
    "NigerianGradingSystem",
    
    # Concurrency
    "IdempotencyManager",
    "CourseCapacityManager",
    
    # Optimization
    "FieldSelector",
    "RetryOptimizer",
    
    # Performance
    "apply_field_selection",
    
    # Observability
    "HealthChecker",
    "CorrelationID",
    "MetricsCollector",
    
    # Types
    "SecurityConfig",
    "TenantConfig",
    "StudentProfile",
    "CourseRegistration",
    "GradeRecord",
    "PaymentRequest",
    
    # ML
    "ModelDriftDetector",
    "TenantMLIsolationManager",
]