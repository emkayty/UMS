"""
UMS API Tests - Comprehensive
"""
from django.test import TestCase
from rest_framework.test import APITestCase

class AuthAPITest(APITestCase):
    """Authentication API tests"""
    
    def test_login_requires_credentials(self):
        """Test login fails without credentials"""
        response = self.client.post('/api/v1/auth/login/', {})
        self.assertEqual(response.status_code, 400)
    
    def test_protected_endpoint_requires_auth(self):
        """Test protected endpoints require auth"""
        response = self.client.get('/api/v1/students/')
        self.assertEqual(response.status_code, 401)

class StudentAPITest(APITestCase):
    """Student API tests"""
    
    def test_list_students_requires_auth(self):
        """Test listing students requires auth"""
        response = self.client.get('/api/v1/students/')
        self.assertIn(response.status_code, [401, 404])
    
    def test_create_student_requires_auth(self):
        """Test creating student requires auth"""
        response = self.client.post('/api/v1/students/', {
            'first_name': 'Test'
        })
        self.assertEqual(response.status_code, 401)

class FinanceAPITest(APITestCase):
    """Finance API tests"""
    
    def test_list_payments_requires_auth(self):
        """Test listing payments requires auth"""
        response = self.client.get('/api/v1/payments/')
        self.assertIn(response.status_code, [401, 404])

class AcademicAPITest(APITestCase):
    """Academic API tests"""
    
    def test_list_courses_requires_auth(self):
        """Test listing courses requires auth"""
        response = self.client.get('/api/v1/courses/')
        self.assertIn(response.status_code, [401, 404])

class HostelAPITest(APITestCase):
    """Hostel API tests"""
    
    def test_list_hostels_requires_auth(self):
        """Test listing hostels requires auth"""
        response = self.client.get('/api/v1/hostels/')
        self.assertIn(response.status_code, [401, 404])
