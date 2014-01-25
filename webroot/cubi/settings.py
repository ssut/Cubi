#-*- coding: utf-8 -*-
import os
import djcelery

HOST = 'localhost:8000'

BROKER_URL = "django://"
CELERY_IMPORTS = ()
djcelery.setup_loader()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')
STATIC_PATH = os.path.join(BASE_DIR, 'static')
STATIC_ROOT_PATH = os.path.join(BASE_DIR, 'static_root')
MEDIA_PATH = os.path.join(BASE_DIR, 'media')

TEMPLATE_DIRS = (
    TEMPLATE_PATH,
)
STATICFILES_DIRS = (
    STATIC_PATH,
)

STATIC_URL = '/static/'
STATIC_ROOT = STATIC_ROOT_PATH
MEDIA_ROOT = MEDIA_PATH
MEDIA_URL = '/media/'

AUTH_USER_MODEL = 'member.CubiUser'
ACCOUNT_ACTIVATION_DAYS = 7

SECRET_KEY = '+hr^u0snco1ma=zb5*uvuvk-0*#up+nw4z*pwt)h9ws&aa_+2)'
FACEBOOK_APP_ID = '442841165838586'
FACEBOOK_APP_SECRET = '31a520eaf17fe3224f3c2b3151ebfae7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'south',
    'kombu.transport.django',
    'djcelery',
    'registration',
    'flynsarmy_paginator',

    'member',
    'board',
    'work',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)

ROOT_URLCONF = 'cubi.urls'
WSGI_APPLICATION = 'cubi.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
