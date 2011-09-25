from settings import *
import os

LOCAL = False
LOCAL_DEVELOPMENT = False

DEBUG = True
THUMBNAIL_DEBUG = False

SITE_ROOT = 'inmycal.com'

APPEND_SLASHES = True

MEDIA_ROOT = PROJECT_ROOT

ADMIN_MEDIA_PREFIX = '/assets/admin-media/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'django',
        'USER': 'django',
        'PASSWORD': 'django',
        'HOST': '',
        'PORT': '',
    }
}
