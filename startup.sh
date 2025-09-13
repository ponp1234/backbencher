#!/bin/bash
# startup.sh - Script to start the Flask application with Gunicorn

# Create logs directory if it doesn't exist
mkdir -p /home/bb/exam/logs

# Change to application directory
cd /home/bb/exam

# Set environment variables (if needed)
export FLASK_ENV=production

# Start Gunicorn with SSL configuration
echo "Starting Gunicorn server..."
gunicorn --config gunicorn_config.py wsgi:app

# Alternative: Command line version (uncomment if you prefer)
# gunicorn --bind 0.0.0.0:443 \
#          --keyfile /home/bb/exam/ssl/bb.key \
#          --certfile /home/bb/exam/ssl/bb.pem \
#          --workers 4 \
#          --worker-class sync \
#          --timeout 30 \
#          --access-logfile /home/bb/exam/logs/gunicorn_access.log \
#          --error-logfile /home/bb/exam/logs/gunicorn_error.log \
#          --log-level info \
#          --preload \
#          wsgi:app