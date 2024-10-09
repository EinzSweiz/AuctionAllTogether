#!/bin/bash
set -e  # Exit on any error
APP_PORT=${PORT:-8080}
cd /app/
# Start Gunicorn
exec /opt/venv/bin/gunicorn --worker-tmp-dir /dev/shm rshome.wsgi:application --bind "0.0.0.0:${APP_PORT}"
