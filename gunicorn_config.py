# gunicorn_config.py - Gunicorn configuration file
import multiprocessing
import os

# Server socket
bind = "0.0.0.0:443"
backlog = 2048

# SSL Configuration
keyfile = "/home/bb/exam/ssl/bb.key"
certfile = "/home/bb/exam/ssl/bb.pem"
ssl_version = 2  # SSLv23
ciphers = 'ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20:!aNULL:!MD5:!DSS'
do_handshake_on_connect = False

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 10
max_requests = 1000
max_requests_jitter = 50

# Create logs directory if it doesn't exist
log_dir = "/home/bb/exam/logs"
os.makedirs(log_dir, exist_ok=True)

# Logging
accesslog = "/home/bb/exam/logs/gunicorn_access.log"
errorlog = "/home/bb/exam/logs/gunicorn_error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "exam_app"

# Server mechanics
daemon = False  # Set to True if you want to run as daemon
pidfile = "/home/bb/exam/gunicorn.pid"
user = None  # Set to your user if running as root
group = None  # Set to your group if running as root
tmp_upload_dir = None

# Application
pythonpath = "/home/bb/exam"
chdir = "/home/bb/exam"

# Environment variables
raw_env = [
    'FLASK_ENV=production',
]

# Preload app for better performance
preload_app = True

# When to restart workers
max_requests = 1000
max_requests_jitter = 50

# Memory management
worker_tmp_dir = "/dev/shm"

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190