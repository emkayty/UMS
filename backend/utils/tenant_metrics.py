"""
Tenant Metrics Dashboard
Provides per-tenant observability and metrics
"""

from typing import Dict, List, Optional, Any
from django.utils import timezone


class TenantMetricsCollector:
    """
    Collect and track metrics per tenant
    Provides tenant-level dashboard data
    """
    
    def __init__(self):
        self._tenant_usage: Dict[str, Dict] = {}
        self._request_history: Dict[str, List] = {}
        self._error_history: Dict[str, List] = {}
    
    def record_request(
        self,
        tenant_id: str,
        endpoint: str,
        latency_ms: float,
        status_code: int
    ):
        """Record API request for tenant"""
        if tenant_id not in self._request_history:
            self._request_history[tenant_id] = []
        
        self._request_history[tenant_id].append({
            'endpoint': endpoint,
            'latency_ms': latency_ms,
            'status_code': status_code,
            'timestamp': timezone.now(),
        })
    
    def record_error(
        self,
        tenant_id: str,
        error_type: str,
        message: str
    ):
        """Record error for tenant"""
        if tenant_id not in self._error_history:
            self._error_history[tenant_id] = []
        
        self._error_history[tenant_id].append({
            'error_type': error_type,
            'message': message,
            'timestamp': timezone.now(),
        })
    
    def get_tenant_usage(self, tenant_id: str) -> Dict[str, Any]:
        """Get usage metrics for tenant"""
        requests = self._request_history.get(tenant_id, [])
        errors = self._error_history.get(tenant_id, [])
        
        if not requests:
            return {
                'tenant_id': tenant_id,
                'total_requests': 0,
                'avg_latency_ms': 0,
                'error_rate': 0,
            }
        
        # Calculate metrics
        total_requests = len(requests)
        avg_latency = sum(r['latency_ms'] for r in requests) / total_requests
        error_count = sum(1 for r in requests if r['status_code'] >= 400)
        error_rate = error_count / total_requests if total_requests > 0 else 0
        
        # Get endpoint breakdown
        endpoints = {}
        for r in requests:
            ep = r['endpoint']
            endpoints[ep] = endpoints.get(ep, 0) + 1
        
        return {
            'tenant_id': tenant_id,
            'total_requests': total_requests,
            'avg_latency_ms': round(avg_latency, 2),
            'error_rate': round(error_rate, 4),
            'error_count': error_count,
            'endpoints': endpoints,
            'errors_this_period': len(errors),
        }
    
    def get_all_tenants_summary(self) -> List[Dict]:
        """Get summary for all tenants"""
        return [
            self.get_tenant_usage(tid)
            for tid in self._request_history.keys()
        ]
    
    def get_performance_report(self, tenant_id: str) -> Dict:
        """Get performance report for tenant"""
        usage = self.get_tenant_usage(tenant_id)
        
        # Determine performance status
        if usage['error_rate'] > 0.05:
            status = 'critical'
        elif usage['error_rate'] > 0.01:
            status = 'warning'
        elif usage['avg_latency_ms'] > 1000:
            status = 'warning'
        else:
            status = 'healthy'
        
        return {
            **usage,
            'performance_status': status,
            'recommendation': self._get_recommendation(status),
        }
    
    def _get_recommendation(self, status: str) -> str:
        recommendations = {
            'critical': 'URGENT: Contact support immediately',
            'warning': 'Review error logs and performance',
            'healthy': 'System functioning normally',
        }
        return recommendations.get(status, 'Unknown')


# Global instance
_tenant_metrics = TenantMetricsCollector()


def get_tenant_metrics() -> TenantMetricsCollector:
    return _tenant_metrics


__all__ = ['TenantMetricsCollector', 'get_tenant_metrics']