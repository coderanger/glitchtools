from django.conf.urls.defaults import patterns, url

from glitchtools.users import views

urlpatterns = patterns('',
    url(r'^token/', views.token, name='glitchtools-users-token'),
    url(r'', views.login, name='glitchtools-users-login'),
)
