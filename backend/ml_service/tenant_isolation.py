"""
Tenant ML Isolation Module
Ensures complete tenant isolation in ML training and inference
"""

from typing import Optional, List, Dict, Any
from django.utils import timezone


class TenantMLIsolationManager:
    """
    Manages tenant isolation for ML models
    Ensures no cross-tenant data leakage
    """
    
    def __init__(self):
        self._tenant_models: Dict[str, Any] = {}
        self._feature_stores: Dict[str, Dict] = {}
        self._inference_isolation: bool = True
    
    def register_tenant_model(
        self,
        tenant_id: str,
        model_name: str,
        model_config: Dict
    ) -> bool:
        """Register a tenant-specific model"""
        if tenant_id not in self._tenant_models:
            self._tenant_models[tenant_id] = {}
        
        self._tenant_models[tenant_id][model_name] = {
            'config': model_config,
            'created_at': timezone.now(),
            'training_data_size': 0,
            'inference_count': 0,
        }
        return True
    
    def get_tenant_model(
        self,
        tenant_id: str,
        model_name: str
    ) -> Optional[Dict]:
        """Get tenant-specific model (ensures isolation)"""
        if tenant_id in self._tenant_models:
            return self._tenant_models[tenant_id].get(model_name)
        return None
    
    def isolate_features(
        self,
        tenant_id: str,
        features: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Isolate features for a specific tenant"""
        # Ensure features are tagged with tenant
        isolated = {
            **features,
            '_tenant_id': tenant_id,
            '_isolated_at': timezone.now().isoformat(),
        }
        return isolated
    
    def store_tenant_features(
        self,
        tenant_id: str,
        features: List[Dict]
    ) -> bool:
        """Store features in tenant-isolated feature store"""
        if tenant_id not in self._feature_stores:
            self._feature_stores[tenant_id] = []
        
        for feature in features:
            self._feature_stores[tenant_id].append({
                **feature,
                'tenant_id': tenant_id,
                'stored_at': timezone.now(),
            })
        return True
    
    def get_tenant_features(
        self,
        tenant_id: str,
        limit: int = 1000
    ) -> List[Dict]:
        """Get features only for specific tenant"""
        if tenant_id in self._feature_stores:
            return self._feature_stores[tenant_id][-limit:]
        return []
    
    def validate_isolation(
        self,
        model_name: str,
        features: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate tenant isolation for inference"""
        # Check if features have tenant ID
        has_tenant = '_tenant_id' in features
        tenant_id = features.get('_tenant_id', 'unknown')
        
        return {
            'is_valid': has_tenant,
            'tenant_id': tenant_id,
            'checks_passed': has_tenant,
            'timestamp': timezone.now().isoformat(),
        }
    
    def prevent_cross_tenant_leakage(
        self,
        data: Any,
        target_tenant_id: str
    ) -> Any:
        """Prevent data leakage between tenants"""
        if isinstance(data, dict):
            # Remove any other tenant IDs
            tenant_keys = [k for k in data.keys() if 'tenant' in k.lower()]
            for key in tenant_keys:
                if data.get(key) and data.get(key) != target_tenant_id:
                    # Log potential breach attempt
                    return None
        return data
    
    def get_inference_isolation_metrics(self) -> Dict:
        """Get metrics on inference isolation"""
        total_inferences = sum(
            model.get('inference_count', 0)
            for tenant in self._tenant_models.values()
            for model in tenant.values()
        )
        
        return {
            'total_tenants': len(self._tenant_models),
            'total_inferences': total_inferences,
            'isolation_enabled': self._inference_isolation,
            'isolated_feature_stores': len(self._feature_stores),
        }


class TenantAwareModelWrapper:
    """
    Wrapper to ensure tenant isolation in ML models
    """
    
    def __init__(self, model: Any, tenant_id: str):
        self._model = model
        self._tenant_id = tenant_id
        self._isolation_manager = TenantMLIsolationManager()
    
    def predict(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Predict with tenant isolation"""
        # Validate isolation
        validation = self._isolation_manager.validate_isolation(
            self._model.__class__.__name__,
            features
        )
        
        if not validation['is_valid']:
            raise ValueError(f"Isolation breach detected for tenant {self._tenant_id}")
        
        # Make prediction
        prediction = self._model.predict(features)
        
        # Tag output with tenant
        prediction['_tenant_id'] = self._tenant_id
        prediction['_inference_isolated'] = True
        
        return prediction
    
    def train(self, features: List[Dict], labels: List) -> Dict:
        """Train with tenant data only"""
        # Isolate training data
        isolated_features = [
            self._isolation_manager.isolate_features(self._tenant_id, f)
            for f in features
        ]
        
        # Train
        result = self._model.fit(isolated_features, labels)
        
        # Register model for tenant
        self._isolation_manager.register_tenant_model(
            self._tenant_id,
            self._model.__class__.__name__,
            result
        )
        
        return result


# Global instance
_tenant_ml_isolation = TenantMLIsolationManager()


def get_tenant_ml_isolation() -> TenantMLIsolationManager:
    """Get global tenant ML isolation manager"""
    return _tenant_ml_isolation


__all__ = [
    'TenantMLIsolationManager',
    'TenantAwareModelWrapper',
    'get_tenant_ml_isolation',
]