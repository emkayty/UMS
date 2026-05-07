"""
Batch Operations for Bulk Data Processing

Provides efficient bulk operations for creating, updating,
and deleting large datasets in the UMS.
"""
from typing import List, Dict, Any, Optional
from django.db import transaction
from django.db.models import QuerySet
import logging

logger = logging.getLogger(__name__)


class BatchOperation:
    """Base class for batch operations"""
    
    def __init__(self, batch_size: int = 1000):
        self.batch_size = batch_size
        self.results = {
            'created': 0,
            'updated': 0,
            'deleted': 0,
            'errors': []
        }
    
    def log_progress(self, operation: str, count: int):
        """Log progress of batch operation"""
        logger.info(f"Batch {operation}: {count} items processed")
    
    def handle_error(self, error: Exception, item: Any):
        """Handle errors during batch operation"""
        error_msg = f"Error processing {item}: {str(error)}"
        logger.error(error_msg)
        self.results['errors'].append(error_msg)


class BulkCreateOperation(BatchOperation):
    """Bulk create operation for creating multiple records"""
    
    def execute(self, model_class, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Bulk create records
        
        Args:
            model_class: Django model class
            items: List of dictionaries representing records
            
        Returns:
            Dictionary with results
        """
        try:
            with transaction.atomic():
                # Process in batches
                for i in range(0, len(items), self.batch_size):
                    batch = items[i:i + self.batch_size]
                    model_class.objects.bulk_create([
                        model_class(**item) for item in batch
                    ])
                    self.results['created'] += len(batch)
                    self.log_progress('create', len(batch))
            
            return self.results
        except Exception as e:
            self.handle_error(e, 'bulk_create')
            return self.results


class BulkUpdateOperation(BatchOperation):
    """Bulk update operation for updating multiple records"""
    
    def execute(self, queryset: QuerySet, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Bulk update records
        
        Args:
            queryset: Django queryset
            updates: Dictionary of field updates
            
        Returns:
            Dictionary with results
        """
        try:
            with transaction.atomic():
                count = queryset.update(**updates)
                self.results['updated'] = count
                self.log_progress('update', count)
            
            return self.results
        except Exception as e:
            self.handle_error(e, 'bulk_update')
            return self.results


class BulkDeleteOperation(BatchOperation):
    """Bulk delete operation for deleting multiple records"""
    
    def execute(self, queryset: QuerySet) -> Dict[str, Any]:
        """
        Bulk delete records
        
        Args:
            queryset: Django queryset
            
        Returns:
            Dictionary with results
        """
        try:
            with transaction.atomic():
                count, _ = queryset.delete()
                self.results['deleted'] = count
                self.log_progress('delete', count)
            
            return self.results
        except Exception as e:
            self.handle_error(e, 'bulk_delete')
            return self.results


class BulkUpsertOperation(BatchOperation):
    """Bulk upsert operation for creating/updating records"""
    
    def execute(
        self,
        model_class,
        items: List[Dict[str, Any]],
        lookup_field: str = 'id'
    ) -> Dict[str, Any]:
        """
        Bulk upsert records
        
        Args:
            model_class: Django model class
            items: List of dictionaries representing records
            lookup_field: Field to use for lookup (default: 'id')
            
        Returns:
            Dictionary with results
        """
        try:
            with transaction.atomic():
                for i in range(0, len(items), self.batch_size):
                    batch = items[i:i + self.batch_size]
                    
                    for item in batch:
                        lookup_value = item.pop(lookup_field, None)
                        if lookup_value:
                            # Update existing
                            obj, created = model_class.objects.update_or_create(
                                **{lookup_field: lookup_value},
                                defaults=item
                            )
                            if created:
                                self.results['created'] += 1
                            else:
                                self.results['updated'] += 1
                        else:
                            # Create new
                            model_class.objects.create(**item)
                            self.results['created'] += 1
                    
                    self.log_progress('upsert', len(batch))
            
            return self.results
        except Exception as e:
            self.handle_error(e, 'bulk_upsert')
            return self.results


def bulk_create(model_class, items: List[Dict[str, Any]], batch_size: int = 1000) -> Dict[str, Any]:
    """Convenience function for bulk creating records"""
    op = BulkCreateOperation(batch_size)
    return op.execute(model_class, items)


def bulk_update(queryset: QuerySet, updates: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience function for bulk updating records"""
    op = BulkUpdateOperation()
    return op.execute(queryset, updates)


def bulk_delete(queryset: QuerySet) -> Dict[str, Any]:
    """Convenience function for bulk deleting records"""
    op = BulkDeleteOperation()
    return op.execute(queryset)


def bulk_upsert(
    model_class,
    items: List[Dict[str, Any]],
    lookup_field: str = 'id',
    batch_size: int = 1000
) -> Dict[str, Any]:
    """Convenience function for bulk upserting records"""
    op = BulkUpsertOperation(batch_size)
    return op.execute(model_class, items, lookup_field)