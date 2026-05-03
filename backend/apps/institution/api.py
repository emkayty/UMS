import json
from typing import Optional
from ninja import Router, Schema
from django.shortcuts import get_object_or_404
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.institution.models import Settings, GradingScaleType, PaymentGateway
from apps.accounts.permissions import IsInstitutionAdmin

router = Router(tags=['Settings'])


class SettingsSchema(Schema):
    id: str
    institution_name: str
    motto: str
    logo_url: str
    primary_color: str
    secondary_color: str
    grading_scale_type: str
    grading_boundaries: list
    academic_year_start: str
    semester_structure: list
    payment_gateway: str
    setup_completed: bool


class SetupWizardSchema(Schema):
    # Step 1: Branding
    institution_name: str
    motto: str = ''
    logo_url: str = ''
    primary_color: str = '#1e3a8a'
    secondary_color: str = '#059669'
    
    # Step 2: Grading
    grading_scale_type: str = 'british_nigerian'
    grading_boundaries: Optional[list] = None
    
    # Step 3: Academic calendar
    academic_year_start: str
    semester_structure: list
    
    # Step 4: Admin account
    admin_email: str
    admin_password: str
    
    # Step 5: Payment
    payment_gateway: str = 'paystack'
    paystack_secret_key: str = ''
    paystack_public_key: str = ''
    flutterwave_secret_key: str = ''
    flutterwave_public_key: str = ''


@router.get('/settings', response=SettingsSchema)
def get_settings(request):
    """Get institution settings."""
    settings = Settings.get_instance()
    return SettingsSchema(
        id=str(settings.id),
        institution_name=settings.institution_name,
        motto=settings.motto,
        logo_url=settings.logo_url,
        primary_color=settings.primary_color,
        secondary_color=settings.secondary_color,
        grading_scale_type=settings.grading_scale_type,
        grading_boundaries=settings.grading_boundaries,
        academic_year_start=settings.academic_year_start.isoformat(),
        semester_structure=settings.semester_structure,
        payment_gateway=settings.payment_gateway,
        setup_completed=settings.setup_completed
    )


@router.post('/setup', response={200: dict, 400: dict})
def setup_wizard(request, data: SetupWizardSchema):
    """Setup wizard - first time configuration."""
    from apps.accounts.models import User
    
    # Check if setup already completed
    settings = Settings.get_instance()
    if settings.setup_completed:
        return 400, {'success': False, 'error': 'Setup already completed'}
    
    # Validate admin email doesn't exist
    if User.objects.filter(email=data.admin_email).exists():
        return 400, {'success': False, 'error': 'Admin email already exists'}
    
    # Update settings
    settings.institution_name = data.institution_name
    settings.motto = data.motto
    settings.logo_url = data.logo_url
    settings.primary_color = data.primary_color
    settings.secondary_color = data.secondary_color
    settings.grading_scale_type = data.grading_scale_type
    settings.grading_boundaries = data.grading_boundaries or []
    settings.academic_year_start = data.academic_year_start
    settings.semester_structure = data.semester_structure
    settings.payment_gateway = data.payment_gateway
    settings.paystack_secret_key = data.paystack_secret_key
    settings.paystack_public_key = data.paystack_public_key
    settings.flutterwave_secret_key = data.flutterwave_secret_key
    settings.flutterwave_public_key = data.flutterwave_public_key
    
    # Create admin user
    admin_user = User.objects.create_user(
        email=data.admin_email,
        password=data.admin_password,
        role='institution_admin',
        is_staff=True
    )
    settings.created_by = admin_user
    settings.setup_completed = True
    settings.save()
    
    return {'success': True, 'message': 'Setup completed successfully'}


@router.patch('/settings', response={200: SettingsSchema, 403: dict})
def update_settings(request, data: SettingsSchema):
    """Update institution settings (admin only)."""
    from apps.accounts.permissions import IsInstitutionAdmin
    
    user = request.auth[0]
    if user.role != 'institution_admin' and not user.is_staff:
        return 403, {'success': False, 'error': 'Permission denied'}
    
    settings = Settings.get_instance()
    
    # Update fields
    for field in ['institution_name', 'motto', 'logo_url', 'primary_color', 
                 'secondary_color', 'grading_scale_type', 'grading_boundaries',
                 'semester_structure', 'payment_gateway']:
        if hasattr(data, field):
            value = getattr(data, field, None)
            if value is not None:
                setattr(settings, field, value)
    
    settings.save()
    
    return SettingsSchema(
        id=str(settings.id),
        institution_name=settings.institution_name,
        motto=settings.motto,
        logo_url=settings.logo_url,
        primary_color=settings.primary_color,
        secondary_color=settings.secondary_color,
        grading_scale_type=settings.grading_scale_type,
        grading_boundaries=settings.grading_boundaries,
        academic_year_start=settings.academic_year_start.isoformat(),
        semester_structure=settings.semester_structure,
        payment_gateway=settings.payment_gateway,
        setup_completed=settings.setup_completed
    )

# === Cookie Consent (GDPR/NDPR) ===
@router.get('/consent')
def get_cookie_consent(request):
    """Get user's cookie consent status."""
    from apps.institution.consent import cookie_consent
    return cookie_consent(request)


@router.post('/consent')
def set_cookie_consent(request):
    """Set user's cookie consent."""
    from apps.institution.consent import cookie_consent
    return cookie_consent(request)


@router.get('/privacy-policy')
def get_privacy_policy(request):
    """Get privacy policy information."""
    from apps.institution.consent import privacy_policy
    return privacy_policy(request)
