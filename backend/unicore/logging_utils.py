"""
Logging Utilities for UMS

Custom logging helpers.
"""
import logging
import json
from typing import Any, Dict, Optional
from datetime import datetime
from django.conf import settings


def get_logger(name: str) -> logging.Logger:
    """Get logger instance"""
    return logging.getLogger(name)


class StructuredLogger:
    """Logger with structured output"""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
    
    def log(
        self,
        level: str,
        message: str,
        extra: Dict[str, Any] = None
    ):
        """Log structured message"""
        data = {
            "timestamp": datetime.now().isoformat(),
            "message": message,
            **extra
        }
        
        getattr(self.logger, level)(json.dumps(data))
    
    def info(self, message: str, **extra):
        self.log("info", message, extra)
    
    def warning(self, message: str, **extra):
        self.log("warning", message, extra)
    
    def error(self, message: str, **extra):
        self.log("error", message, extra)
    
    def debug(self, message: str, **extra):
        self.log("debug", message, extra)


class RequestLogger:
    """Log API requests"""
    
    @staticmethod
    def log_request(request, response_time: float = None):
        """Log request details"""
        logger = logging.getLogger("api")
        logger.info(json.dumps({
            "method": request.method,
            "path": request.path,
            "user": str(request.user) if request.user.is_authenticated else "anonymous",
            "response_time": response_time,
            "timestamp": datetime.now().isoformat()
        }))
    
    @staticmethod
    def log_error(request, error: Exception):
        """Log request error"""
        logger = logging.getLogger("api")
        logger.error(json.dumps({
            "method": request.method,
            "path": request.path,
            "error": str(error),
            "timestamp": datetime.now().isoformat()
        }))


def log_model_change(instance, action: str, user=None):
    """Log model change"""
    logger = logging.getLogger("models")
    logger.info(json.dumps({
        "action": action,
        "model": instance.__class__.__name__,
        "id": str(instance.id),
        "user": str(user) if user else None,
        "timestamp": datetime.now().isoformat()
    }))