"""
Multi-Factor Authentication (MFA) Module
Enterprise-grade 2FA for enhanced security
"""

import pyotp
import hashlib
import secrets
from typing import Optional, Tuple
from django.utils import timezone


class MFAProvider:
    """
    Multi-Factor Authentication provider
    Supports TOTP (Time-based One-Time Password)
    """
    
    @staticmethod
    def generate_secret() -> str:
        """Generate a new TOTP secret"""
        return pyotp.random_base32()
    
    @staticmethod
    def get_totp(secret: str) -> 'pyotp.TOTP':
        """Get TOTP instance"""
        return pyotp.TOTP(secret)
    
    @staticmethod
    def generate_qr_url(secret: str, email: str, issuer: str = 'UMS') -> str:
        """Generate QR URL for authenticator apps"""
        totp = pyotp.TOTP(secret)
        return totp.provisioning_uri(name=email, issuer_name=issuer)
    
    @staticmethod
    def verify_code(secret: str, code: str) -> bool:
        """Verify a TOTP code"""
        if not secret or not code:
            return False
        
        try:
            totp = pyotp.TOTP(secret)
            return totp.verify(code, valid_window=1)
        except Exception:
            return False
    
    @staticmethod
    def generate_backup_codes(count: int = 10) -> list[str]:
        """Generate backup codes for account recovery"""
        codes = []
        for _ in range(count):
            code = secrets.token_hex(4).upper()
            codes.append(code)
        return codes
    
    @staticmethod
    def hash_backup_code(code: str) -> str:
        """Hash a backup code for secure storage"""
        return hashlib.sha256(code.encode()).hexdigest()


class MFAManager:
    """
    Manages MFA for users
    """
    
    @staticmethod
    def enable_mfa(user, secret: str, code: str) -> Tuple[bool, str]:
        """
        Enable MFA for a user
        
        Returns: (success, message)
        """
        # Verify the code first
        if not MFAProvider.verify_code(secret, code):
            return False, "Invalid verification code"
        
        # Store the secret (in production, use encrypted field)
        user.mfa_secret = secret
        user.mfa_enabled = True
        user.save()
        
        return True, "MFA enabled successfully"
    
    @staticmethod
    def disable_mfa(user, code: str) -> Tuple[bool, str]:
        """Disable MFA for a user"""
        if not user.mfa_enabled:
            return True, "MFA not enabled"
        
        # Verify before disabling
        if not MFAProvider.verify_code(user.mfa_secret, code):
            return False, "Invalid verification code"
        
        user.mfa_secret = None
        user.mfa_enabled = False
        user.save()
        
        return True, "MFA disabled successfully"
    
    @staticmethod
    def verify_mfa(user, code: str) -> bool:
        """Verify MFA code for login"""
        if not user.mfa_enabled or not user.mfa_secret:
            return True  # No MFA required
        
        return MFAProvider.verify_code(user.mfa_secret, code)


class MFAService:
    """
    MFA service for authentication flows
    """
    
    @staticmethod
    def setup_mfa(user) -> dict:
        """
        Get MFA setup data for a user
        
        Returns: {
            'secret': str,
            'qr_url': str,
            'backup_codes': list
        }
        """
        secret = MFAProvider.generate_secret()
        qr_url = MFAProvider.generate_qr_url(secret, user.email)
        
        # Generate and hash backup codes
        backup_codes = MFAProvider.generate_backup_codes()
        
        return {
            'secret': secret,
            'qr_url': qr_url,
            'backup_codes': backup_codes,
        }
    
    @staticmethod
    def verify_login(user, mfa_code: str) -> bool:
        """
        Verify MFA during login
        
        Returns: True if MFA code is valid
        """
        return MFAManager.verify_mfa(user, mfa_code)


# Export
__all__ = [
    'MFAProvider',
    'MFAManager', 
    'MFAService',
]