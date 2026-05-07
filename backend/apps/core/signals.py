"""
SIGNALS - Standardized Django Signals
Central signal handlers for the entire system
"""

from django.db.models.signals import (
    pre_save, post_save, pre_delete, post_delete,
    m2m_changed
)
from django.dispatch import receiver
from django.utils import timezone


# ============================================================
# USER SIGNALS
# ============================================================

@receiver(pre_save, dispatch_uid='user_pre_save')
def user_pre_save(sender, instance, **kwargs):
    """Pre-save user processing."""
    # Only process User model
    if sender._meta.model_name != 'user':
        return
    if not hasattr(instance, '_meta'):
        return
        
    if instance.email:
        instance.email = instance.email.lower()
    
    if instance.username:
        instance.username = instance.username.lower()


@receiver(post_save, dispatch_uid='user_post_save')
def user_post_save(sender, instance, created, **kwargs):
    """Post-save user actions."""
    # Only process User model
    if sender._meta.model_name != 'user':
        return
    if created:
        # Audit log - comment out as AuditLog model doesn't exist
        pass


# ============================================================
# STUDENT SIGNALS
# ============================================================

@receiver(post_save, dispatch_uid='student_post_save')
def student_post_save(sender, instance, created, **kwargs):
    """Post-save student actions."""
    # Only process StudentProfile model
    if sender._meta.model_name != 'studentprofile':
        return
    if not hasattr(instance, '_meta'):
        return
        
    if created:
        # Generate student email
        if hasattr(instance, 'user') and instance.user and hasattr(instance, 'student_id') and instance.student_id:
            email = f"{instance.student_id}@student.university.edu"
            if not instance.user.email:
                instance.user.email = email
                instance.user.save()


# ============================================================
# STAFF SIGNALS
# ============================================================

@receiver(post_save, dispatch_uid='staff_post_save')
def staff_post_save(sender, instance, created, **kwargs):
    """Post-save staff actions."""
    # Only process StaffProfile model
    if sender._meta.model_name != 'staffprofile':
        return
    if not hasattr(instance, '_meta'):
        return
        
    if created:
        # Create email
        if hasattr(instance, 'user') and instance.user and hasattr(instance, 'staff_id') and instance.staff_id:
            email = f"{instance.staff_id}@university.edu"
            if not instance.user.email:
                instance.user.email = email
                instance.user.save()


# ============================================================
# COURSE REGISTRATION SIGNALS
# ============================================================

@receiver(post_save, dispatch_uid='registration_post_save')
def registration_post_save(sender, instance, created, **kwargs):
    """Post-save registration actions."""
    # Only process CourseRegistration model
    if sender._meta.model_name != 'courseregistration':
        return
    if not hasattr(instance, '_meta'):
        return
        
    if created and hasattr(instance, 'status') and instance.status == 'approved':
        # Update student's current courses
        pass


# ============================================================
# RESULT SIGNALS
# ============================================================

@receiver(pre_save, dispatch_uid='result_pre_save')
def result_pre_save(sender, instance, **kwargs):
    """Pre-save result processing."""
    # Only process Result model
    if sender._meta.model_name != 'result':
        return
    if not hasattr(instance, '_meta'):
        return
        
    if hasattr(instance, 'score') and instance.score is not None:
        from apps.core.utils import score_to_grade, score_to_grade_point
        instance.grade = score_to_grade(instance.score)
        instance.grade_point = score_to_grade_point(instance.score)


@receiver(post_save, dispatch_uid='result_post_save')
def result_post_save(sender, instance, created, **kwargs):
    """Post-save result actions."""
    # Only process Result model
    if sender._meta.model_name != 'result':
        return
    if not hasattr(instance, '_meta'):
        return
        
    if hasattr(instance, 'approved') and instance.approved:
        # Recalculate student GPA
        from apps.core.models import StudentProfile
        
        if hasattr(instance, 'student'):
            student = instance.student
            results = instance.__class__.objects.filter(
                student=student,
                approved=True
            )
            
            # Calculate new CGPA
            from apps.core.utils import calculate_gpa
            cgpa = calculate_gpa(results)
            
            student.cgpa = cgpa
            student.save()


# ============================================================
# PAYMENT SIGNALS
# ============================================================

@receiver(pre_save, dispatch_uid='payment_pre_save')
def payment_pre_save(sender, instance, **kwargs):
    """Pre-save payment processing."""
    # Only process Payment model
    if sender._meta.model_name != 'payment':
        return
    if not hasattr(instance, '_meta'):
        return
        
    if hasattr(instance, 'status') and instance.status == 'success' and not instance.paid_at:
        instance.paid_at = timezone.now()


@receiver(post_save, dispatch_uid='payment_post_save')
def payment_post_save(sender, instance, created, **kwargs):
    """Post-save payment actions."""
    # Only process Payment model
    if sender._meta.model_name != 'payment':
        return
    if not hasattr(instance, '_meta'):
        return
        
    if created and hasattr(instance, 'status') and instance.status == 'success':
        # Update invoice status
        from apps.core.models import Invoice
        
        invoice = Invoice.objects.filter(
            student=instance.student,
            status__in=['pending', 'partially_paid']
        ).first()
        
        if invoice:
            # Calculate balance
            from apps.core.utils import calculate_fee_balance
            
            payments = instance.__class__.objects.filter(
                student=instance.student,
                status='success'
            )
            
            balance = calculate_fee_balance(invoice, payments)
            
            if balance <= 0:
                invoice.status = 'paid'
            else:
                invoice.status = 'partially_paid'
            
            invoice.save()


# ============================================================
# INVOICE SIGNALS
# ============================================================

@receiver(post_save, dispatch_uid='invoice_post_save')
def invoice_post_save(sender, instance, created, **kwargs):
    """Post-save invoice actions."""
    if created:
        # Send notification
        pass


# ============================================================
# ATTENDANCE SIGNALS
# ============================================================

@receiver(post_save, dispatch_uid='attendance_post_save')
def attendance_post_save(sender, instance, created, **kwargs):
    """Post-save attendance actions."""
    # Only process StudentAttendance model
    if sender._meta.model_name != 'studentattendance':
        return
    if not hasattr(instance, '_meta'):
        return
        
    if created:
        # Check if below threshold - skip if model not available
        pass


# ============================================================
# LEAVE REQUEST SIGNALS
# ============================================================

@receiver(pre_save, dispatch_uid='leave_pre_save')
def leave_pre_save(sender, instance, **kwargs):
    """Pre-save leave processing."""
    # Only process LeaveRequest model
    if sender._meta.model_name != 'leaverequest':
        return
    if not hasattr(instance, '_meta'):
        return
        
    if instance.start_date and instance.end_date:
        instance.days = (instance.end_date - instance.start_date).days + 1


@receiver(post_save, dispatch_uid='leave_post_save')
def leave_post_save(sender, instance, created, **kwargs):
    """Post-save leave actions."""
    # Only process LeaveRequest model
    if sender._meta.model_name != 'leaverequest':
        return
    if not hasattr(instance, '_meta'):
        return
        
    if hasattr(instance, 'status') and instance.status == 'approved':
        # Update leave balance
        pass


# ============================================================
# ANNOUNCEMENT SIGNALS
# ============================================================

@receiver(post_save, dispatch_uid='announcement_post_save')
def announcement_post_save(sender, instance, created, **kwargs):
    """Post-save announcement actions."""
    # Only process Announcement model
    if sender._meta.model_name != 'announcement':
        return
    if not hasattr(instance, '_meta'):
        return
        
    if created and hasattr(instance, 'is_published') and instance.is_published:
        # Send notification to target users
        pass


# ============================================================
# DISCIPLINARY SIGNALS
# ============================================================

@receiver(post_save, dispatch_uid='disciplinary_post_save')
def disciplinary_post_save(sender, instance, created, **kwargs):
    """Post-save disciplinary actions."""
    # Only process StudentDiscipline model
    if sender._meta.model_name != 'studentdiscipline':
        return
    if not hasattr(instance, '_meta'):
        return
        
    if created:
        # Create notification
        pass


# ============================================================
# CLEARANCE SIGNALS
# ============================================================

@receiver(post_save, dispatch_uid='clearance_post_save')
def clearance_post_save(sender, instance, created, **kwargs):
    """Post-save clearance actions."""
    # Only process Clearance model
    if sender._meta.model_name != 'clearance':
        return
    if not hasattr(instance, '_meta'):
        return
        
    if created and hasattr(instance, 'status') and instance.status == 'approved':
        student = instance.student
        student.clearance_complete = True
        student.save()


# ============================================================
# CORE SIGNALS REGISTRATION
# ============================================================

def register_signals():
    """Register all signals."""
    # Import all models to trigger signal registration
    from apps.core import models  # noqa
    from apps.accounts import models as accounts_models  # noqa
    from apps.academic import models as academic_models  # noqa
    from apps.student import models as student_models  # noqa
    from apps.staff import models as staff_models  # noqa
    from apps.finance import models as finance_models  # noqa
    from apps.learning import models as learning_models  # noqa


# ============================================================
# AUTOMATION RULES
# ============================================================

class AutomationRule:
    """Base automation rule."""
    
    @staticmethod
    def check_student_eligibility(student):
        """Check if student can register."""
        return (
            student.status == 'active' and 
            student.programme is not None
        )
    
    @staticmethod
    def check_registration_open():
        """Check if registration is open."""
        from apps.core.models import AcademicSession
        session = AcademicSession.objects.filter(is_current=True).first()
        
        if not session:
            return False
        
        from django.utils import timezone
        today = timezone.now().date()
        
        return (
            session.registration_start <= today <= session.registration_end
            if hasattr(session, 'registration_start') else False
        )
    
    @staticmethod
    def auto_archive_old_records():
        """Archive old records."""
        from django.utils import timezone
        from datetime import timedelta
        
        cutoff = timezone.now() - timedelta(days=365)
        
        # Archive old logs
        # Archive old announcements
        pass
    
    @staticmethod
    def check_fees_due():
        """Check and notify fees due."""
        from apps.core.models import Invoice
        from django.utils import timezone
        
        due_invoices = Invoice.objects.filter(
            status__in=['pending', 'partially_paid'],
            due_date__lte=timezone.now().date()
        )
        
        # Send reminders
        pass
    
    @staticmethod
    def generate_daily_attendance():
        """Generate daily attendance report."""
        pass
    
    @staticmethod
    def generate_weekly_reports():
        """Generate weekly reports."""
        pass
    
    @staticmethod
    def generate_monthly_reports():
        """Generate monthly reports."""
        pass