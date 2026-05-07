"""
Service Layer for UMS

Base service class for business logic layer.
"""
from typing import Any, Dict, List, Optional, Type
from django.db import models
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)


class ServiceError(Exception):
    """Service error"""
    pass


class BaseService:
    """Base service class"""
    
    model: Type[models.Model] = None
    cache_ttl: int = 300  # 5 minutes
    
    def __init__(self):
        if self.model is None:
            raise NotImplementedError("Must set model class")
    
    def get_queryset(self) -> models.QuerySet:
        """Get base queryset"""
        return self.model.objects.all()
    
    def get(self, pk: Any) -> Optional[models.Model]:
        """Get by primary key"""
        return self.get_queryset().filter(pk=pk).first()
    
    def get_by_id(self, id: str) -> Optional[models.Model]:
        """Get by ID field"""
        return self.get_queryset().filter(id=id).first()
    
    def all(self) -> List[models.Model]:
        """Get all records"""
        return list(self.get_queryset())
    
    def filter(self, **kwargs) -> List[models.Model]:
        """Filter records"""
        return list(self.get_queryset().filter(**kwargs))
    
    def create(self, **data) -> models.Model:
        """Create record"""
        return self.model.objects.create(**data)
    
    def update(self, pk: Any, **data) -> Optional[models.Model]:
        """Update record"""
        obj = self.get(pk)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            obj.save()
        return obj
    
    def delete(self, pk: Any) -> bool:
        """Delete record"""
        obj = self.get(pk)
        if obj:
            obj.delete()
            return True
        return False
    
    def count(self) -> int:
        """Count records"""
        return self.get_queryset().count()
    
    def exists(self, **kwargs) -> bool:
        """Check if exists"""
        return self.get_queryset().filter(**kwargs).exists()


class CachedService(BaseService):
    """Service with caching"""
    
    def get_cached(self, key: str) -> Optional[Any]:
        """Get from cache"""
        return cache.get(key)
    
    def set_cached(self, key: str, value: Any, ttl: int = None):
        """Set cache"""
        cache.set(key, value, ttl or self.cache_ttl)
    
    def invalidate_cache(self, key: str):
        """Invalidate cache"""
        cache.delete(key)
    
    def get_or_cache(
        self, 
        key: str, 
        fetch_func, 
        ttl: int = None
    ) -> Any:
        """Get from cache or fetch"""
        value = self.get_cached(key)
        if value is None:
            value = fetch_func()
            self.set_cached(key, value, ttl)
        return value


class StudentService(CachedService):
    """Student service"""
    model = None  # Set in app


class FacultyService(CachedService):
    """Faculty service"""
    model = None  # Set in app


def get_service(name: str) -> BaseService:
    """Get service by name"""
    services = {
        'student': StudentService,
        'faculty': FacultyService,
    }
    if name not in services:
        raise ServiceError(f"Unknown service: {name}")
    return services[name]()