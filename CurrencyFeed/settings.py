"""
Django settings for CurrencyFeed project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

def amLocal():
	from socket import gethostname
	return "rhcloud" not in gethostname()

LOCAL=amLocal()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'w=*=it0m*r(fjg^_lyz^srb6kfg0eb9n7g=aj4t*8yh8n75p(#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
		'alert',
		'filescan',
		'percentages',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'CurrencyFeed.urls'

WSGI_APPLICATION = 'CurrencyFeed.wsgi.application'

if LOCAL==True:
	DATABASES = {
			'default': {
					'ENGINE': 'django.db.backends.postgresql_psycopg2',
					'NAME': 'currency',
					'HOST': 'localhost',
					'USER': 'currency_feed',
					'PASSWORD': 'akkadian',
					'ATOMIC_REQUESTS': 'true'
			}
	}
else:
	DATABASES = {
			'default': {
					'ENGINE': 'django.db.backends.postgresql_psycopg2',
					'NAME': 'currencyfeed',
					'HOST': os.environ['OPENSHIFT_POSTGRESQL_DB_HOST'],
					'ATOMIC_REQUESTS': 'true'
			}
	}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

# logging configuration

LOGGING = {
    'version': 1,
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers':['console'],
            'propagate': True,
            'level':'DEBUG',
        }
    },
}

