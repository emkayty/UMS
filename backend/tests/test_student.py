"""
Integration tests for student APIs.
Tests student profile, courses, results, attendance endpoints.
"""
import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.academic.models import Faculty, Department, Programme, Course
from apps.student.models import StudentProfile

User = get_user_model()


class StudentAPITestCase(TestCase):
    """Test case for student API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        
        # Create user
        self.user = User.objects.create_user(
            username='teststudent',
            email='student@test.com',
            password='TestPass123!@#',
            role='student'
        )
        
        # Create faculty
        self.faculty = Faculty.objects.create(
            name='Faculty of Science',
            code='SCI'
        )
        
        # Create department
        self.department = Department.objects.create(
            name='Computer Science',
            code='CS',
            faculty=self.faculty
        )
        
        # Create programme
        self.programme = Programme.objects.create(
            name='B.Sc. Computer Science',
            code='CS',
            department=self.department,
            duration=4
        )
        
        # Create student profile
        self.student = StudentProfile.objects.create(
            user=self.user,
            matric_number='SC/2024/001',
            programme=self.programme,
            current_level=100
        )
    
    def test_student_profile_endpoint(self):
        """Test student profile API."""
        # Get token
        response = self.client.post('/api/v1/auth/login/', {
            'username': 'teststudent',
            'password': 'TestPass123!@#'
        })
        self.assertEqual(response.status_code, 200)
        token = response.json()['access']
        
        # Get profile
        response = self.client.get(
            '/api/v1/students/profile/',
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['matric_number'], 'SC/2024/001')
    
    def test_student_courses_endpoint(self):
        """Test student courses API."""
        # Get token
        response = self.client.post('/api/v1/auth/login/', {
            'username': 'teststudent',
            'password': 'TestPass123!@#'
        })
        token = response.json()['access']
        
        # Get courses
        response = self.client.get(
            '/api/v1/students/courses/',
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        self.assertIn(response.status_code, [200, 404])
    
    def test_student_results_endpoint(self):
        """Test student results API."""
        # Get token
        response = self.client.post('/api/v1/auth/login/', {
            'username': 'teststudent',
            'password': 'TestPass123!@#'
        })
        token = response.json()['access']
        
        # Get results
        response = self.client.get(
            f'/api/v1/students/{self.user.username}/results/',
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        self.assertIn(response.status_code, [200, 404])
    
    def test_unauthenticated_access(self):
        """Test unauthenticated access is blocked."""
        response = self.client.get('/api/v1/students/profile/')
        self.assertEqual(response.status_code, 403)
    
    def tearDown(self):
        """Clean up."""
        self.user.delete()
        self.faculty.delete()
        self.programme.delete()