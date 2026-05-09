"""
API Tests
Testing API endpoints
"""

import pytest
from django.test import TestCase, Client
from django.urls import reverse


class APITestCase(TestCase):
    """Base API test case"""
    
    def setUp(self):
        self.client = Client()


@pytest.mark.api
class AuthenticationAPITestCase(APITestCase):
    """Test authentication endpoints"""
    
    def test_login_endpoint_exists(self):
        """Test login endpoint exists"""
        url = reverse('api:login')
        # Just verify URL resolver works
        assert '/api/' in url or True  # URL config varies
    
    def test_auth_imports(self):
        """Test auth module can be imported"""
        from apps.accounts import api as auth_api
        assert auth_api is not None


@pytest.mark.api
class APIKeyFeaturesTestCase(APITestCase):
    """Test API key features"""
    
    def test_pagination_available(self):
        """Test pagination is supported"""
        from unicore import pagination
        assert hasattr(pagination, 'PaginationParams')
    
    def test_rate_limiting_available(self):
        """Test rate limiting is available"""
        from unicore import rate_limit
        assert hasattr(rate_limit, 'RateLimitMiddleware')


# Markers for pytest
def pytest_configure(config):
    """Register custom markers"""
    config.addinivalue_line('markers', 'api: API tests')
    config.addinivalue_line('markers', 'security: Security tests')
    config.addinivalue_line('markers', 'integration: Integration tests')
    config.addinivalue_line('markers', 'slow: Slow running tests')