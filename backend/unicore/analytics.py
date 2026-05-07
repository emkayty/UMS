"""
Analytics Utilities for UMS

Basic analytics for tracking and metrics.
"""
from typing import Dict, Any, List
from datetime import datetime, timedelta
from django.db.models import Count, Avg, Sum, Max, Min
from django.utils import timezone


def get_model_stats(model) -> Dict[str, Any]:
    """Get basic model statistics"""
    return {
        'total': model.objects.count(),
        'created_today': model.objects.filter(
            created_at__gte=timezone.now().date()
        ).count(),
    }


def get_user_activity_stats(user) -> Dict[str, Any]:
    """Get user activity stats"""
    return {
        'last_login': user.last_login,
        'date_joined': user.date_joined,
    }


def aggregate_by_field(
    model,
    field: str,
    aggregate: str = 'count'
) -> List[Dict[str, Any]]:
    """Aggregate by field"""
    from django.db.models import Count
    
    aggregates = {
        'count': Count('id'),
        'sum': Sum(field),
        'avg': Avg(field),
        'max': Max(field),
        'min': Min(field),
    }
    
    result = model.objects.values(field).annotate(
        value=aggregates.get(aggregate, Count('id'))
    )
    return list(result)


def get_daily_stats(model, days: int = 7) -> List[Dict[str, Any]]:
    """Get daily statistics"""
    stats = []
    today = timezone.now().date()
    
    for i in range(days):
        date = today - timedelta(days=i)
        count = model.objects.filter(created_at__date=date).count()
        stats.append({
            'date': date.isoformat(),
            'count': count
        })
    
    return stats


def track_api_call(endpoint: str, duration: float):
    """Track API call (integrate with analytics)"""
    # Log to analytics service
    pass


def get_popular_endpoints(limit: int = 10) -> List[Dict[str, Any]]:
    """Get popular endpoints"""
    # Query from logs
    return []