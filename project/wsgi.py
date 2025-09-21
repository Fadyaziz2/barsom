"""
WSGI config for project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# Get the Django WSGI application
application = get_wsgi_application()

# Import the start_scheduler function and call it
from scheduler.scheduler import start_scheduler

try:
    start_scheduler()
except Exception as e:
    # Log the error for debugging purposes
    import logging
    logging.error(f"Error starting scheduler: {str(e)}")

