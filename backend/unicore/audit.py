"""
Audit Trail System for UMS

Provides comprehensive audit logging for all major
operations in the system.
"""
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)


class AuditAction:
    """Audit action types"""
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    LOGIN = "login"
    LOGOUT = "logout"
    EXPORT = "export"
    IMPORT = "import"


class AuditLogger:
    """Audit logger for tracking operations"""
    
    @staticmethod
    def log(
        action: str,
        model: str,
        object_id: Any,
        user_id: Optional[int] = None,
        changes: Optional[Dict[str, Any]] = None,
        description: str = ""
    ):
        """
        Log an audit event
        
        Args:
            action: Action type (create, read, update, delete, etc.)
            model: Model name
            object_id: ID of the object
            user_id: ID of the user (if any)
            changes: Dictionary of field changes
            description: Human-readable description
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "model": model,
            "object_id": str(object_id),
            "user_id": user_id,
            "changes": changes,
            "description": description
        }
        
        logger.info(f"AUDIT: {json.dumps(entry)}")
        
        # Store in database if model exists
        try:
            from apps.core.models import AuditLog
            if user_id:
                user = get_user_model().objects.get(id=user_id) if user_id else None
            else:
                user = None
            AuditLog.objects.create(
                action=action,
                model=model,
                object_id=str(object_id),
                user=user,
                changes=json.dumps(changes) if changes else None,
                description=description
            )
        except Exception as e:
            logger.debug(f"Audit DB log skipped: {e}")
    
    @staticmethod
    def log_create(model: str, object_id: Any, user_id: Optional[int] = None, description: str = ""):
        """Log a create action"""
        AuditLogger.log(AuditAction.CREATE, model, object_id, user_id, description=description)
    
    @staticmethod
    def log_read(model: str, object_id: Any, user_id: Optional[int] = None):
        """Log a read action"""
        AuditLogger.log(AuditAction.READ, model, object_id, user_id)
    
    @staticmethod
    def log_update(
        model: str,
        object_id: Any,
        changes: Dict[str, Any],
        user_id: Optional[int] = None,
        description: str = ""
    ):
        """Log an update action"""
        AuditLogger.log(
            AuditAction.UPDATE,
            model,
            object_id,
            user_id,
            changes,
            description
        )
    
    @staticmethod
    def log_delete(
        model: str,
        object_id: Any,
        user_id: Optional[int] = None,
        description: str = ""
    ):
        """Log a delete action"""
        AuditLogger.log(
            AuditAction.DELETE,
            model,
            object_id,
            user_id,
            description=description
        )


def audit_log(action: str, model: str, object_id: Any, **kwargs):
    """Convenience function for audit logging"""
    AuditLogger.log(action, model, object_id, **kwargs)