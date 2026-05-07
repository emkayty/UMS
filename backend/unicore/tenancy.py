"""
Multi-Tenant Support for UMS

Provides tenant isolation for multi-tenant SaaS deployments.
"""
from typing import Optional, Any
from django.http import HttpRequest
from django.db import models


class TenantContext:
    """Tenant context manager"""
    
    _current_tenant: Optional[models.Model] = None
    
    @classmethod
    def set_tenant(cls, tenant: models.Model):
        """Set current tenant"""
        cls._current_tenant = tenant
    
    @classmethod
    def get_tenant(cls) -> Optional[models.Model]:
        """Get current tenant"""
        return cls._current_tenant
    
    @classmethod
    def clear_tenant(cls):
        """Clear current tenant"""
        cls._current_tenant = None
    
    @classmethod
    def has_tenant(cls) -> bool:
        """Check if tenant is set"""
        return cls._current_tenant is not None


def get_tenant_from_request(request: HttpRequest) -> Optional[str]:
    """Extract tenant ID from request"""
    # Check header
    tenant_id = request.headers.get('X-Tenant-ID')
    if tenant_id:
        return tenant_id
    
    # Check subdomain
    host = request.get_host()
    if '.' in host:
        subdomain = host.split('.')[0]
        if subdomain not in ('localhost', 'www', 'api'):
            return subdomain
    
    return None


def get_current_tenant_id() -> Optional[str]:
    """Get current tenant ID"""
    tenant = TenantContext.get_tenant()
    if tenant:
        return str(tenant.id)
    return None


def require_tenant(request: HttpRequest) -> Optional[str]:
    """Require tenant - returns tenant_id or None"""
    return get_tenant_from_request(request)


class TenantMixin:
    """Mixin to add tenant awareness to models"""
    
    # Override in model
    # tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    
    @property
    def tenant_id(self) -> Optional[str]:
        """Get tenant ID from model"""
        if hasattr(self, 'tenant'):
            return str(self.tenant.id) if self.tenant else None
        return None
    
    class Meta:
        abstract = True


def filter_by_tenant(queryset, tenant_id: str):
    """Filter queryset by tenant"""
    if hasattr(queryset.model, 'tenant'):
        return queryset.filter(tenant_id=tenant_id)
    return queryset