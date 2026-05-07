"""
Async Utilities for UMS

Async helpers and background task support.
"""
import asyncio
import logging
from typing import Callable, Any, List
from functools import wraps

logger = logging.getLogger(__name__)


async def run_async(func: Callable, *args, **kwargs) -> Any:
    """Run sync function in async context"""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, func, *args)


async def gather_async(*tasks) -> List[Any]:
    """Run multiple async tasks"""
    return await asyncio.gather(*tasks)


def async_task(func: Callable) -> Callable:
    """Decorator for async tasks"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(func(*args, **kwargs))
        finally:
            loop.close()
    return wrapper


class BackgroundTask:
    """Background task runner"""
    
    @staticmethod
    def submit(func: Callable, *args, **kwargs):
        """Submit background task"""
        # For Django, use celery or similar
        # celery_app.delay(func, *args, **kwargs)
        logger.info(f"Background task submitted: {func.__name__}")
    
    @staticmethod
    def submit_many(tasks: List[tuple]):
        """Submit many background tasks"""
        for func, args, kwargs in tasks:
            BackgroundTask.submit(func, *args, **kwargs)


def run_in_thread(func: Callable) -> Callable:
    """Run function in thread pool"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        return run_async(func, *args, **kwargs)
    return wrapper