"""
Standard API Response Schema
Standardized format for all API responses across UMS.
"""
from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel
from datetime import datetime


class ApiResponse(BaseModel):
    """Standard API response wrapper."""
    success: bool = True
    message: str = "Success"
    data: Optional[Any] = None
    timestamp: str = datetime.now().isoformat()


class PaginatedResponse(BaseModel):
    """Standard paginated response."""
    success: bool = True
    message: str = "Success"
    data: list = []
    pagination: dict = {}


class ErrorResponse(BaseModel):
    """Standard error response."""
    success: bool = False
    error: str
    code: str = "ERROR"
    details: Optional[dict] = None
    timestamp: str = datetime.now().isoformat()


def success_response(data: Any = None, message: str = "Success") -> dict:
    """Create a success response."""
    return ApiResponse(
        success=True,
        message=message,
        data=data,
        timestamp=datetime.now().isoformat()
    ).model_dump()


def error_response(error: str, code: str = "ERROR", details: dict = None) -> dict:
    """Create an error response."""
    return ErrorResponse(
        success=False,
        error=error,
        code=code,
        details=details,
        timestamp=datetime.now().isoformat()
    ).model_dump()


def paginated_response(data: list, page: int = 1, page_size: int = 20, total: int = 0) -> dict:
    """Create a paginated response."""
    return PaginatedResponse(
        success=True,
        message="Success",
        data=data,
        pagination={
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": (total + page_size - 1) // page_size
        }
    ).model_dump()