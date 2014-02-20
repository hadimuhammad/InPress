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
    url(r'^instructor/login.html', 'module.views.instructorsignin'),
    url(r'^instructor/index.html', 'module.views.instructorindex'),
    url(r'^instructor/addclass.html', 'module.views.addclass'),
    url(r'^instructor/removeclass.html', 'module.views.removeclass'),
    url(r'^instructor/addassessment.html', 'module.views.addassessment'),
    url(r'^instructor/removeassessment.html', 'module.views.removeassessment'),
    url(r'^instructor/course.html', 'module.views.course'),
    url(r'^instructor/addquestion.html', 'module.views.addquestion'),
    url(r'^instructor/data_analysis.html', 'module.views.data_analysis'),
    url(r'^instructor/viewclass.html', 'module.views.viewclass'),
    url(r'^student/course.html', 'module.views.studentcourse'),
    url(r'^student/index.html','module.views.studentindex'),
    url(r'^student/viewassessment.html','module.views.viewassessment'),
    url(r'^student/viewassessmentanswers.html','module.views.viewassessmentanswers'),
    url(r'^student/studentCourseHistory.html','module.views.studentcoursehistory'),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
