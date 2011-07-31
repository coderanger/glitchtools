from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', include('glitchtools.users.urls')),
    url(r'^map/', include('glitchtools.map.urls')),
    url(r'^$', 'glitchtools.core.views.comingsoon'),
)
