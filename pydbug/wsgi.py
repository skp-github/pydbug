"""
WSGI config for pydbug project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os


from django.core.wsgi import get_wsgi_application
import sys
import django
django.setup()

sys.dont_write_bytecode = True

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pydbug.settings")

application = get_wsgi_application()
