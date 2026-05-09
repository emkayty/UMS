"""
UMS Test Configuration
Pytest and Django test settings
"""

import os
import sys
import django

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unicore.settings')


def pytest_configure():
    """Configure pytest for Django"""
    django.setup()


def pytest_collection_modifyitems(items):
    """Skip certain tests based on markers"""
    for item in items:
        # Add slow marker to integration tests
        if 'integration' in item.nodeid:
            item.add_marker('slow')
        
        # Add security marker to security tests
        if 'security' in item.nodeid:
            item.add_marker('security')


# Pytest configuration
pytest_plugins = [
    'pytest_django',
]


def pytest_addoption(parser):
    """Add custom pytest options"""
    parser.addoption(
        '--run-slow',
        action='store_true',
        default=False,
        help='run slow tests'
    )