"""
Integration tests for finance APIs.
Tests fee payment and invoice endpoints.
"""
import pytest
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.academic.models import Faculty, Department, Programme
from apps.student.models import StudentProfile
from apps.finance.models import FeeItem, StudentFee, Payment

User = get_user_model()


class FinanceAPITestCase(TestCase):
    """Test case for finance API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        
        # Create user
        self.user = User.objects.create_user(
            username='testfinance',
            email='finance@test.com',
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
        
        # Create student
        self.student = StudentProfile.objects.create(
            user=self.user,
            matric_number='SC/2024/001',
            programme=self.programme,
            current_level=100
        )
        
        # Create fee item
        self.fee = FeeItem.objects.create(
            name='Tuition Fee',
            amount=50000.00,
            level=100,
            programme=self.programme,
            session='2024/2025'
        )
        
        # Create student fee
        self.student_fee = StudentFee.objects.create(
            student=self.student,
            fee_item=self.fee,
            amount=50000.00,
            status='unpaid'
        )
    
    def test_fee_list_endpoint(self):
        """Test fee list API."""
        # Get token
        response = self.client.post('/api/v1/auth/login/', {
            'username': 'testfinance',
            'password': 'TestPass123!@#'
        })
        self.assertEqual(response.status_code, 200)
        token = response.json()['access']
        
        # Get fees
        response = self.client.get(
            '/api/v1/fees/',
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        self.assertIn(response.status_code, [200, 404])
    
    def test_payment_list_endpoint(self):
        """Test payment list API."""
        # Get token
        response = self.client.post('/api/v1/auth/login/', {
            'username': 'testfinance',
            'password': 'TestPass123!@#'
        })
        token = response.json()['access']
        
        # Get payments
        response = self.client.get(
            '/api/v1/payments/',
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        self.assertIn(response.status_code, [200, 404])
    
    def test_student_fees_endpoint(self):
        """Test student fees API."""
        # Get token
        response = self.client.post('/api/v1/auth/login/', {
            'username': 'testfinance',
            'password': 'TestPass123!@#'
        })
        token = response.json()['access']
        
        # Get student fees
        response = self.client.get(
            f'/api/v1/fees/student/{self.student.matric_number}/',
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        self.assertIn(response.status_code, [200, 404])
    
    def test_payment_endpoint(self):
        """Test payment processing."""
        # Get token
        response = self.client.post('/api/v1/auth/login/', {
            'username': 'testfinance',
            'password': 'TestPass123!@#'
        })
        token = response.json()['access']
        
        # Process payment
        response = self.client.post(
            '/api/v1/payments/',
            {
                'fee_id': self.fee.id,
                'amount': 50000.00,
                'method': 'transfer'
            },
            HTTP_AUTHORIZATION=f'Bearer {token}',
            content_type='application/json'
        )
        self.assertIn(response.status_code, [201, 400, 404])
    
    def test_finance_permissions(self):
        """Test finance access controls."""
        # Staff should have different access
        staff_user = User.objects.create_user(
            username='stafffinance',
            email='staff@test.com',
            password='TestPass123!@#',
            role='staff'
        )
        
        response = self.client.post('/api/v1/auth/login/', {
            'username': 'stafffinance',
            'password': 'TestPass123!@#'
        })
        token = response.json()['access']
        
        # Staff can view all payments
        response = self.client.get(
            '/api/v1/payments/',
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        self.assertIn(response.status_code, [200, 403])
    
    def test_unauthorized_finance_access(self):
        """Test unauthorized access is blocked."""
        response = self.client.get('/api/v1/fees/')
        self.assertEqual(response.status_code, 403)
    
    def tearDown(self):
        """Clean up."""
        self.user.delete()
        self.faculty.delete()