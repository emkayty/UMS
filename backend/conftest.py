"""
Pytest Configuration and Fixtures
UMS Test Suite
"""

import pytest
import os
import sys

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unicore.settings')


@pytest.fixture(scope='session')
def django_db_setup():
    """Setup test database."""
    from django.conf import settings
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }


@pytest.fixture
def db_access_with_duplicates():
    """Allow database access with duplicates."""
    from django.test import override_thread_locals
    yield


# ============================================================
# MODEL FIXTURES
# ============================================================

@pytest.fixture
def faculty(db):
    """Create a test faculty."""
    from apps.academic.models import Faculty
    return Faculty.objects.create(
        name='Faculty of Science',
        code='SCI'
    )


@pytest.fixture
def department(db, faculty):
    """Create a test department."""
    from apps.academic.models import Department
    return Department.objects.create(
        name='Computer Science',
        code='CS',
        faculty=faculty
    )


@pytest.fixture
def programme(db, department):
    """Create a test programme."""
    from apps.academic.models import Programme
    return Programme.objects.create(
        name='Computer Science',
        code='CS',
        duration_years=4,
        department=department
    )


@pytest.fixture
def course(db, department, programme):
    """Create a test course."""
    from apps.academic.models import Course
    return Course.objects.create(
        code='CS101',
        title='Introduction to Programming',
        credit_units=3,
        level=100,
        semester_offered=1,
        department=department,
        programme=programme
    )


@pytest.fixture
def academic_session(db):
    """Create a test academic session."""
    from apps.academic.models import AcademicSession
    return AcademicSession.objects.create(
        name='2024/2025',
        is_current=True
    )


@pytest.fixture
def user(db):
    """Create a test user."""
    from apps.accounts.models import User
    return User.objects.create_user(
        email='test@example.com',
        password='testpass123',
        first_name='Test',
        last_name='User'
    )


@pytest.fixture
def admin_user(db):
    """Create a test admin user."""
    from apps.accounts.models import User
    return User.objects.create_superuser(
        email='admin@example.com',
        password='adminpass123',
        first_name='Admin',
        last_name='User'
    )


@pytest.fixture
def student_profile(db, user, programme):
    """Create a test student profile."""
    from apps.student.models import StudentProfile
    return StudentProfile.objects.create(
        user=user,
        matric_number='2024001',
        programme=programme,
        current_level=100,
        status='active'
    )


@pytest.fixture
def staff_profile(db, user, department):
    """Create a test staff profile."""
    from apps.staff.models import StaffProfile
    return StaffProfile.objects.create(
        user=user,
        staff_id='STF001',
        department=department,
        rank='Lecturer I'
    )


@pytest.fixture
def fee_structure(db, academic_session):
    """Create a test fee structure."""
    from apps.finance.models import FeeStructure
    return FeeStructure.objects.create(
        name='Tuition Fee',
        amount=50000,
        session=academic_session,
        is_compulsory=True
    )


# ============================================================
# API CLIENT FIXTURES
# ============================================================

@pytest.fixture
def api_client():
    """Create API client."""
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, user):
    """Create authenticated API client."""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def admin_client(api_client, admin_user):
    """Create admin API client."""
    api_client.force_authenticate(user=admin_user)
    return api_client


# ============================================================
# FACTORY CLASSES
# ============================================================

class FacultyFactory:
    """Factory for Faculty model."""
    
    @staticmethod
    def create(**kwargs):
        from apps.academic.models import Faculty
        return Faculty.objects.create(
            name=kwargs.get('name', 'Test Faculty'),
            code=kwargs.get('code', 'TST')
        )


class DepartmentFactory:
    """Factory for Department model."""
    
    @staticmethod
    def create(faculty=None, **kwargs):
        from apps.academic.models import Department
        if not faculty:
            faculty = FacultyFactory.create()
        return Department.objects.create(
            name=kwargs.get('name', 'Test Department'),
            code=kwargs.get('code', 'TST'),
            faculty=faculty
        )


class UserFactory:
    """Factory for User model."""
    
    @staticmethod
    def create(**kwargs):
        from apps.accounts.models import User
        return User.objects.create_user(
            email=kwargs.get('email', 'test@test.com'),
            password=kwargs.get('password', 'testpass123'),
            first_name=kwargs.get('first_name', 'Test'),
            last_name=kwargs.get('last_name', 'User')
        )


# ============================================================
# TEST DATASETS
# ============================================================

FAKE_FACULTIES = [
    {'name': 'Faculty of Science', 'code': 'SCI'},
    {'name': 'Faculty of Arts', 'code': 'ART'},
    {'name': 'Faculty of Engineering', 'code': 'ENG'},
    {'name': 'Faculty of Medicine', 'code': 'MED'},
    {'name': 'Faculty of Social Sciences', 'code': 'SOC'},
]

FAKE_DEPARTMENTS = [
    {'name': 'Computer Science', 'code': 'CS'},
    {'name': 'Mathematics', 'code': 'MTH'},
    {'name': 'Physics', 'code': 'PHY'},
    {'name': 'Chemistry', 'code': 'CHM'},
    {'name': 'Biology', 'code': 'BIO'},
]

FAKE_COURSES = [
    {'code': 'CS101', 'title': 'Intro to Programming', 'credit_units': 3},
    {'code': 'CS102', 'title': 'Data Structures', 'credit_units': 3},
    {'code': 'MTH101', 'title': 'Calculus I', 'credit_units': 3},
    {'code': 'PHY101', 'title': 'Physics I', 'credit_units': 4},
]

STUDENT_TEST_DATA = [
    {'email': 'student1@test.com', 'matric': '2024001'},
    {'email': 'student2@test.com', 'matric': '2024002'},
    {'email': 'student3@test.com', 'matric': '2024003'},
]

STAFF_TEST_DATA = [
    {'email': 'staff1@test.com', 'staff_id': 'STF001', 'rank': 'Lecturer I'},
    {'email': 'staff2@test.com', 'staff_id': 'STF002', 'rank': 'Lecturer II'},
    {'email': 'staff3@test.com', 'staff_id': 'STF003', 'rank': 'Senior Lecturer'},
]