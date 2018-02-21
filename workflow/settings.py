"""
Django settings for workflow project.

Generated by 'django-admin startproject' using Django 1.10.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'rest_framework',
	'bdmcore'
]


#REST_FRAMEWORK = {
#    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
#    'PAGE_SIZE': 10
#}
#'rest_framework_xml.parsers.XMLParser'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.AllowAny',),
	'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'PAGE_SIZE': 10,
	'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer'
	)
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'workflow.urls'

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

WSGI_APPLICATION = 'workflow.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
            },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs\\bdmw.log',
            'formatter': 'simple'
            },
        },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
            },
        }
    }


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

#############################################
# Bdm specific

#######################
# GeoServer settings
WFS_UPSTREAM = 'http://bidon:8082/geoserver/ows'
GEOSERVER_REST = 'http://bidon.225:8082/geoserver/rest'
GEOSERVER_USER = 'bidon'
GEOSERVER_PWD = 'bidon'
GEOSERVER_WORKSPACE = 'bidon'
GEOSERVER_DATASTORE = 'bidon'

#######################
# Brugis database
DEVSCHEMA_EDIT =	"bidon"	
DEVSCHEMA_MODIF	=	"bidon"
DEVSCHEMA_INTRA	=	"bidon"
DEVSCHEMA_ADMIN	=	"bidon"
DEVSCHEMA_PUBLISH = "bidon"
DEVSCHEMA_COMMON	=	"bidon"

######################
# Bdm Workflow
BRUGIS_DATAFLOW_COUT	=	"COUT"	
BRUGIS_DATAFLOW_CIN	=	"CIN"	
BRUGIS_DATAFLOW_STAGING	=	"STAGING"	
BRUGIS_DATAFLOW_VALID	=	"VALID"
BRUGIS_DATAFLOW_UNDEFINED	=	"UNDEFINED"

BRUGIS_USERACTION_CHECKOUT	=	"CHECKOUT"
BRUGIS_USERACTION_VALIDATE	=	"VALIDATE"
BRUGIS_USERACTION_STAGING		=	"STAGING"
BRUGIS_USERACTION_UNDOCHECKOUT	=	"UNDOCHECKOUT"
BRUGIS_USERACTION_UNDOSTAGING	=	"UNDOSTAGING"

######################
# Users

ADMIN_USER = '???'

######################
# Bdm Mail config			
BRUGIS_MAIL_ADDR	=	"bidon@bidon.brussels"
BRUGIS_MAIL_SUBJECT	=	"Notification	Brugis"
BRUGIS_MAIL_SMTP	=	"relay.bidon.be"	
BDM_VERSION			=	"0.6"	

######################
# Spatial data
DEFAULTSRID = "EPSG:31378"
GEOMETRYFIELD = "GEOMETRY"
WFS_HEADERS = {"Content-type": "application/xml","Accept": "application/xml"}

try:
	from local_settings import *
except:
	print "missing config"

