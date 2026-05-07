"""
Notification System for UMS

Provides email, SMS, and push notification support.
"""
import logging
from typing import List, Optional, Dict, Any
from django.core.mail import send_mail
from django.conf import settings
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class EmailNotification:
    """Email notification"""
    subject: str
    message: str
    to: List[str]
    html_message: Optional[str] = None


class NotificationService:
    """Notification service"""
    
    @staticmethod
    def send_email(
        subject: str,
        message: str,
        to: List[str],
        html_message: Optional[str] = None,
        from_email: str = None
    ) -> bool:
        """Send email"""
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email or settings.DEFAULT_FROM_EMAIL,
                recipient_list=to,
                html_message=html_message,
                fail_silently=False,
            )
            logger.info(f"Email sent: {subject} to {to}")
            return True
        except Exception as e:
            logger.error(f"Email failed: {e}")
            return False
    
    @staticmethod
    def send_bulk_email(
        notifications: List[EmailNotification]
    ) -> Dict[str, int]:
        """Send bulk emails"""
        results = {"success": 0, "failed": 0}
        
        for notification in notifications:
            success = NotificationService.send_email(
                notification.subject,
                notification.message,
                notification.to,
                notification.html_message
            )
            if success:
                results["success"] += 1
            else:
                results["failed"] += 1
        
        return results
    
    @staticmethod
    def send_sms(phone: str, message: str) -> bool:
        """Send SMS (placeholder - integrate with provider)"""
        logger.info(f"SMS: {phone} - {message}")
        # Integrate with provider (e.g., Twilio, Africa's Talking)
        return True
    
    @staticmethod
    def send_push(user_id: str, title: str, body: str, data: Dict = None) -> bool:
        """Send push notification"""
        logger.info(f"Push: {user_id} - {title}")
        # Integrate with FCM, OneSignal, etc.
        return True


class TemplateRenderer:
    """Render notification templates"""
    
    templates = {
        "welcome": "Welcome to UMS, {name}! Your account is ready.",
        "password_reset": "Reset your password: {link}",
        "admission": "Congratulations {name}! You've been admitted.",
        "result": "Your result for {course} is ready.",
        "payment": "Payment of {amount} received.",
    }
    
    @classmethod
    def render(cls, template: str, **kwargs) -> str:
        """Render template with variables"""
        msg = cls.templates.get(template, "")
        return msg.format(**kwargs)


def notify_student(student, notification_type: str, **kwargs):
    """Notify student"""
    # Send email
    message = TemplateRenderer.render(notification_type, **kwargs)
    NotificationService.send_email(
        subject=f"UMS: {notification_type}",
        message=message,
        to=[student.email]
    )
    
    # Send SMS
    if student.phone:
        NotificationService.send_sms(
            student.phone,
            message
        )


def notify_staff(staff, notification_type: str, **kwargs):
    """Notify staff"""
    message = TemplateRenderer.render(notification_type, **kwargs)
    NotificationService.send_email(
        subject=f"UMS: {notification_type}",
        message=message,
        to=[staff.email]
    )