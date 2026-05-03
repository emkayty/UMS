"""
Comprehensive Model Tests
UMS Test Suite
"""

import pytest
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch, MagicMock


# ============================================================
# AUTHENTICATION TESTS
# ============================================================

@pytest.mark.django_db
class UserModelTests(TestCase):
    """Tests for User model."""
    
    def test_create_user(self):
        """Test user creation."""
        from apps.accounts.models import User
        user = User.objects.create_user(
            email='test@test.com',
            password='testpass123'
        )
        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_create_superuser(self):
        """Test superuser creation."""
        from apps.accounts.models import User
        admin = User.objects.create_superuser(
            email='admin@test.com',
            password='adminpass123'
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
    
    def test_email_normalized(self):
        """Test email normalization."""
        from apps.accounts.models import User
        user = User.objects.create_user(
            email='TEST@TEST.COM',
            password='testpass123'
        )
        self.assertEqual(user.email, 'test@test.com')


@pytest.mark.django_db
class AuthAPITests(APITestCase):
    """Tests for authentication API."""
    
    def test_login_success(self):
        """Test successful login."""
        from apps.accounts.models import User
        User.objects.create_user(
            email='test@test.com',
            password='testpass123'
        )
        
        response = self.client.post('/api/v1/auth/login/', {
            'email': 'test@test.com',
            'password': 'testpass123'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        response = self.client.post('/api/v1/auth/login/', {
            'email': 'invalid@test.com',
            'password': 'wrong'
        })
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# ============================================================
# ACADEMIC TESTS
# ============================================================

@pytest.mark.django_db
class FacultyModelTests(TestCase):
    """Tests for Faculty model."""
    
    def test_create_faculty(self):
        """Test faculty creation."""
        from apps.academic.models import Faculty
        faculty = Faculty.objects.create(
            name='Faculty of Science',
            code='SCI'
        )
        self.assertEqual(str(faculty), 'Faculty of Science')
        self.assertEqual(faculty.code, 'SCI')
    
    def test_faculty_code_uppercase(self):
        """Test faculty code is uppercased."""
        from apps.academic.models import Faculty
        faculty = Faculty.objects.create(
            name='Science',
            code='sci'
        )
        self.assertEqual(faculty.code, 'SCI')


@pytest.mark.django_db
class DepartmentModelTests(TestCase):
    """Tests for Department model."""
    
    def test_create_department(self):
        """Test department creation."""
        from apps.academic.models import Faculty, Department
        
        faculty = Faculty.objects.create(
            name='Science',
            code='SCI'
        )
        department = Department.objects.create(
            name='Computer Science',
            code='CS',
            faculty=faculty
        )
        
        self.assertEqual(str(department), 'Computer Science')
        self.assertEqual(department.faculty, faculty)


@pytest.mark.django_db
class ProgrammeModelTests(TestCase):
    """Tests for Programme model."""
    
    def test_create_programme(self):
        """Test programme creation."""
        from apps.academic.models import Faculty, Department, Programme
        
        faculty = Faculty.objects.create(name='Science', code='SCI')
        dept = Department.objects.create(
            name='CS', code='CS', faculty=faculty
        )
        programme = Programme.objects.create(
            name='Computer Science',
            code='CS',
            duration_years=4,
            department=dept
        )
        
        self.assertEqual(str(programme), 'Computer Science')
        self.assertEqual(programme.duration_years, 4)


@pytest.mark.django_db
class CourseModelTests(TestCase):
    """Tests for Course model."""
    
    def test_create_course(self):
        """Test course creation."""
        from apps.academic.models import Faculty, Department, Programme, Course
        
        faculty = Faculty.objects.create(name='Science', code='SCI')
        dept = Department.objects.create(name='CS', code='CS', faculty=faculty)
        prog = Programme.objects.create(
            name='CS', code='CS', duration_years=4, department=dept
        )
        
        course = Course.objects.create(
            code='CS101',
            title='Intro to Programming',
            credit_units=3,
            level=100,
            semester_offered=1,
            department=dept,
            programme=prog
        )
        
        self.assertEqual(str(course), 'CS101 - Intro to Programming')
        self.assertEqual(course.credit_units, 3)


@pytest.mark.django_db
class AcademicAPITests(APITestCase):
    """Tests for academic API endpoints."""
    
    def setUp(self):
        from apps.accounts.models import User
        self.user = User.objects.create_superuser(
            email='admin@test.com',
            password='adminpass123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_list_faculties(self):
        """Test list faculties."""
        from apps.academic.models import Faculty
        Faculty.objects.create(name='Science', code='SCI')
        
        response = self.client.get('/api/v1/academic/faculties/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_faculty(self):
        """Test create faculty."""
        response = self.client.post('/api/v1/academic/faculties/', {
            'name': 'Faculty of Arts',
            'code': 'ART'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_list_departments(self):
        """Test list departments."""
        from apps.academic.models import Faculty
        faculty = Faculty.objects.create(name='Science', code='SCI')
        from apps.academic.models import Department
        Department.objects.create(name='CS', code='CS', faculty=faculty)
        
        response = self.client.get('/api/v1/academic/departments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_list_programmes(self):
        """Test list programmes."""
        from apps.academic.models import Faculty, Department, Programme
        faculty = Faculty.objects.create(name='Science', code='SCI')
        dept = Department.objects.create(name='CS', code='CS', faculty=faculty)
        Programme.objects.create(name='CS', code='CS', duration_years=4, department=dept)
        
        response = self.client.get('/api/v1/academic/programmes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_list_courses(self):
        """Test list courses."""
        from apps.academic.models import Faculty, Department, Programme, Course
        faculty = Faculty.objects.create(name='Science', code='SCI')
        dept = Department.objects.create(name='CS', code='CS', faculty=faculty)
        prog = Programme.objects.create(name='CS', code='CS', duration_years=4, department=dept)
        Course.objects.create(
            code='CS101', title='Intro', credit_units=3,
            level=100, semester_offered=1, department=dept, programme=prog
        )
        
        response = self.client.get('/api/v1/academic/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# ============================================================
# STUDENT TESTS
# ============================================================

@pytest.mark.django_db
class StudentModelTests(TestCase):
    """Tests for Student model."""
    
    def test_create_student(self):
        """Test student creation."""
        from apps.accounts.models import User
        from apps.academic.models import Faculty, Department, Programme
        from apps.student.models import StudentProfile
        
        user = User.objects.create_user(
            email='student@test.com',
            password='pass123'
        )
        faculty = Faculty.objects.create(name='Science', code='SCI')
        dept = Department.objects.create(name='CS', code='CS', faculty=faculty)
        prog = Programme.objects.create(
            name='CS', code='CS', duration_years=4, department=dept
        )
        
        student = StudentProfile.objects.create(
            user=user,
            matric_number='2024001',
            programme=prog,
            current_level=100,
            status='active'
        )
        
        self.assertEqual(student.matric_number, '2024001')
        self.assertEqual(student.current_level, 100)


@pytest.mark.django_db
class StudentAPITests(APITestCase):
    """Tests for student API."""
    
    def setUp(self):
        from apps.accounts.models import User
        self.user = User.objects.create_superuser(
            email='admin@test.com',
            password='adminpass123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_list_students(self):
        """Test list students."""
        response = self.client.get('/api/v1/students/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# ============================================================
# FINANCE TESTS
# ============================================================

@pytest.mark.django_db
class FinanceModelTests(TestCase):
    """Tests for Finance models."""
    
    def test_create_fee_structure(self):
        """Test fee structure creation."""
        from apps.academic.models import AcademicSession
        from apps.finance.models import FeeStructure
        
        session = AcademicSession.objects.create(
            name='2024/2025',
            is_current=True
        )
        
        fee = FeeStructure.objects.create(
            name=' Tuition Fee',
            amount=50000,
            session=session,
            is_compulsory=True
        )
        
        self.assertEqual(fee.amount, 50000)


@pytest.mark.django_db
class FinanceAPITests(APITestCase):
    """Tests for finance API."""
    
    def setUp(self):
        from apps.accounts.models import User
        self.user = User.objects.create_superuser(
            email='admin@test.com',
            password='adminpass123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_list_fees(self):
        """Test list fee structures."""
        response = self.client.get('/api/v1/fees/structures/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_list_invoices(self):
        """Test list invoices."""
        response = self.client.get('/api/v1/fees/invoices/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# ============================================================
# HEALTH CHECK TESTS
# ============================================================

class HealthCheckTests(APITestCase):
    """Tests for health check endpoints."""
    
    def test_health_endpoint(self):
        """Test health check."""
        response = self.client.get('/api/v1/health/')
        self.assertIn(response.status_code, [200, 503])
    
    def test_ping_endpoint(self):
        """Test ping endpoint."""
        response = self.client.get('/health/ping/')
        self.assertEqual(response.status_code, 200)


# ============================================================
# VALIDATION TESTS
# ============================================================

@pytest.mark.django_db
class ValidationTests(TestCase):
    """Tests for validation."""
    
    def test_faculty_unique_code(self):
        """Test faculty code is unique."""
        from apps.academic.models import Faculty
        
        Faculty.objects.create(name='Science', code='SCI')
        
        with self.assertRaises(Exception):
            Faculty.objects.create(name='Arts', code='SCI')
    
    def test_course_unique_code(self):
        """Test course code is unique."""
        from apps.academic.models import Faculty, Department, Programme, Course
        
        faculty = Faculty.objects.create(name='Science', code='SCI')
        dept = Department.objects.create(name='CS', code='CS', faculty=faculty)
        prog = Programme.objects.create(
            name='CS', code='CS', duration_years=4, department=dept
        )
        
        Course.objects.create(
            code='CS101', title='Intro', credit_units=3,
            level=100, semester_offered=1, department=dept, programme=prog
        )
        
        with self.assertRaises(Exception):
            Course.objects.create(
                code='CS101', title='Another', credit_units=3,
                level=100, semester_offered=1, department=dept, programme=prog
            )


# ============================================================
# UTILITY TESTS
# ============================================================

class UtilsTests(TestCase):
    """Tests for utility functions."""
    
    def test_gpa_calculation(self):
        """Test GPA calculation."""
        from apps.core.utils import calculate_gpa, score_to_grade
        
        # Test grade from score
        self.assertEqual(score_to_grade(85), 'A')
        self.assertEqual(score_to_grade(75), 'AB')
        self.assertEqual(score_to_grade(65), 'B')
        self.assertEqual(score_to_grade(55), 'BC')
        self.assertEqual(score_to_grade(45), 'D')
        self.assertEqual(score_to_grade(35), 'F')
    
    def test_grade_point(self):
        """Test grade point calculation."""
        from apps.core.utils import score_to_grade_point
        
        self.assertEqual(score_to_grade_point(85), 4.0)
        self.assertEqual(score_to_grade_point(75), 3.5)
        self.assertEqual(score_to_grade_point(65), 3.0)
        self.assertEqual(score_to_grade_point(55), 2.5)
        self.assertEqual(score_to_grade_point(45), 1.0)
        self.assertEqual(score_to_grade_point(35), 0.0)


# Run tests: pytest or python manage.py test
if __name__ == '__main__':
    import django
    import sys
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unicore.settings')
    django.setup()
    
    pytest.main([__file__, '-v'])