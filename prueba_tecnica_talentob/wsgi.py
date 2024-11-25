import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prueba_tecnica_talentob.settings')

application = get_wsgi_application()
