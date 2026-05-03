"""
UMS Test Suite - Core Tests
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'apps'))

from django.test import TestCase


class UMSCoreTest(TestCase):
    """Core functionality tests"""
    
    def test_django_configured(self):
        """Test Django is configured"""
        from django.conf import settings
        self.assertIsNotNone(settings.DATABASES)
    
    def test_apps_loaded(self):
        """Test Django apps are loaded"""
        from django.conf import settings
        self.assertIn('apps.academic', settings.INSTALLED_APPS)
    
    def test_static_files(self):
        """Test static files configured"""
        from django.conf import settings
        self.assertIn('staticfiles', settings.INSTALLED_APPS)


class FacultyModelTest(TestCase):
    """Test Faculty model"""
    
    def test_faculty_creation(self):
        """Test faculty can be created"""
        from apps.academic.models import Faculty
        f = Faculty(name="Test Faculty")
        # Just test the name attribute exists
        self.assertEqual(f.name, "Test Faculty")


class DepartmentModelTest(TestCase):
    """Test Department model"""
    
    def test_department_creation(self):
        """Test department can be created"""
        from apps.academic.models import Department
        d = Department(name="Test Dept", code="TD")
        self.assertEqual(d.name, "Test Dept")
        self.assertEqual(d.code, "TD")


class ProgrammeModelTest(TestCase):
    """Test Programme model"""
    
    def test_programme_creation(self):
        """Test programme can be created"""
        from apps.academic.models import Programme
        p = Programme(name="Test Programme", code="TP", qualification="ND")
        self.assertEqual(p.name, "Test Programme")


class HostelModelTest(TestCase):
    """Test Hostel model"""
    
    def test_hostel_creation(self):
        """Test hostel can be created"""
        from apps.institution.models import Hostel
        h = Hostel(name="Test Hostel", gender="male", total_beds=100)
        self.assertEqual(h.name, "Test Hostel")
        self.assertEqual(h.total_beds, 100)


# Simple validation tests - no database required
class ValidationTest(TestCase):
    """Validation tests"""
    
    def test_model_attributes(self):
        """Test model classes exist"""
        from apps import academic, institution, student, staff, finance
        self.assertIsNotNone(academic)
    
    def test_serializers_exist(self):
        """Test serializers exist"""
        from apps.core.serializers import FacultySerializer
        self.assertIsNotNone(FacultySerializer)
    
    def test_viewsets_exist(self):
        """Test viewsets exist"""
        from apps.finance.views import PaymentViewSet
        self.assertIsNotNone(PaymentViewSet)


# API endpoint tests
class APIEndpointTest(TestCase):
    """Test API endpoints configured"""
    
    def test_urls_configured(self):
        """Test URL configuration"""
        from django.urls import reverse, include
        # Just verify urls module can be imported
        from apps.core import urls
        self.assertIsNotNone(urls)


# Run with: python manage.py test