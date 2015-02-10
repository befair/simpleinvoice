from default_settings import *

import locale

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'g8@_)2o_9i^c-g%+^2f%=rr=vd023i^(0=4o(5(=@pr-ed2e+o'

# COMPANY INFO

COMPANY_VAT_PERCENT = 0.22
COMPANY_NAME = "Luca Ferroni"
COMPANY_INTERNET_CONTACTS = "http://www.lucaferroni.it - luca@befair.it"
COMPANY_ADDRESS = "Via Don Minzoni, 158 - 60044 Fabriano"
COMPANY_CONTACTS = ""
COMPANY_VAT_NUMBER = "03130581204"
COMPANY_SSN = "FRRLCU80B17D451Y"
COMPANY_LOGO = ""
COMPANY_IBAN = "IT 47 P 08883 36670 CC0280282342"
DEFAULT_VAT_PERCENT = 0.22

# EMAIL SETTINGS

EMAIL_SENDER = 'simpleinvoice@mysite.it' # overwrite this with proper mail address
EMAIL_TEMPLATES = {
    'INSOLUTE_HTML' : 'base_mail.html',
    'INSOLUTE_TXT' : 'base_mail.txt',
}
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# DATABASE SETTINGS
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

# Localizzazione italiana

locale.setlocale(locale.LC_ALL, 'it_IT.UTF8')

# OLDIES TODO TOREMOVE?

#PREFIX = "simpleinvoice/"
#URL_PREFIX = ""
#MEDIA_URL = '/' + PREFIX + 'static/'
#ADMIN_MEDIA_PREFIX = '/' + PREFIX + 'static/admin_media/'

INSTALLED_APPS.append('fromreescsv')
