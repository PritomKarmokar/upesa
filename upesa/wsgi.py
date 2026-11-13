"""
WSGI config for upesa project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.contrib.staticfiles.handlers import StaticFilesHandler

if os.getenv("STATIC_ENABLED", "1") == "1":
    application = StaticFilesHandler(get_wsgi_application())
else:
    application = get_wsgi_application()