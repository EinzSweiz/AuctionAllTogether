#!/bin/bash
set -e  # Exit on any error
SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-'admin@example.com'}
cd /app/
# Run migrations
/opt/venv/bin/python manage.py migrate --noinput

# Create superuser if it does not exist
if ! /opt/venv/bin/python manage.py createsuperuser --email $SUPERUSER_EMAIL --noinput; then
    echo "Superuser creation failed, it may already exist."
fi
