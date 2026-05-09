"""
Security Tests
Testing security utilities and middleware
"""

import pytest
from django.test import TestCase


class SecurityUtilsTestCase(TestCase):
    """Test security utilities"""
    
    def test_security_utils_import(self):
        """Test SecurityUtils can be imported"""
        from utils.security import SecurityUtils
        assert SecurityUtils is not None
    
    def test_audit_logger_import(self):
        """Test AuditLogger can be imported"""
        from utils.security import AuditLogger
        assert AuditLogger is not None
    
    def test_input_sanitizer_import(self):
        """Test InputSanitizer can be imported"""
        from utils.security import InputSanitizer
        assert InputSanitizer is not None


class SecurityMiddlewareTestCase(TestCase):
    """Test security middleware"""
    
    def test_session_expiry_middleware(self):
        """Test SessionExpiryMiddleware exists"""
        from utils.security_middleware import SessionExpiryMiddleware
        assert SessionExpiryMiddleware is not None
    
    def test_tenant_context_middleware(self):
        """Test TenantContextMiddleware exists"""
        from utils.security_middleware import TenantContextMiddleware
        assert TenantContextMiddleware is not None
    
    def test_jwt_expiry_middleware(self):
        """Test JWTTokenExpiryMiddleware exists"""
        from utils.security_middleware import JWTTokenExpiryMiddleware
        assert JWTTokenExpiryMiddleware is not None


@pytest.mark.security
class RBACTestCase(TestCase):
    """Test RBAC permissions"""
    
    def test_permission_classes_exist(self):
        """Test permission classes are available"""
        from apps.accounts import permissions
        
        permission_classes = [
            'IsAdmin',
            'IsStudent', 
            'IsLecturer',
            'IsHOD',
            'IsDean',
            'IsRegistrar',
            'IsBursar',
        ]
        
        for cls_name in permission_classes:
            assert hasattr(permissions, cls_name), f"Missing permission: {cls_name}"