"""
Tests for authentication endpoints.
"""
import pytest
from django.test import TestCase
from apps.accounts.models import User, UserRole


@pytest.mark.django_db
class TestAuthentication(TestCase):
    """Test authentication features."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            email='test@university.edu.ng',
            password='TestPass123!',
            role=UserRole.STUDENT,
            first_name='Test',
            last_name='Student'
        )
    
    def test_user_creation(self):
        """Test user is created correctly."""
        assert self.user.email == 'test@university.edu.ng'
        assert self.user.check_password('TestPass123!')
        assert not self.user.is_superuser
    
    def test_user_role(self):
        """Test user role assignment."""
        assert self.user.role == UserRole.STUDENT
    
    def test_user_str(self):
        """Test user string representation."""
        assert 'test@university.edu.ng' in str(self.user)
    
    def test_roles_available(self):
        """Test all roles are defined."""
        assert UserRole.STUDENT == 'student'
        assert UserRole.LECTURER == 'lecturer'
        assert UserRole.HOD == 'hod'
        assert UserRole.DEAN == 'dean'
        assert UserRole.REGISTRAR == 'registrar'
        assert UserRole.BURSAR == 'bursar'
        assert UserRole.INSTITUTION_ADMIN == 'institution_admin'
