"""
Webhook System for UMS

Provides webhook integration for external notifications
and event-driven architectures.
"""
import json
import hashlib
import hmac
import logging
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
import requests

logger = logging.getLogger(__name__)


class WebhookEvent:
    """Webhook event"""
    STUDENT_CREATED = "student.created"
    STUDENT_UPDATED = "student.updated"
    STUDENT_DELETED = "student.deleted"
    PAYMENT_SUCCESS = "payment.success"
    PAYMENT_FAILED = "payment.failed"
    RESULT_APPROVED = "result.approved"
    REGISTRATION_COMPLETE = "registration.completed"
    ADMISSION_OFFER = "admission.offer"


class WebhookPayload:
    """Webhook payload builder"""
    
    def __init__(self, event_type: str, data: Dict[str, Any]):
        self.event_type = event_type
        self.data = data
        self.timestamp = datetime.now().isoformat()
        self.id = f"wh_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.event_type,
            "timestamp": self.timestamp,
            "data": self.data
        }


class Webhook:
    """Webhook client for sending events"""
    
    def __init__(self, url: str, secret: str = "", headers: Dict[str, str] = None):
        self.url = url
        self.secret = secret
        self.headers = headers or {}
    
    def sign_payload(self, payload: str) -> str:
        """Sign payload with HMAC-SHA256"""
        if not self.secret:
            return ""
        return hmac.new(
            self.secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
    
    def send(self, event_type: str, data: Dict[str, Any]) -> bool:
        """
        Send webhook event
        
        Args:
            event_type: Type of event
            data: Event data
            
        Returns:
            True if successful
        """
        payload = WebhookPayload(event_type, data)
        payload_str = json.dumps(payload.to_dict())
        
        # Prepare headers
        headers = {
            "Content-Type": "application/json",
            "X-Webhook-Event": event_type,
            **self.headers
        }
        
        # Add signature if secret is set
        if self.secret:
            signature = self.sign_payload(payload_str)
            headers["X-Webhook-Signature"] = signature
        
        try:
            response = requests.post(
                self.url,
                data=payload_str,
                headers=headers,
                timeout=30
            )
            if response.status_code < 400:
                logger.info(f"Webhook sent: {event_type}")
                return True
            else:
                logger.error(f"Webhook failed: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Webhook error: {e}")
            return False


class WebhookRegistry:
    """Registry for managing webhooks"""
    
    _instance = None
    
    def __init__(self):
        self.webhooks: List[Webhook] = []
    
    @classmethod
    def get_instance(cls) -> 'WebhookRegistry':
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def register(self, webhook: Webhook):
        """Register a webhook"""
        self.webhooks.append(webhook)
        logger.info(f"Webhook registered: {webhook.url}")
    
    def unregister(self, url: str):
        """Unregister a webhook"""
        self.webhooks = [w for w in self.webhooks if w.url != url]
    
    def trigger(self, event_type: str, data: Dict[str, Any]) -> Dict[str, int]:
        """
        Trigger event on all webhooks
        
        Args:
            event_type: Type of event
            data: Event data
            
        Returns:
            Dictionary with success/failure counts
        """
        results = {"success": 0, "failed": 0}
        
        for webhook in self.webhooks:
            if webhook.send(event_type, data):
                results["success"] += 1
            else:
                results["failed"] += 1
        
        return results


# Convenience functions
def trigger_webhook(event_type: str, data: Dict[str, Any]):
    """Trigger webhook event"""
    registry = WebhookRegistry.get_instance()
    return registry.trigger(event_type, data)


def register_webhook(url: str, secret: str = ""):
    """Register a webhook"""
    webhook = Webhook(url, secret)
    registry = WebhookRegistry.get_instance()
    registry.register(webhook)