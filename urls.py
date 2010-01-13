from django.conf.urls.defaults import *

from admin.models import site_admin

urlpatterns = patterns('',
    # Example:
    # (r'^invoice4dummies/', include('invoice4dummies.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', site_admin.root),
)
