"""
Abstract Viewsets
Standardized, Professional API Viewsets
"""

from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Prefetch
import logging

logger = logging.getLogger(__name__)


# ============================================================
# BASE VIEWSETS
# ============================================================

class BaseViewSet(viewsets.ModelViewSet):
    """Abstract base viewset with common functionality."""
    
    # Default ordering
    ordering = '-created_at'
    ordering_fields = ['created_at', 'updated_at', 'is_active']
    
    # Filter fields
    filter_fields = ['is_active', 'status', 'created_by']
    
    # Search fields
    search_fields = ['uuid']
    
    # Select/Prefetch related
    select_related = []
    prefetch_related = []
    
    def get_queryset(self):
        qs = super().get_queryset()
        
        # Apply ordering
        if self.ordering:
            qs = qs.order_by(*self.ordering)
        
        # Apply select_related
        if self.select_related:
            qs = qs.select_related(*self.select_related)
        
        # Apply prefetch_related
        if self.prefetch_related:
            qs = qs.prefetch_related(*self.prefetch_related)
        
        # Apply search
        search = self.request.query_params.get('search')
        if search and self.search_fields:
            q = Q()
            for field in self.search_fields:
                q |= Q(**{f'{field}__icontains': search})
            qs = qs.filter(q)
        
        # Apply filters
        for field in self.filter_fields:
            value = self.request.query_params.get(field)
            if value is not None:
                qs = qs.filter(**{field: value})
        
        return qs
    
    def get_serializer_class(self):
        # Override to customize serializer based on action
        action_serializer = getattr(self, f'{self.action}_serializer_class', None)
        if action_serializer:
            return action_serializer
        return super().get_serializer_class()
    
    def create(self, request, *args, **kwargs):
        # Set created_by
        if hasattr(self, 'get_serializer'):
            serializer = self.get_serializer(data=request.data)
            if hasattr(serializer, 'fields') and 'created_by' in serializer.fields:
                request.data['created_by'] = request.user.id
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        # Set updated_by
        if hasattr(self, 'get_serializer'):
            serializer = self.get_serializer(data=request.data)
            if hasattr(serializer, 'fields') and 'updated_by' in serializer.fields:
                request.data['updated_by'] = request.user.id
        return super().update(request, *args, **kwargs)
    
    # Standard actions
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get only active objects."""
        qs = self.get_queryset().filter(is_active=True)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def list_all(self, request):
        """List all objects without pagination."""
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


class ReadOnlyViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    """Read-only viewset."""
    
    pass


class CreateViewSet(mixins.CreateModelMixin,
                 viewsets.GenericViewSet):
    """Create-only viewset."""
    
    pass


class UpdateViewSet(mixins.UpdateModelMixin,
                  mixins.PartialUpdateMixin,
                  viewsets.GenericViewSet):
    """Update-only viewset."""
    
    pass


class DeleteViewSet(mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """Delete-only viewset."""
    
    def destroy(self, request, *args, **kwargs):
        # Soft delete instead
        instance = self.get_object()
        if hasattr(instance, 'delete'):
            instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ============================================================
# PAGINATION
# ============================================================

class BasePagination:
    """Standard pagination."""
    
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


# ============================================================
# FILTERS
# ============================================================

class BaseFilterSet:
    """Base filter set."""
    
    @classmethod
    def filter_queryset(cls, queryset, params):
        # Apply search
        search = params.get('search')
        if search:
            queryset = queryset.filter(
                Q(uuid__icontains=search)
            )
        
        # Apply status
        status = params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Apply is_active
        is_active = params.get('is_active')
        if is_active:
            queryset = queryset.filter(is_active=is_active == 'true')
        
        return queryset


# ============================================================
# PERMISSIONS
# ============================================================

class IsOwnerOrReadOnly(IsAuthenticated):
    """Allow owners to edit."""
    
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj.created_by == request.user


class IsStaffOrReadOnly(IsAuthenticated):
    """Allow staff to edit."""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class IsAdminOrReadOnly(IsAuthenticated):
    """Allow admin to edit."""
    
    def has_permission(self, request, view):
        return request.user and (
            request.user.is_staff or request.user.is_superuser
        )


# ============================================================
# ACTIONS
# ============================================================

class BaseActionMixin:
    """Mixin for standard actions."""
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate object."""
        instance = self.get_object()
        instance.is_active = True
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate object."""
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        """Archive object."""
        instance = self.get_object()
        instance.status = 'archived'
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        """Restore object."""
        instance = self.get_object()
        instance.status = 'active'
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def export(self, request):
        """Export data."""
        from django.http import HttpResponse
        import csv
        import io
        
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write headers
        if serializer.data:
            writer.writerow(serializer.data[0].keys())
            
            # Write data
            for row in serializer.data:
                writer.writerow(row.values())
        
        response = HttpResponse(output.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'
        return response


# ============================================================
# LOGGING
# ============================================================

class BaseLogMixin:
    """Mixin for logging."""
    
    def create(self, request, *args, **kwargs):
        logger.info(f'CREATE: {self.__class__.__name__} by {request.user}')
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        logger.info(f'UPDATE: {self.__class__.__name__} by {request.user}')
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        logger.info(f'DELETE: {self.__class__.__name__} by {request.user}')
        return super().destroy(request, *args, **kwargs)