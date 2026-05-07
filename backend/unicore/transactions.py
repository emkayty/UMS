"""
Database Transaction Helpers for UMS

Provides transaction management utilities.
"""
import logging
from functools import wraps
from typing import Callable, Any
from django.db import transaction, connection, IntegrityError

logger = logging.getLogger(__name__)


class TransactionManager:
    """Transaction manager"""
    
    @staticmethod
    def atomic(func: Callable) -> Callable:
        """Decorator for atomic transactions"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            with transaction.atomic():
                return func(*args, **kwargs)
        return wrapper
    
    @staticmethod
    def with_savepoint(func: Callable) -> Callable:
        """Decorator for transactions with savepoints"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            with transaction.atomic():
                sid = transaction.savepoint()
                try:
                    result = func(*args, **kwargs)
                    transaction.savepoint_commit(sid)
                    return result
                except Exception as e:
                    transaction.savepoint_rollback(sid)
                    raise
        return wrapper


def atomic(func: Callable) -> Callable:
    """Convenience decorator for atomic transactions"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        with transaction.atomic():
            return func(*args, **kwargs)
    return wrapper


def with_retry(max_retries: int = 3, delay: float = 0.1) -> Callable:
    """Decorator for retrying failed transactions"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            import time
            last_exception = None
            for attempt in range(max_retries):
                try:
                    with transaction.atomic():
                        return func(*args, **kwargs)
                except IntegrityError as e:
                    logger.warning(f"Transaction retry {attempt + 1}/{max_retries}: {e}")
                    last_exception = e
                    if attempt < max_retries - 1:
                        time.sleep(delay)
                    continue
            raise last_exception
        return wrapper
    return decorator


def get_connection_status() -> dict:
    """Get database connection status"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        return {
            "connected": True,
            "vendor": connection.vendor,
        }
    except Exception as e:
        return {
            "connected": False,
            "error": str(e)
        }


def execute_raw_sql(sql: str, params: tuple = ()) -> list:
    """Execute raw SQL"""
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        if cursor.description:
            return cursor.fetchall()
        return []