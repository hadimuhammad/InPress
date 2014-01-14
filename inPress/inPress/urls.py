from django.conf.urls import * 

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'inPress.views.home', name='home'),
    # url(r'^inPress/', include('inPress.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^$', 'module.views.studentsignin'),
    url(r'^instructor/login', 'module.views.instructorsignin'),
    url(r'^instructor/index/$', 'module.views.instructorindex'),
    url(r'^instructor/class', 'module.views.instructoraddclass'),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
