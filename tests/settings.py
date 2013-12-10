#-*- coding: utf-8 -*-
import os
import tempfile
DEBUG = True
PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))
TMP_ROOT = tempfile.gettempdir()
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(TMP_ROOT, 'cmsplugin_feed_test.sqlite3'),
    },
}
INSTALLED_APPS = [
    'mptt',
    'south',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'feedparser',
    'cms',
    'sekizai',
    'cmsplugin_feed',
]

ROOT_URLCONF = 'test_urls'

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    'django.contrib.messages.context_processors.messages',
    "django.core.context_processors.i18n",
    "django.core.context_processors.debug",
    "django.core.context_processors.request",
    "django.core.context_processors.media",
    'django.core.context_processors.csrf',
    "cms.context_processors.media",
    "sekizai.context_processors.sekizai",
    "django.core.context_processors.static",
]
CMS_TEMPLATES = [
    ('template.html', 'template.html'),
]
TEMPLATE_LOADERS = (
    'cmsplugin_feed.test_utils.MockLoader',
)
CMS_MODERATOR = False
CMS_PERMISSION = False
CMS_APPHOOKS = ()

# MEDIA_ROOT = os.path.abspath( os.path.join(TMP_ROOT, 'media') )
# MEDIA_URL = '/media/'
# STATIC_URL = '/static/'
SECRET_KEY = '3e7704d1-eb82-43dc-b322-a41e7972a060'
