"""
WSGI config for chatservice project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
# DYNO is a Heroku environment variable
if 'DYNO' in os.environ:
    from whitenoise.django import DjangoWhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatservice.settings")

application = get_wsgi_application()
if 'DYNO' in os.environ:
    application = DjangoWhiteNoise(application)
