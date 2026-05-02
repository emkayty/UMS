"""
Cookie consent management for GDPR/NDPR compliance.
"""
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json


# Simple in-memory consent storage (use Redis/DB in production)
CONSENT_STORAGE = {}


@csrf_exempt
@require_http_methods(["GET", "POST", "OPTIONS"])
def cookie_consent(request):
    """Handle cookie consent: GET returns status, POST sets consent."""
    
    if request.method == 'GET':
        # Return current consent status
        user_id = request.headers.get('X-User-ID', 'anonymous')
        consent = CONSENT_STORAGE.get(user_id, {
            'necessary': True,
            'analytics': False,
            'marketing': False,
            'timestamp': None
        })
        return JsonResponse(consent)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body) if request.body else {}
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        user_id = request.headers.get('X-User-ID', 'anonymous')
        
        # Validate consent keys
        allowed_keys = {'necessary', 'analytics', 'marketing'}
        consent_data = {
            'necessary': True,  # Always required
            'analytics': data.get('analytics', False),
            'marketing': data.get('marketing', False),
            'timestamp': data.get('timestamp')
        }
        
        # Store consent
        CONSENT_STORAGE[user_id] = {
            key: consent_data.get(key, False) 
            for key in allowed_keys
        }
        CONSENT_STORAGE[user_id]['necessary'] = True
        CONSENT_STORAGE[user_id]['timestamp'] = consent_data.get('timestamp')
        
        return JsonResponse({
            'success': True, 
            'consent': CONSENT_STORAGE[user_id]
        })
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@require_http_methods(["GET"])
def privacy_policy(request):
    """Return privacy policy information."""
    return JsonResponse({
        'policy': {
            'controller': 'University Administration',
            'dpo': 'Data Protection Officer',
            'purposes': [
                'Academic management',
                'Student records',
                'Finance',
                'Communications'
            ],
            'rights': [
                'Access',
                'Rectification', 
                'Erasure',
                'Portability'
            ],
            'retention': 'As required by law',
            'complaint': 'Nigeria Data Protection Regulation (NDPR)'
        }
    })
