"""
Library Management System
Books, borrowing, fines, reserves
"""

from django.db import models
import uuid


class Library(models.Model):
    """Library branch/location."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    
    capacity = models.IntegerField(default=200)
    current_occupancy = models.IntegerField(default=0)
    
    is_active = models.BooleanField(default=True)


class Book(models.Model):
    """Library book catalog."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    isbn = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    
    year = models.IntegerField()
    edition = models.CharField(max_length=50, blank=True)
    
    CATEGORY = [
        ('textbook', 'Textbook'),
        ('reference', 'Reference'),
        ('journal', 'Journal'),
        ('novel', 'Novel'),
        ('thesis', 'Thesis'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY)
    
    # Copies
    total_copies = models.IntegerField(default=1)
    available_copies = models.IntegerField(default=1)
    
    # Location
    shelf_location = models.CharField(max_length=50, blank=True)
    floor = models.IntegerField(default=1)
    
    # Status
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class BookLoan(models.Model):
    """Book borrowing records."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='loans'
    )
    student = models.ForeignKey(
        'student.StudentProfile',
        on_delete=models.CASCADE,
        related_name='book_loans'
    )
    
    # Dates
    borrowed_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    returned_at = models.DateField(null=True, blank=True)
    
    STATUS = [
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
        ('lost', 'Lost'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='borrowed')
    
    # Fine
    fine_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    fine_paid = models.BooleanField(default=False)
    
    renewed_count = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['book', 'student', 'status']


class BookReservation(models.Model):
    """Reserved books."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    student = models.ForeignKey(
        'student.StudentProfile',
        on_delete=models.CASCADE
    )
    
    reserved_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateField()
    
    STATUS = [
        ('pending', 'Pending'),
        ('available', 'Available'),
        ('collected', 'Collected'),
        ('expired', 'Expired'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='pending')


class LibraryFine(models.Model):
    """Library fine records."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey(
        'student.StudentProfile',
        on_delete=models.CASCADE,
        related_name='library_fines'
    )
    
    loan = models.ForeignKey(
        BookLoan,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    REASON = [
        ('overdue', 'Overdue'),
        ('lost', 'Lost Book'),
        ('damaged', 'Damaged'),
    ]
    reason = models.CharField(max_length=20, choices=REASON)
    
    STATUS = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('waived', 'Waived'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)


class StudyRoom(models.Model):
    """Library study rooms."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    library = models.ForeignKey(
        Library,
        on_delete=models.CASCADE,
        related_name='rooms'
    )
    
    room_number = models.CharField(max_length=20)
    capacity = models.IntegerField(default=10)
    
    # Booking
    can_book = models.BooleanField(default=True)
    booking_slots = models.JSONField(default=list)
    # ['08:00-10:00', '10:00-12:00']
    
    is_active = models.BooleanField(default=True)


class StudyRoomBooking(models.Model):
    """Study room bookings."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    room = models.ForeignKey(StudyRoom, on_delete=models.CASCADE)
    student = models.ForeignKey(
        'student.StudentProfile',
        on_delete=models.CASCADE
    )
    
    date = models.DateField()
    time_slot = models.CharField(max_length=20)
    
    STATUS = [
        ('booked', 'Booked'),
        ('used', 'Used'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='booked')
    
    class Meta:
        unique_together = ['room', 'date', 'time_slot']