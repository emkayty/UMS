"""
Pagination Utilities

Standard pagination helpers.
"""
from typing import Any, Dict, List
from django.http import HttpRequest


class PaginationParams:
    """Parse pagination params from request"""
    
    DEFAULT_PAGE = 1
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100
    
    def __init__(self, request: HttpRequest):
        self.page = self.DEFAULT_PAGE
        self.page_size = self.DEFAULT_PAGE_SIZE
        
        # Parse page
        page_param = request.GET.get('page')
        if page_param:
            try:
                self.page = max(1, int(page_param))
            except ValueError:
                pass
        
        # Parse page_size
        size_param = request.GET.get('page_size')
        if size_param:
            try:
                self.page_size = min(self.MAX_PAGE_SIZE, max(1, int(size_param)))
            except ValueError:
                pass
        
        # Parse ordering
        self.ordering = request.GET.get('ordering', 'id')
    
    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size
    
    @property
    def limit(self) -> int:
        return self.page_size


def paginate_queryset(
    queryset,
    page: int = 1,
    page_size: int = 20
) -> Dict[str, Any]:
    """Paginate Django queryset"""
    total = queryset.count()
    start = (page - 1) * page_size
    end = start + page_size
    
    items = list(queryset[start:end])
    
    return {
        'items': items,
        'pagination': {
            'page': page,
            'page_size': page_size,
            'total': total,
            'total_pages': (total + page_size - 1) // page_size
        }
    }


def get_pagination_meta(total: int, page: int, page_size: int) -> Dict[str, Any]:
    """Get pagination metadata"""
    return {
        'page': page,
        'page_size': page_size,
        'total': total,
        'total_pages': (total + page_size - 1) // page_size,
        'has_next': page * page_size < total,
        'has_prev': page > 1
    }