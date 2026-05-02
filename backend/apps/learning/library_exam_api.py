"""
Library, Venue, Exam APIs
Library management, venues, timetables, exams
"""

from ninja import Router, Schema
from typing import List, Optional
from django.shortcuts import get_object_or_404

router = Router(tags=['Library_Exams'])


# === Library Schemas ===
class BookSchema(Schema):
    id: str
    isbn: str
    title: str
    author: str
    category: str
    available_copies: int


class BookLoanSchema(Schema):
    id: str
    book_id: str
    student_id: str
    due_date: str
    status: str


class BookBorrowSchema(Schema):
    book_id: str


class VenueSchema(Schema):
    id: str
    name: str
    code: str
    venue_type: str
    seating_capacity: int
    building: str


class VenueBookingSchema(Schema):
    venue_id: str
    course_id: Optional[str]
    day_of_week: str
    start_time: str
    end_time: str


class TimetableSchema(Schema):
    id: str
    course_id: str
    venue_id: Optional[str]
    lecturer_id: Optional[str]
    day: str
    start_time: str
    end_time: str


class ExamSittingSchema(Schema):
    exam_id: str
    venue_id: str
    date: str
    start_time: str
    end_time: str


class InvigilationSchema(Schema):
    exam_id: str
    venue_id: str
    invigilator_id: str
    is_principal: bool


# === Library APIs ===
@router.get('/books')
def list_books(request):
    """List all books."""
    from apps.learning.library import Book
    
    books = Book.objects.filter(is_active=True)
    
    return [
        {
            'id': str(b.id),
            'isbn': b.isbn,
            'title': b.title,
            'author': b.author,
            'category': b.category,
            'available': b.available_copies
        }
        for b in books
    ]


@router.get('/books/{isbn}')
def get_book(request, isbn: str):
    """Get book by ISBN."""
    from apps.learning.library import Book
    
    book = get_object_or_404(Book, isbn=isbn)
    
    return {
        'id': str(book.id),
        'title': book.title,
        'author': book.author,
        'available': book.available_copies,
        'total': book.total_copies,
        'shelf': book.shelf_location
    }


@router.post('/books/borrow')
def borrow_book(request, data: BookBorrowSchema):
    """Borrow a book."""
    from apps.learning.library import BookLoan, Book
    from apps.student.models import StudentProfile
    from django.utils import timezone
    from datetime import timedelta
    
    book = get_object_or_404(Book, id=data.book_id)
    
    if book.available_copies < 1:
        return {'error': 'Book not available'}
    
    student = StudentProfile.objects.filter(user=request.user).first()
    
    # Create loan
    loan = BookLoan.objects.create(
        book=book,
        student=student,
        due_date=timezone.now().date() + timedelta(days=14)
    )
    
    # Update book count
    book.available_copies -= 1
    book.save()
    
    return {'success': True, 'due_date': loan.due_date}


@router.post('/loans/{id}/return')
def return_book(request, id: str):
    """Return borrowed book."""
    from apps.learning.library import BookLoan, Book
    
    loan = get_object_or_404(BookLoan, id=id)
    
    loan.returned_at = timezone.now().date()
    loan.status = 'returned'
    loan.save()
    
    # Update book count
    book = loan.book
    book.available_copies += 1
    book.save()
    
    return {'success': True}


@router.get('/loans')
def list_loans(request):
    """List book loans."""
    from apps.learning.library import BookLoan
    
    loans = BookLoan.objects.all().order_by('-borrowed_at')
    
    return [
        {
            'id': str(l.id),
            'book': l.book.title,
            'student': l.student.user.email if l.student and l.student.user else None,
            'status': l.status,
            'due': str(l.due_date)
        }
        for l in loans
    ]


@router.get('/loans/overdue')
def list_overdue(request):
    """List overdue books."""
    from apps.learning.library import BookLoan
    from django.utils import timezone
    
    loans = BookLoan.objects.filter(
        status='borrowed',
        due_date__lt=timezone.now().date()
    )
    
    return [
        {
            'id': str(l.id),
            'student': l.student.user.email if l.student and l.student.user else None,
            'due': str(l.due_date)
        }
        for l in loans
    ]


# === Venue APIs ===
@router.get('/venues')
def list_venues(request):
    """List venues."""
    from apps.learning.exam_venues import Venue
    
    venues = Venue.objects.filter(is_active=True)
    
    return [
        {
            'id': str(v.id),
            'name': v.name,
            'code': v.code,
            'type': v.venue_type,
            'capacity': v.seating_capacity,
            'building': v.building
        }
        for v in venues
    ]


@router.get('/venues/{id}')
def get_venue(request, id: str):
    """Get venue details."""
    from apps.learning.exam_venues import Venue
    
    venue = get_object_or_404(Venue, id=id)
    
    return {
        'id': str(venue.id),
        'name': venue.name,
        'capacity': venue.seating_capacity,
        'exam_capacity': venue.exam_capacity,
        'has_projector': venue.has_projector,
        'has_ac': venue.has_ac
    }


@router.post('/venues/book')
def book_venue(request, data: VenueBookingSchema):
    """Book a venue."""
    from apps.learning.exam_venues import VenueBooking
    
    booking = VenueBooking.objects.create(
        venue_id=data.venue_id,
        course_id=data.course_id,
        day_of_week=data.day_of_week,
        start_time=data.start_time,
        end_time=data.end_time,
        status='pending',
        requested_by=request.user
    )
    
    # Get default session
    from apps.academic.models import AcademicSession
    session = AcademicSession.objects.filter(is_current=True).first()
    if session:
        booking.session = session
        booking.save()
    
    return {'success': True, 'id': str(booking.id)}


# === Timetable APIs ===
@router.get('/timetable')
def get_timetable(request):
    """Get current timetable."""
    from apps.learning.exam_venues import Timetable, TimetableSlot
    from apps.academic.models import AcademicSession, Semester
    
    session = AcademicSession.objects.filter(is_current=True).first()
    semester = Semester.objects.filter(is_current=True).first()
    
    if not session or not semester:
        return {'error': 'No active session'}
    
    tt = Timetable.objects.filter(
        session=session,
        semester=semester,
        status='published'
    ).first()
    
    if not tt:
        return {'timetable': None, 'slots': []}
    
    slots = TimetableSlot.objects.filter(timetable=tt)
    
    return {
        'id': str(tt.id),
        'status': tt.status,
        'slots': [
            {
                'course': s.course.code if s.course else None,
                'venue': s.venue.code if s.venue else None,
                'day': s.day,
                'start': str(s.start_time),
                'end': str(s.end_time)
            }
            for s in slots
        ]
    }


@router.get('/timetable/student/{student_id}')
def get_student_timetable(request, student_id: str):
    """Get student specific timetable."""
    from apps.learning.exam_venues import Timetable, TimetableSlot
    from apps.student.models import StudentProfile
    
    student = get_object_or_404(StudentProfile, id=student_id)
    # Get student courses and build timetable
    
    return {'student_id': student_id, 'slots': []}


@router.get('/timetable/lecturer/{lecturer_id}')
def get_lecturer_timetable(request, lecturer_id: str):
    """Get lecturer timetable."""
    from apps.learning.exam_venues import TimetableSlot
    
    slots = TimetableSlot.objects.filter(lecturer_id=lecturer_id)
    
    return [
        {
            'course': s.course.code if s.course else None,
            'day': s.day,
            'start': str(s.start_time),
            'end': str(s.end_time)
        }
        for s in slots
    ]


# === Exam Sitting ===
@router.post('/exam/sitting')
def create_exam_sitting(request, data: ExamSittingSchema):
    """Create exam sitting arrangement."""
    from apps.learning.exam_venues import ExamSitting
    from apps.learning.models import Exam
    
    exam = get_object_or_404(Exam, id=data.exam_id)
    
    sitting = ExamSitting.objects.create(
        exam_id=data.exam_id,
        venue_id=data.venue_id,
        date=data.date,
        start_time=data.start_time,
        end_time=data.end_time
    )
    
    # Get default session
    from apps.academic.models import AcademicSession, Semester
    session = AcademicSession.objects.filter(is_current=True).first()
    semester = Semester.objects.filter(is_current=True).first()
    if session:
        sitting.session = session
    if semester:
        sitting.semester = semester
    sitting.save()
    
    return {'success': True, 'id': str(sitting.id)}


@router.post('/exam/sitting/{id}/generate')
def generate_sitting(request, id: str):
    """Auto-generate sitting arrangement."""
    from apps.learning.exam_venues import ExamSitting
    from apps.student.models import StudentProfile
    
    sitting = get_object_or_404(ExamSitting, id=id)
    
    # Get registered students for exam
    from apps.learning.models import ExamRegistration
    registrations = ExamRegistration.objects.filter(exam=sitting.exam)
    
    # Get venue capacity
    capacity = sitting.venue.exam_capacity
    
    students_list = []
    seat = 1
    for i, reg in enumerate(registrations):
        row = chr(65 + (seat // 10))
        seat_num = seat % 10 if seat % 10 else 10
        
        students_list.append({
            'student_id': str(reg.student_id),
            'seat': f"{row}{seat_num}"
        })
        seat += 1
        if seat > capacity:
            break
    
    sitting.students = students_list
    sitting.is_published = True
    sitting.save()
    
    return {'success': True, 'students': len(students_list)}


@router.get('/exam/sitting/{id}')
def get_exam_sitting(request, id: str):
    """Get exam sitting."""
    from apps.learning.exam_venues import ExamSitting
    
    sitting = get_object_or_404(ExamSitting, id=id)
    
    return {
        'id': str(sitting.id),
        'exam': sitting.exam.title if sitting.exam else None,
        'venue': sitting.venue.name if sitting.venue else None,
        'date': str(sitting.date),
        'is_published': sitting.is_published,
        'students': sitting.students
    }


# === Invigilation ===
@router.get('/invigilation')
def list_invigilation(request):
    """List invigilation duties."""
    from apps.learning.exam_venues import ExamInvigilation
    
    duties = ExamInvigilation.objects.all()
    
    return [
        {
            'id': str(d.id),
            'exam': d.exam.title if d.exam else None,
            'venue': d.venue.name if d.venue else None,
            'invigilator': d.invigilator.user.get_full_name() if d.invigilator and d.invigilator.user else None,
            'status': d.status
        }
        for d in duties
    ]


@router.post('/invigilation')
def assign_invigilation(request, data: InvigilationSchema):
    """Assign invigilation."""
    from apps.learning.exam_venues import ExamInvigilation
    
    duty = ExamInvigilation.objects.create(
        exam_id=data.exam_id,
        venue_id=data.venue_id,
        invigilator_id=data.invigilator_id,
        is_principal=data.is_principal
    )
    
    return {'success': True, 'id': str(duty.id)}


@router.post('/invigilation/{id}/report')
def submit_invigilation_report(request, id: str, students_present: int, incidents: str = ''):
    """Submit invigilation report."""
    from apps.learning.exam_venues import ExamInvigilation
    from django.utils import timezone
    
    duty = get_object_or_404(ExamInvigilation, id=id)
    duty.students_present = students_present
    duty.incidents = incidents
    duty.status = 'reported'
    duty.save()
    
    return {'success': True}