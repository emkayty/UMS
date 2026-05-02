#!/bin/bash
# Generate Django migrations
# Run this script AFTER database setup

echo "Generating Django migrations..."

# Activate virtual environment if exists
if [ -f "../venv/bin/activate" ]; then
    source ../venv/bin/activate
fi

# Run migrations for each app
python manage.py makemigrations accounts
python manage.py makemigrations institution
python manage.py makemigrations academic
python manage.py makemigrations student
python manage.py makemigrations staff
python manage.py makemigrations learning
python manage.py makemigrations finance
python manage.py makemigrations communication
python manage.py makemigrations reports
python manage.py makemigrations lifecycle
python manage.py makemigrations offline

# Apply migrations
echo "Applying migrations..."
python manage.py migrate

# Create superuser
echo "Create admin user? (y/n)"
read -r response
if [ "$response" = "y" ]; then
    python manage.py createsuperuser
fi

echo "Done!"
