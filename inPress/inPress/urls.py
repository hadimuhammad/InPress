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
    (r'^$', 'module.views.index'),
    url(r'addassessment', 'module.views.addassessment'),
    url(r'viewassessments', 'module.views.viewassessments'),
    url(r'addquestion', 'module.views.addquestion'),
    url(r'removeassessment', 'module.views.removeassessment'),
    url(r'addcourses', 'module.views.addcourses'),
    url(r'removecourses', 'module.views.removecourses'),
    url(r'stuIndex', 'module.views.stuIndex'),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
