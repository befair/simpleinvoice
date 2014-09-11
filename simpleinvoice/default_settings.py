"""
Django settings for befair_django_base project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os, locale

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
VERSION = __version__ = file(BASE_DIR + '/VERSION').read().strip() 

URL_PREFIX = ""

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'g8@_)2o_9i^c-g%+^2f%=rr=vd023i^(0=4o(5(=@pr-ed2e+o'

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
MANAGERS = ADMINS

DEBUG = False
TEMPLATE_DEBUG = DEBUG

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'invoice',
    'services',
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

ROOT_URLCONF = 'simpleinvoice.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'simpleinvoice.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
	BASE_DIR + '/templates',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'invoice.db'),
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Rome'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'it-IT'

USE_I18N = True

# set this to True if you want the locale-dictated format have higher precedence 
# and be applied instead of using date FORMAT settings. 
# See https://docs.djangoproject.com/en/dev/ref/settings/#date-format
USE_L10N = False

USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = BASE_DIR + '/uploads/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = BASE_DIR + '/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

COMPANY_VAT_PERCENT = 0.22
COMPANY_NAME = "beFair"
COMPANY_INTERNET_CONTACTS = "http://www.befair.it - info@befair.it"
COMPANY_ADDRESS = "Via Don Minzoni, 158 - 60044 Fabriano"
COMPANY_CONTACTS = ""
COMPANY_VAT_NUMBER = ""
COMPANY_SSN = ""
COMPANY_LOGO = "logo.jpg"
COMPANY_IBAN = ""

DEFAULT_VAT_PERCENT = 0.22

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


SITE_ID = 1

EMAIL_SENDER = 'simpleinvoice@mysite.it' # overwrite this with proper mail address in settings.py
EMAIL_TEMPLATES = {
    'INSOLUTE_HTML' : 'base_mail.html',
    'INSOLUTE_TXT' : 'base_mail.txt',
}
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'mails') # change this to a proper location if you would like to use filebased smtp backend

#############
# Localizzazione italiana

locale.setlocale(locale.LC_ALL, 'it_IT.UTF8')
LOCALE_PATHS = ( os.path.join(BASE_DIR, 'locale') , )

#############
# DATE e DATE_TIME format

DATE_FORMAT = 'd/m/Y'
DATETIME_FORMAT = DATE_FORMAT
