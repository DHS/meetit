import os, sys

sys.path.append('/home/web/')
sys.path.append('/home/web/meetit/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'meetit.server_settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
