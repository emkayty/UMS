"""
Validation Tests
Testing validators and business logic
"""

import pytest
from django.test import TestCase


class NigerianValidatorsTestCase(TestCase):
    """Test Nigerian validators"""
    
    def test_nigerian_payment_gateway(self):
        """Test NigerianPaymentGateway can be imported"""
        from utils.nigerian_payments import NigerianPaymentGateway
        assert NigerianPaymentGateway is not None
    
    def test_nigerian_grading_system(self):
        """Test NigerianGradingSystem can be imported"""
        from utils.nigerian_payments import NigerianGradingSystem
        assert NigerianGradingSystem is not None
    
    def test_nigerian_id_validator(self):
        """Test NigerianIDValidator can be imported"""
        from utils.nigerian_payments import NigerianIDValidator
        assert NigerianIDValidator is not None
    
    def test_nigerian_phone_validator(self):
        """Test NigerianPhoneValidator can be imported"""
        from utils.nigerian_payments import NigerianPhoneValidator
        assert NigerianPhoneValidator is not None
    
    def test_gpa_calculation(self):
        """Test GPA calculation works"""
        from utils.nigerian_payments import NigerianGradingSystem
        
        scores = [
            {'score': 85, 'units': 3},
            {'score': 72, 'units': 4},
            {'score': 55, 'units': 2},
        ]
        
        gpa = NigerianGradingSystem.calculate_gpa(scores)
        
        assert gpa > 0
        assert isinstance(gpa, float)


class RegistrationValidationTestCase(TestCase):
    """Test course registration validation"""
    
    def test_validator_import(self):
        """Test CourseRegistrationValidator can be imported"""
        from apps.student.registration_validation import CourseRegistrationValidator
        assert CourseRegistrationValidator is not None
    
    def test_helper_functions(self):
        """Test helper functions exist"""
        from apps.student.registration_validation import (
            validate_course_registration,
            get_available_courses
        )
        assert callable(validate_course_registration)
        assert callable(get_available_courses)


class ConcurrencyTestCase(TestCase):
    """Test concurrency utilities"""
    
    def test_idempotency_manager(self):
        """Test IdempotencyManager can be imported"""
        from utils.concurrency import IdempotencyManager
        assert IdempotencyManager is not None
    
    def test_generate_key(self):
        """Test key generation"""
        from utils.concurrency import IdempotencyManager
        
        key = IdempotencyManager.generate_key()
        
        assert key is not None
        assert len(key) > 0
    
    def test_course_capacity_manager(self):
        """Test CourseCapacityManager can be imported"""
        from utils.concurrency import CourseCapacityManager
        assert CourseCapacityManager is not None
    
    def test_transaction_safe_gpa(self):
        """Test TransactionSafeGPA can be imported"""
        from utils.concurrency import TransactionSafeGPA
        assert TransactionSafeGPA is not None


class NigerianOptimizationTestCase(TestCase):
    """Test Nigerian optimization utilities"""
    
    def test_field_selector(self):
        """Test FieldSelector can be imported"""
        from utils.nigerian_optimization import FieldSelector
        assert FieldSelector is not None
    
    def test_cache_optimizer(self):
        """Test CacheOptimizer can be imported"""
        from utils.nigerian_optimization import CacheOptimizer
        assert CacheOptimizer is not None
    
    def test_retry_optimizer(self):
        """Test RetryOptimizer can be imported"""
        from utils.nigerian_optimization import RetryOptimizer
        assert RetryOptimizer is not None
    
    def test_network_optimizer(self):
        """Test NetworkOptimizer can be imported"""
        from utils.nigerian_optimization import NetworkOptimizer
        assert NetworkOptimizer is not None
    
    def test_field_parse(self):
        """Test field parsing"""
        from utils.nigerian_optimization import FieldSelector
        
        fields_str = 'id,name,email'
        fields = FieldSelector.parse_fields(fields_str)
        
        assert fields == ['id', 'name', 'email']
    
    def test_retry_delay_calculation(self):
        """Test retry delay calculation"""
        from utils.nigerian_optimization import RetryOptimizer
        
        # Test exponential backoff
        delay_0 = RetryOptimizer.calculate_delay(0)
        delay_1 = RetryOptimizer.calculate_delay(1)
        
        assert delay_1 >= delay_0  # Should increase