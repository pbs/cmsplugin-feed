# -*- coding: utf-8 -*-
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

ROOT_URLCONF = 'tests.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'context_processors': (
                "django.contrib.auth.context_processors.auth",
                'django.contrib.messages.context_processors.messages',
                "django.template.context_processors.i18n",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.media",
                'django.template.context_processors.csrf',
                "cms.context_processors.media",
                "sekizai.context_processors.sekizai",
                "django.template.context_processors.static",
            ),
            'loaders': (
                'cmsplugin_feed.tests.utils.MockLoader',
            ),
        },
    },
]

CMS_TEMPLATES = [
    ('template.html', 'template.html'),
]

CMS_MODERATOR = False
CMS_PERMISSION = False
CMS_APPHOOKS = ()

# MEDIA_ROOT = os.path.abspath( os.path.join(TMP_ROOT, 'media') )
# MEDIA_URL = '/media/'
STATIC_URL = '/static/'
SECRET_KEY = '3e7704d1-eb82-43dc-b322-a41e7972a060'
