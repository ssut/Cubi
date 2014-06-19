# -*- coding: utf-8 -*-
import os
import sys

import djcelery

# HOST = 'localhost:8000'
HOST = 'www.tinicube.com'
ALLOWED_HOSTS = ['*']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = TEMPLATE_DEBUG = True
if 'DJANGO_PRODUCTION' in os.environ:
    DEBUG = TEMPLATE_DEBUG = False
TMP_STAGE = True if 'STAGE' in os.environ else False

BROKER_URL = "django://"
CELERY_IMPORTS = ('work.tasks', )
djcelery.setup_loader()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')
STATIC_PATH = os.path.join(BASE_DIR, 'static')
STATIC_ROOT_PATH = os.path.join(BASE_DIR, 'static_root')

# 서비스용, 로컬 분리
if not DEBUG or TMP_STAGE:
    MEDIA_PATH = '/var/www/tinicube-media'
else:
    MEDIA_PATH = os.path.join(BASE_DIR, 'media')

print 'DEBUG: ', DEBUG
print 'BASE_DIR :', BASE_DIR
print 'TEMPLATE_DIR :', TEMPLATE_PATH
print 'STATIC_DIR :', STATIC_PATH
print 'MEDIA_DIR :', MEDIA_PATH

TEMPLATE_DIRS = (
    TEMPLATE_PATH,
)
STATICFILES_DIRS = (
    STATIC_PATH,
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

STATIC_URL = '/static/'
STATIC_ROOT = STATIC_ROOT_PATH
MEDIA_ROOT = MEDIA_PATH
MEDIA_URL = '/media/'

AUTH_USER_MODEL = 'member.TinicubeUser'
ACCOUNT_ACTIVATION_DAYS = 7

SECRET_KEY = '+hr^u0snco1ma=zb5*uvuvk-0*#up+nw4z*pwt)h9ws&aa_+2)'

#STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
PIPELINE_CSS = {
    'master': {
        'source_filenames': (
            'css/*.css',
        ),
        'output_filename': 'css/master.css',
        'variant': 'datauri',
    }
}

# SITE_URL = 'http://192.168.56.1:8000'
# SITE_URL = 'http://localhost:8000'
DEFAULT_PROFILE_IMAGE = STATIC_URL + 'img/default_profile.png'


# Raven (sentry)
RAVEN_DSN = "http://072c38e9bf5747cd883eef67d08d9dda" \
            ":49dd7d63b03143ea96e4c8fcc558bb8f@sentry.ssut.me/3"
RAVEN_CONFIG = {
    'dsn': RAVEN_DSN,
}

INSTALLED_APPS = (
    'grappelli',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'raven.contrib.django.raven_compat',
    'site',

    'south',
    'kombu.transport.django',
    'djcelery',
    'registration',
    # 'pipeline',

    'member',
    'board',
    'work',
    'author',
    'administrator',
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

AUTHENTICATION_BACKENDS = (
    'member.backends.EmailAuthBackend',
    'member.backends.FacebookAuthBackend',
)
AUTH_USER_MODEL = 'member.TinicubeUser'
FACEBOOK_APP_ID = '232589236930454'
FACEBOOK_API_SECRET = 'ba79942815fda6f882c626762cf964ed'

ROOT_URLCONF = 'tinicube.urls'
WSGI_APPLICATION = 'tinicube.wsgi.application'

if not DEBUG or TMP_STAGE:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'tinicube',
            'USER': 'tinicube',
            'PASSWORD': 'gksdud1!',
            'HOST': '',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }


if 'test' in sys.argv:
    filename = os.path.join(os.path.dirname(__file__), 'test.sqlite3')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': filename,
            'TEST_NAME': filename,
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'
