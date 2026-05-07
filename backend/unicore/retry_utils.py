"""
Retry and Cache Utilities

Provides retry decorators and cache utilities.
"""
import time
import logging
from functools import wraps
from typing import Callable, Any, Optional

logger = logging.getLogger(__name__)


# Retry decorators
def retry(
    max_attempts: int = 3,
    delay: float = 0.5,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,)
) -> Callable:
    """
    Retry decorator with exponential backoff
    
    Args:
        max_attempts: Maximum number of attempts
        delay: Initial delay between retries (seconds)
        backoff: Backoff multiplier
        exceptions: Exceptions to catch
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        logger.warning(
                            f"Retry {attempt + 1}/{max_attempts}: {func.__name__} - {e}"
                        )
                        time.sleep(current_delay)
                        current_delay *= backoff
                    continue
            
            raise last_exception
        
        return wrapper
    return decorator


def retry_on_condition(
    max_attempts: int = 3,
    delay: float = 0.5,
    condition: Callable = lambda x: x is None
) -> Callable:
    """
    Retry until condition is met
    
    Args:
        max_attempts: Maximum attempts
        delay: Delay between attempts
        condition: Function to check result
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                result = func(*args, **kwargs)
                if not condition(result):
                    return result
                if attempt < max_attempts - 1:
                    time.sleep(delay)
            return result
        
        return wrapper
    return decorator


# Cache utilities
def cache_key(*args, prefix: str = "") -> str:
    """Generate cache key"""
    parts = [prefix] if prefix else []
    parts.extend([str(arg) for arg in args])
    return ":".join(parts)


def cache_result(ttl: int = 300, prefix: str = ""):
    """Cache function result"""
    from django.core.cache import cache
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = cache_key(*args, prefix=prefix or func.__name__)
            result = cache.get(key)
            
            if result is None:
                result = func(*args, **kwargs)
                cache.set(key, result, ttl)
            
            return result
        
        return wrapper
    return decorator


def invalidate_cache(prefix: str = "", *keys):
    """Invalidate cache keys"""
    from django.core.cache import cache
    
    for key in keys:
        cache.delete(cache_key(key, prefix=prefix))


# Rate limiting
class RateLimiter:
    """Simple rate limiter"""
    
    def __init__(self, key: str, limit: int, period: int = 60):
        self.key = f"rate_limit:{key}"
        self.limit = limit
        self.period = period
    
    def is_allowed(self) -> bool:
        """Check if request is allowed"""
        from django.core.cache import cache
        
        # Get current count
        count = cache.get(self.key, 0)
        
        if count >= self.limit:
            return False
        
        # Increment
        if count == 0:
            cache.set(self.key, 1, self.period)
        else:
            cache.incr(self.key)
        
        return True
    
    def get_remaining(self) -> int:
        """Get remaining requests"""
        from django.core.cache import cache
        count = cache.get(self.key, 0)
        return max(0, self.limit - count)