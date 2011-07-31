from django.conf.urls.defaults import patterns, url

from glitchtools.map import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='glitchtools-map-index'),
)
