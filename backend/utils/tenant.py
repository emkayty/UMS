"""
Multi-Tenant Management
Enterprise-grade multi-tenant isolation for UMS

This module provides:
- TenantManager: Automatic tenant filtering on all queries
- TenantQuerySet: Tenant-aware querysets
- TenantMixin: Model mixin for tenant isolation
- get_tenant_context: Get current tenant from request
- require_tenant: Decorator to enforce tenant
"""

import uuid
from typing import Optional, Any
from django.db import models
from django.db.models import QuerySet, Manager
from django.conf import settings
from django.http import HttpRequest


class TenantManager(Manager):
    """
    Manager that automatically filters by tenant_id
    Use this instead of objects for automatic tenant filtering
    """
    
    def get_queryset(self) -> QuerySet:
        """Override to add tenant filtering"""
        qs = super().get_queryset()
        
        # Get tenant context from settings (set by middleware)
        tenant_id = getattr(settings, 'CURRENT_TENANT_ID', None)
        
        # Superusers see all data (optional - can be disabled for security)
        if tenant_id is None:
            # Check if user is superuser
            user = getattr(settings, 'CURRENT_USER', None)
            if user and getattr(user, 'is_superuser', False):
                return qs
        
        # Filter by tenant if available
        if tenant_id:
            return qs.filter(tenant_id=tenant_id)
        
        return qs
    
    def create(self, **kwargs):
        """Override create to add tenant_id"""
        # Get current tenant
        tenant_id = getattr(settings, 'CURRENT_TENANT_ID', None)
        
        # Add tenant_id if not provided and tenant exists
        if tenant_id and 'tenant_id' not in kwargs:
            kwargs['tenant_id'] = tenant_id
        
        return super().create(**kwargs)


class TenantQuerySet(QuerySet):
    """
    QuerySet with tenant-aware methods
    """
    
    def for_tenant(self, tenant_id: str) -> 'TenantQuerySet':
        """Filter queries by tenant"""
        return self.filter(tenant_id=tenant_id)
    
    def for_current_tenant(self) -> 'TenantQuerySet':
        """Filter by current tenant context"""
        tenant_id = getattr(settings, 'CURRENT_TENANT_ID', None)
        if tenant_id:
            return self.filter(tenant_id=tenant_id)
        return self


class TenantMixin(models.Model):
    """
    Model mixin that provides multi-tenant isolation
    Add this to all tenant-aware models
    
    Usage:
        class MyModel(TenantMixin, models.Model):
            name = models.CharField(max_length=100)
            ...
    """
    
    # Tenant ID - UUID for security (not guessable)
    tenant_id = models.UUIDField(
        null=True,
        blank=True,
        editable=False,
        db_index=True,
        help_text="Tenant identifier for multi-tenant isolation"
    )
    
    # Timestamp for audit
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        abstract = True
        indexes = [
            # Composite index for tenant + common queries
            models.Index(fields=['tenant_id', 'created_at']),
        ]
    
    def save(self, *args, **kwargs):
        """Override save to enforce tenant_id"""
        # Get tenant context
        tenant_id = getattr(settings, 'CURRENT_TENANT_ID', None)
        
        # Set tenant_id if not set and we have context
        if tenant_id and not self.tenant_id:
            self.tenant_id = tenant_id
        
        super().save(*args, **kwargs)


# ============================================================
# TENANT CONTEXT MANAGEMENT
# ============================================================

class TenantContext:
    """
    Thread-local tenant context
    Allows setting tenant_id for current request/thread
    """
    
    _context = {}
    
    @classmethod
    def set(cls, tenant_id: str, user=None):
        """Set tenant context"""
        cls._context['tenant_id'] = tenant_id
        cls._context['user'] = user
        settings.CURRENT_TENANT_ID = tenant_id
        settings.CURRENT_USER = user
    
    @classmethod
    def get(cls) -> Optional[str]:
        """Get current tenant ID"""
        return cls._context.get('tenant_id')
    
    @classmethod
    def clear(cls):
        """Clear tenant context"""
        cls._context = {}
        if hasattr(settings, 'CURRENT_TENANT_ID'):
            delattr(settings, 'CURRENT_TENANT_ID')
        if hasattr(settings, 'CURRENT_USER'):
            delattr(settings, 'CURRENT_USER')


def get_tenant_context(request: HttpRequest) -> Optional[str]:
    """
    Extract tenant_id from request
    Priority: 
    1. X-Tenant-ID header (API)
    2. Subdomain (multi-tenant URL)
    3. User.institution (logged in)
    """
    # 1. Header
    tenant_id = request.headers.get('X-Tenant-ID')
    if tenant_id:
        return tenant_id
    
    # 2. Subdomain
    host = request.get_host()
    if '.' in host:
        subdomain = host.split('.')[0]
        if subdomain not in ['www', 'localhost', 'api']:
            return subdomain
    
    # 3. From user (if authenticated)
    if request.user.is_authenticated:
        # Try to get from user
        if hasattr(request.user, 'institution_id'):
            return str(request.user.institution_id)
        if hasattr(request.user, 'tenant_id'):
            return str(request.user.tenant_id)
    
    return None


def require_tenant(view_func):
    """
    Decorator to require tenant context
    Use on views that need tenant isolation
    
    Usage:
        @require_tenant
        def my_view(request):
            ...
    """
    from functools import wraps
    
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Get tenant
        tenant_id = get_tenant_context(request)
        
        if not tenant_id:
            # Check if user is superuser (bypass)
            if request.user.is_authenticated and getattr(request.user, 'is_superuser', False):
                return view_func(request, *args, **kwargs)
            
            # Deny access
            from django.http import JsonResponse
            return JsonResponse({
                'error': 'Tenant context required',
                'message': 'X-Tenant-ID header or authenticated user required'
            }, status=403)
        
        # Set context
        TenantContext.set(tenant_id, request.user if request.user.is_authenticated else None)
        
        try:
            return view_func(request, *args, **kwargs)
        finally:
            # Clear context after request
            TenantContext.clear()
    
    return wrapper


# ============================================================
# INSTITUTION MODEL
# ============================================================

class Institution(models.Model):
    """
    Institution/Tenant model
    Represents a university or organization
    """
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    # Basic info
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=50, blank=True)
    code = models.CharField(max_length=20, unique=True)
    
    # Contact
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    
    # Settings
    timezone = models.CharField(max_length=50, default='Africa/Lagos')
    currency = models.CharField(max_length=3, default='NGN')
    locale = models.CharField(max_length=10, default='en-NG')
    
    # Branding
    logo = models.ImageField(upload_to='institutions/logos/', blank=True)
    primary_color = models.CharField(max_length=7, default='#1e40af')
    
    # Status
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'institutions'
        verbose_name = 'Institution'
        verbose_name_plural = 'Institutions'
        app_label = 'core'  # Explicit app_label
    
    def __str__(self):
        return self.name
    
    def get_subdomain(self) -> str:
        """Get the subdomain for this institution"""
        return self.code.lower()


# ============================================================
# TENANT-AWARE MANAGER FOR CUSTOM MODELS
# ============================================================

class TenantAwareManager(TenantManager):
    """
    Manager with additional tenant-aware methods
    """
    
    def active(self):
        """Get active records for current tenant"""
        return self.get_queryset().filter(is_active=True)
    
    def for_institution(self, institution_id: str):
        """Filter by specific institution"""
        return self.get_queryset().filter(institution_id=institution_id)


# Export
__all__ = [
    'TenantManager',
    'TenantQuerySet', 
    'TenantMixin',
    'TenantContext',
    'Institution',
    'TenantAwareManager',
    'get_tenant_context',
    'require_tenant',
]