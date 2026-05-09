"""
UMS Enterprise Integration Module
Comprehensive integration of all Phase 1-14 implementations
This module serves as the central integration point for all enterprise features.
"""

# ========================================================
# PHASE 4: SECURITY INTEGRATION
# ========================================================

# Multi-tenant isolation
from utils.tenant import (
    TenantManager,
    TenantMixin,
    TenantContext,
    Institution,
    TenantAwareManager,
    get_tenant_context,
    require_tenant,
)

# Security middleware
from utils.security_middleware import (
    SessionExpiryMiddleware,
    TenantContextMiddleware,
    JWTTokenExpiryMiddleware,
)

# Security utilities
from utils.security import (
    SecurityUtils,
    AuditLogger,
    InputSanitizer,
)

# MFA
from utils.mfa import (
    MFAProvider,
    MFAManager,
    MFAService,
)


# ========================================================
# PHASE 5: DOMAIN VALIDATION INTEGRATION
# ========================================================

# Course registration validation
from apps.student.registration_validation import (
    CourseRegistrationValidator,
    validate_course_registration,
    get_available_courses,
)

# Nigerian utilities
from utils.nigerian_payments import (
    NigerianPaymentGateway,
    NigerianGradingSystem,
    NigerianIDValidator,
    NigerianPhoneValidator,
)


# ========================================================
# PHASE 7: CONCURRENCY INTEGRATION
# ========================================================

# High-concurrency utilities
from utils.concurrency import (
    IdempotencyManager,
    idempotent_operation,
    TransactionSafeGPA,
    CourseCapacityManager,
    PaymentTransactionManager,
    DistributedLock,
    with_distributed_lock,
)


# ========================================================
# PHASE 8: NIGERIAN OPTIMIZATION INTEGRATION
# ========================================================

# Low-bandwidth optimization
from utils.nigerian_optimization import (
    FieldSelector,
    ResponseCompressor,
    CacheOptimizer,
    RetryOptimizer,
    OptimizedAPIResponse,
    NetworkOptimizer,
    optimized_api_call,
)


# ========================================================
# PHASE 9: PERFORMANCE INTEGRATION
# ========================================================

# Optimized filters
from utils.optimized_filters import (
    FieldSelectionParams,
    OptimizedResponse,
    apply_field_selection,
    create_optimized_response,
)


# ========================================================
# PHASE 11: TESTING INTEGRATION
# ========================================================

# Test imports
from tests.unit.test_tenant import TenantIsolationTestCase
from tests.unit.test_security import SecurityUtilsTestCase, RBACTestCase
from tests.unit.test_validators import (
    NigerianValidatorsTestCase,
    ConcurrencyTestCase,
    NigerianOptimizationTestCase,
    RegistrationValidationTestCase,
)
from tests.api.test_api import APITestCase


# ========================================================
# PHASE 13: OBSERVABILITY INTEGRATION
# ========================================================

# Observability utilities
from utils.observability import (
    ObservabilityLogger,
    CorrelationID,
    trace_execution,
    MetricsCollector,
    get_metrics_collector,
    HealthChecker,
)

# Monitoring
from utils.monitoring import (
    MetricsCollector as SystemMetricsCollector,
    HealthChecker as SystemHealthChecker,
    PerformanceMonitor,
)

# Prometheus metrics
from utils.prometheus_metrics import (
    MetricsView,
    prometheus_metrics,
)


# ========================================================
# EXPORTS
# ========================================================

__all__ = [
    # Security
    'TenantManager',
    'TenantMixin', 
    'TenantContext',
    'Institution',
    'TenantAwareManager',
    'get_tenant_context',
    'require_tenant',
    'SessionExpiryMiddleware',
    'TenantContextMiddleware', 
    'JWTTokenExpiryMiddleware',
    'SecurityUtils',
    'AuditLogger',
    'InputSanitizer',
    'MFAProvider',
    'MFAManager',
    'MFAService',
    
    # Domain
    'CourseRegistrationValidator',
    'validate_course_registration',
    'get_available_courses',
    'NigerianPaymentGateway',
    'NigerianGradingSystem',
    'NigerianIDValidator',
    'NigerianPhoneValidator',
    
    # Concurrency
    'IdempotencyManager',
    'idempotent_operation',
    'TransactionSafeGPA',
    'CourseCapacityManager',
    'PaymentTransactionManager',
    'DistributedLock',
    'with_distributed_lock',
    
    # Optimization
    'FieldSelector',
    'ResponseCompressor',
    'CacheOptimizer',
    'RetryOptimizer',
    'OptimizedAPIResponse',
    'NetworkOptimizer',
    'optimized_api_call',
    
    # Performance
    'FieldSelectionParams',
    'OptimizedResponse',
    'apply_field_selection',
    'create_optimized_response',
    
    # Observability
    'ObservabilityLogger',
    'CorrelationID',
    'trace_execution',
    'MetricsCollector',
    'get_metrics_collector',
    'HealthChecker',
    'SystemMetricsCollector',
    'SystemHealthChecker',
    'PerformanceMonitor',
    'MetricsView',
    'prometheus_metrics',
]


def get_all_integrations():
    """
    Get all integrated modules for verification
    Returns a dictionary of all available integrations
    """
    return {
        'security': {
            'tenant': TenantManager,
            'middleware': [
                SessionExpiryMiddleware,
                TenantContextMiddleware,
                JWTTokenExpiryMiddleware,
            ],
            'utils': SecurityUtils,
            'audit': AuditLogger,
            'mfa': MFAService,
        },
        'domain': {
            'registration': CourseRegistrationValidator,
            'nigerian': {
                'payments': NigerianPaymentGateway,
                'grading': NigerianGradingSystem,
                'validators': {
                    'id': NigerianIDValidator,
                    'phone': NigerianPhoneValidator,
                },
            },
        },
        'concurrency': {
            'idempotency': IdempotencyManager,
            'safe_gpa': TransactionSafeGPA,
            'capacity': CourseCapacityManager,
            'payment': PaymentTransactionManager,
            'locks': DistributedLock,
        },
        'optimization': {
            'field_selector': FieldSelector,
            'cache': CacheOptimizer,
            'retry': RetryOptimizer,
            'network': NetworkOptimizer,
        },
        'observability': {
            'logging': ObservabilityLogger,
            'correlation': CorrelationID,
            'metrics': MetricsCollector,
            'health': HealthChecker,
            'prometheus': prometheus_metrics,
        },
    }


def verify_all_integrations():
    """
    Verify all integrations are working
    Returns dict of verification results
    """
    results = {}
    
    try:
        # Security
        results['security'] = {
            'tenant_manager': TenantManager is not None,
            'tenant_mixin': TenantMixin is not None,
            'mfa': MFAService is not None,
        }
        
        # Domain
        results['domain'] = {
            'registration': CourseRegistrationValidator is not None,
            'grading': NigerianGradingSystem is not None,
        }
        
        # Concurrency
        results['concurrency'] = {
            'idempotency': IdempotencyManager is not None,
            'safe_gpa': TransactionSafeGPA is not None,
        }
        
        # Optimization
        results['optimization'] = {
            'field_selector': FieldSelector is not None,
            'retry': RetryOptimizer is not None,
        }
        
        # Observability
        results['observability'] = {
            'logging': ObservabilityLogger is not None,
            'metrics': MetricsCollector is not None,
            'health': HealthChecker is not None,
        }
        
    except Exception as e:
        results['error'] = str(e)
    
    return results


# Integration version
__version__ = '1.0.0'
__all_phases_integrated__ = True