from django.conf.urls.defaults import patterns, include, url
urlpatterns = patterns('',
    # Examples:
    url(r'^/?$', 'accounts.views.home', name='home'),

    url(
        r'^accounts/login/$','django.contrib.auth.views.login',
        dict(
            template_name = 'jqm/login.html',
        ),
        name='login',
    ),
    url(
        r'^accounts/logout/$','django.contrib.auth.views.logout',
        dict(
            template_name = 'jqm/logout.html',
        ),
        name='logout',
    ),

)
