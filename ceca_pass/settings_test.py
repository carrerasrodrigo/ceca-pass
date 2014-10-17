# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'TIMEOUT': 36000,
        'KEY_PREFIX': 'p',
    }
}

INSTALLED_APPS = (
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'ceca_pass',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware'
    )


SECRET_KEY = 'a'

DEFAULT_FROM_EMAIL = 'webmaster@example.com'

TEST_RUNNER = 'django.test.runner.DiscoverRunner'
CECA_PASS_SECRET_STRING = '1'*32
CECA_PASS_PASSWORD_PATH = os.path.join(BASE_DIR, 'ceca_pass', 'tests',
    'dump.json')
CECA_PASS_BASH_PATH = os.path.join(BASE_DIR, 'ceca_pass', 'tests',
    'bash.rc')
CECA_PASS_SYSTEM_BASH_FILE = os.path.join(BASE_DIR, 'ceca_pass', 'tests',
    'mybash.rc')
