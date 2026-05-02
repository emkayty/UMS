"""
SMS Notification Service.
Supports multiple SMS providers.
"""
import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class SMSProvider:
    """Base SMS provider."""
    
    def send(self, to, message):
        raise NotImplementedError


class AfricastalkingSMS(SMSProvider):
    """Africastalking SMS provider."""
    
    def __init__(self):
        self.api_key = getattr(settings, 'AFRICASTALKING_API_KEY', '')
        self.username = getattr(settings, 'AFRICASTALKING_USERNAME', 'sandbox')
        self.base_url = 'https://api.africas-talking.com/api/v1'
    
    def send(self, to, message):
        """Send SMS via Africastalking."""
        if not self.api_key:
            logger.warning("Africastalking API key not configured")
            return False
        
        # Format phone number
        if to.startswith('0'):
            to = '+234' + to[1:]
        elif not to.startswith('+'):
            to = '+234' + to
        
        payload = {
            'username': self.username,
            'to': to,
            'message': message,
        }
        
        headers = {
            'ApiKey': self.api_key,
            'Content-Type': 'application/json',
        }
        
        try:
            response = requests.post(
                f'{self.base_url}/messaging',
                json=payload,
                headers=headers,
                timeout=30
            )
            return response.status_code == 201
        except Exception as e:
            logger.error(f"SMS failed: {e}")
            return False


class TermiiSMS(SMSProvider):
    """Termii SMS provider (Nigeria)."""
    
    def __init__(self):
        self.api_key = getattr(settings, 'TERMII_API_KEY', '')
        self.base_url = 'https://api.termii.com/api/sms/send'
    
    def send(self, to, message):
        """Send SMS via Termii."""
        if not self.api_key:
            logger.warning("Termii API key not configured")
            return False
        
        # Format phone
        if to.startswith('0'):
            to = '234' + to[1:]
        
        payload = {
            'api_key': self.api_key,
            'message_type': 'plain',
            'to': to,
            'from': getattr(settings, 'SMS_SENDER', 'UNIVERSITY'),
            'message': message,
        }
        
        try:
            response = requests.post(self.base_url, json=payload, timeout=30)
            data = response.json()
            return data.get('code') == 'OK'
        except Exception as e:
            logger.error(f"SMS failed: {e}")
            return False


class LogSMS(SMSProvider):
    """Log to console (development)."""
    
    def send(self, to, message):
        logger.info(f"[SMS] To: {to}, Message: {message}")
        return True


def get_sms_provider():
    """Get configured SMS provider."""
    provider = getattr(settings, 'SMS_PROVIDER', 'log').lower()
    
    providers = {
        'africastalking': AfricastalkingSMS,
        'termii': TermiiSMS,
        'log': LogSMS,
    }
    
    return providers.get(provider, LogSMS)()


class SMSService:
    """SMS notification service."""
    
    @classmethod
    def send_admission(cls, phone, status):
        """Send admission SMS."""
        msg = f"UniCore: Your admission status is {status}. Visit portal for details."
        return get_sms_provider().send(phone, msg)
    
    @classmethod
    def send_fee_reminder(cls, phone, amount):
        """Send fee reminder."""
        msg = f"UniCore: Fee reminder - N{amount}. Please pay before deadline."
        return get_sms_provider().send(phone, msg)
    
    @classmethod
    def send_result(cls, phone, semester):
        """Send result notification."""
        msg = f"UniCore: {semester} results are now available."
        return get_sms_provider().send(phone, msg)
    
    @classmethod
    def send_clearance(cls, phone, status):
        """Send clearance notification."""
        msg = f"UniCore: Your graduation clearance is {status}."
        return get_sms_provider().send(phone, msg)
    
    @classmethod
    def send_bulk(cls, recipients, message):
        """Send bulk SMS."""
        results = []
        for phone in recipients:
            result = get_sms_provider().send(phone, message)
            results.append({'to': phone, 'success': result})
        return results
