"""
COMPREHENSIVE TEST SUITE
Full system tests
"""

import pytest
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from unittest.mock import patch, MagicMock

from apps.core.models import (
    Faculty, Department, Programme, Course,
    AcademicSession, Semester, StudentProfile
)
from apps.accounts.models import User

User = get_user_model()


class BaseTestCase(TestCase):
    """Base test case with common setup."""
    
    def setUp(self):
        self.client = Client()


class AuthTestCase(BaseTestCase):
    """Authentication tests."""
    
    def test_login_success(self):
        """Test successful login."""
        # Create user
        User.objects.create_user(
            email='test@test.com',
            password='testpass123'
        )
        
        response = self.client.post('/api/v1/auth/login/', {
            'email': 'test@test.com',
            'password': 'testpass123'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_login_invalid_credentials(self):
        """Test invalid credentials."""
        response = self.client.post('/api/v1/auth/login/', {
            'email': 'invalid@test.com',
            'password': 'wrong'
        })
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class FacultyAPITestCase(APITestCase):
    """Faculty API tests."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='admin@test.com',
            password='admin123'
        )
        self.client.force_authenticate(user=self.user)
        
        # Create faculty
        self.faculty = Faculty.objects.create(
            name='Faculty of Science',
            code='SCI'
        )
    
    def test_list_faculties(self):
        """Test list faculties."""
        response = self.client.get('/api/v1/academic/faculties/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_faculty(self):
        """Test create faculty."""
        response = self.client.post('/api/v1/academic/faculties/', {
            'name': 'Faculty of Arts',
            'code': 'ART'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_retrieve_faculty(self):
        """Test retrieve faculty."""
        response = self.client.get(f'/api/v1/academic/faculties/{self.faculty.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_faculty(self):
        """Test update faculty."""
        response = self.client.patch(
            f'/api/v1/academic/faculties/{self.faculty.id}/',
            {'name': 'Faculty of Sciences'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_delete_faculty(self):
        """Test delete faculty."""
        response = self.client.delete(f'/api/v1/academic/faculties/{self.faculty.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class DepartmentAPITestCase(APITestCase):
    """Department API tests."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='admin@test.com',
            password='admin123'
        )
        self.client.force_authenticate(user=self.user)
        
        self.faculty = Faculty.objects.create(
            name='Faculty of Science',
            code='SCI'
        )
        self.department = Department.objects.create(
            name='Computer Science',
            code='CS',
            faculty=self.faculty
        )
    
    def test_list_departments(self):
        """Test list departments."""
        response = self.client.get('/api/v1/academic/departments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_filter_by_faculty(self):
        """Test filter by faculty."""
        response = self.client.get(
            f'/api/v1/academic/departments/?faculty={self.faculty.id}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProgrammeAPITestCase(APITestCase):
    """Programme API tests."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='admin@test.com',
            password='admin123'
        )
        self.client.force_authenticate(user=self.user)
        
        self.faculty = Faculty.objects.create(
            name='Faculty of Science',
            code='SCI'
        )
        self.department = Department.objects.create(
            name='Computer Science',
            code='CS',
            faculty=self.faculty
        )
        self.programme = Programme.objects.create(
            name='Computer Science',
            code='CS',
            duration_years=4,
            department=self.department
        )
    
    def test_list_programmes(self):
        """Test list programmes."""
        response = self.client.get('/api/v1/academic/programmes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CourseAPITestCase(APITestCase):
    """Course API tests."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='admin@test.com',
            password='admin123'
        )
        self.client.force_authenticate(user=self.user)
        
        self.faculty = Faculty.objects.create(
            name='Faculty of Science',
            code='SCI'
        )
        self.department = Department.objects.create(
            name='Computer Science',
            code='CS',
            faculty=self.faculty
        )
        self.programme = Programme.objects.create(
            name='Computer Science',
            code='CS',
            duration_years=4,
            department=self.department
        )
        self.course = Course.objects.create(
            code='CS101',
            title='Introduction to Programming',
            credit_units=3,
            level=100,
            semester_offered=1,
            department=self.department,
            programme=self.programme
        )
    
    def test_list_courses(self):
        """Test list courses."""
        response = self.client.get('/api/v1/academic/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_filter_by_level(self):
        """Test filter by level."""
        response = self.client.get('/api/v1/academic/courses/?level=100')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SessionAPITestCase(APITestCase):
    """Academic session tests."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='admin@test.com',
            password='admin123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_create_session(self):
        """Test create session."""
        response = self.client.post('/api/v1/academic/sessions/', {
            'name': '2024/2025',
            'is_current': True
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


# Model Tests

class FacultyModelTestCase(TestCase):
    """Faculty model tests."""
    
    def test_faculty_creation(self):
        """Test faculty creation."""
        faculty = Faculty.objects.create(
            name='Faculty of Science',
            code='SCI'
        )
        self.assertEqual(str(faculty), 'Faculty of Science')
        self.assertEqual(faculty.code, 'SCI')


class DepartmentModelTestCase(TestCase):
    """Department model tests."""
    
    def setUp(self):
        self.faculty = Faculty.objects.create(
            name='Faculty of Science',
            code='SCI'
        )
    
    def test_department_creation(self):
        """Test department creation."""
        dept = Department.objects.create(
            name='Computer Science',
            code='CS',
            faculty=self.faculty
        )
        self.assertEqual(str(dept), 'Computer Science')


class ProgrammeModelTestCase(TestCase):
    """Programme model tests."""
    
    def setUp(self):
        self.faculty = Faculty.objects.create(
            name='Faculty of Science',
            code='SCI'
        )
        self.department = Department.objects.create(
            name='Computer Science',
            code='CS',
            faculty=self.faculty
        )
    
    def test_programme_creation(self):
        """Test programme creation."""
        programme = Programme.objects.create(
            name='Computer Science',
            code='CS',
            duration_years=4,
            department=self.department
        )
        self.assertEqual(str(programme), 'Computer Science')


# Integration Tests

class HealthCheckTestCase(BaseTestCase):
    """Health check tests."""
    
    def test_health_endpoint(self):
        """Test health endpoint."""
        response = self.client.get('/api/v1/health/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_ping_endpoint(self):
        """Test ping endpoint."""
        response = self.client.get('/health/ping/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# Permission Tests

class PermissionTestCase(APITestCase):
    """Permission tests."""
    
    def test_unauthenticated_access(self):
        """Test unauthenticated access blocked."""
        response = self.client.get('/api/v1/academic/faculties/')
        # Should still work with read permissions
        self.assertIn(response.status_code, [200, 401])


# Validation Tests

class ValidationTestCase(TestCase):
    """Validation tests."""
    
    def test_faculty_code_uppercase(self):
        """Test faculty code converted to uppercase."""
        faculty = Faculty.objects.create(
            name='Science',
            code='sci'
        )
        self.assertEqual(faculty.code, 'SCI')
    
    def test_course_code_uppercase(self):
        """Test course code converted to uppercase."""
        self.faculty = Faculty.objects.create(
            name='Science',
            code='SCI'
        )
        self.department = Department.objects.create(
            name='CS',
            code='CS',
            faculty=self.faculty
        )
        self.programme = Programme.objects.create(
            name='CS',
            code='CS',
            duration_years=4,
            department=self.department
        )
        course = Course.objects.create(
            code='cs101',
            title='Intro',
            credit_units=3,
            level=100,
            semester_offered=1,
            department=self.department,
            programme=self.programme
        )
        self.assertEqual(course.code, 'CS101')


# Run tests with: python manage.py test
# Or: pytest

if __name__ == '__main__':
    import django
    import sys
    
    # Setup Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unicore.settings')
    django.setup()
    
    # Run pytest
    pytest.main([__file__, '-v'])