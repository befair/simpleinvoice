from django.conf.urls import patterns, include, url
from settings import URL_PREFIX, MEDIA_ROOT

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'simpleinvoice.views.home', name='home'),
    # url(r'^simpleinvoice/', include('simpleinvoice.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^%sdisplay/' % URL_PREFIX, 'invoice.views.display', name="display-multiple"),
    url(r'^%sadmin/' % URL_PREFIX, include(admin.site.urls)),
	(r'^%sstatic/(?P<path>.*)$' % URL_PREFIX, 'django.views.static.serve', {'document_root': MEDIA_ROOT }),

    # API ---
    url(r'^api/get-services/(?P<customer_id>\d+)/', "services.views.get_services"),

)
