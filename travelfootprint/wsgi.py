import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "lib"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "travelfootprint.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
