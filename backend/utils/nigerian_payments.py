"""
NIGERIAN PAYMENT INTEGRATION
Remita & Native Payment Gateway Support
"""

import hashlib
import hmac
import json
import time
from datetime import datetime
from typing import Optional
from django.conf import settings

# Try importing requests, make optional
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    requests = None


class NigerianPaymentGateway:
    """
    Nigerian Payment Gateway Integration
    Supports: Remita, Flutterwave, Paystack
    """
    
    # Nigerian bank codes
    BANKS = {
        '044': 'Access Bank',
        '023': 'Citi Bank',
        '014': 'Diamond Bank',
        '063': 'First Bank of Nigeria',
        '011': 'First City Monument Bank',
        '058': 'Guaranty Trust Bank (GTBank)',
        '058': 'Heritage Bank',
        '030': 'Jaiz Bank',
        '082': 'Keystone Bank',
        '076': 'Skye Bank',
        '084': 'Sterling Bank',
        '032': 'Union Bank of Nigeria',
        '027': 'United Bank for Africa (UBA)',
        '035': 'Unity Bank',
        '057': 'Zenith Bank',
    }
    
    def __init__(self, gateway: str = 'remita'):
        self.gateway = gateway.lower()
        self.merchant_id = getattr(settings, 'REMITA_MERCHANT_ID', '')
        self.api_key = getattr(settings, 'REMITA_API_KEY', '')
        self.environment = getattr(settings, 'REMITA_ENV', 'test')
        
    def initiate_payment(
        self, 
        amount: float, 
        description: str,
        customer_email: str,
        student_id: Optional[str] = None,
        metadata: Optional[dict] = None
    ) -> dict:
        """Initiate payment transaction"""
        
        if self.gateway == 'remita':
            return self._remita_initiate(
                amount, description, customer_email, student_id, metadata
            )
        elif self.gateway == 'flutterwave':
            return self._flutterwave_initiate(
                amount, description, customer_email, student_id, metadata
            )
        elif self.gateway == 'paystack':
            return self._paystack_initiate(
                amount, description, customer_email, student_id, metadata
            )
        else:
            raise ValueError(f"Unsupported gateway: {self.gateway}")
    
    def _remita_initiate(
        self,
        amount: float,
        description: str,
        customer_email: str,
        student_id: Optional[str],
        metadata: Optional[dict]
    ) -> dict:
        """Remita payment initiation"""
        
        # Generate unique reference
        ref = f"UMS{int(time.time())}{student_id or ''}"
        
        payload = {
            "merchantId": self.merchant_id,
            "apiKey": self.api_key,
            "amount": int(amount * 100),  # Convert to kobo
            "description": description,
            "reference": ref,
            "customer": {
                "email": customer_email,
            },
            "metadata": metadata or {},
            "responseUrl": getattr(settings, 'REMITA_RESPONSE_URL', ''),
        }
        
        base_url = 'https://remita.inc' if self.environment == 'live' else 'https://remitademo.com'
        
        try:
            response = requests.post(
                f"{base_url}/payment/v1/paymentinit",
                json=payload,
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {'status': 'error', 'message': str(e)}
    
    def verify_payment(self, reference: str) -> dict:
        """Verify payment status with Remita"""
        
        base_url = 'https://remita.inc' if self.environment == 'live' else 'https://remitademo.com'
        
        # Generate verification hash
        hash_string = f"{reference}{self.api_key}{self.merchant_id}"
        hash_hash = hashlib.sha256(hash_string.encode()).hexdigest()
        
        try:
            response = requests.get(
                f"{base_url}/payment/v1_paymentstatus/{self.merchant_id}/{reference}/{hash_hash}",
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {'status': 'error', 'message': str(e)}
    
    def _flutterwave_initiate(
        self,
        amount: float,
        description: str,
        customer_email: str,
        student_id: Optional[str],
        metadata: Optional[dict]
    ) -> dict:
        """Flutterwave payment initiation"""
        
        return {
            'status': 'pending_implementation',
            'gateway': 'flutterwave',
            'note': 'Contact support@flutterwave.com to enable'
        }
    
    def _paystack_initiate(
        self,
        amount: float,
        description: str,
        customer_email: str,
        student_id: Optional[str],
        metadata: Optional[dict]
    ) -> dict:
        """Paystack payment initiation"""
        
        return {
            'status': 'pending_implementation',
            'gateway': 'paystack', 
            'note': 'Contact support@paystack.com to enable'
        }


class NigerianGradingSystem:
    """
    Nigerian University Grading System
    Implements NUC-approved grading scale
    """
    
    # Standard Nigerian grading scale (4-point system)
    GRADE_POINTS = {
        'A': 5.0,   # 70-100%
        'B': 4.0,   # 60-69%
        'C': 3.0,   # 50-59%
        'D': 2.0,   # 45-49%
        'E': 1.0,   # 40-44%
        'F': 0.0,   # 0-39%
    }
    
    # Grade boundaries
    GRADE_BOUNDARIES = {
        'A': (70, 100),
        'B': (60, 69),
        'C': (50, 59),
        'D': (45, 49),
        'E': (40, 44),
        'F': (0, 39),
    }
    
    @classmethod
    def score_to_grade(cls, score: float) -> str:
        """Convert numerical score to letter grade"""
        for grade, (lower, upper) in cls.GRADE_BOUNDARIES.items():
            if lower <= score <= upper:
                return grade
        return 'F'
    
    @classmethod
    def score_to_gp(cls, score: float) -> float:
        """Convert score to grade point"""
        grade = cls.score_to_grade(score)
        return cls.GRADE_POINTS[grade]
    
    @classmethod
    def calculate_gpa(cls, courses: list) -> float:
        """Calculate GPA from list of courses"""
        if not courses:
            return 0.0
        
        total_points = 0.0
        total_units = 0
        
        for course in courses:
            score = course.get('score', 0)
            units = course.get('units', 0)
            gp = cls.score_to_gp(score)
            
            total_points += gp * units
            total_units += units
        
        if total_units == 0:
            return 0.0
        
        return round(total_points / total_units, 2)
    
    @classmethod
    def calculate_cgpa(cls, semesters: list) -> float:
        """Calculate CGPA from multiple semesters"""
        if not semesters:
            return 0.0
        
        total_points = 0.0
        total_units = 0
        
        for semester in semesters:
            gpa = semester.get('gpa', 0)
            units = semester.get('total_units', 0)
            
            total_points += gpa * units
            total_units += units
        
        if total_units == 0:
            return 0.0
        
        return round(total_points / total_units, 2)


class NigerianIDValidator:
    """
    Nigerian ID Validation
    Validates: NIN, BVN, Driver's License, Voter Card
    """
    
    @staticmethod
    def validate_nin(nin: str) -> bool:
        """
        Validate NIN (National Identification Number)
        NIN is 11 digits
        """
        if not nin or len(nin) != 11:
            return False
        return nin.isdigit()
    
    @staticmethod
    def validate_bvn(bvn: str) -> bool:
        """
        Validate BVN (Bank Verification Number)
        BVN is 11 digits
        """
        if not bvn or len(bvn) != 11:
            return False
        return bvn.isdigit()
    
    @staticmethod
    def validate_driver_license(license_number: str) -> bool:
        """
        Validate Driver's License Number
        Format: 2 letters + 6 digits + 1 letter
        """
        if not license_number or len(license_number) != 9:
            return False
        
        pattern = r'^[A-Z]{2}\d{6}[A-Z]$'
        import re
        return bool(re.match(pattern, license_number.upper()))
    
    @staticmethod
    def validate_voter_card(voter_number: str) -> bool:
        """
        Validate PVC (Permanent Voter's Card)
        Format: 3 letters + 12 digits
        """
        if not voter_number or len(voter_number) != 15:
            return False
        
        return voter_number.replace('/', '').isdigit()


class NigerianPhoneValidator:
    """
    Nigerian Phone Number Validation
    Supports: All Nigeria networks
    """
    
    # Nigeria country code
    COUNTRY_CODE = '+234'
    
    # Network prefixes
    NETWORKS = {
        '0802': 'Airtel',
        '0803': 'Airtel',
        '0808': 'Airtel',
        '0702': 'Airtel',
        '0902': 'Airtel',
        '0905': 'Airtel',
        '0810': 'MTN',
        '0803': 'MTN',
        '0806': 'MTN',
        '0703': 'MTN',
        '0704': 'MTN',
        '0816': 'MTN',
        '0813': 'MTN',
        '0814': 'MTN',
        '0903': 'MTN',
        '0906': 'MTN',
        '0805': 'Glo',
        '0807': 'Glo',
        '0811': 'Glo',
        '0815': 'Glo',
        '0905': 'Glo',
        '0705': '9mobile',
        '0808': '9mobile',
        '0908': '9mobile',
        '0817': '9mobile',
    }
    
    @classmethod
    def validate(cls, phone: str) -> bool:
        """Validate Nigerian phone number"""
        # Remove common formatting
        phone = phone.replace('+', '').replace(' ', '').replace('-', '')
        
        if phone.startswith('0'):
            phone = '234' + phone[1:]
        
        if phone.startswith('234') and len(phone) == 13:
            return phone[3:].isdigit()
        
        return False
    
    @classmethod
    def format_for_display(cls, phone: str) -> str:
        """Format phone for display (_local format)"""
        phone = phone.replace('+', '').replace(' ', '').replace('-', '')
        
        if phone.startswith('234'):
            return '0' + phone[3:]
        
        return phone
    
    @classmethod
    def detect_network(cls, phone: str) -> Optional[str]:
        """Detect network from phone number"""
        if not cls.validate(phone):
            return None
        
        phone = phone.replace('+', '').replace(' ', '').replace('-', '')
        if phone.startswith('234'):
            phone = '0' + phone[3:]
        
        prefix = phone[:4]
        return cls.NETWORKS.get(prefix, 'Unknown')


# Export utilities
__all__ = [
    'NigerianPaymentGateway',
    'NigerianGradingSystem', 
    'NigerianIDValidator',
    'NigerianPhoneValidator',
]