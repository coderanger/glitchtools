from django.conf.urls.defaults import patterns, url

from glitchtools.auth import views

urlpatterns = patterns('',
    url(r'^token/', views.token, name='glitchtools-auth-token'),
    url(r'', views.login, name='glitchtools-auth-login'),
)
