"""
Nigerian Operational Optimization Utilities
Optimized for low bandwidth, unstable internet, and mobile-first
"""

import gzip
import hashlib
import time
from typing import Any, Callable, Dict, List, Optional
from functools import wraps
from django.core.cache import cache
from django.http import HttpRequest


class FieldSelector:
    """
    Select specific fields from API responses
    Reduces payload size for low-bandwidth optimization
    
    Usage:
        ?fields=id,name,email
    Returns only id, name, email
    """
    
    @staticmethod
    def parse_fields(fields_str: str) -> List[str]:
        """Parse comma-separated fields"""
        if not fields_str:
            return []
        return [f.strip() for f in fields_str.split(',') if f.strip()]
    
    @staticmethod
    def filter_object(obj: Any, fields: List[str]) -> Dict:
        """Filter object to only selected fields"""
        if not fields:
            return obj
        
        if hasattr(obj, '__dict__'):
            # Django model
            return {f: getattr(obj, f, None) for f in fields if hasattr(obj, f)}
        
        if isinstance(obj, dict):
            return {f: obj.get(f) for f in fields if f in obj}
        
        return obj
    
    @staticmethod
    def filter_queryset(queryset, fields: List[str]):
        """Filter queryset to only selected fields - for optimized queries"""
        if not fields:
            return queryset.only(*fields)
        return queryset.only(*fields)


class ResponseCompressor:
    """
    Compress API responses for low bandwidth
    Uses gzip compression
    """
    
    @staticmethod
    def compress(data: bytes) -> bytes:
        """Compress bytes using gzip"""
        return gzip.compress(data, compresslevel=6)
    
    @staticmethod
    def decompress(data: bytes) -> bytes:
        """Decompress bytes"""
        return gzip.decompress(data)


class CacheOptimizer:
    """
    Optimized caching for Nigerian conditions
    Uses longer timeouts for slow connections
    """
    
    # Default timeouts optimized for Nigeria
    SHORT_TIMEOUT = 60 * 5  # 5 minutes
    MEDIUM_TIMEOUT = 60 * 30  # 30 minutes  
    LONG_TIMEOUT = 60 * 60 * 24  # 24 hours
    
    @staticmethod
    def get_stale_while_validate(key: str, stale_timeout: int = 300):
        """
        Cache pattern: serve stale while revalidating
        Good for slow connections
        """
        # Try to get cached value
        cached = cache.get(key)
        
        if cached:
            return cached, True
        
        return None, False
    
    @staticmethod
    def cache_with_fallback(
        key: str,
        fetcher: Callable,
        timeout: int = MEDIUM_TIMEOUT,
        fallback_timeout: int = LONG_TIMEOUT
    ):
        """
        Cache with fallback - use cached while fetching new
        Optimized for slow networks
        """
        # Try cache first
        cached = cache.get(key)
        if cached:
            return cached
        
        # Fetch fresh
        try:
            fresh = fetcher()
            cache.set(key, fresh, timeout)
            return fresh
        except Exception as e:
            # Try fallback cache
            fallback = cache.get(f'{key}_fallback')
            if fallback:
                return fallback
            raise e


class RetryOptimizer:
    """
    Optimized retry logic for unstable Nigerian networks
    Longer delays, more retries
    """
    
    # Optimized for Nigerian conditions
    DEFAULT_RETRIES = 5
    INITIAL_DELAY = 2  # 2 seconds
    MAX_DELAY = 30  # 30 seconds
    BACKOFF_FACTOR = 2
    
    @staticmethod
    def calculate_delay(attempt: int) -> int:
        """Calculate delay with exponential backoff"""
        delay = min(
            RetryOptimizer.INITIAL_DELAY * (RetryOptimizer.BACKOFF_FACTOR ** attempt),
            RetryOptimizer.MAX_DELAY
        )
        return delay
    
    @staticmethod
    def should_retry(exception: Exception) -> bool:
        """Determine if error is retryable"""
        retryable = (
            ConnectionError,
            TimeoutError,
            ConnectionResetError,
        )
        return isinstance(exception, retryable)


class OptimizedAPIResponse:
    """
    Creates optimized API responses for Nigerian conditions
    Smaller payloads, faster perceived performance
    """
    
    @staticmethod
    def create_response(
        data: Any,
        fields: Optional[List[str]] = None,
        use_compression: bool = True,
        include_meta: bool = True
    ) -> Dict:
        """Create optimized response"""
        # Filter fields if specified
        if fields:
            if isinstance(data, list):
                data = [
                    FieldSelector.filter_object(item, fields) 
                    for item in data
                ]
            else:
                data = FieldSelector.filter_object(data, fields)
        
        response = {'data': data}
        
        # Include lightweight metadata
        if include_meta:
            response['meta'] = {
                'generated_at': int(time.time()),
                'optimized': bool(fields),
            }
        
        return response


class NetworkOptimizer:
    """
    Optimize for slow/unstable networks
    """
    
    @staticmethod
    def get_client_ip(request: HttpRequest) -> str:
        """Get client IP for rate limiting"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR', '')
    
    @staticmethod
    def is_slow_network(request: HttpRequest) -> bool:
        """Detect slow network via headers"""
        # Check for save-data header
        save_data = request.META.get('HTTP_SAVE_DATA', '')
        return save_data.lower() == 'on'
    
    @staticmethod
    def get_optimizations_for_request(request: HttpRequest) -> Dict:
        """Get optimizations for this request"""
        optimizations = {
            'minimal': False,
            'compressed': True,
            'cached': True,
        }
        
        # Check for slow network
        if NetworkOptimizer.is_slow_network(request):
            optimizations['minimal'] = True
            optimizations['compressed'] = True
        
        return optimizations


# Decorator for optimized API calls
def optimized_api_call(
    cache_key: Optional[str] = None,
    timeout: int = 300,
    retry: bool = True
):
    """
    Decorator to optimize API calls for Nigerian conditions
    
    Usage:
        @optimized_api_call(cache_key='user:1', timeout=300)
        def get_user_data():
            return User.objects.get(id=1)
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Try cache first
            if cache_key:
                cached = cache.get(cache_key)
                if cached:
                    return cached
            
            # Retry logic
            max_retries = 3 if retry else 1
            
            for attempt in range(max_retries):
                try:
                    result = func(*args, **kwargs)
                    
                    # Cache result
                    if cache_key and result:
                        cache.set(cache_key, result, timeout)
                    
                    return result
                    
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    delay = RetryOptimizer.calculate_delay(attempt)
                    time.sleep(delay)
            
        return wrapper
    return decorator


# Export
__all__ = [
    'FieldSelector',
    'ResponseCompressor', 
    'CacheOptimizer',
    'RetryOptimizer',
    'OptimizedAPIResponse',
    'NetworkOptimizer',
    'optimized_api_call',
]