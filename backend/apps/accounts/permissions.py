"""
Django Ninja Permission Classes
Production-ready RBAC without DRF dependencies.
"""
from apps.accounts.models import User, UserRole


def is_authenticated(request):
    """Check if user is authenticated."""
    return hasattr(request, 'user') and request.user and request.user.is_authenticated


def has_role(request, *roles):
    """Check if user has any of the specified roles."""
    if not is_authenticated(request):
        return False
    return request.user.role in roles


class BasePermission:
    """Base permission class for Django Ninja."""

    allowed_roles = []

    def __call__(self, request):
        if not is_authenticated(request):
            return False

        if not self.allowed_roles:
            return True

        return request.user.role in self.allowed_roles


class IsStudent(BasePermission):
    allowed_roles = [UserRole.STUDENT]


class IsLecturer(BasePermission):
    allowed_roles = [UserRole.LECTURER]


class IsHOD(BasePermission):
    allowed_roles = [UserRole.HOD]


class IsDean(BasePermission):
    allowed_roles = [UserRole.DEAN]


class IsRegistrar(BasePermission):
    allowed_roles = [UserRole.REGISTRAR]


class IsBursar(BasePermission):
    allowed_roles = [UserRole.BURSAR]


class IsInstitutionAdmin(BasePermission):
    allowed_roles = [UserRole.INSTITUTION_ADMIN]


class IsAdmin(BasePermission):
    """Admin includes Institution Admin or superuser."""

    def __call__(self, request):
        if not is_authenticated(request):
            return False
        return request.user.is_staff or request.user.role == UserRole.INSTITUTION_ADMIN


class IsReadOnly:
    """Allow read-only access."""

    def __call__(self, request):
        SAFE_METHODS = {'GET', 'HEAD', 'OPTIONS'}
        return request.method in SAFE_METHODS


# === Decorator for Django Ninja ===
def require_role(*allowed_roles):
    """Role-based permission decorator for Django Ninja routers."""
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if not is_authenticated(request):
                return {'success': False, 'error': 'Authentication required'}
            if allowed_roles and request.user.role not in allowed_roles:
                return {'success': False, 'error': 'Insufficient permissions'}
            return func(request, *args, **kwargs)
        return wrapper
    return decorator