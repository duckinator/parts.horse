"""gunicorn WSGI server configuration."""
from multiprocessing import cpu_count
from os import environ

preload = True
forwarded_allow_ips = '*'
bind = '0.0.0.0:' + environ.get('PORT', '8000')
workers = (cpu_count() * 2) + 1
worker_class = 'eventlet'
worker_connections = 1500

backlog = 1500 * (workers - 1)

# Logging

errorlog = '-' # stdout
loglevel = 'info' # debug, info, warning, error, critical
accesslog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

#--preload --forwarded-allow-ips='*' --workers=9 --worker-class=eventlet --worker-connections=1500
