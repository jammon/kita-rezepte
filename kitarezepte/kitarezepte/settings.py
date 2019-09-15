"""
Django settings for kitarezepte project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import string
from configparser import ConfigParser, NoSectionError
from random import choice


def random_string(length=50):
    return ''.join([choice(string.digits + string.ascii_letters) for i in range(length)])

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


CONFIG_FILE = os.path.join(BASE_DIR, 'kita-rezepte.cnf')
config = ConfigParser()
config.read_string("""
    [django]
    [server]
        mode: production
        domain: kita-rezepte
        fulldomain: kita-rezepte.de
""")
config.read(CONFIG_FILE)
try:
    SECRET_KEY = config['django']['key']
except KeyError:
    config['django']['key'] = SECRET_KEY = random_string(50)
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

KITAREZEPTE_DOMAIN = config['server']['domain']
KITAREZEPTE_FULL_DOMAIN = config['server']['fulldomain']

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
servermode = config['server']['mode']
if servermode=='development':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
elif servermode=='production':
    DB_CONFIG_FILE = os.path.expanduser('~/.my.cnf')
    db_config = ConfigParser()
    with open(DB_CONFIG_FILE) as db_conf_file:
        db_config.read_file(db_conf_file)

    db_username = db_config['client']['user']
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': db_username,
            'USER': db_username,
            'PASSWORD': db_config['client']['password'],
            'TEST': {
                'NAME': db_username + '_test',
            },
            'CONN_MAX_AGE': 5,
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = servermode=='development'

ALLOWED_HOSTS = (
    [] if DEBUG else 
    ['.kita-rezepte.de', '.kitarez.uber.space'])

ADMINS = [("Johannes Ammon", "j.ammon@dr-ammon.de")]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'taggit',
    'tinymce',
    'rezepte.apps.RezepteConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE
    INTERNAL_IPS = ['127.0.0.1']

ROOT_URLCONF = 'kitarezepte.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'kitarezepte.wsgi.application'



# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'de-de'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

if servermode=='production':
    STATIC_ROOT = "/var/www/virtual/kitarez/html/static/"
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

LOGIN_URL = '/login/'

SECURE_CONTENT_TYPE_NOSNIFF = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'debug.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

