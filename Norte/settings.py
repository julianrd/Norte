"""
Django settings for Norte project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zathwu=xwdv3t1v5os6@7bb6gw)u0+5*$p#_bl+850x0s09&dp'

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
    'FacturasNorte',
    'django_markdown',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'Norte.urls'

WSGI_APPLICATION = 'Norte.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'sqlserver_ado',
        'NAME': 'FacturasNorte',

        'HOST': 'PABLOHP',#'JORGIED',
        'USER': 'sa',
        'PASSWORD': 'Norte1234',#'dni36017874',

        'OPTIONS': {
            'provider': 'SQLNCLI',
            'use_mars': 'DataTypeCompatibility=80;MARS Connection=True;'
        }
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'UTC-3'

USE_I18N = False

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR,'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATIC_URL = '/static/'

STATIC_ROOT = ''

TEMPLATE_DIRS = ('templates',
    'FacturasNorte/templates'
)

#AUTHENTICATION
AUTH_PROFILE_MODULE = 'FacturasNorte.Administrador'
AUTH_PROFILE_MODULE = 'FacturasNorte.Empleado'
AUTH_PROFILE_MODULE = 'FacturasNorte.Cliente'

AUTHENTICATION_BACKENDS = ('FacturasNorte.backends.Emailbackend','django.contrib.auth.backends.ModelBackend')

#Path for date formats
FORMAT_MODULE_PATH  = 'Norte.formats'

#LOGIN PATHS
LOGIN_REDIRECT_URL = 'FacturasNorte:index'

LOGIN_URL = 'FacturasNorte:login'

# #FORMAT FILES
# FORMAT_MODULE_PATH = [
#     'Norte.formats',
#     'FacturasNorte.formats',
# ]

#EMAIL BACKEND
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

#EMAIL OPTIONS
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'julian.rd7@gmail.com'
EMAIL_HOST_PASSWORD = 'tel563539'
EMAIL_USE_TLS = True


#MEDIA
MEDIA_ROOT = 'C:/Users/Julian/Documents/Diario Norte/Proyecto Norte/PDFs/'

MEDIA_ULR = '/pdf/'
