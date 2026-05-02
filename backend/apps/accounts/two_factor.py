"""
Two-Factor Authentication
UMS 2FA Module
"""

from django_otp import devices
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_static.models import StaticDevice
import pyotp
import qrcode
import io
import base64


def generate_2fa_secret():
    """Generate a new 2FA secret key."""
    return pyotp.random_base32()


def get_totp_uri(secret, email):
    """Get TOTP URI for QR code generation."""
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(email, issuer_name='UniCore UMS')


def create_qr_code(uri):
    """Create QR code image as base64."""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(uri)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    
    return base64.b64encode(buffer.getvalue()).decode()


class TwoFactorAuthManager:
    """Manager for 2FA operations."""
    
    @staticmethod
    def get_user_devices(user):
        """Get all devices for a user."""
        return list(user.otp_devices.all())
    
    @staticmethod
    def get_verified_devices(user):
        """Get verified devices only."""
        return [d for d in user.otp_devices.all() if d.verified]
    
    @staticmethod
    def create_totp_device(user, name='Default'):
        """Create a new TOTP device for user."""
        device, created = TOTPDevice.objects.get_or_create(
            user=user,
            name=name,
            defaults={
                'key': generate_2fa_secret(),
                'confirmed': False,
            }
        )
        return device
    
    @staticmethod
    def verify_token(user, token):
        """Verify a TOTP token."""
        for device in user.otp_devices.all():
            if device.verify_token(token):
                return True
        return False
    
    @staticmethod
    def enable_2fa(user):
        """Enable 2FA for a user."""
        for device in user.otp_devices.all():
            device.confirmed = True
            device.save()
        return True
    
    @staticmethod
    def disable_2fa(user):
        """Disable 2FA for a user."""
        user.otp_devices.all().delete()
        return True
    
    @staticmethod
    def is_2fa_enabled(user):
        """Check if 2FA is enabled."""
        return user.otp_devices.filter(confirmed=True).exists()


# 2FA View Mixin
class TwoFactorAuthMixin:
    """Mixin for 2FA-protected views."""
    
    def dispatch(self, request, *args, **kwargs):
        # Check if user has 2FA enabled
        if hasattr(request.user, 'otp_devices'):
            if request.user.otp_devices.exists() and not request.user.otp_devices.filter(confirmed=True).exists():
                # Force 2FA setup
                return redirect('2fa-setup')
        
        return super().dispatch(request, *args, **kwargs)


# Decorator for 2FA required
def require_2fa(view_func):
    """Decorator to require 2FA for a view."""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        if hasattr(request.user, 'otp_devices'):
            if not request.user.otp_devices.filter(confirmed=True).exists():
                return redirect('2fa-setup')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


# QR Code generator view
def generate_2fa_qr(request):
    """Generate QR code for 2FA setup."""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    # Create device if not exists
    device = TwoFactorAuthManager.create_totp_device(request.user)
    
    # Generate URI
    uri = get_totp_uri(device.key, request.user.email)
    
    # Generate QR code
    qr_code = create_qr_code(uri)
    
    return JsonResponse({
        'qr_code': f'data:image/png;base64,{qr_code}',
        'secret': device.key,
    })


# Verify 2FA view
def verify_2fa(request):
    """Verify and enable 2FA."""
    if not request.method == 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    token = request.POST.get('token')
    
    if not token:
        return JsonResponse({'error': 'Token required'}, status=400)
    
    if TwoFactorAuthManager.verify_token(request.user, token):
        TwoFactorAuthManager.enable_2fa(request.user)
        return JsonResponse({'success': True, 'message': '2FA enabled'})
    
    return JsonResponse({'error': 'Invalid token'}, status=400)


# Disable 2FA view
def disable_2fa(request):
    """Disable 2FA."""
    if not request.method == 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    # Don't allow disabling for superusers
    if request.user.is_superuser:
        return JsonResponse({'error': 'Cannot disable 2FA for superusers'}, status=403)
    
    TwoFactorAuthManager.disable_2fa(request.user)
    
    return JsonResponse({'success': True, 'message': '2FA disabled'})