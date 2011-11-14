from django.conf.urls.defaults import *
from settings import URL_PREFIX, MEDIA_ROOT

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^simpleinvoice/', include('simpleinvoice.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^%sdisplay/' % URL_PREFIX, 'simpleinvoice.invoice.views.display', name="display-multiple"),
    (r'^%sadmin/' % URL_PREFIX, include(admin.site.urls)),

	(r'^%sstatic/(?P<path>.*)$' % URL_PREFIX, 'django.views.static.serve', {'document_root': MEDIA_ROOT }),
)
