"""
Optimized API Filters
Provides field selection and low-bandwidth optimizations
"""

from typing import List, Optional, Any, Dict
from ninja import Query, Router, Schema
from pydantic import Field


class FieldSelectionParams(Schema):
    """Query parameters for field selection"""
    fields: Optional[str] = Field(
        None, 
        description="Comma-separated fields to include"
    )
    limit: Optional[int] = Field(
        20, 
        ge=1, 
        le=100,
        description="Max records to return"
    )
    offset: Optional[int] = Field(
        0, 
        ge=0,
        description="Records to skip"
    )


class OptimizedResponse(Schema):
    """Optimized response wrapper"""
    data: List[Dict] = Field(default_factory=list)
    meta: Dict = Field(default_factory=dict)


def apply_field_selection(
    queryset: Any,
    fields: Optional[str],
    limit: int = 20,
    offset: int = 0
) -> tuple[Any, Dict]:
    """
    Apply field selection to queryset
    
    Returns: (optimized_queryset, metadata)
    """
    # Parse fields
    field_list = []
    if fields:
        field_list = [f.strip() for f in fields.split(',') if f.strip()]
    
    # Apply field selection if specified
    if field_list:
        queryset = queryset.only(*field_list)
    
    # Apply pagination
    total = queryset.count()
    queryset = queryset[offset:offset + limit]
    items = list(queryset.values() if field_list else queryset)
    
    # Build metadata
    meta = {
        'total': total,
        'limit': limit,
        'offset': offset,
        'has_more': (offset + limit) < total,
        'optimized': bool(field_list),
    }
    
    return items, meta


def create_optimized_response(
    data: List[Any],
    total: int,
    limit: int = 20,
    offset: int = 0,
    optimized: bool = False
) -> Dict:
    """
    Create an optimized API response
    """
    return {
        'data': data,
        'meta': {
            'total': total,
            'limit': limit,
            'offset': offset,
            'has_more': (offset + limit) < total,
            'optimized': optimized,
        }
    }


# Export
__all__ = [
    'FieldSelectionParams',
    'OptimizedResponse', 
    'apply_field_selection',
    'create_optimized_response',
]