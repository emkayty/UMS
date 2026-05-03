import uuid
from django.db import models
from apps.accounts.models import User


# ============================================================
# NIGERIAN UNIVERSITY & POLYTECHNIC PROGRAMME TYPES
# ============================================================

class ProgrammeType(models.TextChoices):
    # Universities (NUC)
    BSc = 'bsc', 'Bachelor of Science (BSc)'
    BA = 'ba', 'Bachelor of Arts (BA)'
    BScEd = 'bsced', 'Bachelor of Education (BSc.Ed)'
    BTech = 'btch', 'Bachelor of Technology (BTech)'
    LLB = 'llb', 'Bachelor of Law (LLB)'
    MBBS = 'mbbs', 'Bachelor of Medicine (MBBS)'
    BPharm = 'bpharm', 'Bachelor of Pharmacy'
    BScN = 'bscn', 'Bachelor of Nursing'
    MSc = 'msc', 'Master of Science (MSc)'
    MA = 'ma', 'Master of Arts (MA)'
    MTech = 'mtech', 'Master of Technology (MTech)'
    PhD = 'phd', 'Doctor of Philosophy (PhD)'
    
    # Polytechnics (NBTE)
    ND = 'nd', 'National Diploma (ND)'
    HND = 'hnd', 'Higher National Diploma (HND)'
    PGD = 'pgd', 'Postgraduate Diploma'
    
    # Education
    PGDE = 'pgde', 'Postgraduate Diploma in Education'
    
    # ============================================================
    # AMERICAN UNIVERSITY DEGREE TYPES
    # ============================================================
    
    # Associate Degrees (Community College)
    AA = 'aa', 'Associate of Arts (AA)'
    AS = 'as', 'Associate of Science (AS)'
    AAS = 'aas', 'Associate of Applied Science (AAS)'
    ABA = 'aba', 'Associate of Business Administration'
    
    # Bachelor Degrees
    BBA = 'bba', 'Bachelor of Business Administration (BBA)'
    BS = 'bs', 'Bachelor of Science (BS)'
    BAL = 'bal', 'Bachelor of Arts (Liberal Arts)'
    BE = 'be', 'Bachelor of Engineering'
    BSN = 'bsn', 'Bachelor of Science in Nursing'
    
    # Master Degrees
    MBA = 'mba', 'Master of Business Administration (MBA)'
    MPA = 'mpa', 'Master of Public Administration'
    MPH = 'mph', 'Master of Public Health'
    MEd = 'med', 'Master of Education'
    MSW = 'msw', 'Master of Social Work'
    
    # Doctoral Degrees
    EdD = 'edd', 'Doctor of Education (EdD)'
    DBA = 'dba', 'Doctor of Business Administration'
    MD = 'md', 'Doctor of Medicine (MD)'
    DDS = 'dds', 'Doctor of Dental Surgery'
    PharmD = 'pharmd', 'Doctor of Pharmacy'


class GradeLetter(models.TextChoices):
    # ============================================================
    # NIGERIAN GRADING SYSTEM
    # ============================================================
    A = 'A', 'Excellent (70-100%)'
    B = 'B', 'Very Good (60-69%)'
    C = 'C', 'Good (50-59%)'
    D = 'D', 'Satisfactory (45-49%)'
    E = 'E', 'Pass (40-44%)'
    F = 'F', 'Fail (0-39%)'


class GradePoint(models.TextChoices):
    """
    Grade Points for CGPA calculation.
    Nigerian: A=5, B=4, C=3, D=2, E=1, F=0
    """
    A = 'A', '5 points'
    B = 'B', '4 points'
    C = 'C', '3 points'
    D = 'D', '2 points'
    E = 'E', '1 point'
    F = 'F', '0 points'


class USGradeLetter(models.TextChoices):
    """
    American Grading System (4.0 Scale).
    Used by US universities and adopted by some international institutions.
    """
    A_PLUS = 'A+', 'A+ (97-100%) - 4.0'
    A = 'A', 'A (93-96%) - 4.0'
    A_MINUS = 'A-', 'A- (90-92%) - 3.7'
    B_PLUS = 'B+', 'B+ (87-89%) - 3.3'
    B = 'B', 'B (83-86%) - 3.0'
    B_MINUS = 'B-', 'B- (80-82%) - 2.7'
    C_PLUS = 'C+', 'C+ (77-79%) - 2.3'
    C = 'C', 'C (73-76%) - 2.0'
    C_MINUS = 'C-', 'C- (70-72%) - 1.7'
    D_PLUS = 'D+', 'D+ (67-69%) - 1.3'
    D = 'D', 'D (63-66%) - 1.0'
    D_MINUS = 'D-', 'D- (60-62%) - 0.7'
    F = 'F', 'F (0-59%) - 0.0'


class USGradePoint(models.TextChoices):
    """
    American Grade Point Values (4.0 Scale).
    """
    A_PLUS = '4.0', '4.0'
    A = '4.0', '4.0'
    A_MINUS = '3.7', '3.7'
    B_PLUS = '3.3', '3.3'
    B = '3.0', '3.0'
    B_MINUS = '2.7', '2.7'
    C_PLUS = '2.3', '2.3'
    C = '2.0', '2.0'
    C_MINUS = '1.7', '1.7'
    D_PLUS = '1.3', '1.3'
    D = '1.0', '1.0'
    D_MINUS = '0.7', '0.7'
    F = '0.0', '0.0'


class Faculty(models.Model):
    """Faculty model - Nigerian University structure."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=10, unique=True, db_index=True)
    dean = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='dean_of'
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
        related_name='hod_of'
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