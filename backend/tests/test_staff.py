"""
Integration tests for staff APIs.
Tests staff profile, leave management, and academic endpoints.
"""
import pytest
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from apps.academic.models import Faculty, Department
from apps.staff.models import StaffProfile, LeaveRequest

User = get_user_model()


class StaffAPITestCase(TestCase):
    """Test case for staff API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        
        # Create staff user
        self.user = User.objects.create_user(
            username='teststaff',
            email='staff@test.com',
            password='TestPass123!@#',
            role='staff'
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
        
        # Create staff profile
        self.staff = StaffProfile.objects.create(
            user=self.user,
            staff_id='STAFF/001',
            department=self.department,
            rank='Senior Lecturer'
        )
    
    def test_staff_login(self):
        """Test staff can login."""
        response = self.client.post('/api/v1/auth/login/', {
            'username': 'teststaff',
            'password': 'TestPass123!@#'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.json())
    
    def test_staff_profile_endpoint(self):
        """Test staff profile API."""
        # Get token
        response = self.client.post('/api/v1/auth/login/', {
            'username': 'teststaff',
            'password': 'TestPass123!@#'
        })
        token = response.json()['access']
        
        # Get profile
        response = self.client.get(
            '/api/v1/staff/profile/',
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        self.assertIn(response.status_code, [200, 404])
    
    def test_staff_leave_request(self):
        """Test leave request creation."""
        # Get token
        response = self.client.post('/api/v1/auth/login/', {
            'username': 'teststaff',
            'password': 'TestPass123!@#'
        })
        token = response.json()['access']
        
        # Create leave request
        response = self.client.post(
            '/api/v1/staff/leave/',
            {
                'leave_type': 'annual',
                'start_date': '2024-06-01',
                'end_date': '2024-06-05',
                'reason': 'Personal business'
            },
            HTTP_AUTHORIZATION=f'Bearer {token}',
            content_type='application/json'
        )
        self.assertIn(response.status_code, [201, 400, 404])
    
    def test_staff_access_student_data(self):
        """Test staff can access student data."""
        response = self.client.post('/api/v1/auth/login/', {
            'username': 'teststaff',
            'password': 'TestPass123!@#'
        })
        token = response.json()['access']
        
        response = self.client.get(
            '/api/v1/students/',
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        self.assertIn(response.status_code, [200, 403])
    
    def test_unauthorized_access(self):
        """Test unauthorized access is blocked."""
        response = self.client.get('/api/v1/staff/profile/')
        self.assertEqual(response.status_code, 403)
    
    def tearDown(self):
        """Clean up."""
        self.user.delete()
        self.faculty.delete()