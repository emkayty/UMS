from rest_framework import permissions
from apps.accounts.models import User, UserRole


class RoleBasedPermission(permissions.BasePermission):
    """Permission class that checks user roles."""
    
    allowed_roles = []
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if not self.allowed_roles:
            return True
        
        return request.user.role in self.allowed_roles


class IsStudent(RoleBasedPermission):
    allowed_roles = [UserRole.STUDENT]


class IsLecturer(RoleBasedPermission):
    allowed_roles = [UserRole.LECTURER]


class IsHOD(RoleBasedPermission):
    allowed_roles = [UserRole.HOD]


class IsDean(RoleBasedPermission):
    allowed_roles = [UserRole.DEAN]


class IsRegistrar(RoleBasedPermission):
    allowed_roles = [UserRole.REGISTRAR]


class IsBursar(RoleBasedPermission):
    allowed_roles = [UserRole.BURSAR]


class IsInstitutionAdmin(RoleBasedPermission):
    allowed_roles = [UserRole.INSTITUTION_ADMIN]


class IsAdmin(RoleBasedPermission):
    """Admin includes Institution Admin or superuser."""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.is_staff or request.user.role == UserRole.INSTITUTION_ADMIN


class IsReadOnly(permissions.BasePermission):
    """Allow read-only access."""
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS