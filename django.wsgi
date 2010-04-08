import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'simpleinvoice.settings'

sys.path.append('/var/www/dj')

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

