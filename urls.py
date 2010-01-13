from django.conf.urls.defaults import *
from settings import URL_PREFIX, MEDIA_ROOT

from admin.models import site_admin

urlpatterns = patterns('',
    # Example:
    # (r'^invoice4dummies/', include('invoice4dummies.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', site_admin.root),

	(r'^%sstatic/(?P<path>.*)$' % URL_PREFIX, 'django.views.static.serve', {'document_root': MEDIA_ROOT }),
)
