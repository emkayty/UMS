"""
Tests for academic models.
"""
import pytest
from django.test import TestCase
from apps.academic.models import Faculty, Department, Programme, Course


@pytest.mark.django_db
class TestAcademicModels(TestCase):
    """Test academic structure models."""
    
    def setUp(self):
        """Set up test data."""
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
            semester=1,
            programme=self.programme,
            department=self.department,
            learning_hours=150,
            ects_credits=3.0
        )
    
    def test_faculty_creation(self):
        """Test faculty is created correctly."""
        assert self.faculty.name == 'Faculty of Science'
        assert self.faculty.code == 'SCI'
    
    def test_department_creation(self):
        """Test department is created correctly."""
        assert self.department.name == 'Computer Science'
        assert self.department.faculty == self.faculty
    
    def test_programme_creation(self):
        """Test programme is created correctly."""
        assert self.programme.name == 'Computer Science'
        assert self.programme.duration_years == 4
        assert self.programme.department == self.department
    
    def test_course_creation(self):
        """Test course is created correctly."""
        assert self.course.code == 'CS101'
        assert self.course.credit_units == 3
        assert self.course.learning_hours == 150
        assert self.course.ects_credits == 3.0
    
    def test_course_str(self):
        """Test course string representation."""
        assert 'CS101' in str(self.course)
        assert 'Introduction to Programming' in str(self.course)
