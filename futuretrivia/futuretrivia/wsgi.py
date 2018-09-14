"""
WSGI config for futuretrivia project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os, sys

sys.path.append('/home/defi/Desktop/futureTrivia')
sys.path.append('/home/defi/Desktop/futureTrivia/futuretrivia')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'futuretrivia.settings')

application = get_wsgi_application()
