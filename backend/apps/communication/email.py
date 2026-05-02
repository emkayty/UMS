"""
Email Notification Service.
"""
import logging
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)


class EmailService:
    """Email notification service."""
    
    DEFAULT_FROM = 'noreply@university.edu.ng'
    
    @classmethod
    def send_email(cls, to, subject, template, context, html=True, from_email=None):
        """Send email using template."""
        try:
            # Render templates
            html_content = render_to_string(f'emails/{template}.html', context)
            text_content = strip_tags(html_content)
            
            from_addr = from_email or getattr(settings, 'DEFAULT_FROM_EMAIL', cls.DEFAULT_FROM)
            
            if html:
                msg = EmailMultiAlternatives(subject, text_content, from_addr, [to])
                msg.attach_alternative(html_content, 'text/html')
            else:
                msg = EmailMultiAlternatives(subject, text_content, from_addr, [to])
            
            msg.send(fail_silently=False)
            return True
        except Exception as e:
            logger.error(f"Email send failed: {e}")
            return False
    
    @classmethod
    def send_admission_notification(cls, student, status):
        """Send admission status notification."""
        template = 'admission'
        context = {'student': student, 'status': status}
        return cls.send_email(
            student.user.email,
            f'Admission {status.title()}',
            template, context
        )
    
    @classmethod
    def send_fee_reminder(cls, student, amount_due):
        """Send fee payment reminder."""
        context = {'student': student, 'amount': amount_due}
        return cls.send_email(
            student.user.email,
            'Fee Payment Reminder',
            'fee_reminder', context
        )
    
    @classmethod
    def send_result_notification(cls, student, semester):
        """Send result published notification."""
        context = {'student': student, 'semester': semester}
        return cls.send_email(
            student.user.email,
            f'Results Published - {semester}',
            'result_published', context
        )
    
    @classmethod
    def send_leave_approval(cls, leave_request, approved):
        """Send leave approval notification."""
        status = 'approved' if approved else 'rejected'
        context = {'leave': leave_request, 'status': status}
        return cls.send_email(
            leave_request.staff.user.email,
            f'Leave Request {status.title()}',
            'leave_approval', context
        )
    
    @classmethod
    def send_clearance_complete(cls, student):
        """Send graduation clearance complete."""
        context = {'student': student}
        return cls.send_email(
            student.user.email,
            'Clearance Complete',
            'clearance_complete', context
        )
    
    @classmethod
    def send_transcript_ready(cls, student):
        """Send transcript ready notification."""
        context = {'student': student}
        return cls.send_email(
            student.user.email,
            'Transcript Ready',
            'transcript_ready', context
        )


# Quick send without templates
def send_simple_email(to, subject, message, from_email=None):
    """Send simple email without template."""
    try:
        send_mail(
            subject,
            message,
            from_email or EmailService.DEFAULT_FROM,
            [to],
            fail_silently=False
        )
        return True
    except Exception as e:
        logger.error(f"Email failed: {e}")
        return False
