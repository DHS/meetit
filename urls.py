from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'demo/', 'meetit.meetit.views.demo', name='demo'),
    url(r'events/', 'meetit.meetit.views.events', name='events'),
    url(r'confirm/','meetit.meetit.views.confirm', name='confirm'),
    url(r'email/', 'meetit.meetit.views.email', name='email'),
    url(r'journeys/', 'meetit.meetit.views.journeys', name='journeys'),
    url(r'signup/', 'meetit.meetit.views.signup', name='signup'),
    url(r'^$', 'meetit.meetit.views.home', name='home'),

    url(r'^admin/', include(admin.site.urls)),
)


if settings.LOCAL_DEVELOPMENT:
    urlpatterns += patterns("django.views",
        url(r'%s(?P<path>.*)/$' % settings.MEDIA_URL[1:], 'static.serve', {
            "document_root": settings.MEDIA_ROOT,
        })
    )

