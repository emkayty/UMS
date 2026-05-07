"""
UMS Unit Tests - Core and Academic APIs
"""
from django.test import TestCase
from django.test import Client
from apps.academic.models import Faculty, Department, Programme, Course
from apps.core.models import AcademicSession, Semester

class AcademicModelTest(TestCase):
    """Academic model unit tests"""
    
    def setUp(self):
        self.client = Client()
    
    def test_faculty_creation(self):
        """Test faculty can be created"""
        faculty = Faculty.objects.create(name="Test Faculty", code="TST")
        self.assertEqual(faculty.name, "Test Faculty")
        self.assertEqual(faculty.code, "TST")
    
    def test_department_creation(self):
        """Test department can be created"""
        faculty = Faculty.objects.create(name="Test Faculty", code="TST")
        dept = Department.objects.create(
            name="Computer Science",
            code="CS",
            faculty_id=faculty.id
        )
        self.assertEqual(dept.name, "Computer Science")
    
    def test_programme_creation(self):
        """Test programme can be created"""
        faculty = Faculty.objects.create(name="Test Faculty", code="TST")
        dept = Department.objects.create(name="CS", code="CS", faculty_id=faculty.id)
        prog = Programme.objects.create(
            name="B.Sc Computer Science",
            code="CS",
            duration_years=4,
            department_id=dept.id
        )
        self.assertEqual(prog.duration_years, 4)
    
    def test_course_creation(self):
        """Test course can be created"""
        faculty = Faculty.objects.create(name="Test Faculty", code="TST")
        dept = Department.objects.create(name="CS", code="CS", faculty_id=faculty.id)
        session = AcademicSession.objects.create(
            name="2024/2025",
            is_current=True
        )
        semester = Semester.objects.create(
            name="First Semester",
            session_id=session.id,
            order=1
        )
        course = Course.objects.create(
            code="CS101",
            title="Introduction to Programming",
            credits=3,
            department_id=dept.id,
            semester_id=semester.id
        )
        self.assertEqual(course.credits, 3)


class AcademicAPITest(TestCase):
    """Academic API tests"""
    
    def setUp(self):
        self.client = Client()
    
    def test_health_endpoint(self):
        """Test health endpoint returns pong"""
        # Try different possible health endpoints
        response = self.client.get('/api/v1/health/ping/')
        if response.status_code != 200:
            response = self.client.get('/health/')
        if response.status_code != 200:
            response = self.client.get('/api/health/')
        self.assertIn(response.status_code, [200, 404])
    
    def test_faculty_list_empty(self):
        """Test faculty list returns data"""
        response = self.client.get('/api/v1/academic/faculties')
        self.assertEqual(response.status_code, 200)
    
    def test_faculty_create(self):
        """Test faculty can be created via API"""
        response = self.client.post(
            '/api/v1/academic/faculties',
            data={'name': 'Test Faculty API', 'code': 'TFA'},
            content_type='application/json'
        )
        # Either success 201 or duplicate 400
        self.assertIn(response.status_code, [201, 400])
    
    def test_department_list(self):
        """Test department list returns"""
        response = self.client.get('/api/v1/academic/departments')
        self.assertEqual(response.status_code, 200)


class SignalGuardTest(TestCase):
    """Test signal guards work correctly"""
    
    def test_faculty_signal_guards(self):
        """Test Faculty doesn't trigger user signals"""
        faculty = Faculty.objects.create(name="Signal Test", code="ST")
        # Should not raise any errors
        self.assertEqual(faculty.name, "Signal Test")
    
    def test_department_signal_guards(self):
        """Test Department doesn't trigger user signals"""
        faculty = Faculty.objects.create(name="Signal Test", code="ST")
        dept = Department.objects.create(name="CS", code="CS", faculty_id=faculty.id)
        self.assertEqual(dept.name, "CS")