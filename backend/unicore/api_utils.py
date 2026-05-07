"""
API Utilities for UMS

API-level helpers.
"""
from typing import Any, Dict, List, Optional
from django.http import HttpRequest, JsonResponse
import json


def success_json(data: Any = None, message: str = "Success") -> JsonResponse:
    """Return success JSON response"""
    return JsonResponse({
        "success": True,
        "message": message,
        "data": data
    })


def error_json(
    error: str,
    code: str = "ERROR",
    status: int = 400
) -> JsonResponse:
    """Return error JSON response"""
    return JsonResponse({
        "success": False,
        "error": error,
        "code": code
    }, status=status)


def paginated_json(
    items: List,
    page: int = 1,
    page_size: int = 20,
    total: int = 0
) -> JsonResponse:
    """Return paginated JSON response"""
    return JsonResponse({
        "success": True,
        "data": items,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "pages": (total + page_size - 1) // page_size
        }
    })


def get_client_ip(request: HttpRequest) -> str:
    """Get client IP from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')


def get_request_data(request: HttpRequest) -> Dict[str, Any]:
    """Get request data (JSON or form)"""
    if request.method == 'POST':
        if request.content_type and 'application/json' in request.content_type:
            try:
                return json.loads(request.body)
            except:
                return {}
        return dict(request.POST)
    return dict(request.GET)


def validate_json_payload(request: HttpRequest) -> Optional[Dict]:
    """Validate JSON payload"""
    try:
        return json.loads(request.body)
    except:
        return None


def require_params(params: List[str]) -> callable:
    """Decorator to require parameters"""
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            data = get_request_data(request)
            missing = [p for p in params if p not in data]
            if missing:
                return error_json(f"Missing parameters: {missing}")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator