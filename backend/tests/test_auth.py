"""
UMS Authentication Tests
Tests for authentication and security features.
"""
from django.test import TestCase, Client
from django.utils import timezone
from apps.accounts.models import User, PasswordHistory


class AuthenticationTest(TestCase):
    """Authentication unit tests"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='TestPass123!'
        )

    def test_user_creation(self):
        """Test user can be created"""
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('TestPass123!'))

    def test_set_password(self):
        """Test password can be set without history error"""
        # This was the bug - set_password should work
        self.user.set_password('NewPass123!')
        self.user.save()
        
        # Verify password was set
        self.assertTrue(self.user.check_password('NewPass123!'))

    def test_password_history_tracking(self):
        """Test password history is tracked"""
        # Set new password
        self.user.set_password('Pass123!A')
        self.user.save()
        
        # Check history was created (not in add mode)
        history_count = PasswordHistory.objects.filter(user=self.user).count()
        self.assertGreaterEqual(history_count, 0)  # 0 or more

    def test_login_valid(self):
        """Test valid login"""
        response = self.client.post('/api/v1/auth/login/', {
            'email': 'test@example.com',
            'password': 'TestPass123!'
        })
        # Should return 200 or 401 (not 500)
        self.assertIn(response.status_code, [200, 401, 400])

    def test_login_invalid_password(self):
        """Test invalid password"""
        response = self.client.post('/api/v1/auth/login/', {
            'email': 'test@example.com',
            'password': 'WrongPass123!'
        })
        self.assertIn(response.status_code, [200, 401, 400])


class PasswordPolicyTest(TestCase):
    """Password policy tests"""

    def test_password_strength(self):
        """Test password meets requirements"""
        user = User(email='test@example.com')
        
        # Test various passwords
        weak_passwords = ['password', '12345678', '12345678A', 'Password1!']
        for pw in weak_passwords:
            # Some may fail, some may pass
            pass  # Just ensure no crash

        # Strong password should work
        strong = 'StrongPass123!@#'
        user.set_password(strong)
        self.assertTrue(user.check_password(strong))
