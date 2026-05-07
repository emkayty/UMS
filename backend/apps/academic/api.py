from ninja import Router, Schema
from typing import Optional, List
from uuid import UUID
from django.shortcuts import get_object_or_404

from apps.academic.models import (
    Faculty, Department, Programme, Course, CoursePrerequisite,
    AcademicSession, Semester
)
from apps.academic.grading import GradingPolicy

router = Router(tags=['Academic Structure'])


# === Schemas ===
class FacultySchema(Schema):
    id: UUID  # Changed from str to UUID
    name: str
    code: str
    dean_id: Optional[UUID] = None


class FacultyCreateSchema(Schema):
    name: str
    code: str
    dean_id: Optional[UUID] = None


class DepartmentSchema(Schema):
    id: UUID
    name: str
    code: str
    faculty_id: UUID
    hod_id: Optional[UUID] = None


class DepartmentCreateSchema(Schema):
    name: str
    code: str
    faculty_id: UUID
    hod_id: Optional[UUID] = None


class ProgrammeSchema(Schema):
    id: UUID
    name: str
    code: str
    duration_years: int
    department_id: UUID


class ProgrammeCreateSchema(Schema):
    name: str
    code: str
    duration_years: int
    department_id: UUID


class CourseSchema(Schema):
    id: UUID
    code: str
    title: str
    credit_units: int
    level: int
    semester: int
    semester_offered: list
    programme_id: UUID
    department_id: UUID
    has_prerequisites: bool


class GradingPolicySchema(Schema):
    id: UUID
    name: str
    scale_type: str
    grade_boundaries: list
    pass_mark: int
    max_score: int
    faculty_id: Optional[UUID] = None
    programme_id: Optional[UUID] = None
    course_id: Optional[UUID] = None


class AcademicSessionSchema(Schema):
    id: UUID
    name: str
    start_date: str
    end_date: str
    is_current: bool


class SemesterSchema(Schema):
    id: UUID
    session_id: UUID
    name: str
    start_date: str
    end_date: str
    registration_start: str
    registration_end: str
    add_drop_end: Optional[str] = None


# === Faculty APIs ===
@router.get('/faculties', response=List[FacultySchema])
def list_faculties(request):
    return Faculty.objects.all()


@router.post('/faculties', response=FacultySchema)
def create_faculty(request, data: FacultyCreateSchema):
    faculty = Faculty.objects.create(
        name=data.name,
        code=data.code,
        dean_id=data.dean_id
    )
    return faculty


@router.get('/faculties/{id}', response=FacultySchema)
def get_faculty(request, id: str):
    return get_object_or_404(Faculty, id=id)


@router.patch('/faculties/{id}', response=FacultySchema)
def update_faculty(request, id: str, data: FacultySchema):
    faculty = get_object_or_404(Faculty, id=id)
    for field in ['name', 'code', 'dean_id']:
        value = getattr(data, field, None)
        if value is not None:
            setattr(faculty, field, value)
    faculty.save()
    return faculty


@router.delete('/faculties/{id}')
def delete_faculty(request, id: str):
    faculty = get_object_or_404(Faculty, id=id)
    faculty.delete()
    return {'success': True}


# === Department APIs ===
@router.get('/departments', response=List[DepartmentSchema])
def list_departments(request, faculty_id: UUID = None):
    qs = Department.objects.all()
    if faculty_id:
        qs = qs.filter(faculty_id=faculty_id)
    return qs[:100]


@router.post('/departments', response=DepartmentSchema)
def create_department(request, data: DepartmentCreateSchema):
    dept = Department.objects.create(
        name=data.name,
        code=data.code,
        faculty_id=data.faculty_id,
        hod_id=data.hod_id
    )
    return dept


@router.get('/departments/{id}', response=DepartmentSchema)
def get_department(request, id: str):
    return get_object_or_404(Department, id=id)


@router.patch('/departments/{id}', response=DepartmentSchema)
def update_department(request, id: str, data: DepartmentSchema):
    dept = get_object_or_404(Department, id=id)
    for field in ['name', 'code', 'faculty_id', 'hod_id']:
        value = getattr(data, field, None)
        if value is not None:
            setattr(dept, field, value)
    dept.save()
    return dept


@router.delete('/departments/{id}')
def delete_department(request, id: str):
    dept = get_object_or_404(Department, id=id)
    dept.delete()
    return {'success': True}


# === Programme APIs ===
@router.get('/programmes', response=List[ProgrammeSchema])
def list_programmes(request, department_id: UUID = None):
    qs = Programme.objects.all()
    if department_id:
        qs = qs.filter(department_id=department_id)
    return qs


@router.post('/programmes', response=ProgrammeSchema)
def create_programme(request, data: ProgrammeCreateSchema):
    prog = Programme.objects.create(
        name=data.name,
        code=data.code,
        duration_years=data.duration_years,
        department_id=data.department_id
    )
    return prog


# === Course APIs ===
@router.get('/courses', response=List[CourseSchema])
def list_courses(request, programme_id: UUID = None, level: int = None):
    qs = Course.objects.all()
    if programme_id:
        qs = qs.filter(programme_id=programme_id)
    if level:
        qs = qs.filter(level=level)
    return qs


@router.post('/courses', response=CourseSchema)
def create_course(request, data: CourseSchema):
    course = Course.objects.create(
        code=data.code,
        title=data.title,
        credit_units=data.credit_units,
        level=data.level,
        semester=data.semester,
        semester_offered=data.semester_offered,
        programme_id=data.programme_id,
        department_id=data.department_id,
        has_prerequisites=data.has_prerequisites
    )
    return course


# === Grading Policy APIs ===
@router.get('/grading-policies', response=List[GradingPolicySchema])
def list_grading_policies(request):
    return GradingPolicy.objects.all()


@router.post('/grading-policies', response=GradingPolicySchema)
def create_grading_policy(request, data: GradingPolicySchema):
    policy = GradingPolicy.objects.create(
        name=data.name,
        scale_type=data.scale_type,
        grade_boundaries=data.grade_boundaries,
        pass_mark=data.pass_mark,
        max_score=data.max_score,
        faculty_id=data.faculty_id,
        programme_id=data.programme_id,
        course_id=data.course_id
    )
    return policy


@router.get('/grading-policies/{id}', response=GradingPolicySchema)
def get_grading_policy(request, id: str):
    return get_object_or_404(GradingPolicy, id=id)


@router.get('/resolve-grading-policy')
def resolve_grading_policy(request, registration_id: UUID = None, course_id: UUID = None, 
                     programme_id: UUID = None, faculty_id: UUID = None):
    """Resolve effective grading policy with inheritance."""
    policy = GradingPolicy.resolve_policy(course_id, programme_id, faculty_id)
    return GradingPolicySchema(
        id=str(policy.id),
        name=policy.name,
        scale_type=policy.scale_type,
        grade_boundaries=policy.grade_boundaries,
        pass_mark=policy.pass_mark,
        max_score=policy.max_score
    )


# === Academic Session APIs ===
@router.get('/sessions', response=List[AcademicSessionSchema])
def list_sessions(request):
    return AcademicSession.objects.all()


@router.post('/sessions', response=AcademicSessionSchema)
def create_session(request, data: AcademicSessionSchema):
    session = AcademicSession.objects.create(
        name=data.name,
        start_date=data.start_date,
        end_date=data.end_date,
        is_current=data.is_current
    )
    return session


# === Semester APIs ===
@router.get('/semesters', response=List[SemesterSchema])
def list_semesters(request, session_id: UUID = None):
    qs = Semester.objects.all()
    if session_id:
        qs = qs.filter(session_id=session_id)
    return qs


@router.post('/semesters', response=SemesterSchema)
def create_semester(request, data: SemesterSchema):
    semester = Semester.objects.create(
        session_id=data.session_id,
        name=data.name,
        start_date=data.start_date,
        end_date=data.end_date,
        registration_start=data.registration_start,
        registration_end=data.registration_end,
        add_drop_end=data.add_drop_end
    )
    return semester