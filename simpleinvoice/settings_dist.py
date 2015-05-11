from default_settings import *

import locale

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'g8@_)2o_9i^c-g%+^2f%=rr=vd023i^(0=4o(5(=@pr-ed2e+o'

DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

WSGI_APPLICATION = 'simpleinvoice.wsgi.application'

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'invoice.db'),
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'

COMPANY_VAT_PERCENT = 0.22
COMPANY_NAME = "Luca Ferroni"
COMPANY_INTERNET_CONTACTS = "http://www.lucaferroni.it - luca@befair.it"
COMPANY_ADDRESS = "Via Don Minzoni, 158 - 60044 Fabriano"
COMPANY_CONTACTS = ""
COMPANY_VAT_NUMBER = "03130581204"
COMPANY_SSN = "FRRLCU80B17D451Y"
COMPANY_LOGO = ""
COMPANY_IBAN = "IT 47 P 08883 36670 CC0280282342"
DEFAULT_VAT_PERCENT = 0.21

#############

SITE_ID = 1

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/home/letti/src/app' # change this to a proper location

try:
    locale.setlocale(locale.LC_ALL, 'it_IT.UTF8')
except locale.Error:
    locale.setlocale(locale.LC_ALL, 'en_US.UTF8')

LOCALE_PATHS = ( 
    os.path.join(BASE_DIR, 'locale',
)
)

#PREFIX = "simpleinvoice/"
#URL_PREFIX = ""
#MEDIA_URL = '/' + PREFIX + 'static/'
#ADMIN_MEDIA_PREFIX = '/' + PREFIX + 'static/admin_media/'
#DATABASE_NAME = os.path.join(BASE_DIR, 'invoice-beFair-20110507.db')  # Or path to database file if using sqlite3.
