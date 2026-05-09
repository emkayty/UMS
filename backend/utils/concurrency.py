"""
Concurrency Utilities with type hints
High-Concurrency Transaction Utilities
Provides safe transaction patterns for high-concurrency operations
"""

import hashlib
import uuid
from functools import wraps
from typing import Callable, Any, Optional, List, Dict
from django.db import transaction
from django.db.models import F


class IdempotencyManager:
    """
    Manages idempotency keys to prevent duplicate operations
    Use for: payments, registrations, approvals
    """
    
    @staticmethod
    def generate_key() -> str:
        """Generate a unique idempotency key"""
        return str(uuid.uuid4())
    
    @staticmethod
    def hash_key(data: str) -> str:
        """Create a deterministic key from data"""
        return hashlib.sha256(data.encode()).hexdigest()[:32]


def idempotent_operation(
    key_field: str = 'idempotency_key',
    model_class: Any = None,
    lookup_field: str = 'idempotency_key'
):
    """
    Decorator to make an operation idempotent
    
    Usage:
        @idempotent_operation(key_field='payment_key', model_class=Payment)
        def process_payment(payment, data):
            # Process payment
            pass
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get idempotency key from kwargs
            idempotency_key = kwargs.get(key_field)
            
            if not idempotency_key:
                # Generate if not provided
                idempotency_key = IdempotencyManager.generate_key()
                kwargs[key_field] = idempotency_key
            
            # Check if already processed
            if model_class:
                existing = model_class.objects.filter(
                    **{lookup_field: idempotency_key}
                ).first()
                
                if existing:
                    return existing  # Return existing record
            
            # Execute operation
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


class TransactionSafeGPA:
    """
    Transaction-safe GPA calculation
    Prevents race conditions when calculating GPA
    """
    
    @staticmethod
    def calculate(
        student,
        session=None,
        use_locking=True
    ):
        """
        Calculate GPA with proper transaction safety
        
        Args:
            student: Student user
            session: AcademicSession (optional)
            use_locking: Use row-level locking
        """
        from apps.core.models import Result
        
        # Build query
        queryset = Result.objects.filter(student=student)
        
        if session:
            queryset = queryset.filter(course__session=session)
        
        # Apply locking if requested
        if use_locking:
            queryset = queryset.select_for_update()
        
        # Get results
        results = list(queryset.select_related('course'))
        
        if not results:
            return 0.0
        
        # Calculate GPA
        total_points = 0
        total_units = 0
        
        for result in results:
            if result.grade_point and result.course:
                gp = float(result.grade_point)
                units = result.course.credit_units
                total_points += gp * units
                total_units += units
        
        if total_units == 0:
            return 0.0
        
        return round(total_points / total_units, 2)


class CourseCapacityManager:
    """
    Manages course capacity with proper locking
    Prevents over-registration
    """
    
    @staticmethod
    @transaction.atomic
    def register_student(student, course, force=False):
        """
        Register student for course with atomic capacity check
        
        Args:
            student: Student user
            course: Course model
            force: Skip capacity check (for admins)
            
        Returns:
            Registration or raises exception
        """
        from apps.student.models import CourseRegistration
        from django.core.exceptions import ValidationError
        
        # Lock the course row
        course = Course.objects.select_for_update().get(id=course.id)
        
        # Check capacity (unless forced)
        if not force:
            if course.max_capacity and course.current_registration_count >= course.max_capacity:
                raise ValidationError(
                    f"Course {course.code} is full. Maximum capacity: {course.max_capacity}"
                )
        
        # Check if already registered
        existing = CourseRegistration.objects.filter(
            student=student,
            course=course,
            status__in=['registered', 'completed']
        ).first()
        
        if existing:
            raise ValidationError(f"Already registered for {course.code}")
        
        # Create registration
        registration = CourseRegistration.objects.create(
            student=student,
            course=course,
            session=course.session,
            semester=course.semester,
            status='registered'
        )
        
        # Increment capacity
        Course.objects.filter(id=course.id).update(
            current_registration_count=F('current_registration_count') + 1
        )
        
        return registration
    
    @staticmethod
    @transaction.atomic
    def drop_registration(registration):
        """
        Drop course registration with atomic capacity update
        """
        course = registration.course
        
        # Delete registration
        registration.delete()
        
        # Decrement capacity
        Course.objects.filter(id=course.id).update(
            current_registration_count=F('current_registration_count') - 1
        )


class PaymentTransactionManager:
    """
    Manages payment transactions with idempotency
    Prevents duplicate payments
    """
    
    @staticmethod
    @transaction.atomic
    def process_payment(
        student,
        amount,
        payment_type,
        idempotency_key=None,
        metadata=None
    ):
        """
        Process payment with idempotency guarantee
        
        Args:
            student: Student user
            amount: Payment amount
            payment_type: Type of payment
            idempotency_key: Unique key for idempotency
            metadata: Additional payment data
            
        Returns:
            Payment object
        """
        from apps.finance.models import Payment, PaymentStatus
        
        # Generate idempotency key if not provided
        if not idempotency_key:
            idempotency_key = IdempotencyManager.generate_key()
        
        # Check for existing payment
        existing = Payment.objects.filter(
            idempotency_key=idempotency_key
        ).first()
        
        if existing:
            return existing  # Return existing, don't process again
        
        # Create payment
        payment = Payment.objects.create(
            student=student,
            amount=amount,
            payment_type=payment_type,
            status=PaymentStatus.PENDING,
            idempotency_key=idempotency_key,
            metadata=metadata or {}
        )
        
        # Process payment (simulated)
        payment.status = PaymentStatus.COMPLETED
        payment.save()
        
        return payment


class DistributedLock:
    """
    Distributed lock using Redis
    For coordinating across multiple processes
    """
    
    @staticmethod
    def acquire(lock_name: str, timeout: int = 30) -> bool:
        """
        Acquire a distributed lock
        
        Args:
            lock_name: Name of the lock
            timeout: Lock timeout in seconds
            
        Returns:
            True if lock acquired
        """
        try:
            from django.core.cache import cache
            return cache.add(f'lock:{lock_name}', '1', timeout)
        except Exception:
            return False
    
    @staticmethod
    def release(lock_name: str) -> bool:
        """
        Release a distributed lock
        """
        try:
            from django.core.cache import cache
            return cache.delete(f'lock:{lock_name}')
        except Exception:
            return False


def with_distributed_lock(lock_name: str):
    """
    Decorator to acquire a distributed lock for a function
    
    Usage:
        @with_distributed_lock('course_registration')
        def register_student(student, course):
            pass
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not DistributedLock.acquire(lock_name):
                raise Exception(f"Could not acquire lock: {lock_name}")
            
            try:
                return func(*args, **kwargs)
            finally:
                DistributedLock.release(lock_name)
        
        return wrapper
    return decorator


# Export
__all__ = [
    'IdempotencyManager',
    'idempotent_operation',
    'TransactionSafeGPA',
    'CourseCapacityManager',
    'PaymentTransactionManager',
    'DistributedLock',
    'with_distributed_lock',
]