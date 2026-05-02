import uuid
from django.db import models
from apps.accounts.models import User


class Faculty(models.Model):
    """Faculty model."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=10, unique=True, db_index=True)
    dean = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='dean_of', limit_choices_to={'role': 'dean'}
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'faculties'
        ordering = ['name']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"


class Department(models.Model):
    """Department model."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=10, db_index=True)
    faculty = models.ForeignKey(
        Faculty, on_delete=models.CASCADE, related_name='departments'
    )
    hod = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='hod_of', limit_choices_to={'role': 'hod'}
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'departments'
        unique_together = ['code', 'faculty']
        ordering = ['faculty', 'name']
        indexes = [
            models.Index(fields=['code', 'faculty']),
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"


class Programme(models.Model):
    """Programme model."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, db_index=True)
    duration_years = models.IntegerField(default=4)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name='programmes'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'programmes'
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"


class Course(models.Model):
    """Course model."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10)
    title = models.CharField(max_length=200)
    credit_units = models.IntegerField(default=3)
    level = models.IntegerField(default=100, help_text='Level e.g. 100, 200, 300, 400')
    semester = models.IntegerField(default=1, help_text='1 or 2')
    semester_offered = models.JSONField(
        default=list, help_text='Semesters course is offered e.g. [1, 2]'
    )
    programme = models.ForeignKey(
        Programme, on_delete=models.CASCADE, related_name='courses'
    )
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name='courses'
    )
    has_prerequisites = models.BooleanField(default=False)
    # Bologna/ECTS compliance
    learning_hours = models.IntegerField(
        default=150, help_text='Total learning hours per semester (1 credit = 25-30 hours)'
    )
    ects_credits = models.FloatField(
        default=3.0, help_text='ECTS credits (1 credit = 30 hours)'
    )
    # Course metadata
    is_elective = models.BooleanField(default=False)
    max_students = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'courses'
        unique_together = ['code', 'programme', 'level']
        ordering = ['level', 'code']

    def __str__(self):
        return f"{self.code} - {self.title}"


class CoursePrerequisite(models.Model):
    """Course prerequisites."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='prerequisites'
    )
    prerequisite_course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='required_for'
    )
    minimum_grade = models.CharField(max_length=2, blank=True)

    class Meta:
        db_table = 'course_prerequisites'
        unique_together = ['course', 'prerequisite_course']

    def __str__(self):
        return f"{self.course.code} requires {self.prerequisite_course.code}"


class AcademicSession(models.Model):
    """Academic session."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, help_text='e.g. 2023/2024')
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'academic_sessions'
        ordering = ['-start_date']

    def save(self, *args, **kwargs):
        if self.is_current:
            AcademicSession.objects.filter(is_current=True).update(is_current=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Semester(models.Model):
    """Semester within an academic session."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(
        AcademicSession, on_delete=models.CASCADE, related_name='semesters'
    )
    name = models.CharField(max_length=50, help_text='e.g. First Semester')
    start_date = models.DateField()
    end_date = models.DateField()
    registration_start = models.DateField()
    registration_end = models.DateField()
    add_drop_end = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'semesters'
        unique_together = ['session', 'name']
        ordering = ['session', 'start_date']

    def __str__(self):
        return f"{self.session.name} - {self.name}"