#!/bin/bash
# UMS Startup Script

set -e

echo "🎓 Starting UMS..."

# Wait for database
echo "Waiting for database..."
python manage.py wait_for_db || true

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create cache table if using database cache
python manage.py createcachetable || true

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn unicore.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --worker-class=sync \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -