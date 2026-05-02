"""
UniCore - University Operating System
Django application for managing university operations.
"""
import os
from django.core.management import execute_from_command_line
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unicore.settings')

application = get_wsgi_application()

if __name__ == '__main__':
    execute_from_command_line()