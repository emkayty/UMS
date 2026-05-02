"""
Exams, Venues, Timetables, Invigilation
Exam management and sitting arrangements
"""

from django.db import models
import uuid


class Venue(models.Model):
    """Exam/lecture venue."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    
    TYPE = [
        ('lecture_hall', 'Lecture Hall'),
        ('exam_hall', 'Exam Hall'),
        ('classroom', 'Classroom'),
        ('auditorium', 'Auditorium'),
        ('open_space', 'Open Space'),
    ]
    venue_type = models.CharField(max_length=20, choices=TYPE)
    
    # Capacity
    seating_capacity = models.IntegerField(default=50)
    exam_capacity = models.IntegerField(default=40)
    
    # Location
    building = models.CharField(max_length=100)
    floor = models.IntegerField(default=1)
    
    # Amenities
    has_projector = models.BooleanField(default=False)
    has_whiteboard = models.BooleanField(default=True)
    has_ac = models.BooleanField(default=False)
    has_podium = models.BooleanField(default=False)
    
    # Status
    is_active = models.BooleanField(default=True)


class VenueBooking(models.Model):
    """Venue booking/allocation."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    venue = models.ForeignKey(
        Venue,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    
    # Course or exam
    course = models.ForeignKey(
        'academic.Course',
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    exam = models.ForeignKey(
        'learning.Exam',
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    
    session = models.ForeignKey('academic.AcademicSession', on_delete=models.CASCADE)
    semester = models.ForeignKey('academic.Semester', on_delete=models.CASCADE)
    
    # Time
    day_of_week = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    # Status
    STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    
    requested_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True, related_name='+'
    )
    
    class Meta:
        unique_together = ['venue', 'session', 'semester', 'day_of_week', 'start_time']


class Timetable(models.Model):
    """Master timetable."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    session = models.ForeignKey('academic.AcademicSession', on_delete=models.CASCADE)
    semester = models.ForeignKey('academic.Semester', on_delete=models.CASCADE)
    
    # Status
    STATUS = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('locked', 'Locked'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='draft')
    
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class TimetableSlot(models.Model):
    """Timetable slot."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    timetable = models.ForeignKey(
        Timetable,
        on_delete=models.CASCADE,
        related_name='slots'
    )
    
    course = models.ForeignKey('academic.Course', on_delete=models.CASCADE)
    venue = models.ForeignKey(
        Venue,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    lecturer = models.ForeignKey(
        'staff.StaffProfile',
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    
    # Time
    day = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    # Week pattern
    week_pattern = models.JSONField(default=list)
    # [1, 2, 3, 4] - weeks
    
    class Meta:
        unique_together = ['timetable', 'day', 'start_time', 'venue']


class ExamSitting(models.Model):
    """Exam sitting arrangement."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    exam = models.ForeignKey(
        'learning.Exam',
        on_delete=models.CASCADE,
        related_name='sittings'
    )
    session = models.ForeignKey('academic.AcademicSession', on_delete=models.CASCADE)
    semester = models.ForeignKey('academic.Semester', on_delete=models.CASCADE)
    
    # Venue
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    
    # Sitting arrangement
    students = models.JSONField(default=list)
    # [{'student_id': '...', 'seat': 'A1'}]
    
    # Time
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    # Status
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class ExamAttendance(models.Model):
    """Exam attendance tracking."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    exam = models.ForeignKey('learning.Exam', on_delete=models.CASCADE)
    student = models.ForeignKey(
        'student.StudentProfile',
        on_delete=models.CASCADE,
        related_name='exam_attendance'
    )
    
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    
    STATUS = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='absent')
    
    minutes_late = models.IntegerField(default=0)
    arrival_time = models.TimeField(null=True, blank=True)
    
    invigilator = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True, related_name='+'
    )
    
    marked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['exam', 'student']


class ExamInvigilation(models.Model):
    """Invigilation assignments (more detailed)."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    exam = models.ForeignKey('learning.Exam', on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    
    invigilator = models.ForeignKey(
        'staff.StaffProfile',
        on_delete=models.CASCADE,
        related_name='invigilation_duties'
    )
    
    is_principal = models.BooleanField(default=False)
    
    STATUS = [
        ('assigned', 'Assigned'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('reported', 'Reported'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='assigned')
    
    # Report
    students_present = models.IntegerField(default=0)
    students_absent = models.IntegerField(default=0)
    incidents = models.TextField(blank=True)
    
    # Time
    arrived_at = models.TimeField(null=True, blank=True)
    left_at = models.TimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['exam', 'venue', 'invigilator']