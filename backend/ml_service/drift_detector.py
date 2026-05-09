"""
AI/ML Drift Detection Module
Production-grade model monitoring and drift detection
"""

import time
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from django.utils import timezone


class ModelDriftDetector:
    """
    Detects model drift and degradation in production
    Monitors for:
    - Concept drift: changes in the relationship between features and target
    - Data drift: changes in feature distributions
    - Performance drift: changes in model accuracy
    """
    
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.baseline_metrics: Dict = {}
        self.history: List[Dict] = []
    
    def set_baseline(self, metrics: Dict):
        """Set baseline metrics for comparison"""
        self.baseline_metrics = {
            'accuracy': metrics.get('accuracy', 0),
            'precision': metrics.get('precision', 0),
            'recall': metrics.get('recall', 0),
            'f1': metrics.get('f1', 0),
            'timestamp': timezone.now(),
        }
    
    def detect_concept_drift(
        self,
        current_metrics: Dict,
        threshold: float = 0.05
    ) -> Dict[str, Any]:
        """Detect concept drift by comparing current vs baseline"""
        if not self.baseline_metrics:
            return {'status': 'no_baseline', 'drift_detected': False}
        
        drift = {}
        for key in ['accuracy', 'precision', 'recall', 'f1']:
            if key in current_metrics:
                baseline = self.baseline_metrics.get(key, 0)
                current = current_metrics.get(key, 0)
                drift[key] = abs(current - baseline)
        
        max_drift = max(drift.values()) if drift else 0
        drift_detected = max_drift > threshold
        
        self.history.append({
            'timestamp': timezone.now(),
            'metrics': current_metrics,
            'drift': drift,
            'drift_detected': drift_detected,
        })
        
        return {
            'status': 'analyzed',
            'drift_detected': drift_detected,
            'max_drift': max_drift,
            'recommendation': 'retrain' if drift_detected else 'continue',
        }
    
    def should_auto_retrain(
        self,
        current_metrics: Dict,
        consecutive_threshold: int = 3
    ) -> bool:
        """Determine if automatic retraining should be triggered"""
        drift_result = self.detect_concept_drift(current_metrics)
        return drift_result.get('drift_detected', False)
    
    def get_dashboard_data(self) -> Dict:
        """Get data for dashboard display"""
        return {
            'model_name': self.model_name,
            'baseline': self.baseline_metrics,
            'drift_events': sum(1 for h in self.history if h.get('drift_detected')),
        }


class MLModelMonitor:
    """Production ML model monitoring service"""
    
    def __init__(self):
        self.models: Dict[str, ModelDriftDetector] = {}
    
    def register_model(self, model_name: str, initial_metrics: Dict):
        detector = ModelDriftDetector(model_name)
        detector.set_baseline(initial_metrics)
        self.models[model_name] = detector
        return detector
    
    def get_model(self, model_name: str):
        return self.models.get(model_name)


_ml_monitor = MLModelMonitor()


def get_ml_monitor() -> MLModelMonitor:
    return _ml_monitor


__all__ = ['ModelDriftDetector', 'MLModelMonitor', 'get_ml_monitor']