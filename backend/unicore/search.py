"""
Search Utilities for UMS

Search and filter helpers.
"""
from typing import List, Dict, Any, Optional
from django.db.models import Q
import re


def search_queryset(
    queryset,
    search_fields: List[str],
    query: str
):
    """Search queryset"""
    if not query:
        return queryset
    
    q = Q()
    for field in search_fields:
        q |= Q(**{f"{field}__icontains": query})
    
    return queryset.filter(q)


def advanced_search(
    queryset,
    filters: Dict[str, Any]
):
    """Advanced search with multiple filters"""
    for field, value in filters.items():
        if value is not None and value != "":
            if isinstance(value, list):
                queryset = queryset.filter(**{f"{field}__in": value})
            else:
                queryset = queryset.filter(**{field: value})
    
    return queryset


def fuzzy_search(
    queryset,
    field: str,
    query: str,
    threshold: float = 0.6
):
    """Fuzzy search (simple implementation)"""
    if not query:
        return queryset
    
    # Simple contains search
    return queryset.filter(**{f"{field}__icontains": query})


def search_by_multiple_fields(
    queryset,
    query: str,
    fields: List[str]
) -> List[Dict[str, Any]]:
    """Search by multiple fields"""
    results = []
    
    for item in queryset:
        item_dict = {f: getattr(item, f, "") for f in fields}
        if any(query.lower() in str(v).lower() for v in item_dict.values()):
            results.append(item)
    
    return results


def build_filters(params: Dict[str, Any]) -> Dict[str, Any]:
    """Build filters from request params"""
    filters = {}
    
    for key, value in params.items():
        if value and value != "" and value != "null":
            filters[key] = value
    
    return filters