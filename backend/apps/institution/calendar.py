"""
Academic Calendar System
Events, schedules, and academic calendar management
"""

import uuid
from django.db import models


class CalendarEventType(models.TextChoices):
    # Academic Events
    LECTURE = 'lecture', 'Lectures'
    EXAM = 'exam', 'Examination'
    REGISTRATION = 'registration', 'Course Registration'
    ADD_DROP = 'add_drop', 'Add/Drop'
    START_SESSION = 'start_session', 'Session Start'
    END_SESSION = 'end_session', 'Session End'
    MATRICULATION = 'matriculation', 'Matriculation'
    CONVOCATION = 'convocation', 'Convocation'
    ORIENTATION = 'orientation', 'Freshers/Returning Orientation'
    
    # Administrative
    STAFF_MEETING = 'staff_meeting', 'Staff Meeting'
    SENATE = 'senate', 'Senate Meeting'
    COUNCIL = 'council', 'Council Meeting'
    HOD_MEETING = 'hod_meeting', 'HOD Meeting'
    
    # Sports & Activities
    SPORTS = 'sports', 'Sports'
    CULTURAL = 'cultural', 'Cultural Day'
    EXCURSION = 'excursion', 'Excursion'
    
    # Payments
    FEE_DEADLINE = 'fee_deadline', 'Fee Payment Deadline'
    FEE_REMINDER = 'fee_reminder', 'Fee Reminder'


class EventStatus(models.TextChoices):
    SCHEDULED = 'scheduled', 'Scheduled'
    ONGOING = 'ongoing', 'Ongoing'
    COMPLETED = 'completed', 'Completed'
    CANCELLED = 'cancelled', 'Cancelled'
    POSTPONED = 'postponed', 'Postponed'


# ============================================================
# ACADEMIC CALENDAR
# ============================================================

class AcademicCalendar(models.Model):
    """Academic calendar - session events."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    session = models.ForeignKey(
        'academic.AcademicSession', on_delete=models.CASCADE,
        related_name='calendar'
    )
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'academic_calendars'

    def __str__(self):
        return f"{self.session.name} - Calendar"


# ============================================================
# CALENDAR EVENT
# ============================================================

class CalendarEvent(models.Model):
    """Academic event in the calendar."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    calendar = models.ForeignKey(
        AcademicCalendar, on_delete=models.CASCADE,
        related_name='events'
    )
    
    # Event Details
    event_type = models.CharField(
        max_length=20, choices=CalendarEventType.choices
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Date & Time
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    
    # All day
    is_all_day = models.BooleanField(default=True)
    
    # Recurrence
    recurrence = models.CharField(
        max_length=20, blank=True,
        choices=[
            ('', 'None'),
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
        ]
    )
    recurrence_end = models.DateField(null=True, blank=True)
    
    # Status
    status = models.CharField(
        max_length=20, choices=EventStatus.choices,
        default=EventStatus.SCHEDULED
    )
    
    # Venue
    venue = models.CharField(max_length=200, blank=True)
    virtual_link = models.URLField(blank=True)
    
    # Target
    target_levels = models.JSONField(default=list, blank=True)
    target_programmes = models.JSONField(default=list, blank=True)
    target_departments = models.JSONField(default=list, blank=True)
    
    # Notifications
    send_reminder = models.BooleanField(default=True)
    reminder_days = models.JSONField(default=list)
    
    # Visibility
    is_public = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'calendar_events'
        ordering = ['start_date', 'start_time']

    def __str__(self):
        return f"{self.title} - {self.start_date}"


# ============================================================
# SCHEDULE (TIMETABLE)
# ============================================================

class Timetable(models.Model):
    """Course schedule/timetable."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    session = models.ForeignKey(
        'academic.AcademicSession', on_delete=models.CASCADE
    )
    programme = models.ForeignKey(
        'academic.Programme', on_delete=models.CASCADE
    )
    level = models.IntegerField()
    semester = models.IntegerField()
    
    is_active = models.BooleanField(default=True)
    approved_by = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL,
        null=True, blank=True
    )
    approved_at = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'timetables'
        unique_together = ['session', 'programme', 'level', 'semester']

    def __str__(self):
        return f"{self.programme.code} - {self.level}L"


class TimetableSlot(models.Model):
    """Individual timetable slot."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    timetable = models.ForeignKey(
        Timetable, on_delete=models.CASCADE,
        related_name='slots'
    )
    
    # Day & Time
    day_of_week = models.CharField(
        max_length=15,
        choices=[
            ('monday', 'Monday'),
            ('tuesday', 'Tuesday'),
            ('wednesday', 'Wednesday'),
            ('thursday', 'Thursday'),
            ('friday', 'Friday'),
            ('saturday', 'Saturday'),
        ]
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    # Course
    course = models.ForeignKey(
        'academic.Course', on_delete=models.CASCADE
    )
    
    # Venue
    venue = models.CharField(max_length=100)
    
    # Lecturer
    lecturer = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='timetable_slots'
    )
    
    # Virtual
    virtual_link = models.URLField(blank=True)
    
    class Meta:
        db_table = 'timetable_slots'
        unique_together = ['timetable', 'day_of_week', 'start_time']

    def __str__(self):
        return f"{self.day_of_week} {self.start_time} - {self.course.code}"


# ============================================================
# REMINDER
# ============================================================

class EventReminder(models.Model):
    """Reminders for events."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    event = models.ForeignKey(
        CalendarEvent, on_delete=models.CASCADE,
        related_name='reminders'
    )
    
    days_before = models.IntegerField()
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'event_reminders'

    def __str__(self):
        return f"{self.event.title} - {self.days_before} days"